import MySQLdb

from app.config import Config


class MySQL:

    _conn = None

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        if not MySQL._conn:
            db_config = Config.get('db')
            MySQL._conn = MySQLdb.connect(user=db_config.get('user'), passwd=db_config.get('password'),
                                          host=db_config.get('host'), db=db_config.get('database'))
        return MySQL._conn

    @staticmethod
    def run(query):
        conn = MySQL.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        conn.commit()
        return res

    @staticmethod
    def create_database(database):
        db_config = Config.get('db')
        conn = MySQLdb.connect(user=db_config.get('user'), passwd=db_config.get('password'), host=db_config.get('host'))
        cursor = conn.cursor()
        # MySQL generates a warning if we try to create a database that already exists even
        # if we specify "IF NOT EXISTS" in the query.
        import warnings
        warnings.filterwarnings(action="ignore", category=MySQLdb.Warning,
                                message="Can't create database '{}'; database exists".format(database))
        cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(database))
