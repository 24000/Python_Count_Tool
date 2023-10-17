import PySimpleGUI as sg
import sys

from enums import ExitSituation
from config_file import ConfigFile
from user_login import UserLogin
from window import Window



def main():

    file_path = "z_設定ファイル.txt" 
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
    except:
        return

    
    


    while True:
        
        boot_window = window.create_main()

        # combo_boxにauto_completeさせるための前処理
        combos = []
        if window.next_layer == 0:
            combos.append(boot_window["0combo_box"]) 
        else:
            if window.is_finish_select():
                for i in range( window.next_layer ):
                    combos.append(boot_window[ str(i) + "combo_box"] ) 
            else:
                for i in range( window.next_layer + 1 ):
                    combos.append(boot_window[ str(i) + "combo_box"] ) 
           
        bind_r_combos = []
        for i, combo in enumerate(combos):
            combo.bind('<Return>', ' R') #Enterキー押下　key_nameが"combo名 R"でくる。
            bind_r_combos.append(combo.key + ' R')
        

        if window.is_finish_select() == False:
            combos[ window.next_layer ].set_focus()
            combos[ window.next_layer ].TKCombo.focus()
            


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
            

            if key_name in bind_r_combos: # combo_boxでエンターキー押下→auto complete
                idx=0
                for i,item in enumerate(bind_r_combos):
                    if key_name == item:
                        idx = i
                search_combo(combos[idx],window.get_combo_values(idx))


            if key_name.find("combo") != -1 and key_name.find("R") == -1:
                selected_layer =  int(key_name[0])
                task_name = values[key_name]
                window.set_selected_combo_info(selected_layer,task_name)
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
                

            


# auto_complete
def search_combo(combo,combo_values):
    # 入力された値を取得
    value=combo.widget.get()
    if value =="":
        combo.update(values=combo_values)
    else:
        f_lst=[]
        count=0
        for item in combo_values:
            if value.lower() in item.lower():
                f_lst.append(item)
                count += 1
        if count > 0:
            combo.update(value,values=f_lst)
            combo.Widget.event_generate('<Key-Down>') # to show the list within the Combo
        else:
            combo.update('',values=combo_values)



if __name__ == "__main__":
    main()
