import os

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

abs_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(abs_path)
Base = declarative_base()


def get_vd_version_table():
    class Vd_Vesion_Table(Base):
        __tablename__ = "vd_version"
        __table_args__ = (
            UniqueConstraint("eds_version", "date", name="uq_eds_version_date"),
            {"extend_existing": True},
        )
        id = Column("id", Integer, primary_key=True, autoincrement=True)
        eds_version = Column("eds_version", String(30))
        date = Column("date", String(20))
        alias = Column("alias", String(200))

    return Vd_Vesion_Table


def get_vd_mode_table_model():
    class Vd_Mode_Table(Base):
        __tablename__ = "vd_mode"
        __table_args__ = (
            ForeignKeyConstraint(["version_id"], ["vd_version.id"]),
            {"extend_existing": True},
        )
        id = Column("id", Integer, primary_key=True, autoincrement=True)

        version_id = Column("version_id", Integer)

        mode = Column("mode", String(20))
        thread = Column("thread", String(20))
        io_size = Column("io_size", String(20))
        # io_pattern = Column("io_pattern", String(20))
        file_size = Column("file_size", String(20))
        file_num = Column("file_num", String(20))

        def __repr__(self):
            return self.name

    return Vd_Mode_Table


def get_vd_detail_table_model(table_name):
    class Vd_Detail_Table(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}

        id = Column("id", Integer, primary_key=True, autoincrement=True)
        mode_id = Column("mode_id", Integer, ForeignKey("vd_mode.id"))

        timestamp = Column("timestamp", String(30))
        Run = Column("Run", String(70))
        Rate = Column("Rate", String(20))
        MB_sec = Column("MB/sec", String(20))
        Resp = Column("Resp", String(20))

        def __repr__(self):
            return self.name

    return Vd_Detail_Table
