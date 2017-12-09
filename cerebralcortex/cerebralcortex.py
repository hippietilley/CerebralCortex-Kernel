# Copyright (c) 2017, MD2K Center of Excellence
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

import os
import uuid
from datetime import datetime
from typing import List

from cerebralcortex.core.config_manager.config import Configuration
from cerebralcortex.core.data_manager.object.data import ObjectData
from cerebralcortex.core.data_manager.sql.data import SqlData
from cerebralcortex.core.data_manager.time_series.data import TimeSeriesData
from cerebralcortex.core.datatypes.datapoint import DataPoint
from cerebralcortex.core.datatypes.datastream import DataStream
from cerebralcortex.core.file_manager.file_io import FileIO

from cerebralcortex.core.data_manager.raw.stream_handler import DataSet
from cerebralcortex.core.data_manager.raw.data import RawData
from cerebralcortex.core.messaging_manager.messaging_queue import MessagingQueue

class CerebralCortex:
    def __init__(self, configuration_filepath=None, timezone='UTC'):

        if not configuration_filepath:
            configuration_filepath = os.path.join(os.path.dirname(__file__), 'core/resources/cc_configuration.yml')
        self.config_filepath = configuration_filepath
        self.config = Configuration(configuration_filepath).config
        self.timezone = timezone

        self.RawData = RawData(self)
        self.SqlData = SqlData(self)
        self.ObjectData = ObjectData(self)
        self.TimeSeriesData = TimeSeriesData(self)
        self.MessagingQueue = MessagingQueue(self)
        self.FileIO = FileIO()

    ###########################################################################
    ############### RAW DATA MANAGER METHODS ##################################
    ###########################################################################
    def save_stream(self, datastream: DataStream):
        """
        Saves datastream raw data in Cassandra and metadata in MySQL.
        :param datastream:
        """
        self.RawData.save_stream(datastream)

    def get_stream(self, stream_id: uuid, day:str, start_time: datetime = None, end_time: datetime = None,
                   data_type=DataSet.COMPLETE) -> DataStream:
        """

        :param stream_id:
        :param day:
        :param start_time:
        :param end_time:
        :param data_type:
        :return:
        """
        return self.RawData.get_stream(stream_id, day, start_time, end_time, data_type)

    def get_stream_samples(self, stream_id, day, start_time=None, end_time=None) -> List[DataPoint]:
        """
        returns list of DataPoint objects
        :param stream_id:
        :param day:
        :param start_time:
        :param end_time:
        :return:
        """
        return self.RawData.get_stream_samples(stream_id, day, start_time, end_time)

    ###########################################################################
    ############### SQL DATA MANAGER METHODS ##################################
    ###########################################################################

    ################### STREAM RELATED METHODS ################################

    def is_stream(self, stream_id: uuid) -> bool:
        """

        :param stream_id:
        :return:
        """
        return self.SqlData.is_stream(stream_id)

    def get_stream_name(self, stream_id: uuid) -> str:
        """

        :param stream_id:
        :return:
        """
        return self.SqlData.get_stream_name(stream_id)

    def get_stream_id(self, stream_name: str) -> str:
        """

        :param stream_name:
        :return:
        """
        return self.SqlData.get_stream_id(stream_name)

    def is_user(self, user_id: uuid=None, user_name:uuid=None) -> str:
        """

        :param user_id:
        :return:
        """
        return self.SqlData.is_user(user_id, user_name)

    def get_user_id(self, user_name: str) -> str:
        """

        :param user_name:
        :return:
        """
        return self.SqlData.get_user_id(user_name)

    def get_user_name(self, user_id: uuid) -> str:
        """

        :param user_id:
        :return:
        """
        return self.SqlData.get_user_name(user_id)

    def get_user_streams_metadata(self, user_id: str) -> uuid:
        """

        :param user_id:
        :return:
        """
        return self.SqlData.get_user_streams_metadata(user_id)

    def get_user_streams(self, user_id: uuid) -> dict:
        """

        :param user_id:
        :return:
        """
        return self.SqlData.get_user_streams(user_id)

    def get_all_users(self, study_name: str) -> dict:
        """

        :param study_name:
        :return:
        """
        return self.get_all_users(study_name)

    def get_stream_duration(self, stream_id: uuid) -> dict:
        """

        :param stream_id:
        :return:
        """
        return self.SqlData.get_stream_duration(stream_id)

    def get_stream_names_ids_by_user(self, user_id: uuid, stream_name: str = None, start_time: datetime = None,
                                     end_time: datetime = None) -> List:
        """
        Returns all the stream ids and name that belongs to an owner-id
        :param user_id:
        :return:
        """
        return self.SqlData.get_stream_names_ids_by_user(user_id, stream_name, start_time, end_time)

    def get_stream_metadata(self, stream_id: uuid) -> dict:
        """

        :param stream_id:
        :return:
        """
        return self.SqlData.get_stream_metadata(stream_id)

    ################### USER RELATED METHODS ##################################

    def get_user_metadata(self, user_id, username: str = None) -> List:
        """

        :param user_id:
        :param username:
        :return:
        """
        return self.SqlData.get_user_metadata(user_id, username)

    def login_user(self, username: str, password: str) -> bool:
        """

        :param username:
        :param password:
        :return:
        """
        return self.SqlData.login_user(username, password)

    def is_auth_token_valid(self, token_owner: str, auth_token: str, auth_token_expiry_time: datetime) -> bool:
        """

        :param token_owner:
        :param auth_token:
        :param auth_token_expiry_time:
        :return:
        """
        return self.SqlData.is_auth_token_valid(token_owner, auth_token, auth_token_expiry_time)

    def update_auth_token(self, username: str, auth_token: str, auth_token_issued_time: datetime,
                          auth_token_expiry_time: datetime) -> str:
        """

        :param username:
        :param auth_token:
        :param auth_token_issued_time:
        :param auth_token_expiry_time:
        :return uuid of the current user
        """
        return self.SqlData.update_auth_token(username, auth_token, auth_token_issued_time, auth_token_expiry_time)

    def gen_random_pass(self, string_type: str, size: int = 8) -> str:
        """
        :param string_type:
        :param size:
        :return:
        """
        return self.SqlData.gen_random_pass(string_type, size)

    def encrypt_user_password(self, user_password: str) -> str:
        """
        :param user_password:
        :return:
        """
        self.SqlData.encrypt_user_password(user_password)

    ################### KAFKA RELATED METHODS ##################################

    def store_or_update_Kafka_offset(self, topic: str, topic_partition: str, offset_start: str, offset_until: str):
        """

        :param topic:
        :param topic_partition:
        :param offset_start:
        :param offset_until:
        """
        self.SqlData.store_or_update_Kafka_offset(topic, topic_partition, offset_start, offset_until)

    def get_kafka_offsets(self, topic: str) -> dict:
        """

        :param topic:
        :return:
        """
        return self.SqlData.get_kafka_offsets(topic)

    ###########################################################################
    ############### OBJECTS DATA MANAGER METHODS ##############################
    ###########################################################################

    def create_bucket(self, bucket_name: str) -> bool:
        """
        creates a bucket
        :param bucket_name:
        """
        return self.ObjectData.create_bucket(bucket_name)

    def upload_object(self, bucket_name: str, object_name: str, object_filepath: object) -> bool:
        """
        Uploads an object to Minio storage
        :param bucket_name:
        :param object_name:
        :param object_filepath: it shall contain full path of a file with file name (e.g., /home/nasir/obj.zip)
        :return: True/False, in case of an error {"error": str}
        """
        return self.ObjectData.upload_object(bucket_name, object_name, object_filepath)

    def get_buckets(self) -> List:
        """
        returns all available buckets in Minio storage
        :return: [{bucket-name: str, last_modified: str}], in case of an error [{"error": str}]
        """
        return self.ObjectData.get_buckets()

    def get_bucket_objects(self, bucket_name: str) -> List:
        """
        returns a list of all objects stored in the specified Minio bucket
        :param bucket_name:
        :return:{object-name:{stat1:str, stat2, str}},  in case of an error [{"error": str}]
        """
        return self.ObjectData.get_bucket_objects(bucket_name)

    def get_object_stats(self, bucket_name: str, object_name: str) -> dict:
        """
        Returns properties (e.g., object type, last modified etc.) of an object stored in a specified bucket
        :param bucket_name:
        :param object_name:
        :return: {stat1:str, stat2, str},  in case of an error {"error": str}
        """
        return self.ObjectData.get_object_stats(bucket_name, object_name)

    def get_object(self, bucket_name: str, object_name: str) -> dict:
        """
        Returns stored object (HttpResponse)
        :param bucket_name:
        :param object_name:
        :return: object (HttpResponse), in case of an error {"error": str}
        """
        return self.ObjectData.get_object(bucket_name, object_name)

    def is_bucket(self, bucket_name: str) -> bool:
        """

        :param bucket_name:
        :return: True/False, in case of an error {"error": str}
        """
        self.ObjectData.is_bucket(bucket_name)

    ###########################################################################
    ############### TIME SERIES DATA MANAGER METHODS ##########################
    ###########################################################################

    def store_data_to_influxdb(self, datastream: DataStream):
        """
        :param datastream:
        """
        self.TimeSeriesData.store_data_to_influxdb(datastream)

    ###########################################################################
    ############### IO MANAGER METHODS ########################################
    ###########################################################################

    def read_file(self, filepath: str) -> str:
        """

        :param filepath:
        :return:
        """
        return self.FileIO.read_file(filepath)

    def file_processor(self, msg: dict, zip_filepath: str) -> DataStream:
        """
        :param msg:
        :param zip_filepath:
        :return:
        """
        return self.FileIO.file_processor(msg, zip_filepath)

    def get_gzip_file_contents(self, filepath: str) -> str:
        """
        Read and return gzip compressed file contents
        :param filepath:
        :return:
        """
        self.FileIO.get_gzip_file_contents(filepath)

    #################################################
    #   Kafka consumer producer
    #################################################

    def kafka_produce_message(self, topic: str, msg: str):
        """

        :param topic:
        :param msg:
        """
        self.MessagingQueue.produce_message(topic, msg)

    def kafka_subscribe_to_topic(self, topic: str, auto_offset_reset: str="largest"):
        """

        :param topic:
        :param auto_offset_reset:
        """
        return self.MessagingQueue.subscribe_to_topic(topic)