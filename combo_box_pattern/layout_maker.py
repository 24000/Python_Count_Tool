import PySimpleGUI as sg
import json

from enums import Status


class LayoutMaker():
    def __init__(self):
        with open(r'./業務名一覧.json',encoding="utf-8") as f:
            self.__json = json.load(f)
            self.__combo_values =[] # combo_boxのauto complete実現のためだけ
            self.__is_finish_select = False # combo_boxのauto complete実現のためだけ


    def create(self,next_layer,selected_buttons,timer_status,suspend_num):
        task_name_json = self.__json.copy()
        
        layout=[]
        combo_box_hierarchy,task_name_json = self.__get_combo_box_hierarchy(next_layer,task_name_json,selected_buttons,timer_status)
        
        # 業務名の階層が続かない（jsonの値が""）の場合はtimer関連ボタンを追加してbreak
        if  task_name_json == "":
            self.__is_finish_select = True
            if suspend_num != 0:
                if timer_status == Status.in_measurement:
                    layout.append(combo_box_hierarchy)
                else:
                    layout.append(self.__get_row_of_restart_button_and(combo_box_hierarchy))
            else:
                layout.append(combo_box_hierarchy)

            timer_buttons = self.__get_timer_buttons(timer_status)
            layout.append(timer_buttons)
            
            return layout
        else:
            self.__is_finish_select = False
            if suspend_num == 0:
                layout.append(combo_box_hierarchy)
                layout.append([sg.Text("※作業を選択してください",font=("",10,""))])
            elif suspend_num != 0:
                if timer_status == Status.in_measurement:
                    layout.append(combo_box_hierarchy)
                    layout.append([sg.Text("※作業を選択してください\r\n",font=("",10,""))])
                else:
                    layout.append(self.__get_row_of_restart_button_and(combo_box_hierarchy))
                    layout.append([sg.Text("※作業を選択してください\r\n",font=("",10,""))])
        
        return layout
    
    
    def __get_combo_box_hierarchy(self,next_layer,task_name_json,selected_buttons,timer_status):
        self.__combo_values = []

        # combo box生成
        combo_box_hierarchy = []
        for target_layer in range(next_layer+1):
            task_name_json = self.__get_target_layer_task_name_json(target_layer,task_name_json,selected_buttons)

            if task_name_json == "":
                break            
            combo_box = self.__get_target_layer_combo_box(target_layer,task_name_json,selected_buttons,timer_status)
            combo_box_hierarchy.append(combo_box)
        
        return combo_box_hierarchy,task_name_json
    

    def __get_target_layer_task_name_json(self,target_layer,task_name_json,selected_buttons):
        # target_layerの業務名をjsonから取得するため、task_name_jsonを調整
            if target_layer == 0:
                #jsonの1階層目のプロパティ名をそのまま使用するので何もしない
                return task_name_json
            elif target_layer != 0:
                selected_button_name = selected_buttons[target_layer-1]
                return task_name_json[selected_button_name]
    

    def __get_target_layer_combo_box(self,target_layer,task_name_json,selected_buttons,timer_status):
        
        # combo_boxにつけるkeynameを生成
        key_name = str(target_layer) + "combo_box"

        # 業務名が各レイヤーで選択された業務名と一致したらdefaultの値として取得
        default = ""
        for key in  task_name_json.keys():
            if key in selected_buttons:
                default = key
        
        #コンボボックスの選択肢を取得
        combo_values =[ task_name for task_name in task_name_json.keys()]
        self.__combo_values.append(combo_values)

        # 計測開始後は変更不可としたい
        if timer_status == Status.in_measurement:
            combo_box = [sg.Combo(combo_values,default,size=(30,1),enable_events=False,key=key_name,readonly=True,disabled=True)]
        else:
            combo_box = [sg.Combo(combo_values,default,size=(30,1),enable_events=True,key=key_name)]

        return combo_box
    

    def __get_row_of_restart_button_and(self,radio_button_hierarchy):
         col1 = sg.Column(radio_button_hierarchy)
         col2 = sg.Column([[sg.Button("再開")]])
         return [col1,col2]


    def __get_timer_buttons(self,timer_status):
        if timer_status == Status.in_measurement:
            start_button = sg.Button("開始",disabled=True)
            stop_button = sg.Button("終了")
            suspend_button = sg.Button("一時停止")
            cancel_button = sg.Button("キャンセル")
        elif timer_status == Status.stop:
            start_button = sg.Button("開始")
            stop_button = sg.Button("終了",disabled=True)
            suspend_button = sg.Button("一時停止",disabled=True)
            cancel_button = sg.Button("キャンセル",disabled=True)
        elif timer_status == Status.suspend:
            start_button = sg.Button("開始")
            stop_button = sg.Button("終了",disabled=True)
            suspend_button = sg.Button("一時停止",disabled=True)
            cancel_button = sg.Button("キャンセル",disabled=True)
   
        return  [start_button,stop_button,suspend_button,cancel_button]
    


    def get_combo_values(self,layer):
        return self.__combo_values[layer]
    
    def is_finish_select(self):
        return self.__is_finish_select