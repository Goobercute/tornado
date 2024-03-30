import os
import re

import pandas as pd

from database.db import get_db_connetion
from database.vd_table import (
    get_vd_detail_table_model,
    get_vd_mode_table_model,
    get_vd_version_table,
)
from tornado import web

abs_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(abs_path)

from tools.ssh import SSHConnection


def find_matching_directories(sftp, remote_path, pattern):
    matching_dirs = []

    def _search_directory(path):
        try:
            dir_items = sftp.listdir(path)
            for item in dir_items:
                item_path = os.path.join(path, item)
                if sftp.isdir(item_path):
                    _search_directory(item_path)
                elif sftp.isfile(item_path):
                    if pattern.match(item):
                        matching_dirs.append(
                            {"directory": path, "html_file": item_path}
                        )
                        break  # Assuming only one xxxx.html per directory
        except Exception as e:
            print(f"Error while searching directory {path}: {e}")

    _search_directory(remote_path)
    return matching_dirs


def scan_remote_file(host_ip, username, password, remote_file_path):
    ssh_conn = SSHConnection(host_ip, username=username, password=password)
    sftp = ssh_conn.sftp
    # Call the function to find matching directories
    pattern = re.compile(r"^[^_]+_[^_]+_[^_]+_[^_]+_[^_]+$")
    matching_dirs = find_matching_directories(sftp, remote_file_path, pattern)

    # Print the matching directories
    for dir_path in matching_dirs:
        print(dir_path)

    # Close the SSH connection
    ssh_conn.close()


class Vdbench_Result_Handler(web.RequestHandler):
    async def get(self):
        eds_version = self.get_argument("eds_version")
        mode = self.get_argument("mode")
        thread = self.get_argument("thread")
        io_size = self.get_argument("io_size")
        io_pattern = self.get_argument("io_pattern")
        file_size = self.get_argument("file_size")
        file_num = self.get_argument("file_num")
        # 读取CSV文件
        file_path = (
            abs_path
            + f"/vdbench_result/{eds_version}/{mode}/{thread}/{io_size}_{io_pattern}_{file_size}_{file_num}.csv"
        )
        print(file_path)
        df = pd.read_csv(file_path)
        # 按任务名分组到多个列表中
        task_groups = {}
        for task_name, group_df in df.groupby("Run"):
            task_groups[task_name] = group_df.drop("Run", axis=1).values.tolist()

        # # 打印结果
        # for task_name, task_data in task_groups.items():
        #     print(f"Task: {task_name}")
        #     for row in task_data:
        #         print(row)
        #     print()

        self.write(task_groups)


class Vdbench_Result_Upload_Handler(web.RequestHandler):

    # 从配置文件中获取数据库连接URL
    db_handler = get_db_connetion()

    async def post(self):
        # 后续补充 step1: 获取body参数，ip等配置 step2: 读取远端文件到本地指定目录
        # step3: 读取本地文件到数据库
        # 解析文件名，获取version、date、mode、io_size、file_size、file_num、thread
        file_name = "EDS5.0.2.226_20240329-1541_hit_1m_200m_120G_72"
        version, date, mode, io_size, file_size, file_num, thread = file_name.split("_")
        print(version, date, mode, io_size, file_size, file_num, thread)

        # 插入vd_version数据
        vd_version_table = get_vd_version_table()
        vd_version_data = vd_version_table(
            eds_version=version, date=date, alias=file_name,
        )
        version_id = self.db_handler.insert_data(vd_version_data)
        # 插入vd_mode数据
        vd_mode_table = get_vd_mode_table_model()
        vd_mode_data = vd_mode_table(
            version_id=version_id,
            mode=mode,
            thread=thread,
            io_size=io_size,
            file_size=file_size,
            file_num=file_num,
        )
        mode_id = self.db_handler.insert_data(vd_mode_data)
        # 检查vd_detail表是否存在，不存在则创建
        vd_detail_table = get_vd_detail_table_model(version)
        if not self.db_handler.check_table_exist(vd_detail_table):
            self.db_handler.create_table(vd_detail_table)
        # 读取CSV文件
        df = pd.read_csv(parent_path + f"/vdbench_result/{file_name}.csv")
        df["mode_id"] = mode_id
        df.rename(columns={"MB/sec": "MB_sec"}, inplace=True)
        data = df.to_dict(orient="records")
        # 批量插入数据
        self.db_handler.bulk_insert_data(vd_detail_table, data)


class Vdbench_Result_List_Handler(web.RequestHandler):
    db_handler = get_db_connetion()

    def get(self):
        host_table = get_host_table_model()
        res = self.db_handler.query_data(host_table)
        self.write(json.dumps(res))
