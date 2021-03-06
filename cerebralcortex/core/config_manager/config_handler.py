# Copyright (c) 2018, MD2K Center of Excellence
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

import yaml

class ConfigHandler():
    def load_file(self, filepath: str):
        """
        Helper function to load a yaml file
        :param config_dir_path: path to a yml configuration file for Cerebral Cortex
        """

        # if config_dir_path[-1]!="/":
        #     config_dir_path += "/"

        # if ".yml" not in config_dir_path:
        #     filepath = config_dir_path+"cerebralcortex.yml"

        with open(filepath, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)



        if "hdfs" in self.config and self.config["hdfs"]["raw_files_dir"]!="" and self.config["hdfs"]["raw_files_dir"][-1] !="/":
            self.config["hdfs"]["raw_files_dir"]+="/"

        # if self.config["data_ingestion"]["filesystem_path"]!="" and self.config["data_ingestion"]["filesystem_path"][-1] !="/":
        #     self.config["data_ingestion"]["filesystem_path"]+="/"
        #
        # if self.config["data_replay"]["data_dir"]!="" and self.config["data_replay"]["data_dir"][-1] !="/":
        #     self.config["data_replay"]["data_dir"]+="/"


