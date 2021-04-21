from datetime import datetime

import pytz
import pytest

from data.tests.helpers.sample_data import exchange_data_1
from database.model.models import Exchange, Symbol, ExchangeData, Asset


@pytest.fixture
def create_exchange(db):
    return Exchange.objects.create(name='binance')


@pytest.fixture
def create_assets(db):
    obj1 = Asset.objects.create(symbol='BTC')
    obj2 = Asset.objects.create(symbol='USDT')

    return [obj1, obj2]

@pytest.fixture
def create_symbol(db):
    return Symbol.objects.create(name='BTCUSDT', base_id='BTC', quote_id='USDT')


@pytest.fixture
def exchange_data_factory(db, create_exchange, create_assets, create_symbol):
    # Closure
    def create_exchange_data(**kwargs):
        return ExchangeData.objects.create(**exchange_data_1, **kwargs)
    return create_exchange_data


@pytest.fixture
def exchange_data(db, exchange_data_factory):
    return exchange_data_factory()