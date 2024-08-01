# test.py

from greydata import parse_arguments

def main():
    args = parse_arguments()

    # Hiển thị các tham số để kiểm tra
    print(f"Group: {args.group}")
    print(f"Task ID: {args.task_id}")
    print(f"Note: {args.note}")
    print(f"Auto Pass: {args.auto_pass}")
    print(f"Has Wallet User: {args.has_wallet_user}")

if __name__ == '__main__':
    main()
