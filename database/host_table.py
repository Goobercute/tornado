import os

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

abs_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(abs_path)
Base = declarative_base()


def get_host_table_model():
    class Host_Table(Base):
        __tablename__ = "host"
        __table_args__ = {"extend_existing": True}
        id = Column("host_id", Integer, primary_key=True, autoincrement=True)
        host_ip = Column("host_ip", String(30), primary_key=True)
        username = Column("username", String(20))
        password = Column("password", String(30))
        port = Column("port", Integer)
        group = Column("group", String(20))
        status = Column("status", String(20))

        def __init__(self, host_ip, username, password, port, group, status):
            self.host_ip = host_ip
            self.username = username
            self.password = password
            self.port = port
            self.group = group
            self.status = status

    return Host_Table
