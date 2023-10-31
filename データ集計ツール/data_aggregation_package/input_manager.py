import glob
import os
import datetime as dt

import pandas as pd
import numpy as np

class InputManager():

    def __init__(self):
        self.__data_list = []
        self.__header = "社員番号,社員名,日付,タスク名,開始時間,終了時間,差分(秒),作業時間合計(秒),中断時間合計,中断回数,中断時間リスト".split(",")
        self.__dtype = dtype={0: str, 1: str, 
                              2:str, 3: str, 4: str,5: str, 6: str,7: str,
                              8: str, 9: int, 10: str }
        
    def csv_union_all(self, folder_path : str, start_day : dt.datetime, end_day : dt.datetime) -> pd.DataFrame:
        """
        概要
            対象フォルダ内のCSVで、ユーザー指定対象期間に該当するものを、一つのDataframeとして統合し返却。
        params
            folder_path : str 
                ユーザー指定のCSV格納フォルダパス
            start_day : datetime
                ユーザー指定の対象期間開始日
            end_day : datetime
                ユーザー指定の対象期間終了日
        return : DataFrame
            統合されたCSVデータ
        """
        target = os.path.join(folder_path,"*.csv")
        file_path_list = glob.glob(target)

        self.__data_list = []
        for file_path in file_path_list:
            file_date = os.path.basename(file_path).split("_")[0]
            file_date = dt.datetime.strptime(file_date,"%Y-%M-%d")

            if start_day <= file_date <= end_day:
                self.__data_list.append(

                    pd.read_csv(
                        file_path, 
                        header=None, 
                        skiprows=1,
                        dtype=self.__dtype
                        # parse_dates=[6,7]
                        )

                    )
        
        df = pd.concat(self.__data_list,axis=0,sort=True)
        df[2] = pd.to_datetime(df[2] ).dt.strftime("%m/%d")
        df[6] = pd.to_timedelta(df[6]) #total_seconds()を使うためにtimedeltaへ変換
        df[7] = pd.to_timedelta(df[7])
        df[6] = np.floor(df[6].dt.total_seconds()).astype(int)
        df[7] = np.floor(df[7].dt.total_seconds()).astype(int)
        # print(df.dtypes)
        # print("=====")
        # print(df)
        df.columns = self.__header
        return df
        