
from pathlib import Path
import json
from itertools import product

from tqdm import tqdm

import numpyro
from backend.estimation import estimate_epsilon

numpyro.set_host_device_count(5)

human_ratings_range = [0, 10, 100, 500, 1000, 2000, 5000, 10_000]
human_rho_eta_range = [0, 10, 100, 500, 1000, 2000, 5000, 10_000]
binary_ratings_range = [0, 500, 1000, 5000, 10_000, 20_000, 50_000, 100_000, 1_000_000]

rho_range = list(range(55, 100, 10))
eta_range = list(range(55, 100, 10))
alpha_range = list(range(0, 110, 10))


out_file = Path("./data/static_file.jsonl")

if not out_file.exists():
    out_file.touch()

done_already = set()
with out_file.open('r') as fin:
    for line in fin:
        entry = json.loads(line.strip())
        tup = (
            entry['n_human_rating'],
            entry['n_human_rho_eta'],
            entry['n_binary_rating'],
            int(100 * entry['rho']),
            int(100 * entry['eta']),
            int(100 * entry['alpha']),
        )
        done_already.add(tup)


for n_tuple in tqdm(product(human_ratings_range, human_rho_eta_range, binary_ratings_range, rho_range, eta_range, alpha_range)):
    if n_tuple in done_already:
        continue
    line = {
        'n_human_rating': n_tuple[0],
        'n_human_rho_eta': n_tuple[1],
        'n_binary_rating': n_tuple[2],
        'rho': n_tuple[3] / 100,
        'eta': n_tuple[4] / 100,
        'alpha': n_tuple[5] / 100,
    }

    line['epsilon'] = estimate_epsilon(**line)

    j_line = json.dumps(line)

    with out_file.open('a') as fout:
        fout.write(f'{j_line}\n')
