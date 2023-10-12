import PySimpleGUI as sg

from enum_status import Status
from task_timer import TaskTimer
from layout_maker import LayoutMaker

class Window():

    def __init__(self):
        self.layout = LayoutMaker()
        self.__previous_selected_layer = 0
        self.__selected_layer = 0
        self.__next_layer = 0     #radiobuttonグループの数
        self.__selected_buttons = []
        self.__window_pos = (None, None)     #WIndowの表示座標
        
    
        self._timer_id = 1 #インクリメント
        self.__completed_timer = [] # 計測完了データ保管用
        self.__current_timer = None # 計測中タイマー
        self.__suspend_list = [] #一時停止中データ保管用
        
        self._timer_status = Status.stop    #現在のタイマーの状態

    # windowを生成・返却
    def create_main(self):
        
        layout = self.layout.create(self.__next_layer,self.__selected_buttons,self._timer_status,len(self.__suspend_list))
        return sg.Window("TEST", layout, location=self.__window_pos)
    
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

    # window表示位置の保存
    def set_window_position(self,location):
        self.__window_pos = location

    
    # 開始ボタン押下時
    def start_timer(self):
        task_name = self.__get_selected_task_name_string()
        self.__current_timer = TaskTimer(self._timer_id,task_name)
        self._timer_id += 1
        self._timer_status = Status.in_measurement
    

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
            self._timer_status = Status.stop
        else:
            self._timer_status = Status.suspend

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
        self._timer_status = Status.suspend
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

        self._timer_status = Status.in_measurement

    # 現在の計測をキャンセル
    def cancel_timer(self):
        self.__current_timer = None
        if len(self.__suspend_list) == 0:
            self._timer_status = Status.stop
        else:
            self._timer_status = Status.suspend
        self.__initialize_only_window_display_status()