import pymysql
import numpy as np
import json
import sys
from sshtunnel import SSHTunnelForwarder
from os import path

config = None

def load_config(config_file = "config.json"):
    """Load the configuration from config.json, exit if fail"""

    global config

    data = {
    "ip": "120.27.144.199",
    "username": "root",
    "ssh-password": "ERG3010!",
    "db-password": "ERG3010",
    "db":"group1",
    "suffix": "117010343"
    }

    json_str = json.dumps(data)
    config = json.loads(json_str)
    print("config:", config)

    for key in config:
        # Check if every configuration is set
        if config[key]=="":
            print("Please complete the config.json first!")
            sys.exit(1)
    else:
        config["default-suffix"] = config["suffix"]
        config["default-table"] = "try_crawl_" + config["suffix"]

        print("Configuration Check success")


def insert_data(v):
    """Save a vector and insert a record in the database."""
    
    try:
        assert(type(v) is np.ndarray)
    except:
        print("The input v should be a numpy array!")
        return None
    
    conn, tunnel = create_db_conn()
    cur = conn.cursor()

    last_id = None
        
    try:
        cur.execute("USE %s;"%(config['db']))
        cur.execute("INSERT INTO %s () VALUES ();"%(config["default-table"]))
        cur.execute("SELECT LAST_INSERT_ID();")

        conn.commit()
        last_id = cur.fetchone()[0]
        print("last_id:", last_id)

        np.save(path.join(config["data-dir"], str(last_id)), v)

    except Exception as e:
        print("insert_data failed")
        print(e)

    conn.close()
    tunnel.close()
    return last_id



def create_ssh_tunnel():
    """Create an SSH tunnel to access the database"""
    
    # Reference link: https://sshtunnel.readthedocs.io/en/latest/
    tunnel = SSHTunnelForwarder(
        (config['ip'], 22),
        ssh_username=config['username'],
        ssh_password=config["ssh-password"],
        remote_bind_address=('localhost', 3306),
    )

    tunnel.start() 
    print("SSH Connected") 
    return tunnel

def create_db_conn():
    """Create and return a SSH Tunnel for MySQL connection. Require manual close after usage."""
    
    tunnel = create_ssh_tunnel()
    conn = pymysql.Connect(host='127.0.0.1',
                            port=tunnel.local_bind_port,
                            user=config['username'],
                            passwd=config['db-password'])
    return conn, tunnel

def check_table(table_name = None):
    """Check if the table exist."""

    if table_name is None:
        table_name = config["default-table"]

    conn, tunnel = create_db_conn()
    
    result = None

    try:
        cur = conn.cursor()
        cur.execute("""
            USE %s
            """%(config['db'], ))

        cur.execute("""
            SHOW TABLES;
            """)
        
        all_tables = cur.fetchall()
        if (table_name,) in all_tables:
            result = True
        else:
            result = False
    except Exception as e:
        print("check_table FAILED")
        print(e)

    conn.close()
    tunnel.close()
    return result

def setup_user_table(table_name = None, reconstruct = False):
    """Create the user table for this project."""
    
    if table_name is None:
        table_name = config["default-table"]

    conn, tunnel = create_db_conn()   
    try:
        cur = conn.cursor()
        cur.execute("""
            USE %s
            """%(config['db'], ))
 
        if reconstruct:
            cur.execute("""
                DROP TABLE IF EXISTS `%s`;
                """%(table_name,))
            cur.execute("""CREATE TABLE `%s` (
                    id varchar(20) NOT NULL,
                    screen_name varchar(30),
                    gender varchar(10),
                    statuses_count INT,
                    followers_count INT,
                    follow_count INT,
                    PRIMARY KEY (id)
                )
                ;"""%(table_name,))
            conn.commit()

        cur.execute("""
            SHOW TABLES;
            """)
        conn.commit()
        
        all_tables = cur.fetchall()
        assert((table_name,) in all_tables)
        print("setup_table PASSED")
        print("table ‘user’ 创建完毕")
    except Exception as e:
        print("setup_table FAILED")
        print(e)

    conn.close()
    tunnel.close()
    
 
def setup_weibo_table(table_name = None, reconstruct = False):
    """Create the weibo table for this project."""
    
    if table_name is None:
        table_name = config["default-table"]

    conn, tunnel = create_db_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            USE %s
            """%(config['db'], ))

        if reconstruct:
            cur.execute("""
                DROP TABLE IF EXISTS `%s`;
                """%(table_name,))
            cur.execute("""CREATE TABLE `%s` (
                    user_id varchar(20) NOT NULL,
                    id varchar(20) NOT NULL,
                    text varchar(2000),
                    created_at DATETIME,
                    attitudes_count INT,
                    comments_count INT,
                    reposts_count INT,
                    topics varchar(200),
                    PRIMARY KEY (id)
                )
                ;"""%(table_name,))
            conn.commit()

        cur.execute("""
            SHOW TABLES;
            """)
        conn.commit()
        
        all_tables = cur.fetchall()
        assert((table_name,) in all_tables)
        print("setup_table PASSED")
        print("table ‘weibo’ 创建完毕")
    except Exception as e:
        print("setup_table FAILED")
        print(e)

    conn.close()
    tunnel.close()

        