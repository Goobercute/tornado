import paramiko
import logging


class SSHConnection:
    def __init__(self, hostname, port=22, username="root", password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def close(self):
        if self.transport.is_active():
            self.sftp.close()
            self.transport.close()

    def put_file(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self.sftp.get(remote_path, local_path)

    def exec_command(self, command):
        ssh = self.transport.open_session()
        try:
            ssh.exec_command(command)
        except paramiko.SSHException as e:
            logging.error(f"Failed to execute command: {command}. Error: {e}")

    def check_remote_file_exists(self, remote_path):
        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False
        except (IOError, Exception) as e:
            logging.error(
                f"Failed to check remote file existence: {remote_path}. Error: {e}"
            )
            return False
