from knext.ca.service.service_deployer import TritonServiceDeployer


def main():
    triton_deployer = TritonServiceDeployer(
        deploy_url='localhost',
        deploy_dir='/root/Codes/LLMKG/kNext/python/knext/knext/examples/ca_models/deploys',
        service_name='ca_simple',
        version_name='1',
    )    
    triton_deployer.upload_dag()
    triton_deployer.deploy_service()


if __name__ == '__main__':
    main()