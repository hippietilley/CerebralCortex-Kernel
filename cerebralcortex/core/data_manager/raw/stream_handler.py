# Copyright (c) 2019, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import gzip
import json
import os
import pickle
import traceback
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import List

import pytz
from pytz import timezone as pytimezone

from cerebralcortex.core.datatypes.datapoint import DataPoint
from cerebralcortex.core.datatypes.datastream import DataStream
from cerebralcortex.core.util.data_types import deserialize_obj
from cerebralcortex.core.util.datetime_helper_methods import get_timezone
from cerebralcortex.core.metadata_manager.metadata import Metadata

class DataSet(Enum):
    COMPLETE = 1,
    ONLY_DATA = 2,
    ONLY_METADATA = 3


class StreamHandler():
    
    ###################################################################
    ################## GET DATA METHODS ###############################
    ###################################################################
    def get_stream(self, stream_name:str, data_type=DataSet.COMPLETE) -> DataStream:

        # query datastream(mysql) for metadata
        if stream_name is None or stream_name=="":
            raise ValueError("stream_name cannot be None or empty")

        stream_metadata = self.sql_data.get_stream_metadata_by_name(stream_name)
        metadata_obj = Metadata.from_json(stream_metadata)

        if len(stream_metadata) > 0:
            if data_type == DataSet.COMPLETE:
                df = self.nosql.read_file(stream_name)
                stream = DataStream(df,metadata_obj)
            elif data_type == DataSet.ONLY_DATA:
                df = self.nosql.read_file(stream_name)
                stream = DataStream(df)
            elif data_type == DataSet.ONLY_METADATA:
                stream = DataStream(metadata_obj)
            else:
                raise ValueError("Invalid type parameter: data_type "+str(data_type))
            return stream
        else:
            return DataStream()

    ###################################################################
    ################## STORE DATA METHODS #############################
    ###################################################################
    def save_stream(self, data, metadata, ingestInfluxDB=False):

        # user_id = datastream.owner
        # stream_name = datastream.name
        # stream_id = datastream.identifier
        # data_descriptor = datastream.data_descriptor
        # execution_context = datastream.execution_context
        # annotations = datastream.annotations
        # stream_type = datastream.datastream_type
        # stream_version = "1" #TODO: add version in DataStream

        try:

            # get start and end time of a stream
            if data:
                status = self.nosql.write_file(stream_name, data)

                if status:
                    # save metadata in SQL store
                    self.sql_data.save_stream_metadata(metadata)
                else:
                    print(
                        "Something went wrong in saving data points.")
        except Exception as e:
            self.logging.log(
                error_message="STREAM ID:  - Cannot save stream. " + str(traceback.format_exc()),
                error_type=self.logtypes.CRITICAL)

    def save_stream_old(self, datastream: DataStream, ingestInfluxDB=False):

        owner_id = datastream.owner
        stream_name = datastream.name
        stream_id = datastream.identifier
        data_descriptor = datastream.data_descriptor
        execution_context = datastream.execution_context
        annotations = datastream.annotations
        stream_type = datastream.datastream_type
        stream_version = "1" #TODO: add version in DataStream
        data = datastream.data

        try:

            # get start and end time of a stream
            if data:
                status = self.nosql.write_file(stream_name, owner_id, stream_version, data)

                if status:
                    new_df = data.sort(data.timestamp.desc()).take(1) # TODO: taking first or last row is expensive. Remove it from mysql table?
                    first_raw = data.head(1)
                    #last_row = data.tail(1)
                    start_time = ""
                    end_time = ""
                    # save metadata in SQL store
                    # self.sql_data.save_stream_metadata(stream_id, stream_name, owner_id,
                    #                                    data_descriptor, execution_context,
                    #                                    annotations,
                    #                                    stream_type, start_time, end_time)
                else:
                    print(
                        "Something went wrong in saving data points.")
        except Exception as e:
            self.logging.log(
                error_message="STREAM ID: " + stream_id + " - Cannot save stream. " + str(traceback.format_exc()),
                error_type=self.logtypes.CRITICAL)


    def save_stream_old(self, datastream: DataStream, localtime=False, ingestInfluxDB=False):

        """
        Stores metadata in MySQL and raw data in HDFS, file system, Cassandra, OR ScyllaDB (nosql data store could be changed in CC yaml file)
        :param datastream:
        :param localtime: if localtime is True then all DataPoints in a DataStream would be converted to UTC from localtime
        """
        owner_id = datastream.owner
        stream_name = datastream.name
        stream_id = ""
        data_descriptor = datastream.data_descriptor
        execution_context = datastream.execution_context
        annotations = datastream.annotations
        stream_type = datastream.datastream_type
        data = datastream.data
        if isinstance(data, list) and len(data) > 0 and (data[0].offset == "" or data[0].offset is None):
            raise ValueError(
                "Offset cannot be None and/or empty. Please set the same time offsets you received using get_stream.")

        data = self.filter_sort_datapoints(data)
        if localtime:
            data = self.convert_to_UTCtime(data)
        try:

            # get start and end time of a stream
            if data:
                if isinstance(data, list):
                    total_dp = len(data) - 1
                    if not datastream.start_time:
                        new_start_time = data[0].start_time
                    else:
                        new_start_time = datastream.start_time
                    if not datastream.end_time:
                        new_end_time = data[total_dp].start_time
                    else:
                        new_end_time = datastream.end_time
                else:
                    if not datastream.start_time:
                        new_start_time = data.start_time
                    else:
                        new_start_time = datastream.start_time
                    if not datastream.end_time:
                        new_end_time = data.start_time
                    else:
                        new_end_time = datastream.end_time

                stream_id = datastream.identifier
                
                status = self.nosql.write_file(owner_id, stream_id, data)

                if status:
                    # save metadata in SQL store
                    self.sql_data.save_stream_metadata(stream_id, stream_name, owner_id,
                                                       data_descriptor, execution_context,
                                                       annotations,
                                                       stream_type, new_start_time, new_end_time)
                    try:
                        if ingestInfluxDB:
                            self.timeSeriesData.store_data_to_influxdb(datastream=datastream)
                    except:
                        raise Exception
                else:
                    print(
                        "Something went wrong in saving data points. Please check error logs /var/log/cerebralcortex.log")
        except Exception as e:
            self.logging.log(
                error_message="STREAM ID: " + stream_id + " - Cannot save stream. " + str(traceback.format_exc()),
                error_type=self.logtypes.CRITICAL)
