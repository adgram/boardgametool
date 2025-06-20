from .wuziqi import App_五子棋, App_井字棋
from .weiqi import App_围棋13, App_围棋19, App_围棋9
from .biesiniu import App_憋死牛
from ...gridrule import APPS



APPS.update({
    '五子棋': App_五子棋,
    '井字棋': App_井字棋,

    '围棋13': App_围棋13,
    '围棋': App_围棋19,
    '围棋9': App_围棋9,
    '憋死牛': App_憋死牛,

})