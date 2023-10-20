import PySimpleGUI as sg
import os


class ConfigFile():

    def __init__(self,config_file_path):
        self.__EMPLOYEE_INFO = "対象社員情報"
        self.__OUTPUT_FOLDER_PATH = "出力データ格納先パス"
        self.__config_file = {}
        try:
            self.__read(config_file_path)
        except Exception as e:
            sg.popup("設定.txtが同一フォルダ内に存在しません。")
            raise e
    

    # 設定ファイルを読込、辞書として保持
    def __read(self,config_file_path):
        
        current_key = ""
        with open(config_file_path, "r",encoding="utf-8") as config_file:
            for line in config_file:
                if line == "\n" or line[0] == "/":  # 空行とコメント行は無視（先頭が”/”はコメント行）
                    continue
              
                if line[0] == "*":  # 先頭が"*"は項目名の行 
                    current_key = line[1:].rstrip("\n")
                    self.__set_config_file_key_and_data_structure(current_key) 
                else:  # 先頭記号なしは項目名に対する値
                    value = line.rstrip("\n")
                    if value == "Desktop": #出力先指定がこれならlocalPCのDesktopPathに変換
                        value = os.path.expanduser("~/Desktop")
                    
                    result_msg = self.__verify_value(current_key,value)
                    if result_msg == "":
                        self.__set_config_file_value(current_key, value)
                    else:
                            sg.popup("設定ファイルの内容に以下の不備があります。\r\n" + \
                                        "修正してから再度実行してください\r\n\r\n" + result_msg)
                            raise Exception
    
            

    def __set_config_file_key_and_data_structure(self, current_key):
            if current_key == self.__EMPLOYEE_INFO:
                self.__config_file[current_key] = {}
            else:
                self.__config_file[current_key] = []


    def __verify_value(self,current_key,value):
        if current_key == self.__EMPLOYEE_INFO:
            if value.find("_") == -1 or len( value.split("_") ) != 2:
                return "対象社員情報に記述が不正な行があります。\r\n" + \
                           value
            else:
                employee_num,employee_name = value.split("_")
                if employee_num == "" or employee_name == "":
                        return "対象社員情報に社員番号か社員名が未入力の行があります。\r\n" + \
                                  employee_num + ":" + employee_name
        elif current_key == self.__OUTPUT_FOLDER_PATH:
            if os.path.isdir(value) == False:
                return "指定された出力先フォルダが存在しません。\r\n" + \
                           value
        
        return  ""


    def __set_config_file_value(self, current_key, value):
            if current_key == self.__EMPLOYEE_INFO:
                    employee_num,employee_name = value.split("_")
                    self.__config_file[current_key][employee_num] = employee_name
            elif current_key == self.__OUTPUT_FOLDER_PATH:
                    self.__config_file[current_key].append(value)
        

    @property
    def output_folder_path(self):
        path = self.__config_file[self.__OUTPUT_FOLDER_PATH][0]

        if path == "Desktop":
            desktop_path = os.path.expanduser('~\Desktop')
            return desktop_path
        else:
            return path 
    
    
    def exists_employee(self,employee_num):
        employee_info = self.__config_file[self.__EMPLOYEE_INFO]
        if employee_num in employee_info:
            return True
        else:
            return False
    

    def get_employee_name(self,employee_num):
        employee_info = self.__config_file[self.__EMPLOYEE_INFO]
        return employee_info[employee_num]
        