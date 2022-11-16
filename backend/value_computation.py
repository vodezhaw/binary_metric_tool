import random
import json
from flask import request

from backend.estimation import estimate_epsilon


def compute_single_value():
    header_data = json.loads(request.args.get('data', None))

    eps = estimate_epsilon(
        n_human=header_data['n_human_rating'],
        n_rho_eta=header_data['n_human_rho_eta'],
        n_metric=header_data['n_binary_rating'],
        rho=header_data['rho'] / 100.,
        eta=header_data['eta'] / 100.,
        alpha=header_data['alpha'] / 100.,
    )

    return {
        'value': eps,
    }


routes = [
    {'url': '/api/compute_single_value',
     'name': 'compute_single_value',
     'fn': compute_single_value,
     'methods': ['GET']}
]