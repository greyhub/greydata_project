# greydata/__init__.py

__version__ = "0.1.4"

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Greydata command line interface")

    # Định nghĩa các tham số dòng lệnh với các tên viết tắt
    parser.add_argument('-g', '--group', type=str, default='.', help='Group type, default is "."')
    parser.add_argument('-t', '--task_id', type=str, default='.', help='Task ID, default is "."')
    parser.add_argument('-n', '--note', type=str, help='Additional note, optional')
    parser.add_argument('-p', '--auto_pass', type=int, choices=[0, 1], default=0,
                        help='Flag to auto-pass, default is 0')
    parser.add_argument('-w', '--has_wallet_user', type=int, choices=[0, 1], default=0,
                        help='Flag to indicate if the user has a wallet, default is 0')

    # Có thể thêm các tham số khác nếu cần
    args = parser.parse_args()
    return args

def main():
    # Đọc các tham số từ dòng lệnh
    args = parse_arguments()

    # Hiển thị thông tin tham số đã phân tích
    print(f"Group: {args.group}")
    print(f"Task ID: {args.task_id}")
    print(f"Note: {args.note}")
    print(f"Auto Pass: {args.auto_pass}")
    print(f"Has Wallet User: {args.has_wallet_user}")

    # Thực hiện các tác vụ khác dựa trên tham số
    # Ví dụ: xử lý dựa trên tham số
    handle_parameters(args)

def handle_parameters(args):
    # Hàm xử lý tham số
    if args.auto_pass:
        print("Auto-pass is enabled.")
    else:
        print("Auto-pass is disabled.")

    if args.has_wallet_user:
        print("User has a wallet.")
    else:
        print("User does not have a wallet.")

    # Xử lý dựa trên các tham số khác
    if args.group != '.':
        print(f"Handling group: {args.group}")

    if args.task_id != '.':
        print(f"Handling task ID: {args.task_id}")

    if args.note:
        print(f"Note provided: {args.note}")

if __name__ == '__main__':
    main()
