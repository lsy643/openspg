import re
import json
from knext.ca.module.base import CABaseModule
from knext.ca.module.llms import LLMModule

URL = '121.41.29.31'


class ExtractNamesToJsonFromModule(CABaseModule):
    def __init__(self):
        super().__init__()
    def invoke(self, in_text):
        output_lines = in_text.split('\n')
        extract_pattern = re.compile(r'《(.+?)》')
        
        names_list = []
        #['add one']
        for line in output_lines:
            line_match = extract_pattern.findall(line)
            names_list.extend(line_match)
        return names_list


class NL2DSLModule(CABaseModule):
    def __init__(self, user_module_init_info):
        super().__init__()
        self.llm_module = LLMModule(url=user_module_init_info['llm_url'])
        self.parse_llm_module = ExtractNamesToJsonFromModule()
        
    def invoke(self, query):
        llm_output = self.llm_module(prompt=query)
        print(f'llm_output: {llm_output}')
        parsed_outputs = self.parse_llm_module(in_text=llm_output)
        return parsed_outputs

def create_user_module(user_module_init_info):
    return NL2DSLModule(user_module_init_info)


def local_main():
    # create user module
    nl2dsl = NL2DSLModule(url=URL)
    # run module

    results = nl2dsl(
        query = '周杰伦在2008年发表了哪些歌曲?',
        return_as_native = True
    )
    print(f'results: {results}')


def create_json():
    user_module_config = {
        'url': '121.41.29.31'
    }
    with open('user_module_config.json', 'w') as json_file:
        json.dump(user_module_config, json_file, indent=4)



# 部署为服务
# 完善triton的python backend

if __name__ == '__main__':
    #simple()
    create_json()
    #main()



