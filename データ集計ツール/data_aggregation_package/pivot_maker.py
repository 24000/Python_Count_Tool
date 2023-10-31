import pandas as pd
import numpy as np
from typing import Any

class PivotMaker():
    """
    概要
        データの集計処理を担当
    """
    def __init__(self, index, columns, values) -> None:
        self.__index = index
        self.__columns = columns
        self.__values = values


    def make(self,data : pd.DataFrame, func : any) -> pd.DataFrame:
        pivot = data.pivot_table(
            index = self.__index, 
            columns= self.__columns, 
            values= self.__values, 
            aggfunc= func,
            fill_value=0,
            margins=True, 
            margins_name="合計"
            )
        # meanの場合、小数点以下が6桁続くので文字列としてフォーマット修正の上、int型で返す
        return pivot.applymap("{:.0f}".format).astype(int)