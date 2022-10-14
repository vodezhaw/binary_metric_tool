import json
from flask import request
from collections import defaultdict

with open('data/static_file.jsonl', 'rt', encoding='utf-8') as ifile:
    data = []
    for line in ifile:
        dline = json.loads(line)
        data.append(dline)

    headers = list(data[0].keys())
    range_for_header = {}
    for header in headers:
        if header == 'epsilon':
            continue
        range_for_header[header] = sorted(list((set([dp[header] for dp in data]))))

    final_headers = [{
        'header_name': header,
        'header_values': vals
    } for header, vals in range_for_header.items()]


def get_headers():
    return {
        'header_data': final_headers
    }


def get_table_for_header_values():
    header_data = json.loads(request.args.get('data', None))
    fixed_headers = {header: range_for_header[header][idx] for header, idx in header_data.items() if not idx == -1}
    table_labels = [header for header, idx in header_data.items() if idx == -1]
    table_candidates = []
    for dp in data:
        keep = all([dp[key] == val for key, val in fixed_headers.items()])
        if keep:
            table_candidates.append(dp)

    col_name, row_name = table_labels[0], table_labels[1]
    row_to_data = defaultdict(lambda: [])
    for dp in table_candidates:
        row_to_data[dp[row_name]].append([dp[col_name], dp['epsilon']])
    row_to_data = sorted(row_to_data.items(), key=lambda x: x[0])
    sorted_row_data = []
    for row_val, row_data in row_to_data:
        sorted_row = sorted(row_data, key=lambda x: x[0])
        sorted_row_data.append(sorted_row)

    col_values = [col for col, _ in sorted_row_data[0]]
    row_values = [row for row, _ in row_to_data]
    return {
        'table': {
            'col_name': col_name,
            'row_name': row_name,
            'data': sorted_row_data,
            'col_values': col_values,
            'row_values': row_values
        }
    }


routes = [
    {'url': '/api/get_headers',
     'name': 'get_headers',
     'fn': get_headers,
     'methods': ['GET']},
    {'url': '/api/get_table_for_header_values',
     'name': 'get_table_for_header_values',
     'fn': get_table_for_header_values,
     'methods': ['GET']}
]
