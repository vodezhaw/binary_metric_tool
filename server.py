from flask import Flask
import backend.test_api as test_api
import backend.static_file_query as static_file
import backend.value_computation as val_comp
import backend.plot_api as plt_api
from backend.config import load_config


config = load_config()

app = Flask(__name__)

API_MODULES = [test_api, static_file, val_comp, plt_api]


def register_route(url_path, name, fn, methods=['GET']):
    """
    Registers the given `fn` function as the handler, when Flask receives a
    request to `url_path`.
    """
    app.add_url_rule(url_path, name, fn, methods=methods)


# Register all modules stored in API_MODULES
for api_module in API_MODULES:
    for r in api_module.routes:
        register_route(r['url'], r['name'], r['fn'], r['methods'])

if __name__ == "__main__":
    import numpyro
    numpyro.set_host_device_count(8)
    app.run(host='localhost', port=config['local_port'], debug=True)
