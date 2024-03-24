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

import os
from abc import ABC, abstractmethod
from typing import Union
import logging

logger = logging.getLogger(__name__)


class LoraHub(object):
    def __init__(self, base_model, base_model_version=None):
        """
        Initialize the LoraHub with a base model and an optional base model version.
        If no version is provided, it defaults to 'latest'.

        :param base_model: Identifier for the base model used by the LoraHub.
        :param base_model_version: The version of the base model. Defaults to 'latest'.
        """
        self.base_model = base_model
        self.base_model_version = base_model_version or 'latest'

    def deploy_lora(self, lora_name, local_lora_dir):
        """
        Deploy a LoRa configuration by uploading it from a local directory to a remote location.

        :param lora_name: The name of the LoRa configuration to be deployed.
        :param local_lora_dir: The directory path on the local system where the LoRa configuration is stored.
        """
        remote_lora_dir = self.get_remote_lora_dir(lora_name)
        upload_dir_with_info(local_lora_dir, remote_lora_dir)

    def deploy_multi_lora(self, lora_name, local_lora_dir_list):
        """
        Deploy multiple LoRa configurations by uploading each from a list of local directories to their respective remote locations.

        :param lora_name: The name of the base LoRa configuration under which multiple configurations will be grouped.
        :param local_lora_dir_list: A list of directory paths on the local system where the LoRa configurations are stored.
        """
        for local_lora_dir in local_lora_dir_list:
            base_name = os.path.basename(local_lora_dir)
            remote_lora_dir = os.path.join(self.get_remote_lora_dir(lora_name), base_name)
            upload_dir_with_info(lora_dir, oss_dir)

    def get_remote_lora_dir(self, lora_name):
        """
        Abstract method to be implemented by subclasses to determine the remote directory for a given LoRa configuration name.

        :param lora_name: The name of the LoRa configuration.
        :return: The remote directory path for the LoRa configuration.
        """
        raise NotImplementedError

    def upload_dir_with_info(self, local_dir, remote_dir):
        raise NotImplementedError


class AliyunOSSLoraHub(LoraHub):
    def __init__(self, aliyun_oss_client, base_model, base_model_version=None, oss_lora_prefix=''):
        """
        Initialize AliyunOSSLoraHub with an instance of AliyunOSSClient and base model information.

        :param aliyun_oss_client: An instance of AliyunOSSClient prepared to interact with Alibaba Cloud OSS.
        :param base_model: Identifier for the base model used by the LoraHub.
        :param base_model_version: The version of the base model, defaults to 'latest' if not specified.
        :parma oss_lora_prefix: The prefix path to store lora at aliyun oss
        """
        super().__init__(
            base_model=base_model,
            base_model_version=base_model_version,
        )
        self.aliyun_oss_client = aliyun_oss_client
        self.oss_lora_prefix = oss_lora_prefix

    def get_remote_lora_dir(self, lora_name):
        """
        Generate the path for the remote directory in OSS based on the lora_name, base model, and version.

        :param lora_name: The name of the LoRa configuration.
        :return: The generated remote directory path for the LoRa configuration.
        """
        # Here you can define the logic to generate the base remote directory path
        # For simplicity, the example below uses the lora_name and base_model_version
        # to create a directory structure.
        return os.path.join(f'oss://{self.aliyun_oss_client.bucket}', self.oss_lora_prefix, self.base_model, self.base_model_version, self.lora_name)

    def upload_dir_with_info(self, local_dir, remote_dir):
        """
        Upload a local directory to the specified remote directory in Alibaba Cloud OSS, utilizing AliyunOSSClient.

        :param local_dir: The local directory path to be uploaded.
        :param remote_dir: The remote directory path in OSS where the local directory contents will be uploaded.
        """
        try:
            self.logger.info(f"Uploading directory {local_dir} to OSS at {remote_dir}")
            self.aliyun_oss_client.upload_dir(local_dir, remote_dir)
            self.logger.info("Upload successful.")
        except Exception as e:
            self.logger.error(f"An error occurred while uploading: {e}")
            raise