import concurrent.futures
import sys
import time

from pupila.lib.input import input
from pupila.lib.output import output
from pupila.lib.worker import worker
from pupila.lib.logger import logger, update_logger_level
from pupila.lib.config import Config

def run_all(user_app_class):
    executor = concurrent.futures.ProcessPoolExecutor()
    t_output = executor.submit(output.output)
    time.sleep(1) # Allow to create sockets
    t_worker = executor.submit(worker.worker, user_app_class)
    time.sleep(1) # Allow to create sockets
    t_input = executor.submit(input.input)
    concurrent.futures.wait([t_output, t_worker, t_input])

class Pupila():
    """
    Main class of the framework
    """
    def __init__(self, _config, component=None, user_app_module = None):
        """
        Parameters:
        - config(Config): Configuration provided by the user
        - component(str): Component to initialize
        """
        # Initialize global configuration
        config = Config(_config)

        update_logger_level(config.get_log_level())

        logger.info(f'Running component: {component}')

        if component == 'input':
            input.input()
        elif component == 'output':
            output.output()
        elif component == 'worker':
            worker.worker(user_app_module)
        elif component == 'all':
            run_all(user_app_module)
        else:
            logger.warning(f'No (or wrong) component provided: {component}. Defaulting to all.')
            run_all(user_app_module)

if __name__ == "__main__":
    # The config comes from the CLI in usua environments.
    # Adding this here just for easy of manual testing while developing.
    config = {
        'input': {
            'video': {
                'enable': True,
                'uri': 'some_hardcoded-uri'
            },
            'address': { # address where the input component runs for the nng connections
                'host': 'localhost',
                'port': 1234
            },
        },
        "output": {
            'video': {
                'enable': True,
                'uri': 'file:///tmp/my-video.mp4'
            },
            'address': { # address where the input component runs for the nng connections
                'host': 'localhost',
                'port': 1236
            },
        }
    }

    component = sys.argv[1]
    Pupila(config, component, None)
