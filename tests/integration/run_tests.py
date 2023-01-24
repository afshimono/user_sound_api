import sys
import os
from unittest import TextTestRunner, TestLoader
import requests
import backoff

def run_suite(module: str):
    suite = TestLoader().discover(module)
    test_runner = TextTestRunner(verbosity=2)
    result = test_runner.run(suite)
    sys.exit(not result.wasSuccessful())


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError, max_tries=10)
def host_online(host: str) -> bool:
    response = requests.get(url=f"{host}/health")
    return response.status_code == 200

if __name__=="__main__":
    runner = TextTestRunner()
    host = os.environ["HOST_URL"]
    if not host_online(host):
        raise ConnectionError(f"App is not available for the URL {host}")
    run_suite("tests.integration")