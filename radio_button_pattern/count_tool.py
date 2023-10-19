import PySimpleGUI as sg
import sys

from enums import ExitSituation
from config_file import ConfigFile
from user_login import UserLogin
from window import Window



def main():

    file_path = "設定.txt" 
    try:
       config_file = ConfigFile(file_path)
    except:
        return

    try:
        login = UserLogin()
        login.Do(config_file)
    except:
        return

    try:
        window = Window(config_file, login.employee_num, login.employee_name)
    except Exception as e:
        return



    while True:
        
        boot_window = window.create_main()
        

        while True:
            key_name, values = boot_window.read()

            if key_name == sg.WIN_CLOSED:
                situation = window.check_exit_situation()

                if situation == ExitSituation.exit_cancel:
                    window.close(boot_window)
                    break
                elif situation == ExitSituation.no_data:
                    sys.exit()
                elif situation == ExitSituation.exists_complete_data_only:
                    window.write_data()
                    sys.exit()
                elif situation == ExitSituation.exists_incomplete_data:
                    window.stop_all_incomplete_timer()
                    window.write_data()
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
                # if sg.popup_yes_no("停止中のタスクを再開しますか？") == "No":
                #     window.close(boot_window)
                #     break
                popup = window.create_restart_popup()
                event, value = popup.read()

                if event.find("radio") != -1:
                    popup.close()
                    selected_index = int(event.split("_")[0])
                    window.restart_timer(selected_index)
                    window.close(boot_window)
                    break

                elif event in (sg.WIN_CLOSED,"やはり再開しない"):
                    popup.close()
                    window.close(boot_window)
                    break
            
            if key_name == "キャンセル":
                if sg.popup_yes_no("現在のタスク計測をキャンセルしますか？") == "No":
                    window.close(boot_window)
                    break

                window.cancel_timer()
                sg.popup("現在のタスク計測をキャンセルしました。\r\nキャンセルされたタスク計測分は記録に残りません。")
                window.close(boot_window)
                break




if __name__ == "__main__":
    main()
