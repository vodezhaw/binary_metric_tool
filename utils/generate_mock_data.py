import json
import random
import numpy as np
from itertools import product
from tqdm import tqdm

human_ratings_range = [0, 10, 100, 500, 1000, 2000, 5000, 10_000]
human_rho_eta_range = [0, 10, 100, 500, 1000, 2000, 5000, 10_000]
binary_ratings_range = [0, 500, 1000, 5000, 10_000, 20_000, 50_000, 100_000, 1_000_000]

rho_range = list(np.arange(0.55, 1, 0.1))
eta_range = list(np.arange(0.55, 1, 0.1))
alpha_range = list(np.arange(0, 1.1, 0.1))

print(rho_range)
print(eta_range)
print(alpha_range)

with open('data/static_file.jsonl', 'wt', encoding='utf-8') as ofile:
    for n_tuple in tqdm(product(human_ratings_range, human_rho_eta_range, binary_ratings_range, rho_range, eta_range, alpha_range)):
        line = {
            'n_human_rating': n_tuple[0],
            'n_human_rho_eta': n_tuple[1],
            'n_binary_rating': n_tuple[2],
            'rho': n_tuple[3],
            'eta': n_tuple[4],
            'alpha': n_tuple[5],
            'epsilon': random.random()
        }

        j_line = json.dumps(line)

        ofile.write(f'{j_line}\n')