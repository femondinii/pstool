import paramiko


class SSHClient:

    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )

    def execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(
            command,
            get_pty=True
        )

        output = stdout.read().decode(errors="ignore")
        error = stderr.read().decode(errors="ignore")

        if output:
            print(output)

        if error:
            print(error)

    def close(self):
        self.client.close()