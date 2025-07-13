from typing import Callable
from .signals import TSignals


class PlayerClock:
    __slots__ = ('time_num', 'player_signals')
    def __init__(self, player:str, time_num: int):
        self.time_num = time_num
        self.player_signals:TSignals = TSignals()

    def start(self):
        """开始计时"""
        ...
    
    def stop(self):
        """结束计时"""
        ...
    
    def change(self):
        """暂停计时"""
        ...


class ClockManager:
    """计时器"""
    __slots__ = ('player_signals', )
    def __init__(self):
        self.player_signals:TSignals = TSignals()

    def set_clock(self, player:str, time_num: int):
        """设置倒计时"""
        ...

    def set_clocks(self, player_times:dict[str, int]):
        """设置倒计时"""
        ...

    def reset_clocks(self, player_times:dict[str, int]):
        """设置倒计时"""
        ...

    def start_clock(self, player:str = ''):
        """开始倒计时"""
        ...

    def change_clock(self, player:str = ''):
        """暂停或继续倒计时"""
        ...

    def over_clock(self, player:str = ''):
        """结束倒计时"""
        ...

    def get_time(self, player:str):
        ...

    def set_time(self, player:str = '', time_num: int = 0):
        ...
        
    def call_signal(key: str, player:str):
        """调用信号"""
        ...

    def set_signal(key: str, func: Callable[[str], None]):
        """设置信号"""
        ...