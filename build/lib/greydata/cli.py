import argparse

def main():
    parser = argparse.ArgumentParser(description='greydata command line interface')
    parser.add_argument('action', help='Action to perform', choices=['analyze', 'report'])
    parser.add_argument('--file', '-f', help='Input file for data analysis', required=True)
    
    args = parser.parse_args()
    
    if args.action == 'analyze':
        analyze(args.file)
    elif args.action == 'report':
        report(args.file)
    
def analyze(file_path):
    # Thực hiện phân tích dữ liệu từ file_path
    print(f'Analyzing data from {file_path}')

def report(file_path):
    # Tạo báo cáo từ file_path
    print(f'Generating report from {file_path}')

if __name__ == '__main__':
    main()
