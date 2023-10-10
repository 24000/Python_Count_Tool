import PySimpleGUI as sg
import sys
import re

from window import Window



window = Window()

while True:
    
    boot_window = window.create_main()
    

    while True:
        key_name, values = boot_window.read()

        if key_name == sg.WIN_CLOSED:
            sys.exit()

        if key_name.find("radio") != -1:
            selected_layer =  int(key_name[0])
            task_name = key_name.split("_",1)[1]
            window.set_selected_radio_info(selected_layer,task_name)
            window.close(boot_window)
            break

        if key_name == "開始":
            window.start_timer()
            window.close(boot_window)
            break

        if key_name == "終了":
            window.stop_timer()
            window.close(boot_window)
            break
        
        if key_name == "一時停止":
            window.suspend_timer()
            window.close(boot_window)
            break

        if key_name == "再開":
            if sg.popup_yes_no("停止中のタスクを再開しますか？") == "No":
                window.close(boot_window)
                break

            popup = window.create_restart_popup()

            answer = ""
            event, value = popup.read()

            if event.find("radio") != -1:
                popup.close()
                selected_index = int(event.split("_")[0])
                window.restart_timer(selected_index)
                window.close(boot_window)
                break

            elif event in (None,"やはり再開しない"):
                popup.close()
                window.close(boot_window)
                break


