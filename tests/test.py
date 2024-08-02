from greydata import data_engineer as DE

# Tạo bản ghi mới trong db1
data_to_insert = {
    'column1': 'value1',
    'column2': 'value2'
}
DE.create_record('db1', 'table_name', data_to_insert)

# Đọc bản ghi từ db2
records = DE.read_records('db2', 'table_name', "column1 = 'value1'")
print("Records from db2:", records)

# Cập nhật bản ghi trong db1
data_to_update = {
    'column2': 'new_value'
}
DE.update_record('db1', 'table_name', data_to_update, "column1 = 'value1'")

# Xóa bản ghi trong db2
DE.delete_record('db2', 'table_name', "column1 = 'value1'")
