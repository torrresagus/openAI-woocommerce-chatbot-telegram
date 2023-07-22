import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

def create_connection():
    try:
        # MySQL Database Connection Configuration
        connection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            database=os.environ['MYSQL_DATABASE']
        )
        print("Connection to the MySQL database established.")
        return connection

    except mysql.connector.Error as error:
        print("Error connecting to the MySQL database: {}".format(error))
        return None