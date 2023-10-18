import datetime as dt


# 1taskにつき、1タイマーとして各種情報を辞書として保持
class TaskTimer():

    # 開始ボタン押下時にインスタンス化される
    def __init__(self,id,task_name): 
        self.__data ={"id":id,
                        "タスク名":task_name,
                        "開始時間":dt.datetime.now(),
                        "終了時間":None,
                        "差分":None,
                        "作業時間合計":None,
                        "中断時間合計":None,
                        "中断回数":0,
                        "中断時間リスト":[],    # 「中断開始時間と終了時間のリスト」を格納するリスト
                        }
    
    @property
    def measurement_date(self):
        return self.__data["開始時間"].strftime("%Y/%m/%d")
    
    @property
    def task_name(self):
        return self.__data["タスク名"]
    
    @property
    def start_time(self):
        return self.__data["開始時間"].strftime("%H:%M:%S.%f")[:-5]
    
    @property
    def stop_time(self):
        return self.__data["終了時間"].strftime("%H:%M:%S.%f")[:-5]
    
    @property
    def diff_time(self):
        return str(self.__data["差分"])[:-5]
    
    @property
    def suspend_num(self):
        num = str(self.__data["中断回数"])
        if num == "":
            return "0"
        else:
            return num
    
    @property
    def suspend_time_list(self):
        suspend_list =  self.__data["中断時間リスト"]
   
        if len(suspend_list) == 0:
            return dt.datetime(1,1,1,0,0,0,0).strftime("%H:%M:%S")
        else:
            string = ""
            for suspend_start_end in suspend_list:
                suspend_start = suspend_start_end[0].strftime("%H:%M:%S.%f")[:-5]
                suspend_end = suspend_start_end[1].strftime("%H:%M:%S.%f")[:-5]
                string += f"{suspend_start}-{suspend_end}_"
            
            return  string.rstrip("_")

    @property
    def total_suspend_time(self):
        if self.__data["中断時間合計"] == None:
            return dt.datetime(1,1,1,0,0,0,0).strftime("%H:%M:%S")
        else:
            return str(self.__data["中断時間合計"])[:-5]

    @property
    def total_work_time(self):
        return str(self.__data["作業時間合計"])[:-5]
            

    # 終了ボタン押下時の処理
    def set_stop_time(self):
        self.__data["終了時間"] = dt.datetime.now()

        diff_time =  self.__data["終了時間"] - self.__data["開始時間"]
        self.__data["差分"]  = diff_time

        total_time = diff_time
        if self.__data["中断回数"] != 0:
            suspend_total = self.__calculate_suspend_total()
            self.__data["中断時間合計"] = suspend_total
            total_time  -= suspend_total

        self.__data["作業時間合計"] = total_time

        # if self.__data["中断回数"] != 0:
        #     sg.popup("開始時間:" + str(self.__data["開始時間"]) + "\r\n終了時間:" + str(self.__data["終了時間"]) + "\r\n差分時間:" + str(diff_time) + "\r\n作業時間:" + str(total_time) + "\r\n" + "中断時間:" + str(suspend_total) )
        # else:
        #     sg.popup("開始時間:" + str(self.__data["開始時間"]) + "\r\n終了時間:" + str(self.__data["終了時間"]) + "\r\n差分時間:" + str(diff_time) + "\r\n作業時間:" + str(total_time) + "\r\n" + "中断時間:00:00:00" )
        # sg.popup("作業時間" + total_time.strftime ("%H : %M : %S") + "\r\n" + "中断時間" + self.__data["中断時間合計"].strftime ("%H : %M : %S") )


    # 一時停止の合計時間を算出
    def __calculate_suspend_total(self):
        suspend_total = dt.timedelta()
        for suspend_start_end in self.__data["中断時間リスト"]:
            suspend_start =  suspend_start_end[0]
            suspend_end = suspend_start_end[1]
            suspend_total  +=  suspend_end - suspend_start
        return suspend_total


    # 一時停止ボタン押下時の処理
    def set_suspend_start_data(self):
        self.__data["中断回数"] += 1
        suspend_start =dt.datetime.now()
        suspend_start_end = [suspend_start]
        self.__data["中断時間リスト"].append(suspend_start_end)

        # print(self.__data["中断時間リスト"][self.__data["中断回数"]-1])


    def get_task_id(self):
        return self.__data["id"]


    def get_task_name(self):
        return self.__data["タスク名"]
    

    def set_suspend_end_data(self):
        suspend_end = dt.datetime.now()
        suspend_index = self.__data["中断回数"] -1
        self.__data["中断時間リスト"][suspend_index].append(suspend_end)


    @classmethod
    def Get_Today(cls):
        return str(dt.date.today()) 

      