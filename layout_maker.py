import PySimpleGUI as sg
import json

from enums import Status


class LayoutMaker():
    def __init__(self):
        with open(r'./JSON\test.json',encoding="utf-8") as f:
            self.__json = json.load(f)
    
    def create(self,next_layer,selected_buttons,timer_status,suspend_num):
        task_name_json = self.__json.copy()
        
        layout=[]

        radio_button_hierarchy,task_name_json = self.__get_radio_button_hierarchy(next_layer,task_name_json,selected_buttons,timer_status)
        # layout.append(radio_button_hierarchy)
        
        # 業務名の階層が続かない（jsonの値が""）の場合はtimer関連ボタンを追加してbreak
        if  task_name_json == "":
            if suspend_num != 0:
                if timer_status == Status.in_measurement:
                    layout.append(radio_button_hierarchy)
                else:
                    layout.append(self.__get_row_of_restart_button_and(radio_button_hierarchy))
            else:
                layout.append(radio_button_hierarchy)

            timer_buttons = self.__get_timer_buttons(timer_status)
            layout.append(timer_buttons)
            
            return layout
        else:
            if suspend_num == 0:
                layout.append(radio_button_hierarchy)
                layout.append([sg.Text("※作業を選択してください",font=("",10,""))])
            elif suspend_num != 0:
                if timer_status == Status.in_measurement:
                    layout.append(radio_button_hierarchy)
                    layout.append([sg.Text("※作業を選択してください\r\n",font=("",10,""))])
                else:
                    layout.append(self.__get_row_of_restart_button_and(radio_button_hierarchy))
                    layout.append([sg.Text("※作業を選択してください\r\n",font=("",10,""))])
        
        return layout
    
    
    def __get_radio_button_hierarchy(self,next_layer,task_name_json,selected_buttons,timer_status):
        # radioButton生成
        radio_button_hierarchy = []
        for target_layer in range(next_layer+1):
            task_name_json = self.__get_target_layer_task_name_json(target_layer,task_name_json,selected_buttons)
            if task_name_json == "":
                break            
            radio_buttons = self.__get_target_layer_radio_buttons(target_layer,task_name_json,selected_buttons,timer_status)
            radio_button_hierarchy.append(radio_buttons)
        
        return radio_button_hierarchy,task_name_json
    

    def __get_target_layer_task_name_json(self,target_layer,task_name_json,selected_buttons):
        # target_layerの業務名をjsonから取得するための調整
            if target_layer == 0:
                #jsonの1階層目のプロパティ名をそのまま使用するので何もしない
                return task_name_json
            elif target_layer != 0:
                selected_button_name = selected_buttons[target_layer-1]
                return task_name_json[selected_button_name]
    

    def __get_target_layer_radio_buttons(self,target_layer,task_name_json,selected_buttons,timer_status):
        radios = []
        for key in  task_name_json.keys():
            # ラジオボタンにつけるkeynameを生成
            key_name = str(target_layer) + "radio_" + key

            # 業務名が各レイヤーで選択された業務名と一致したらdefault＝True設定
            if key in selected_buttons:
                if timer_status == Status.in_measurement:
                    radios.append(sg.Radio(key,group_id=target_layer,default=True,key=key_name))
                else:
                    radios.append(sg.Radio(key,group_id=target_layer,default=True,key=key_name, enable_events=True))
            else:
                if timer_status == Status.in_measurement:
                    radios.append(sg.Radio(key,group_id=target_layer,key=key_name,text_color="#000",disabled=True))
                else:
                    radios.append(sg.Radio(key,group_id=target_layer,key=key_name, enable_events=True))
        
        return radios
    
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