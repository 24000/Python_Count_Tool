import datetime as dt

class TaskTimer():

    def __init__(self,id,task_name): 
        self.__data ={"id":id,
                        "タスク名":task_name,
                        "開始時間":dt.datetime.today(),
                        "終了時間":None,
                        "中断回数":0,
                        "中断時間":[],
                        "中断時間合計":None,
                        "作業時間合計":None}
    
    def set_stop_time(self):
        self.__data["終了時間"] = dt.datetime.today()

        total_time =  self.__data["終了時間"] - self.__data["開始時間"]

        if self.__data["中断回数"] != 0:
            suspend_total = 0
            for suspend_set in self.__data["中断時間"]:
               suspend_total  += suspend_set[1] - suspend_set[0]
            self.__data["中断時間合計"] = suspend_total
            total_time  -= suspend_total

        self.__data["作業時間合計"] = total_time
        print(self.__data["作業時間合計"])

    def set_suspend(self):
        self.__data["中断回数"] += 1
        suspend_start =dt.datetime.today()
        suspend_set = [suspend_start]
        self.__data["中断時間"].append(suspend_set)

        print(self.__data["中断時間"][self.__data["中断回数"]-1])

    def get_task_id(self):
        return self.__data["id"]
    
    def get_task_name(self):
        return self.__data["タスク名"]

      