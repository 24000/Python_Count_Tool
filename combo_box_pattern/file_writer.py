import os

class FileWriter():
    
    def __init__(self) -> None:
        pass

    def write_csv_file(self,file_path,employee_num,employee_name,complete_timers):
        if os.path.isfile(file_path) == False:
            with open(file_path, 'w+') as f:
                f.write("社員番号,社員名,日付,タスク名,開始時間,終了時間,差分,作業時間合計,中断時間合計,中断回数,中断時間リスト\n")
            os.chmod(file_path,0o777)

        with open(file_path,"a") as f:
            for timer in complete_timers:
                write_data = f"{employee_num},{employee_name},{timer.measurement_date},{timer.task_name},{timer.start_time},{timer.stop_time},{timer.diff_time},{timer.total_work_time},{timer.total_suspend_time},{timer.suspend_num},{timer.suspend_time_list}\n"
                f.write(write_data)