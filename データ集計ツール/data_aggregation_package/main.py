import datetime as dt
import os

from window_manager import WindowManager
from input_manager import InputManager
from pivot_maker import PivotMaker
from output_manager import OutputManager

def main():
    
    window_mgr = WindowManager()

    main_window  = window_mgr.create_main()

    while True:
        key, values = main_window.read()
        
        if key in ("Quit", None):
            break
        elif key == "start":
            msg = window_mgr.validata_input_values(values)
            if msg != "":
                window_mgr.popup(msg)
                continue
            else:
                try:
                    execute_aggregation(values["selected_folder"],values["start_day"],values["end_day"])
                    window_mgr.popup("集計が完了しました。\r\n※本ツールと同一フォルダ内にexcelファイルが出力されています。")
                    break
                except PermissionError as e:
                    window_mgr.popup(e)


def execute_aggregation(folder_path : str, start_day : str, end_day : str) -> None:
    """
    概要
        集計の実行
    params
        folder_path : str
            ユーザーに選択されたCSVファイル格納フォルダパス
        start_day : str
            ユーザーに選択された対象期間の開始日
        end_day : str
        ユーザーに選択された対象期間の終了日
    """

    # CSVファイルを全て読込、一つのファイルにまとめる
    input = InputManager()
    df_all_data = input.csv_union_all(
        folder_path,
        dt.datetime.strptime(start_day,"%Y-%M-%d"),
        dt.datetime.strptime(end_day,"%Y-%M-%d")
        )

    # 項目別、日ごとのクロス集計を作成
    pivots = []
    sheet_names =["日別_全体_件数","日別_全体_平均処理秒数","日別_個人_件数","日別_個人_平均処理秒数"]
    pivot1 = PivotMaker(index="タスク名", columns="日付", values="作業時間合計(秒)")
    pivots.append( pivot1.make(df_all_data, "count") )
    pivots.append( pivot1.make(df_all_data, "mean") )
    
    # タスク、社員別、日ごとのクロス集計を作成
    pivot2 = PivotMaker(index=["社員名","タスク名"], columns="日付", values="作業時間合計(秒)")
    pivots.append( pivot2.make(df_all_data, "count") )
    pivots.append( pivot2.make(df_all_data, "mean") )

    # 出力
    output_folder = os.path.dirname(__file__)
    output_excel_name =  f"{start_day}_{end_day}_集計.xlsx"
    output = OutputManager()
    # 集計結果をエクセル出力
    try:
        output.excel(pivots,sheet_names, output_folder, output_excel_name)
    except PermissionError as e:
        raise PermissionError("出力ファイル名である以下のファイルが既に存在。\r\n\r\n" +
                output_excel_name + "\r\n\r\n" +
                "上書き時にエラー発生。\r\n" +
                "上記ファイルが開かれている可能性あり。\r\n\r\n" +
                "ファイルが開かれていないか確認してやり直して下さい。")
    
    # ローデータを出力するなら
    # output_csv_name =  f"{start_day}_{end_day}_rawdata.csv "
    # output.csv(df_all_data, output_folder,output_csv_name)
    





# unittestのテスト用
def sum(arg1 : int, arg2 : int):
    if type(arg1) is not int or type(arg2) is not int:
        raise ValueError
    
    result = arg1 + arg2
    return result



if __name__ == "__main__":
    main()