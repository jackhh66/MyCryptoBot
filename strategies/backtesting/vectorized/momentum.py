import numpy as np

from strategies.backtesting.strategies import MomentumBase
from strategies.backtesting.vectorized.base import VectorizedBacktester


class MomentumVectBacktester(MomentumBase, VectorizedBacktester):
    """ Class for the vectorized backtesting of simple Contrarian trading strategies.
    """

    def __init__(self, data, window=10, trading_costs=0, symbol='BTCUSDT'):
        MomentumBase.__init__(self)
        VectorizedBacktester.__init__(self, data, symbol=symbol, trading_costs=trading_costs)

        self.window = window

        self._update_data()

    def test_strategy(self, window=None, plot_results=True):
        """ Backtests the trading strategy.
        """
        self._set_parameters(window)

        data = self.data.copy().dropna()
        data["position"] = np.sign(data[self.returns_col].rolling(self.window).mean())

        title = self.__repr__()

        return self._assess_strategy(data, plot_results, title)
