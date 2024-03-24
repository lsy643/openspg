# Deploying a Service on Aliyun ECS with Python

This tutorial guides you through deploying a service on an Aliyun Elastic Compute Service (ECS) instance. You'll learn how to request ECS resources, start a container, build user logic, use a deployer interface, deploy the service, and verify its operation.

## Prerequisites

- An Aliyun account
- Python installed on your local machine
- Docker installed if you're using containers
- Basic understanding of Python and Docker (if containers are used)

## 1. Requesting Aliyun ECS Resources and Starting the Corresponding Container

Before you begin, ensure you have an Aliyun account and create an ECS instance with GPU driver

Follow these steps to start your container on the ECS instance:

1. SSH into your ECS instance:

    ```bash
    ssh root@<your_ecs_ip>
    ```

2. Install Docker on your ECS instance if it's not already installed:

    ```bash
    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    apt-cache policy docker-ce
    sudo apt install docker-ce
    sudo systemctl status docker

    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    ```

3. Run your Docker container:

   ```bash
   docker run --shm-size=1g \
           --ulimit memlock=-1 \
           -p 8000:8000 \
           -p 8001:8001 \
           -p 8002:8002 \
           --ulimit stack=67108864 \
           --gpus all\
           -v /root:/root \
           -ti nvcr.io/nvidia/tritonserver:24.02-pyt-python-py3e
   ```



## 3. Building User Logic

Create a `user_module.py` file to define your user logic. This will depend on what your application is designed to do. Here's an example structure:

```python
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
```

## 4. Using the Deployer Interface

Use TritonServiceDeployer to deploy your service. This typically involves importing the deployer module and calling its deployment method:

    ```python
    triton_deployer = TritonServiceDeployer(
        deploy_url='localhost',
        deploy_dir='/root/Codes/LLMKG/kNext/python/knext/knext/examples/ca_models/deploys',
        service_name='ca_simple',
        version_name='1',
    )    
    triton_deployer.upload_dag()
    ```

Ensure you review your deployer's documentation for specific details on how to use it.

## 5. Deploying the Service

Deploying the service usually involves executing a script or a command that uses the deployer's interface you've just set up. If the previous step was successful, your service should now be running on the ECS instance.

## 6. Verifying with `client.py`

Finally, verify that your service is running as expected. This typically involves calling an endpoint exposed by your service or running a client script that interacts with your service.

Assuming you have a `client.py` script for verification, run it:

```bash
python client.py
```

