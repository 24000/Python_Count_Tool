import PySimpleGUI as sg
import sys
import re



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
        
        self._timer_status = Status.stop

    # windowを生成・返却
    def create(self):
        
        layout = self.layout.create(self.__next_layer,self.__selected_buttons,self._timer_status)
        return sg.Window("TEST", layout, location=self.__window_pos)
    

    #radio_buttonクリック時
    def set_selected_radio_info(self,selected_layer,selected_task_name):
        self.__previous_selected_layer = self.__selected_layer
        self.__selected_layer = selected_layer
        self.__next_layer = selected_layer + 1
      
        if self.__selected_layer == 0:
            self.__selected_buttons = []
        elif self.__selected_layer == self.__previous_selected_layer:
            self.__selected_buttons = self.__selected_buttons[:self.__previous_selected_layer]
        elif self.__selected_layer < self.__previous_selected_layer:
            self.__selected_buttons = self.__selected_buttons[:self.__selected_layer]
        
        self.__selected_buttons.append(selected_task_name)

    def set_window_position(self,location):
        self.__window_pos = location

    
    # 開始ボタン押下時
    def start_timer(self):
        task_name = self.__get_selected_task_name_string()
        self.__current_timer = TaskTimer(self._timer_id,task_name)
        self._timer_id += 1
        self._timer_status = Status.start
    

    def __get_selected_task_name_string(self):
        task_name = ""
        for name in self.__selected_buttons:
            task_name += (name +"/")
        
        return task_name


    # 終了ボタン押下時
    def stop_timer(self):
        self.__current_timer.set_stop_time()
        self.__completed_timer.append(self.__current_timer)
        self.__current_timer = None
        self._timer_status = Status.stop
        self.__initialize_only_window_display_status()


    def __initialize_only_window_display_status(self):
        self.__previous_selected_layer = 0
        self.__selected_layer = 0
        self.__next_layer = 0     #radiobuttonグループの数
        self.__selected_buttons = []

    def suspend_timer(self):
        self.__current_timer.set_suspend()
        self.__suspend_list.append(self.__current_timer)
        self.__current_timer = None
        self._timer_status = Status.suspend
        self.__initialize_only_window_display_status()
    
    
    def get_suspend_tasks(self):
        suspend_tasks = []
        for suspend_timer in self.__suspend_list:
            task_name = suspend_timer.get_task_name()
            suspend_tasks.append(task_name)
        return suspend_tasks

    def restart_timer(self):
        pass