from enum import Enum


class Status(Enum):
    in_measurement = 1
    suspend = 2
    stop = 3


class ExitSituation(Enum):
    no_data = 1
    exists_complete_data_only = 2
    exists_incomplete_data = 3
    exit_cancel = 4