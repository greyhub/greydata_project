import streamlit as st
from .database import *
import time
import warnings

warnings.filterwarnings('ignore')


def create_crud_ui():
    if "login" not in st.session_state:
        st.session_state.login = False
    
    if "connection_config" not in st.session_state:
        st.session_state.connection_config = None
    
    if "table_name" not in st.session_state:
        st.session_state.table_name = None

    if not st.session_state.login:
        login_db()
    else:
        # if st.button('QUERY'):
        #     connection = connect_to_db(st.session_state.connection_config)
        #     query = f"SELECT * FROM {st.session_state.table_name}"
        #     df = pd.read_sql(query, con=connection)
        #     st.dataframe(df)
        run_crud_ui(st.session_state.connection_config, st.session_state.table_name)


def login_db(config_file="config.json"):
    
    st.title("Login to Oracle Database")

    # Load database configurations
    db_configs = list_db_config(config_file)
    
    # Select database configuration
    db_name = st.selectbox("Select Database", list(db_configs.keys()))

    # Display available tables for the selected database
    tables = db_configs[db_name].get("tables", [])

    if not tables:
        st.error(f"No tables available for database {db_name}")
        return

    # Select table
    st.header("Table Selection")
    table_name = st.selectbox("Select Table", tables)

    config = db_configs[db_name]

    # Database login form
    st.subheader("Database Login")
    host = st.text_input("Host", config['host'])
    port = st.text_input("Port", config['port'])
    service_name = st.text_input("Service Name", config['service_name'])
    username = st.text_input("Username", config['username'])
    password = st.text_input("Password", config['password'], type="password")
    # conn = None

    if st.button("Connect"):
        try:
            # Load the database configuration
            config = {
                "host": host,
                "port": port,
                "service_name": service_name,
                "username": username,
                "password": password
            }

            # Attempt to connect to the selected database
            st.session_state.login = True
            st.session_state.connection_config = config
            st.session_state.table_name = table_name

            with st.spinner('Wait for it...'):
                time.sleep(1)
            
            st.rerun(scope="app")
        except Exception as e:
            st.error(f"Failed to connect to {db_name}: {str(e)}")
            # return

    # If connected, show CRUD operations
    # return conn, table_name

def run_crud_ui(connection_config, table_name):
    """Run the Streamlit CRUD application."""
    st.title("Oracle Database CRUD Application")

    st.write(f"Welcome {st.session_state.connection_config['username']}")
    st.write(f"Table name: {st.session_state.table_name}")

    connection = connect_to_db(connection_config)

    # Sidebar to choose the action
    action = st.sidebar.selectbox("Choose Action", ["Read", "Create", "Update", "Delete"])

    if action == "Create":
        st.subheader("Add New Record")
        columns, values = [], []

        # Get column names from the database to display input fields
        st.write(connection)
        st.write(table_name)

        df = read(connection, table_name)
        column_names = df.columns
        with st.form("create_form"):
            for col in column_names:
                value = st.text_input(f"Enter {col}", "")
                columns.append(col)
                values.append(value)
            submitted = st.form_submit_button("Add")

            if submitted:
                data = dict(zip(columns, values))
                insert(connection, table_name, data)
                st.success("Record added successfully!")

    elif action == "Read":
        st.subheader("Read Records")
        df = read(connection, table_name)
        st.dataframe(df)

    elif action == "Update":
        st.subheader("Update Record")
        condition = st.text_input("Enter condition to update the record", "")
        if condition:
            df = read(connection, table_name)
            column_names = df.columns
            with st.form("update_form"):
                updated_data = {col: st.text_input(f"Update {col}", "") for col in column_names}
                submitted = st.form_submit_button("Update")

                if submitted:
                    update(connection, table_name, updated_data, condition)
                    st.success("Record updated successfully!")

    elif action == "Delete":
        st.subheader("Delete Record")
        condition = st.text_input("Enter condition to delete the record", "")
        if condition:
            if st.button("Delete"):
                delete(connection, table_name, condition)
                st.success("Record deleted successfully!")

    # Close the connection
    connection.close()
