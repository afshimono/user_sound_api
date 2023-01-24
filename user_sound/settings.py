from dataclasses import dataclass
import os

@dataclass
class EnvVariables:
    
    db_password: str
    db_login: str
    db_name: str
    env: str
    instance_unix_socket: str = None
    db_url: str = None

    def __init__(self) -> None:
        self.db_login = os.environ["DATABASE_LOGIN"]
        self.db_password = os.environ["DATABASE_PASSWORD"]
        self.db_name = os.environ["DATABASE_NAME"]
        self.env = os.environ["ENV"]
        self.instance_unix_socket = os.environ.get("INSTANCE_UNIX_SOCKET")
        self.db_url = os.environ.get("DATABASE_URL")


env_vars = EnvVariables()
