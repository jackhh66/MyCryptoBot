import shared.exchanges.binance.constants as const

import pandas as pd

from data.tests.setup.test_data.sample_data import processed_historical_data_5m

data = pd.DataFrame(processed_historical_data_5m).set_index('open_time')

data.iloc[1, data.columns.get_loc("volume")] = 0
data.iloc[3, data.columns.get_loc("trades")] = 0

candle_size = '5m'
exchange = 'binance'
symbol = 'BTCUSDT'
aggregation_method = const.COLUMNS_AGGREGATION
is_removing_zeros = False
is_removing_rows = False
