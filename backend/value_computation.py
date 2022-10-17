import random
import json
from flask import request


def compute_single_value():
    header_data = json.loads(request.args.get('data', None))
    header_sum = sum([val for k, val in header_data.items()])
    return {
        'value': header_sum
    }


routes = [
    {'url': '/api/compute_single_value',
     'name': 'compute_single_value',
     'fn': compute_single_value,
     'methods': ['GET']}
]