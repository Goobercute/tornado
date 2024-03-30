import json
import os

import tornado
from tornado import web

from database.db import get_db_connetion
from database.host_table import get_host_table_model

abs_path = os.path.dirname(os.path.abspath(__file__))


class Host_Handler(web.RequestHandler):
    db_handler = get_db_connetion()

    def post(self):
        # 从json中获取参数
        body = tornado.escape.json_decode(self.request.body)
        host_ip = body.get("host_ip", "")
        username = body.get("username", "root")
        password = body.get("password", "eds@1234sangfornetwork")
        port = body.get("port", "22")
        group = body.get("group", "")
        status = body.get("status", "healthy")
        # 插入数据
        host_table = get_host_table_model()
        host_data = host_table(
            host_ip=host_ip,
            username=username,
            password=password,
            port=port,
            group=group,
            status=status,
        )
        res = self.db_handler.insert_data(host_data)
        self.write({"id": res})

    def put(self, id):
        # 从json中获取参数
        body = tornado.escape.json_decode(self.request.body)
        host_ip = body.get("host_ip", "")
        username = body.get("username", "root")
        password = body.get("password", "eds@1234sangfornetwork")
        port = body.get("port", "22")
        group = body.get("group", "")
        # 插入数据
        host_table = get_host_table_model()
        host_data = {
            "host_ip": host_ip,
            "username": username,
            "password": password,
            "port": port,
            "group": group,
        }
        res = self.db_handler.update_data_by_id(host_table, host_data, id)
        self.write({"id": res})

    def get(self, id):
        host_table = get_host_table_model()
        res = self.db_handler.query_data_by_id(host_table, id)
        self.write(res)

    def delete(self, id):
        host_table = get_host_table_model()
        res = self.db_handler.delete_data_by_id(host_table, id)
        self.write("success")


class Hosts_Handler(web.RequestHandler):
    db_handler = get_db_connetion()

    def get(self):
        host_table = get_host_table_model()
        res = self.db_handler.query_data(host_table)
        self.write(json.dumps(res))
