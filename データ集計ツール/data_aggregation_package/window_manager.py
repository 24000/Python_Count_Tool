import PySimpleGUI as sg
import datetime as dt

class WindowManager():
    """
    概要
        Window表示に関する処理を受け持つ
    """

    def create_main(self) -> sg.Window:
        """
        概要
            メインウィンドウ生成
        return : 
            sg.window 
        """
        self.__layout =[
            [sg.T("CSV格納フォルダを指定してください")],
            [sg.InputText(key="selected_folder",disabled=True),
             sg.FolderBrowse(key='folder_select',target="selected_folder")],
            [sg.T("")],
            [sg.T("集計対象とする期間の開始日と終了日を選択してください")],
            [sg.InputText(size=(13,1),key="start_day",disabled=True),
              sg.CalendarButton("開始日選択",locale="ja_JP",target="start_day",format="%Y-%m-%d",month_names=[ f"{x}月" for x in range(1,13) ]),
              sg.InputText(size=(13,1),key="end_day",disabled=True),
              sg.CalendarButton("終了日選択",locale="ja_JP",target="end_day",format="%Y-%m-%d",month_names=[ f"{x}月" for x in range(1,13)])],
            [sg.T("")],
            [sg.Button("集計開始",key="start")]
        ]
        return sg.Window("test",self.__layout)
    


    def popup(self,msg) -> None:
        sg.popup(msg)


    def validata_input_values(self,values : dict) -> str:
        """
        概要
            ユーザー入力値の検証
        params
            values : dict
                GUI上でのユーザー入力値
        return str
            検証結果メッセージ。成功時は””を返却。失敗時にはエラーメッセージを返却。
        """

        msg = ""
        if values["selected_folder"] == "":
            msg += "フォルダを選択して下さい\r\n"

        if values["start_day"] == "":
            msg += "開始日を入力して下さい\r\n"
        else:
            start_day = dt.datetime.strptime(values["start_day"],"%Y-%M-%d")

        if values["end_day"] == "":
            msg += "終了日を入力してください\n\r" 
        else:
            end_day = dt.datetime.strptime(values["end_day"],"%Y-%M-%d")
        
        if msg != "":
            return msg
        
        if start_day != "" and end_day != "":
            if start_day > end_day:
                msg += "終了日は開始日以降の日付を選択してください\n\r"
        
        return msg