import os
from sqlalchemy import update
import yaml
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.inspection import inspect

abs_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(abs_path)
Base = declarative_base()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class DatabaseHandler:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData()

    def create_table(self, table):  # 如果表已经存在，不再创建
        try:
            table.__table__.create(self.engine)
        except Exception as e:
            print(e)

    def check_table_exist(self, table):
        inspector = inspect(self.engine)
        if inspector.has_table(table.__tablename__):
            return True
        else:
            return False

    def insert_data(self, data):
        try:
            self.session.add(data)
            self.session.commit()
            return data.id
        except Exception as e:
            self.session.rollback()
            # 打印异常信息
            print(e)
            raise e
        finally:
            self.session.close()

    def bulk_insert_data(self, table, data):
        try:
            self.session.bulk_insert_mappings(table, data)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def update_data_by_id(self, table, data, id):
        try:
            res = self.session.query(table).filter_by(id=id).first()
            for key, value in data.items():
                setattr(res, key, value)
            self.session.commit()
            return id
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def query_data_by_id(self, table, id):
        try:
            res = self.session.query(table).filter_by(id=id).first()
            return object_as_dict(res)
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def query_data(self, table):
        try:
            res = self.session.query(table).all()
            return [object_as_dict(item) for item in res]
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def delete_data_by_id(self, table, id):
        try:
            res = self.session.query(table).filter_by(id=id).first()
            self.session.delete(res)
            self.session.commit()
            return id
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()


def get_db_connetion():
    with open(abs_path + "/mysql.yaml", encoding="utf-8") as stream:
        yaml_data = yaml.load(stream=stream, Loader=yaml.FullLoader)
    db_url = (
        f"mysql+mysqlconnector://"
        f"{yaml_data['mysql']['user']}:"
        f"{yaml_data['mysql']['password']}@"
        f"{yaml_data['mysql']['host']}:"
        f"{yaml_data['mysql']['port']}/"
        f"{yaml_data['mysql']['database']}"
        f"?auth_plugin=mysql_native_password"
    )
    db_handler = DatabaseHandler(db_url)
    return db_handler
