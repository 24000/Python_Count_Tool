import PySimpleGUI as sg

class UserLogin():

    def __init__(self):
        self.__employee_num = ""
        self.__employee_name = ""
    

    @property
    def employee_num(self):
        return self.__employee_num


    @property
    def employee_name(self):
        return self.__employee_name


    def Do(self,config_file):
        while True:
            
            answer = self.__user_input()
            if answer =="Cancel":
                raise Exception
            
            if config_file.exists_employee(answer):
                self.__employee_num = answer
                self.__employee_name = config_file.get_employee_name(answer)
                break
            else:
                answer = sg.popup_ok_cancel(
                    "入力された社員番号が設定ファイルに存在しません。\r\n" \
                    "再入力する場合「OK」、中止する場合「Cancel」を押してください")
                if answer == "Cancel":
                    raise Exception
    

    def __user_input(self):
        layout =[]
        layout.append([ sg.Text("あなたの社員番号を入力してください") ])
        layout.append([ sg.Input(key="Input") ])
        layout.append([  sg.Button("OK") , sg.Button("Cancel")  ])
        user_input_window = sg.Window('社員番号入力', layout,modal=True,return_keyboard_events=True)
        
        while True:
            event, value = user_input_window.read()
            if event in (sg.WIN_CLOSED,"Cancel"):
                user_input_window.close()
                return "Cancel"
            elif event in ( "OK", "\r" ):
                user_input_window.close()
                user_input = value["Input"]
                return user_input

        