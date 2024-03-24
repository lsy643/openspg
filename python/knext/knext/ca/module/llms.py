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
import time
import requests
import json
import numpy as np
from knext.ca.module.base import CABaseModule


class LLMClient(object):
    def __init__(self, url) -> None:
        self.generate_url = f'http://{url}:8000/v2/models/vllm_model/generate'
        self.fetch_config_url = f"http://{url}:8000/v2/models/vllm_model/config"
        self.headers = {'Content-Type': 'application/json'}
        
    def call_service(self, prompt, max_tokens=32, temperature=0):
        data = {
            'text_input': prompt,
            'parameters': {
                'stream': False, 
                'temperature': temperature,
                'max_tokens': max_tokens,
                #'exclude_inputs_in_outputs': True,
            }
        }
        
        response = requests.post(self.generate_url, headers=self.headers, data=json.dumps(data))
    
        if response.status_code == 200:
            #print(f'response from server: {response.json()}')
            response_result = response.json()['text_output']
            newline_pos = response_result.find('\n')
            if newline_pos != -1:
                return response_result[newline_pos+1:]
            else:
                return response_result
        else:
            return (f'Error: {response.status_code} - {response.text}')
        
    def display_model_config(self):
        response = requests.get(self.fetch_config_url)

        if response.status_code == 200:
            # 将结果解析为JSON格式
            config = response.json()
            # 结构化打印JSON结果
            print(json.dumps(config, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        
class LLMModule(CABaseModule):
    def __init__(self, url):
        super(LLMModule, self).__init__()
        self.llm_client  = LLMClient(url)

    def invoke(self,
               prompt,
               max_output_len=64
               ):
        result = self.llm_client.call_service(
            prompt=prompt, 
            max_tokens=max_output_len)
        return result#{'response', result}


def main():
    llm_client = LLMClient(url='8.139.252.237')
    response = llm_client.call_service(
        prompt='What is Triton Inference Server?',
        )
    print(f'response: {response}')
    #llm_client.display_model_config()

if __name__ == '__main__':
    main()