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
import string
import shutil
import pathlib
import logging
import tempfile

logger = logging.getLogger(__name__)
from knext.ca.service.file_manager import create_uploader


class ServiceDeployer(object):
    """
    This is a base class designed to provide a generic interface for deploying services to various environments.
    It is intended to be extended by subclassing to handle specific deployment strategies needed for different
    platforms such as Alibaba Cloud, internal company environments, or other cloud providers.

    Subclasses should implement the necessary methods to manage the deployment process according to the
    requirements of their target environment. These may include setup, teardown, update, and status checking
    functionalities.

    By providing a consistent interface across different environments, `ServiceDeployer` allows for greater
    flexibility and ease of use when managing deployments across multiple platforms.
    """
    def __init__(self, *args, **kwargs):
        pass

    def upload_model(self):
        raise NotImplementedError

    def upload_dag(self):
        raise NotImplementedError

    def deploy_service(self, *args, **kwargs):
        raise NotImplementedError


class TritonServiceDeployer(object):
    def __init__(self, service_name, version_name, file_manager, deploy_dir, working_dir=None, local_deploy_dir=None) -> None:
        super(TritonServiceDeployer, self).__init__()
        self.service_name = service_name
        self.version_name = version_name
        self.deploy_dir = deploy_dir
        self.ca_dir = pathlib.Path(__file__).parent.parent
        self.service_template_dir = os.path.join(self.ca_dir, 'service', 'template')
        self.working_dir = working_dir if working_dir else os.getcwd()
        self.local_deploy_dir = local_deploy_dir if local_deploy_dir else tempfile.mkdtemp()
        self.file_manager = file_manager
        logger.info(f'****local_deploy_dir: {local_deploy_dir}****')
        
    def upload_model(self):
        # upload model 
        pass

    def upload_dag(self):
        # prepare a local dir
        self.prepare_local_deploy_dir(self.local_deploy_dir)
        # upload local_deploy_dir to remote dir
        self.file_manager.upload_dir(
            local_path=self.local_deploy_dir,
            remote_path=self.deploy_dir
        )
     
    def prepare_local_deploy_dir(self, local_deploy_dir):
        # create service directory
        service_dir = os.path.join(local_deploy_dir, self.service_name)        
        os.makedirs(service_dir, exist_ok=True)
        # create version directory
        version_dir = os.path.join(service_dir, self.version_name)
        os.makedirs(version_dir, exist_ok=True)
        
        # upload user related files to version_dir
        shutil.copytree(self.working_dir, version_dir, dirs_exist_ok=True)
        
        # upload model.py from template to version_dir
        org_model_path = os.path.join(self.service_template_dir, 'model.py')
        dst_model_path = os.path.join(version_dir, 'model.py')
        shutil.copy(org_model_path, dst_model_path)
        logger.info(f'copy from {org_model_path} to {dst_model_path}')
        
        # upload config.py from template to service_dir
        config_template_path = os.path.join(self.service_template_dir, 'template.pbtxt')
        with open(config_template_path, 'r') as file:
            template_content = file.read()

        template = string.Template(template_content)
        config_data = {
            'service_name': self.service_name
        }
        
        config_content = template.safe_substitute(config_data)
        dst_config_path = os.path.join(service_dir, 'config.pbtxt')
        with open(dst_config_path, 'w') as file:
            file.write(config_content)
                        
    def deploy_service(self, backend='python', *args, **kwargs):
        if backend == 'vllm':
            # deploy llm with gpu
            image = 'nvcr.io/nvidia/tritonserver:24.02-vllm-python-py3'
        elif backend == 'python':
            # deploy with 
            images = 'nvcr.io/nvidia/tritonserver:24.02-pyt-python-py3'
        else:
            raise ValueError(f'backend not in [vllm, python]')
        
        container_name = f'{self.service_name}_{self.version_name}'
        container_workdir = os.path.join(self.local_deploy_dir, self.service_name)
        command_to_run = f'tritonserver --model-repository ./model_repository'
        # create command
        docker_command = (
            f"docker run --gpus all -it --net=host "
            f"--rm "
            f"--name {container_name} "
            f"--shm-size=10.24gb --ulimit memlock=-1 "
            f"--ulimit stack=67108864 "
            f"--gpus all "
            f"-v /root:/root "
            f"-w {container_workdir} "  # 设置工作目录
            f"{image} "
            f"/bin/bash -c '{command_to_run}'"  # 容器内执行的命令
        )
        
        print(f'docker_command: {docker_command}')
        # start triton service
        # execute remotely
        self.file_manager.execute_command(docker_command)
             


