import unittest
import sys
sys.path.append(r"C:\Users\user\Desktop\プログラム各種\python\test\Count_Tool\データ集計ツール\data_aggregation_package")
import main
from window_manager import WindowManager
from csv_aggl 

class TestExecutor(unittest.TestCase):
    # テスト実施前に共通で実施したい処理
    def setUp(self):
        self.window = WindowManager()
    
    # テスト実施後に共通で実施したい処理
    def tearDown(self):
        del self.window

    def test_sum(self):
        arg1 = 1
        arg2 = 2
        expected = 3

        # 関数結果確認　実行結果,期待値
        self.assertEqual(main.sum(arg1,arg2),expected)

        # exception発生確認
        with self.assertRaises(ValueError):
            main.sum("1","1")
    
    def test_window_manager(self):
        self.window.popup()


if __name__ == "__main__":
    # 呼出しはこれ
    unittest.main()