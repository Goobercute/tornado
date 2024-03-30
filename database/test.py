import os

import pandas as pd

from database.db import get_db_connetion
from database.host_table import get_host_table_model
from database.vd_table import (
    get_vd_detail_table_model,
    get_vd_version_table,
    get_vd_mode_table_model,
)

abs_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(abs_path)

if __name__ == "__main__":
    # 从配置文件中获取数据库连接URL
    db_handler = get_db_connetion()
    # # 创建host表
    host_table = get_host_table_model()
    print(db_handler.check_table_exist(host_table))
    db_handler.create_table(host_table)
    # # 创建vd_version表
    vd_version_table = get_vd_version_table()
    db_handler.create_table(vd_version_table)
    # 创建vd_mode表
    vd_mode_table = get_vd_mode_table_model()
    db_handler.create_table(vd_mode_table)

    # 插入host数据
    host_data = host_table(
        host_ip="10.39.193.64",
        username="root",
        password="eds@1234sangfornetwork",
        port=22,
        group="group1",
        status="healthy",
    )
    res = db_handler.insert_data(host_data)
    print(res)

    # 解析文件名，获取version、date、mode、io_size、file_size、file_num、thread
    file_name = "EDS5.0.2.226_20240329-1541_hit_1m_200m_120G_72"
    version, date, mode, io_size, file_size, file_num, thread = file_name.split("_")
    print(version, date, mode, io_size, file_size, file_num, thread)

    # 插入vd_version数据
    vd_version_data = vd_version_table(eds_version=version, date=date, alias=file_name,)
    version_id = db_handler.insert_data(vd_version_data)
    print(res)

    # 插入vd_mode数据
    vd_mode_data = vd_mode_table(
        version_id=version_id,
        mode=mode,
        thread=thread,
        io_size=io_size,
        file_size=file_size,
        file_num=file_num,
    )
    mode_id = db_handler.insert_data(vd_mode_data)
    print(res)

    # # 创建vd_detail表
    vd_detail_table = get_vd_detail_table_model(version)
    db_handler.create_table(vd_detail_table)

    # 读取CSV文件
    df = pd.read_csv(
        parent_path
        + "/vdbench_result/EDS5.0.2.226_20240329-1541_hit_1m_200m_120G_72.csv"
    )
    df["mode_id"] = mode_id
    df.rename(columns={"MB/sec": "MB_sec"}, inplace=True)
    data = df.to_dict(orient="records")
    # 批量插入数据
    db_handler.bulk_insert_data(vd_detail_table, data)
