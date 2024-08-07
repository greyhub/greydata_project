import cx_Oracle
import json
import pandas as pd


def load_db_config(config_name, config_file='config.json'):
    """
    Load the database configuration from a JSON file.

    Args:
        config_name (str): Name of the database configuration.
        config_file (str): Path to the configuration JSON file.

    Returns:
        dict: The database configuration.
    """
    with open(config_file, 'r') as file:
        config = json.load(file)

    if config_name == "":
        return config['databases']

    return config['databases'].get(config_name)

def connect_to_db(config):
    """
    Connect to the Oracle database using the configuration provided.

    Args:
        config (dict): Database configuration dictionary.

    Returns:
        cx_Oracle.Connection: Oracle database connection.
    """
    dsn = cx_Oracle.makedsn(
        config['host'],
        config['port'],
        service_name=config['service_name']
    )
    connection = cx_Oracle.connect(
        config['username'],
        config['password'],
        dsn
    )
    return connection

def insert(db_name, table_name, data, config_file='config.json'):
    """
    Insert a record into the specified table.

    Args:
        db_name (str): Database name as per configuration.
        table_name (str): Table name where data will be inserted.
        data (dict): Data to insert, as a dictionary of column-value pairs.
        config_file (str): Path to the configuration JSON file.
    """
    db_config = load_db_config(db_name, config_file)
    connection = connect_to_db(db_config)
    cursor = connection.cursor()
    
    # Cấu trúc lại tên biến bind theo chuẩn của Oracle
    valid_data = {f'param_{k}': v for k, v in data.items() if len(k) <= 30 and k.isidentifier()}
    
    columns = ', '.join(f'"{col}"' for col in data.keys())
    values = ', '.join(f':{col}' for col in valid_data.keys())
    sql = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values})'

    try:
        cursor.execute(sql, valid_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

def read(db_name, table_name, condition=None, config_file='config.json'):
    """
    Read records from the specified table.

    Args:
        db_name (str): Database name as per configuration.
        table_name (str): Table name from which data will be read.
        condition (str, optional): SQL condition for filtering records.
        config_file (str): Path to the configuration JSON file.

    Returns:
        pd.DataFrame: DataFrame containing the fetched records.
    """
    config = load_db_config(db_name, config_file)
    connection = connect_to_db(config)
    cursor = connection.cursor()

    sql = f'SELECT * FROM {table_name}'
    if condition:
        sql += f' WHERE {condition}'

    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return pd.DataFrame(rows, columns=columns)

def update(db_name, table_name, data, condition, config_file='config.json'):
    """
    Update records in the specified table.

    Args:
        db_name (str): Database name as per configuration.
        table_name (str): Table name where records will be updated.
        data (dict): Data to update, as a dictionary of column-value pairs.
        condition (str): SQL condition to specify which records to update.
        config_file (str): Path to the configuration JSON file.
    """
    config = load_db_config(db_name, config_file)
    connection = connect_to_db(config)
    cursor = connection.cursor()

    # Ensure column names are valid
    valid_data = {f'param_{k}': v for k, v in data.items() if len(k) <= 30 and k.isidentifier()}
    
    # Properly quote column names to handle special characters or reserved words
    set_clause = ', '.join(f'"{col}" = :param_{col}' for col in data.keys())
    
    # Build SQL query with quoted table name and columns
    sql = f'UPDATE "{table_name}" SET {set_clause} WHERE {condition}'
    
    try:
        cursor.execute(sql, valid_data)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


def delete(db_name, table_name, condition, config_file='config.json'):
    """
    Delete records from the specified table.

    Args:
        db_name (str): Database name as per configuration.
        table_name (str): Table name from which records will be deleted.
        condition (str): SQL condition to specify which records to delete.
        config_file (str): Path to the configuration JSON file.
    """
    config = load_db_config(db_name, config_file)
    connection = connect_to_db(config)
    cursor = connection.cursor()

    sql = f'DELETE FROM {table_name} WHERE {condition}'
    cursor.execute(sql)
    
    connection.commit()
    cursor.close()
    connection.close()
