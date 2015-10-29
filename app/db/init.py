from mysql import MySQL

from app.config import Config


# Create the database from the config
MySQL.create_database(Config.get('db').get('database'))

MySQL.run('''
    CREATE TABLE IF NOT EXISTS user (
        user_id       INT(8) UNSIGNED PRIMARY KEY,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

MySQL.run('''
    CREATE TABLE IF NOT EXISTS user_device (
        device_id      INT(8) UNSIGNED PRIMARY KEY,
        user_id        INT(8) UNSIGNED,
        platform       TEXT CHARACTER SET utf8,
        system_version TEXT CHARACTER SET utf8,
        app_version    TEXT CHARACTER SET utf8,
        push_token     TEXT CHARACTER SET utf8,
        creation_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen      TIMESTAMP
)''')
