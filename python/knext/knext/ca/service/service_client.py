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

import numpy as np
import json
from abc import ABC, abstractmethod
from typing import Union
import tritonclient.http as httpclient
from tritonclient.utils import *


class ServiceClient(object):
    def __init__(self):
        pass

    def call_service(self, inputs_dict):
        raise NotImplementedError


class TritonHttpClient(ServiceClient):

    def __init__(self, model_name, url) -> None:
        super(TritonHttpClient, self).__init__()
        self.model_name = model_name
        self._client = httpclient.InferenceServerClient(f"{url}:8000")
        
    def call_service(self, inputs_dict):
        # prepare inputs
        inputs_data = json.dumps(inputs_dict).encode('utf-8')
        inputs_data_np = np.array([inputs_data])
        inputs = [
            httpclient.InferInput("INPUT0", [1], "BYTES")            
        ]
        inputs[0].set_data_from_numpy(inputs_data_np)

        # prepare outputs
        outputs = [
            httpclient.InferRequestedOutput("OUTPUT0"),
        ]

        #call infer
        response = self._client.infer(self.model_name, inputs, request_id=str(1), outputs=outputs)
        
        # parse outputs
        #result = response.get_response()
        output0_data = response.as_numpy("OUTPUT0")[0].decode('utf-8')
        outputs_dict = json.loads(output0_data)
        return outputs_dict