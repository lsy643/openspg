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
import logging
logger = logging.getLogger(__file__)


class FileManager(object):
    def __init__(self) -> None:
        pass
    
    def upload_dir(self, local_path, remote_path):
        raise NotImplementedError



class LocalFileManger(FileManager):
    def __init__(self, **kwargs) -> None:
        super().__init__
    
    def upload_dir(self, local_path, remote_path):
        pass
    

class SSHFileManager(FileManager):
    def __init__(self, host, port=22, username=None, password=None, key_file=None):
        super().__init__()
        import paramiko
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_file is not None:
            private_key = paramiko.RSAKey.from_private_key_file(key_file)
            self.ssh.connect(host, port=port, username=username, pkey=private_key)
        else:
            self.ssh.connect(host, port=port, username=username, password=password)
        self.sftp = self.ssh.open_sftp()

    def mkdir_p(self, remote_path):
        dir_path = str()
        for dir_folder in remote_path.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"/{0}".format(dir_folder)
            try:
                self.sftp.listdir(dir_path)
            except IOError:
                self.sftp.mkdir(dir_path)

    def upload_dir(self, local_path, remote_path):
        self.mkdir_p(remote_path)
        for item in os.listdir(local_path):
            local_item_path = os.path.join(local_path, item)
            remote_item_path = os.path.join(remote_path, item)
            print(f'start put {local_item_path} to {remote_item_path}')
            if os.path.isfile(local_item_path):
                try:
                    self.sftp.put(local_item_path, remote_item_path)
                except Exception as err:
                    print(f'sftp put from {local_item_path} to {remote_item_path} Failed for {err}')
            elif os.path.isdir(local_item_path):
                try:
                    self.sftp.mkdir(remote_item_path)
                except IOError:
                    pass  
                self.upload_dir(local_item_path, remote_item_path)
    
        def __del__(self):
            self.sftp.close()
            self.ssh.close()

    def execute_command(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        print(stdout.read().decode('utf-8'))
    
    def __del__(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()

def create_file_manager(host, **kwargs):
    if host == 'localhost':
        return LocalFileManger(**kwargs)
    else:
        return SSHFileManager(host=host, **kwargs)
    