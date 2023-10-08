import PySimpleGUI as sg
import sys
import re

from window import Window



window = Window()

while True:
    
    boot_window = window.create()
    

    while True:
        key_name, values = boot_window.read()

        if key_name == sg.WIN_CLOSED:
            sys.exit()

        if key_name.find("radio") != -1:
            selected_layer =  int(key_name[0])
            task_name = key_name.split("_",1)[1]
            window.set_selected_radio_info(selected_layer,task_name)
            window.set_window_position(boot_window.current_location())
            boot_window.close()
            break

        if key_name == "開始":
            window.start_timer()
            boot_window.close()
            break

        if key_name == "終了":
            window.stop_timer()
            boot_window.close()
            break
        
        if key_name == "一時停止":
            window.suspend_timer()
            boot_window.close()
            break

        if key_name == "再開":
            if sg.popup_yes_no("停止中のタスクを再開しますか？") == "No":
                break

            msg = "以下から再開するタスクを選択してください。"
            layout =[]
            layout.append([sg.Text(msg)])

            suspend_tasks = window.get_suspend_tasks() 
            for suspend_task_name in suspend_tasks:
                layout.append([sg.Radio(suspend_task_name,key="radio_" + suspend_task_name ,group_id=1,enable_events=True)])
            
            layout.append([sg.Button("やはり再開しない")])

            popup = sg.Window('確認', layout)

            answer = ""
            event, value = popup.read()
            if event.find("radio") != -1:
                restart_target_task_name = event.split("_",1)[1]
                popup.close()
            elif event in (None,"やはり再開しない"):
                popup.close()

            print(restart_target_task_name)


