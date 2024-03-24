# Copyright 2023 Ant Group CO., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from abc import ABC, abstractmethod
from typing import Union
import os
import oss2
import logging
import json
import importlib

logger = logging.getLogger(__name__)


def create_service_module(working_dir):

    user_module_init_info = {}
    # create service_module
    user_module = importlib.import_module('user_module')

    user_module_config_path = os.path.join(working_dir, 'user_module_config.json')
    if os.path.exists(user_module_config_path):
        with open(user_module_config_path, 'r') as json_file:
            user_module_config = json.load(json_file)
            user_module_init_info.update(user_module_config)
    user_module_instance = user_module.create_user_module(user_module_init_info)
    return user_module_instance


class BaseService(object):
    """
    BaseService is an abstract base class intended to serve as a template for various service implementations.
    This class provides a basic structure for services such as large model processing, embedding generation,
    and other computational tasks that can be encapsulated as a service.

    Child classes should override the __call__ method to provide the specific functionality required for
    the service they are implementing.

    """
    def __init__(self, service_info):
        self.service_info = service_info

    def __call__(self, inputs_dict):
        raise NotImplementedError


class AliyunOSSClient(object):
    def __init__(self, bucket_name, access_key_id, access_key_secret, endpoint='https://oss-cn-hangzhou.aliyuncs.com'):
        """
        Initialize the AliyunOSSClient with credentials and an endpoint.
        This client will allow you to interact with the Alibaba Cloud OSS service.

        :param bucket_name: The name of the OSS bucket to which files will be uploaded.
        :param access_key_id: The access key ID for OSS authentication.
        :param access_key_secret: The access key secret for OSS authentication.
        :param endpoint: The endpoint URL for the OSS service. Defaults to the Hangzhou region.
        """
        self.bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

    def upload_single_file(self, local_file_path, oss_file_path):
        """
        Upload a single file to the specified path in OSS.

        :param local_file_path: The path to the local file to be uploaded.
        :param oss_file_path: The path in OSS where the file will be stored.
        """
        self.bucket.put_object_from_file(oss_file_path, local_file_path)

    def upload_dir(self, local_dir, oss_dir):
        """
        Recursively upload a directory and its contents to OSS.

        :param local_dir: The local directory path whose contents are to be uploaded.
        :param oss_dir: The OSS directory path where the contents will be stored.
        """
        if not os.path.isdir(local_dir):
            raise NotADirectoryError("The local directory does not exist: " + local_dir)

        # Recursively upload all files in the directory
        for root, dirs, files in os.walk(local_dir):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(local_file_path, local_dir)
                oss_file_path = os.path.join(oss_dir, relative_path)
                self.upload_single_file(local_file_path, oss_file_path.replace('\\', '/'))  # replace for Windows paths
