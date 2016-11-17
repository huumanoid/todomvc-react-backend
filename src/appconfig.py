import logging
from tg import AppConfig

from model import Model

def createConfig(**args):
    config = AppConfig(**args)

    config.use_sqlalchemy = True
    config['sqlalchemy.url'] = 'mysql://_ru_hmnid_tstusr:password@localhost/_ru_hmnid_testdb'
    config.model = Model()
    config.serve_static = True
    config.paths['static_files'] = 'todomvc/examples/react'

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    return config
