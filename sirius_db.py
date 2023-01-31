import pymysql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()
HOST = os.environ.get("mysql_host")
USER = os.environ.get("mysql_user")
PASSWORD = os.environ.get("mysql_pass")
DATABASE = os.environ.get("mysql_db")

# Connect to MYSQL Server
connection = pymysql.connect( 
    HOST, 
    USER, 
    PASSWORD, 
    DATABASE
    )
cursor = connection.cursor()

DB_DATA = 'mysql+pymysql://' + USER + ':' + PASSWORD + '@' + 'localhost' + ':3306/' + DATABASE + '?charset=utf8mb4'
engine = create_engine(DB_DATA)
engine.connect()