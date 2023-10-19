import PySimpleGUI as sg
import sys
import unicodedata

from enums import ExitSituation
from config_file import ConfigFile
from user_login import UserLogin
from window import Window



def main():

    file_path = "設定.txt" 
    try:
       config_file = ConfigFile(file_path)
    except Exception as e:
        return

    try:
        login = UserLogin()
        login.Do(config_file)
    except Exception as e:
        return

    try:
        window = Window(config_file, login.employee_num, login.employee_name)
    except Exception as e:
        return


    while True:
        
        boot_window = window.create_main()
        boot_window.force_focus()

        # combo_boxにauto_completeを実装するための前処理
        combos = get_combos_on(window,boot_window)
        bind_key_combo_names = []
        for i, combo in enumerate(combos):
            combo.bind("<KeyPress>", " K") #何かしらのキー押下　key_nameが"combo名 K"でくる。
            bind_key_combo_names.append(combo.key + " K")
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
            

            if key_name in bind_key_combo_names: # combo_boxで入力があると発火
                index=0
                for i,item in enumerate(bind_key_combo_names):
                    if key_name == item:
                        index = i
                
                if combos[index].user_bind_event.keycode == 40: # 40=keyDown
                    # 引数でcombos[index]で渡すと描画不具合が発生する。
                    # 関数内でcombos[index]と使用すると安定。メモリ参照の関係か？
                    clear_combo_tooltip(combos,index)
                else:
                    task_names = window.get_combo_values(index)
                    symbol_text_updated(combos,index,task_names)


            if key_name.find("combo") != -1 and key_name.find("K") == -1:
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
                


# combo_boxにAuto completeを実装するための関数群
# ==========================================

def get_combos_on(window,boot_window):
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
    
    return combos


def symbol_text_updated( combos,index ,all_values) :
    input_text = combos[index].widget.get()
    input_text =unicodedata.normalize('NFKC', input_text.lower())
    if input_text == "":
        combos[index].update(values=all_values)
        clear_combo_tooltip(combos,index)
        return
    else:
        word_list=[]
        count=0
        for item in all_values:
            if input_text in unicodedata.normalize('NFKC', item.lower()):
                word_list.append(item)
                count += 1
 
        combos[index].update(input_text, values=word_list)
        clear_combo_tooltip(combos,index)
        show_combo_tooltip(combos,index, tooltip="\n".join(word_list))


def clear_combo_tooltip(combos,index):
    if combos[index].TooltipObject != None:
        tooltip = combos[index].TooltipObject
        tooltip.hidetip()
        combos[index].TooltipObject = None


def show_combo_tooltip(combos,index, tooltip):
    combos[index].set_tooltip(tooltip)
    tooltip = combos[index].TooltipObject
    tooltip.y += 45
    tooltip.showtip()

# ========================================


if __name__ == "__main__":
    main()
