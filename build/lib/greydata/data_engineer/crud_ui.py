import streamlit as st
import pandas as pd
from greydata.data_engineer.database import load_db_config, connect_to_db, read, insert, update, delete

def run_crud_ui():
    """
    Run the Streamlit UI for selecting and viewing database tables.
    """
    st.title("Database Table Viewer and Editor")

    # Load database configuration
    config = load_db_config("", "config.json")
    databases = list(config.keys())

    # Sidebar for database and table selection
    st.sidebar.header("Database Selection")
    selected_db = st.sidebar.selectbox("Select a database", databases)

    # Initialize session state variables
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    if 'selected_table' not in st.session_state:
        st.session_state.selected_table = None
    if 'connection' not in st.session_state:
        st.session_state.connection = None
    if 'df' not in st.session_state:
        st.session_state.df = None

    if selected_db:
        tables = config[selected_db]["tables"]
        selected_table = st.sidebar.selectbox("Select a table", tables, key='table_select')

        # Connect button
        if st.sidebar.button("Connect"):
            # Connect to the selected database
            db_config = load_db_config(selected_db, "config.json")
            st.session_state.connection = connect_to_db(db_config)

            # Show connection success message
            st.success(f"Connected to database: {selected_db}")
            st.session_state.connected = True
            st.session_state.selected_table = selected_table

            # Load and display table data
            try:
                st.session_state.df = read(selected_db, selected_table, config_file="config.json")
                # st.dataframe(st.session_state.df)
            except Exception as e:
                st.error(f"Failed to load data: {str(e)}")

        if st.sidebar.button("Refresh"):
            st.rerun()

    # Check if connected to a database
    if st.session_state.connected:
        st.info(f"Currently viewing table: {st.session_state.selected_table}")

        # Display the data
        st.dataframe(st.session_state.df)

        # CRUD Operations
        st.header("CRUD Operations")

        # Insert new record
        st.subheader("Insert Record")
        with st.form("insert_form"):
            new_record = {}
            for column in st.session_state.df.columns:
                new_record[column] = st.text_input(f"Enter {column}", key=f"insert_{column}")
            submitted = st.form_submit_button("Insert")
            if submitted:
                try:
                    insert(selected_db, st.session_state.selected_table, new_record)
                    st.success("Record inserted successfully.")
                    # Refresh data to show changes
                    st.session_state.df = read(selected_db, st.session_state.selected_table, config_file="config.json")
                    st.dataframe(st.session_state.df)
                except Exception as e:
                    st.error(f"Failed to insert record: {str(e)}")

        # Update existing record
        st.subheader("Update Record")
        with st.form("update_form"):
            update_condition = st.text_input("Enter condition to select record(s) for update (e.g., 'id=1')", "", key='update_condition')
            updated_values = {}
            for column in st.session_state.df.columns:
                updated_values[column] = st.text_input(f"Update {column}", key=f"update_{column}")
            update_submitted = st.form_submit_button("Update")
            if update_submitted:
                try:
                    update(selected_db, st.session_state.selected_table, updated_values, update_condition)
                    st.success("Record(s) updated successfully.")
                    # Refresh data to show changes
                    st.session_state.df = read(selected_db, st.session_state.selected_table, config_file="config.json")
                    st.dataframe(st.session_state.df)
                except Exception as e:
                    st.error(f"Failed to update record(s): {str(e)}")

        # Delete record
        st.subheader("Delete Record")
        with st.form("delete_form"):
            delete_condition = st.text_input("Enter condition to select record(s) for deletion (e.g., 'id=1')", "", key='delete_condition')
            delete_submitted = st.form_submit_button("Delete")
            if delete_submitted:
                try:
                    delete(selected_db, st.session_state.selected_table, delete_condition)
                    st.success("Record(s) deleted successfully.")
                    # Refresh data to show changes
                    st.session_state.df = read(selected_db, st.session_state.selected_table, config_file="config.json")
                    st.dataframe(st.session_state.df)
                except Exception as e:
                    st.error(f"Failed to delete record(s): {str(e)}")
    else:
        st.warning("Please select a database and table, then click Connect.")

if __name__ == "__main__":
    run_crud_ui()
