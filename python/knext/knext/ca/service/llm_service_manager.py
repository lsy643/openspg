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


class LLMServiceManager(object):
    """
    The LLMServiceManager class serves as an abstract base class for managing different aspects of
    a deployed Large Language Model (LLM). It provides an interface for subclasses that are tailored
    to handle LLM operations in particular environments, such as Alibaba Cloud (Aliyun) or an internal
    corporate environment.

    The class is designed to facilitate lightweight updates to a deployed LLM. These updates can include
    deploying or removing elements such as LoRAs (lightweight re-rankers or adaption layers), prompts,
    or draft models. Each of these elements plays a role in enhancing or customizing the LLM's behavior
    without the need for full-scale retraining or redeployment.

    Subclasses should implement the specific logic for interacting with the underlying infrastructure
    or platform to carry out the actions defined by the base class's interface.
    """
    def __init__(self, base_model_name, lora_hub):
        self.base_model_name = base_model_name
        self.lora_hub = lora_hub

    def deploy_lora(self, lora_name, lora_dir_or_list):
        if isinstance(lora_dir_or_list, str):
            self.lora_hub.deploy_lora(lora_name=lora_name, lora_dir=lora_dir_or_list)
        elif isinstance(lora_dir_or_list, (tuple, list)):
            self.lora_hub.deploy_multi_lora(lora_name, local_lora_dir_list=lora_dir_or_list)

    def remove_lora(self, lora_name):
        raise NotImplementedError

    def deploy_prompt(self, prompt_name, prompt):
        raise NotImplementedError

    def remove_prompt(self, prompt_name):
        raise NotImplementedError

    def deploy_draft_model(self, draft_model_name, draft_model):
        raise NotImplementedError

    def remove_draft_model(self, draft_model_name):
        raise NotImplementedError