import os

import django
from django.core.paginator import Paginator
from flask import Blueprint, jsonify

from data.service.external_requests import get_strategies
from data.service.helpers._helpers import convert_queryset_to_dict
from shared.data.format_converter import ORDER_FORMAT_CONVERTER, PIPELINE_FORMAT_CONVERTER
from shared.exchanges.binance.constants import CANDLE_SIZES_MAPPER

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "database.settings")
django.setup()

from database.model.models import Symbol, Exchange, Orders, Pipeline

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/resources/<resources>')
def get_resources(resources):

    resources = resources.split(',')

    response = {}

    for resource in resources:
        if resource == 'symbols':
            symbols = Symbol.objects.all().values()
            response["symbols"] = convert_queryset_to_dict(symbols)

        elif resource == 'exchanges':
            exchanges = Exchange.objects.all().values()
            response["exchanges"] = convert_queryset_to_dict(exchanges)

        elif resource == 'strategies':
            strategies = get_strategies()
            response["strategies"] = strategies

        elif resource == 'candleSizes':
            response["candleSizes"] = {key: key for key in CANDLE_SIZES_MAPPER.keys()}

    return jsonify(response)


@dashboard.route('/orders', defaults={'page': None})
@dashboard.route('/orders/<page>')
def get_orders(page):

    response = {}

    orders = Orders.objects.all().order_by('transact_time').values()

    paginator = Paginator(orders, 20)

    if page is None:
        page_obj = paginator.get_page(1)
        response["orders"] = list(page_obj)

    elif isinstance(page, int):
        page_obj = paginator.get_page(page)
        response["orders"] = list(page_obj)

    response["orders"] = [
        {ORDER_FORMAT_CONVERTER[key]: value for key, value in order.items() if key in ORDER_FORMAT_CONVERTER}
        for order in response["orders"]
    ]

    return jsonify(response)


@dashboard.route('/pipelines', defaults={'page': None})
@dashboard.route('/pipelines/<page>')
def get_pipelines(page):

    response = {}

    pipelines = Pipeline.objects.all().order_by('id').values()

    paginator = Paginator(pipelines, 20)

    if page is None:
        page_obj = paginator.get_page(1)
        response["pipelines"] = list(page_obj)

    elif isinstance(page, int):
        page_obj = paginator.get_page(page)
        response["pipelines"] = list(page_obj)

    response["pipelines"] = [
        {PIPELINE_FORMAT_CONVERTER[key]: value for key, value in pipeline.items() if key in PIPELINE_FORMAT_CONVERTER}
        for pipeline in response["pipelines"]
    ]

    return jsonify(response)
