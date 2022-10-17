import io

import matplotlib.pyplot as plt
from flask import request, send_file
import numpy as np
import seaborn as sns
import pandas as pd

def data_to_fig(data_prc, x_axis_name):
    plt.figure(figsize=(10,6))
    sns_plot = sns.lineplot(x=x_axis_name, y='value', hue='variable', data=pd.melt(data_prc, [x_axis_name]))
    plt.xlabel(x_axis_name)
    plt.ylabel("Epsilon")
    #sns_plot.set(ylabel='Epsilon')
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.tight_layout()
    im_buf = io.BytesIO()
    sns_plot.get_figure().savefig(im_buf, format='png', dpi=150)
    im_buf.seek(0)
    plt.clf()
    return send_file(im_buf, mimetype='image/png')


def create_col_wise_plot(x_axis_name, x_axis, label_name, data, labels):
    prep_data = {
        f'{x_axis_name}': np.array(x_axis)
    }
    for data_row, label in zip(data, labels):
        y = [val[1] for val in data_row]
        prep_data[f'{label_name} = {label:.2f}'] = np.array(y)
    data_prc = pd.DataFrame(prep_data)
    return data_to_fig(data_prc, x_axis_name)


def create_row_wise_plot(x_axis_name, x_axis, label_name, data, labels):
    prep_data = {
        f'{x_axis_name}': np.array(x_axis)
    }
    for idx, label in enumerate(labels):
        y = [y[idx][1] for y in data]
        prep_data[f'{label_name} = {label:.2f}'] = np.array(y)
    data_prc = pd.DataFrame(prep_data)
    return data_to_fig(data_prc, x_axis_name)

def get_plot_for_table():
    if request.method == 'POST':
        data = request.get_json(force=True)
        table_data = data['table_data']['table']
        x_axis = data['x_axis']
        col_name = table_data['col_name']
        row_name = table_data['row_name']
        row_values = table_data['row_values']
        col_values = table_data['col_values']
        data = table_data['data']

        if x_axis == col_name:
            return create_col_wise_plot(x_axis, col_values, row_name, data, row_values)
        else:
            return create_row_wise_plot(x_axis, row_values, col_name, data, col_values)
    else:
        return 'OK', 201


routes = [
    {'url': '/api/get_plot_for_table',
     'name': 'get_plot_for_table',
     'fn': get_plot_for_table,
     'methods': ['POST']}
]
