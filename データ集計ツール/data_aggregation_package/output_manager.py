import os

import pandas as pd
import openpyexcel as xl


class OutputManager():
    def __init__(self):
        pass

    def csv(self, data : pd.DataFrame, folder_path : str, file_name :str) -> None:
        file_path = os.path.join(folder_path, file_name)
        data.to_csv(file_path, index=False,encoding="shift-jis")


    def excel(self, pivots : list, sheet_names : list, folder_path : str, file_name :str) -> None:
        # エクセルブックを作成し、必要数のシートを挿入する
        wb = xl.Workbook()
        for i,sheet_name in enumerate(sheet_names):
            wb.create_sheet(sheet_name)

        # sheet1を削除
        wb.remove(wb.worksheets[0])
        # save,close
        file_path = os.path.join(folder_path,  file_name)
        try:
            wb.save(file_path)
            wb.close
        except PermissionError as e:
            wb.close()
            raise e

        # 書き込み
        with pd.ExcelWriter(file_path,engine="openpyxl",mode="a",if_sheet_exists="replace") as writer:
            for pivot, sheet_name in zip(pivots, sheet_names):
                pivot.to_excel(writer, sheet_name=sheet_name, na_rep="0")
                # , float_format="%.1f"
        
        # フォーマットの調整(書き込み前に設定すると無効化されるため、書き込み後処理)
        wb = xl.load_workbook(file_path)
        for i,sheet_name in enumerate(sheet_names):
            ws = wb.worksheets[i]
            if i in (0,1):
                ws.column_dimensions["A"].width = 40
            else:
                ws.column_dimensions["A"].width = 16
                ws.column_dimensions["B"].width = 40
        
        wb.save(file_path)
        wb.close
       
