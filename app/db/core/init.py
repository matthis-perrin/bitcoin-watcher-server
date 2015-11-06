from mysql import MySQL

from app.config import Config


# Create the database from the config
MySQL.create_database(Config.get('db').get('database'))

MySQL.run('''
    CREATE TABLE IF NOT EXISTS user (
        user_id       INT(8) UNSIGNED,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    )
''')

MySQL.run('''
    CREATE TABLE IF NOT EXISTS user_device (
        device_id      INT(8) UNSIGNED,
        user_id        INT(8) UNSIGNED,
        platform       VARCHAR(255) CHARACTER SET utf8,
        system_version VARCHAR(255) CHARACTER SET utf8,
        app_version    VARCHAR(255) CHARACTER SET utf8,
        push_token     VARCHAR(255) CHARACTER SET utf8,
        creation_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_seen      TIMESTAMP,
        PRIMARY KEY (device_id)
    )
''')

MySQL.run('''
    CREATE TABLE IF NOT EXISTS user_address (
        user_id       INT(8) UNSIGNED,
        address       VARCHAR(255) CHARACTER SET utf8,
        address_type  VARCHAR(255) CHARACTER SET utf8,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, address)
    )
''')

MySQL.run('''
    CREATE TABLE IF NOT EXISTS address_lookup (
        user_id       INT(8) UNSIGNED,
        address       VARCHAR(255) CHARACTER SET utf8,
        xpub          VARCHAR(255) CHARACTER SET utf8,
        offset        INT(8) UNSIGNED,
        creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, address)
    )
''')
