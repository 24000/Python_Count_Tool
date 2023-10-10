import PySimpleGUI as sg
import json

from enum_status import Status

class LayoutMaker():
    def __init__(self):
        with open(r'./JSON\test.json',encoding="utf-8") as f:
            self.__json = json.load(f)
    
    def create(self,next_layer,selected_buttons,timer_status,suspend_num):
        task_name_json = self.__json.copy()
        layout=[]
        for target_layer in range(next_layer+1):
            task_name_json = self.__get_target_layer_task_name_json(target_layer,task_name_json,selected_buttons)
            if task_name_json == "":
                break            
            # radioButton生成
            radio_buttons = self.__get_target_layer_radio_buttons(target_layer,task_name_json,selected_buttons)
            layout.append(radio_buttons)
        
        # 業務名の階層が続かない（jsonの値が""）の場合はtimer関連ボタンを追加してbreak
        if  task_name_json == "":
            timer_buttons = self.__get_timer_buttons(timer_status)
            layout.append(timer_buttons)
            if suspend_num != 0:
      
                layout.append([sg.Column([sg.Button("再開",)],element_justification="c",)])
                # layout.append([sg.Button("再開",)])
            return layout
  
        if suspend_num != 0:
            layout.append([sg.Text("")])
            layout.append([sg.Button("再開",)])

        return layout
    

    def __get_target_layer_task_name_json(self,target_layer,task_name_json,selected_buttons):
        # target_layerの業務名をjsonから取得するための調整
            if target_layer == 0:
                #jsonの1階層目のプロパティ名をそのまま使用するので何もしない
                return task_name_json
            elif target_layer != 0:
                selected_button_name = selected_buttons[target_layer-1]
                return task_name_json[selected_button_name]
    

    def __get_target_layer_radio_buttons(self,target_layer,task_name_json,selected_buttons):
        radios = []
        for key in  task_name_json.keys():
            # ラジオボタンにつけるkeynameを生成
            key_name = str(target_layer) + "radio_" + key

            # 業務名が各レイヤーで選択された業務名と一致したらdefault＝True設定
            if key in selected_buttons:
                radios.append(sg.Radio(key,group_id=target_layer,default=True,key=key_name, enable_events=True))
            else:
                radios.append(sg.Radio(key,group_id=target_layer,key=key_name, enable_events=True))
        
        return radios
    

    def __get_timer_buttons(self,timer_status):
        buttons = []
        if timer_status == Status.in_measurement:
            start_button = sg.Button("開始",disabled=True)
            stop_button = sg.Button("終了")
            suspend_button = sg.Button("一時停止")
            # restart_button = sg.Button("再開",disabled=True)
        elif timer_status == Status.stop:
            start_button = sg.Button("開始")
            stop_button = sg.Button("終了",disabled=True)
            suspend_button = sg.Button("一時停止",disabled=True)
            # restart_button = sg.Button("再開",disabled=True)
        elif timer_status == Status.suspend:
            start_button = sg.Button("開始")
            stop_button = sg.Button("終了",disabled=True)
            suspend_button = sg.Button("一時停止",disabled=True)
            # restart_button = sg.Button("再開")
   
        return  [start_button,stop_button,suspend_button]