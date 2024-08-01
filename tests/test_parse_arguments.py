# tests/test_parse_arguments.py

import unittest
import sys
from greydata import parse_arguments

class TestParseArguments(unittest.TestCase):

    def setUp(self):
        """Cài đặt môi trường kiểm tra."""
        # Lưu lại tham số dòng lệnh hiện tại
        self.original_args = sys.argv

    def tearDown(self):
        """Khôi phục môi trường kiểm tra."""
        # Khôi phục tham số dòng lệnh gốc
        sys.argv = self.original_args

    def test_default_values(self):
        """Kiểm tra các giá trị mặc định khi không có tham số dòng lệnh."""
        sys.argv = ['greydata']
        args = parse_arguments()
        self.assertEqual(args.group, '.')
        self.assertEqual(args.task_id, '.')
        self.assertIsNone(args.note)
        self.assertEqual(args.auto_pass, 0)
        self.assertEqual(args.has_wallet_user, 0)

    def test_custom_values(self):
        """Kiểm tra các giá trị tùy chỉnh khi có tham số dòng lệnh."""
        sys.argv = ['greydata', '--group', 'DAILY', '--task_id', 'TASK123', '--note', 'Test note', '--auto_pass', '1', '--has_wallet_user', '1']
        args = parse_arguments()
        self.assertEqual(args.group, 'DAILY')
        self.assertEqual(args.task_id, 'TASK123')
        self.assertEqual(args.note, 'Test note')
        self.assertEqual(args.auto_pass, 1)
        self.assertEqual(args.has_wallet_user, 1)

    def test_short_options(self):
        """Kiểm tra các tùy chọn viết tắt."""
        sys.argv = ['greydata', '-g', 'DAILY', '-t', 'TASK123', '-n', 'Test note', '-p', '1', '-w', '1']
        args = parse_arguments()
        self.assertEqual(args.group, 'DAILY')
        self.assertEqual(args.task_id, 'TASK123')
        self.assertEqual(args.note, 'Test note')
        self.assertEqual(args.auto_pass, 1)
        self.assertEqual(args.has_wallet_user, 1)

if __name__ == '__main__':
    unittest.main()
