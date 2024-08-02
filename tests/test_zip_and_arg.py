from greydata import data_engineer as DE

# Ví dụ về sử dụng hàm setup_arguments
args = DE.setup_arguments()
print("Parsed Arguments:", args)

# Ví dụ về sử dụng hàm zip_folder
DE.zip_folder('../greydata', '../../greydata.zip')
