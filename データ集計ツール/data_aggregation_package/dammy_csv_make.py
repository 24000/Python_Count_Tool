import os 
import datetime as dt
import random

import pandas as pd

def dummy_simple():
    folder = os.path.dirname(__file__) + "\\dummy_data"
    header = "社員番号,社員名,日付,タスク名,開始時間,終了時間,差分,作業時間合計,中断時間合計,中断回数,中断時間リスト".split(",")
    
    
    emp_nums = ["1234","1111","2222"]
    emp_names = ["山田太郎","鈴木誠一","田中博"]
    
    for num in range(1,4):
        d = dt.datetime(2023,10,num)
        for emp in range(3):
            df_list = []
            emp_num = emp_nums[emp]
            emp_name = emp_names[emp]
            now = dt.datetime.combine( d.date(), dt.time(12,0,0))
            for _ in range(3):
                start = now
                end = now + dt.timedelta(hours=1)
                dif = str(end - start)
                data = [emp_num,emp_name,d,"事務//資料作成",start,end,dif,dif,0,0,0]
                df_list.append(data)
                now = end
    
            df = pd.DataFrame(df_list,columns=header)
            filename = f"{str(d.date())}_{emp_num}_{emp_name}.csv "
            filepath = os.path.join(folder,filename)
            df.to_csv(filepath,index=False)


def dummy_random():
    folder = os.path.dirname(__file__) + "\\dummy_data"
    header = "社員番号,社員名,日付,タスク名,開始時間,終了時間,差分,作業時間合計,中断時間合計,中断回数,中断時間リスト".split(",")
    
    
    emp_nums = ["1234","1111","2222","3333","4444","5555","6666","7777","8888","9999"]
    emp_names = ["山田太郎","鈴木誠一","田中博","横山真一","佐藤元太","清水裕子","広瀬花子","佐々木信二","広中学","貝原良子"]
    task_names = ["受電//通常対応//請求案内","受電//通常対応//設定変更","受電//通常対応//セールス",
                  "受電//クレーム対応//SVにて完結","受電//クレーム対応//社員相談","受電//内線対応",
                  "事務//経費精算","事務//報告書作成","事務//提案資料作成","研修//新人研修","研修//スキルアップ研修","研修//事務研修"]
    
    for num in range(1,32): #日付
        d = dt.datetime(2023,10,num)
        for _ in range(7): #その日付で出勤する社員数＝その日付で出力されるファイル数(emp_no重複上書きで必ず5というわけではない)
            emp_no = random.randint(0, 9)
            df_list = []
            emp_num = emp_nums[emp_no]
            emp_name = emp_names[emp_no]
            now = dt.datetime.combine( d.date(), dt.time(9,0,0)) # 9時始業
            for _ in range(40): #ファイル内の生成データ数
                h = 0
                m = random.randint(0,20)
                s = random.randint(0,60)
                start = now
                end = now + dt.timedelta(hours=h,minutes=m,seconds=s)
                dif = str(end - start)
                task_no = random.randint(0,11)
                task_name = task_names[task_no]
                data = [emp_num,emp_name,d.date(),task_name,start.time(),end.time(),dif,dif,0,0,0]
                df_list.append(data)
                now = end
    
            df = pd.DataFrame(df_list,columns=header)
            filename = f"{str(d.date())}_{emp_num}_{emp_name}.csv "
            filepath = os.path.join(folder,filename)
            df.to_csv(filepath,index=False)



if __name__ == "__main__":
    dummy_random()