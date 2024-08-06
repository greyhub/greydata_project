import cx_Oracle
import json
import os
import pandas as pd


def list_db_config(config_file='config.json'):
    """
    List database configuration from a JSON file.

    Args:
        config_file (str): Path to the configuration file (default: 'config.json').

    Returns:
        dict: Database configuration details.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found.")

    with open(config_file, 'r') as f:
        configs = json.load(f).get("databases")

    return configs


def load_db_config(config_name, config_file='config.json'):
    """
    Load database configuration from a JSON file.

    Args:
        config_name (str): Config name of db.
        config_file (str): Path to the configuration file (default: 'config.json').

    Returns:
        dict: Database configuration details.
    """
    configs = list_db_config(config_file)
    
    return configs.get(config_name)


def connect_to_db(db_config):
    """
    Connect to the Oracle database using the specified configuration.

    Args:
        db_config (dict): Database configurations.

    Returns:
        cx_Oracle.Connection: Oracle database connection object.
    """
    try:
        dsn = cx_Oracle.makedsn(
            db_config['host'],
            db_config['port'],
            service_name=db_config['service_name']
        )
        
        connection = cx_Oracle.connect(
            user=db_config['username'],
            password=db_config['password'],
            dsn=dsn,
            encoding=db_config.get('encoding', 'UTF-8')
        )
        return connection
    except cx_Oracle.Error as error:
        print("Error connecting to Oracle database:", error)
        raise


def insert(connection, table_name, data):
    """
    Create a new record in the specified table.

    Args:
        connection (str): DB connection.
        table_name (str): Name of the table to insert the data into.
        data (dict): Data to insert as a new record.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    cursor = connection.cursor()

    try:
        columns = ', '.join(data.keys())
        values = ', '.join([':' + key for key in data.keys()])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        cursor.execute(insert_query, data)
        connection.commit()
        return True
    except cx_Oracle.Error as error:
        print("Error inserting record:", error)
        return False
    finally:
        cursor.close()


def read(connection, table_name, condition=None):
    """
    Read records from the specified table with an optional condition.

    Args:
        connection (str): DB connection.
        table_name (str): Name of the table to read from.
        condition (str, optional): SQL condition to filter records.

    Returns:
        list: List of tuples representing records.
    """
    cursor = connection.cursor()

    try:
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"

        # cursor.execute(query)
        # rows = cursor.fetchall()
        # columns = [column[0] for column in cursor.description]
        df = pd.read_sql(query, con=connection)
        return df
    except cx_Oracle.Error as error:
        print("Error reading records:", error)
        return None
    finally:
        cursor.close()


def update(connection, table_name, data, condition):
    """
    Update an existing record in the specified table.

    Args:
        connection (str): DB connection.
        table_name (str): Name of the table to update.
        data (dict): Data to update in the record.
        condition (str): SQL condition to specify which records to update.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    cursor = connection.cursor()

    try:
        set_clause = ', '.join([f"{key} = :{key}" for key in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

        cursor.execute(update_query, data)
        connection.commit()
        return True
    except cx_Oracle.Error as error:
        print("Error updating record:", error)
        return False
    finally:
        cursor.close()


def delete(connection, table_name, condition):
    """
    Delete records from the specified table based on a condition.

    Args:
        connection (str): DB connection.
        table_name (str): Name of the table to delete records from.
        condition (str): SQL condition to specify which records to delete.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    cursor = connection.cursor()

    try:
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"

        cursor.execute(delete_query)
        connection.commit()
        return True
    except cx_Oracle.Error as error:
        print("Error deleting record:", error)
        return False
    finally:
        cursor.close()
