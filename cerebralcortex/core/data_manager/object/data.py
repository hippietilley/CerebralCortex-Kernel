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

from cerebralcortex.core.log_manager.log_handler import LogTypes
from minio import Minio

from cerebralcortex.core.data_manager.object.minio_handler import MinioHandler


class ObjectData(MinioHandler):
    def __init__(self, CC):
        """

        :param CC: CerebralCortex object reference
        """
        self.CC = CC
        self.config = CC.config

        self.logging = CC.logging
        self.logtypes = LogTypes()

        self.host = self.config["minio"]["host"]
        self.port = self.config["minio"]["port"]
        self.access_key = self.config["minio"]["access_key"]
        self.secret_key = self.config["minio"]["secret_key"]
        self.secure = self.config["minio"]["secure"]

        if self.config["nosql_storage"]=="aws_s3":
            db_url = str(self.host)
        else:
            db_url = str(self.host) + ":" + str(self.port)
        self.minioClient = Minio(db_url, access_key=self.access_key, secret_key=self.secret_key, secure=self.secure)
