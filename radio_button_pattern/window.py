import os
import PySimpleGUI as sg

from enums import Status
from enums import ExitSituation
from task_timer import TaskTimer
from layout_maker import LayoutMaker
from file_writer import FileWriter

class Window():

    def __init__(self,config_file,employee_num,employee_name):
        self.__config_file = config_file
        self.__employee_num = employee_num
        self.__employee_name = employee_name

        self.__file_name = f"{TaskTimer.Get_Today()}_{self.__employee_num}_{self.__employee_name}.csv"
        self.__file_path = os.path.join(self.__config_file.output_folder_path,self.__file_name)
        if os.path.isfile(self.__file_path):
            file_close,msg = self.__is_file_close()
            if not file_close:
                sg.popup(msg)
                raise Exception
        
        self.layout = LayoutMaker()
        self.__previous_selected_layer = 0
        self.__selected_layer = 0
        self.__next_layer = 0     #radiobuttonグループの数
        self.__selected_buttons = []
        self.__window_pos = (None, None)     #WIndowの表示座標
        
    
        self.__timer_id = 1 #インクリメント
        self.__completed_timer = [] # 計測完了データ保管用
        self.__current_timer = None # 計測中タイマー
        self.__suspend_list = [] #一時停止中データ保管用
        
        self.__timer_status = Status.stop    #現在のタイマーの状態
    

    def __is_file_close(self):
        try:
            f = open(self.__file_path, 'a')
            f.close()
            return True,""
        except Exception as e:
            msg = self.__file_name + "が開かれています。\r\n" +  \
                        "ファイルが開かれているとデータが保存できません。\r\n"  +  \
                        "閉じてからやり直して下さい。"
            return False, msg


    # windowを生成・返却
    def create_main(self):
        layout = self.layout.create(self.__next_layer,self.__selected_buttons,self.__timer_status,len(self.__suspend_list))
        title = self.__employee_num + "：" + self.__employee_name
        if self.__window_pos == (None,None):
            return sg.Window(title, layout,use_default_focus=True)
        else:
            return sg.Window(title, layout, location=self.__window_pos,use_default_focus=True)
    

    def close(self,boot_window):
        self.__window_pos = boot_window.current_location()
        boot_window.close()
    

    #radio_buttonクリック時
    def set_selected_radio_info(self,selected_layer,selected_task_name):
        self.__previous_selected_layer = self.__selected_layer
        self.__selected_layer = selected_layer
        self.__next_layer = selected_layer + 1

        # 押されたボタンのレイヤーによって、選択されたボタンリストの中身を調整
        if self.__selected_layer == 0:
            self.__selected_buttons = []
        elif self.__selected_layer == self.__previous_selected_layer:
            self.__selected_buttons = self.__selected_buttons[:self.__previous_selected_layer]
        elif self.__selected_layer < self.__previous_selected_layer:
            self.__selected_buttons = self.__selected_buttons[:self.__selected_layer]
        
        self.__selected_buttons.append(selected_task_name)

    
    # 開始ボタン押下時
    def start_timer(self):
        task_name = self.__get_selected_task_name_string()
        self.__current_timer = TaskTimer(self.__timer_id,task_name)
        self.__timer_id += 1
        self.__timer_status = Status.in_measurement
    

    # 開始ボタン押下時に選択されているボタンのタスク名を//つなぎで文字列化
    def __get_selected_task_name_string(self):
        task_name = ""
        for name in self.__selected_buttons:
            task_name += (name +"//")
        task_name = task_name[:-2] #末尾の//を削除
        return task_name


    # 終了ボタン押下時
    def stop_timer(self):
        self.__current_timer.set_stop_time()
        self.__completed_timer.append(self.__current_timer)
        self.__current_timer = None

        # 一時停止中のタイマーがあれば、再開ボタンあり。なければ再開ボタンなし。
        if len(self.__suspend_list) == 0:
            self.__timer_status = Status.stop
        else:
            self.__timer_status = Status.suspend

        self.__initialize_only_window_display_status()


    # window表示に関する設定を初期化
    def __initialize_only_window_display_status(self):
        self.__previous_selected_layer = 0
        self.__selected_layer = 0
        self.__next_layer = 0     #radiobuttonグループの数
        self.__selected_buttons = []


    # 一時停止ボタン押下字
    def suspend_timer(self):
        self.__current_timer.set_suspend_start_data()
        self.__suspend_list.append(self.__current_timer)
        self.__current_timer = None
        self.__timer_status = Status.suspend
        self.__initialize_only_window_display_status()
    

    # 再開するタスクをユーザーに選択させるポップアップウィンドウを生成
    def create_restart_popup(self):
        layout =[]
        layout.append([sg.Text("以下から再開するタスクを選択してください。")])

        for i,suspend_timer in enumerate(self.__suspend_list):
            task_name = suspend_timer.get_task_name()
            layout.append([sg.Radio(task_name,key= str(i) + "_" + "radio_" ,group_id=1,enable_events=True)])
        
        layout.append([sg.Button("やはり再開しない")])

        return sg.Window('確認', layout,modal=True)
    

    # 一時停止完了時間を登録し、計測タイマーとして再設定
    def restart_timer(self,selected_index):
        restart_target_timer = self.__suspend_list.pop(selected_index)
        restart_target_timer.set_suspend_end_data()
        self.__current_timer = restart_target_timer

        # 画面表示を再開タスク選択状態にするための操作
        task_names = restart_target_timer.get_task_name().split("//") 
        self.__previous_selected_layer = len(task_names) -2
        self.__selected_layer = len(task_names) -1
        self.__next_layer = len(task_names) 
        self.__selected_buttons = task_names.copy()

        self.__timer_status = Status.in_measurement

    # 現在の計測をキャンセル
    def cancel_timer(self):
        self.__current_timer = None
        if len(self.__suspend_list) == 0:
            self.__timer_status = Status.stop
        else:
            self.__timer_status = Status.suspend
        self.__initialize_only_window_display_status()


    # 未完了のタイマーを全て完了させる
    def stop_all_incomplete_timer(self):
        if self.__current_timer != None:
            self.stop_timer()
        
        if len(self.__suspend_list) != 0:
            for suspend_timer in self.__suspend_list:
                suspend_timer.set_suspend_end_data()
                self.__current_timer = suspend_timer
                self.stop_timer()


    def check_exit_situation(self):
        # 状況とユーザーの意思を確認
        situation = self.__check_situation()
        # ファイル書き込み不要パターンはそのままreturn
        if situation in (ExitSituation.no_data,ExitSituation.exit_cancel):
            return situation

        # ファイル書き込み必要パターンの場合、ファイルが開かれているとセーブできないため、
        # ファイルが閉じらえているかチェック
        file_close,msg = self.__is_file_close()
        # 閉じられていればそのままreturn、閉じられていなければ強制キャンセル
        if file_close:
            return situation
        else:
            sg.popup(msg)
            return ExitSituation.exit_cancel


    def __check_situation(self):
        if self.__is_all_timer_completed():
            if len(self.__completed_timer)== 0:
                answer = sg.PopupYesNo("計測されたデータはまだ何もありません。\r\nこのまま終了しますか？")
                if answer == "Yes":
                    return ExitSituation.no_data
                else:
                    return ExitSituation.exit_cancel
            else:
                answer = sg.PopupYesNo("計測した全てのデータをファイルに保存し、終了しますか？")
                if answer =="Yes":
                    return  ExitSituation.exists_complete_data_only
                else:
                    return  ExitSituation.exit_cancel
        else:
            exit_msg = self.__get_exists_incomplete_timer_message()
            answer = sg.PopupYesNo(exit_msg)
            if answer == "Yes":
                return  ExitSituation.exists_incomplete_data
            else:
                return  ExitSituation.exit_cancel


    def __is_all_timer_completed(self):
        if self.__current_timer == None and  len(self.__suspend_list) == 0:
            return True
        else:
            return False
        


    def __get_exists_incomplete_timer_message(self):
        msg = ""
        if self.__current_timer != None:
            msg += "・現在計測中のタスクが未完了\r\n"
        
        suspend_list_num =  len(self.__suspend_list)
        if suspend_list_num != 0:
            msg += "・一時停止中タスクが" + str(suspend_list_num) + "件あり\r\n"

        msg += "\r\n"
        msg += "上記については全て現在時刻を終了時間として登録し、\r\n" \
                     "処理を終了しますがよろしいですか？\r\n\r\n"
        
        return msg
        

    def write_data(self):
        witer = FileWriter()
        witer.write_csv_file(self.__file_path,self.__employee_num,self.__employee_name,self.__completed_timer)
    

    def is_finish_select(self):
        return self.layout.is_finish_select()
