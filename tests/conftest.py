from collections import Counter
import logging
import pytest
from playwright.sync_api import sync_playwright
from utility.settings import BASE_URL
from utility.api_client import APIClient
from utility.data_generator import DataGenerator

# --- Loggers ---

@pytest.fixture(scope="session", autouse=True)
def configure_logger():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("test_log.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger # return logger so other fixtures can use it

def pytest_runtest_logreport(report): 
    """Hook called after each test phase (setup/call/teardown).""" 
    logger = logging.getLogger("test_logger")

    if report.when == "setup" : 
        logger.info(f"[TEST START] {report.nodeid}")

    if report.when == "call": 
        # only log the actual test outcome 
        outcome = "PASSED" if report.passed else "FAILED" 
        # report.nodeid includes the test name + parametrize ID 
        logger.info(f"[TEST RESULT] {report.nodeid} → {outcome}")

# --- Setup ---

@pytest.fixture(scope="session")
def api_client(configure_logger):
    logger = configure_logger 
    logger.info("Starting Playwright and creating API client...")
    
    with sync_playwright() as p:
        context = p.request.new_context(
            base_url = BASE_URL,
            extra_http_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        client = APIClient(context, logger)
        logger.info("API client created successfully.")
        yield client

        logger.info("Disposing Playwright context and closing API client...") 
        context.dispose() 
        logger.info("API client disposed.")

@pytest.fixture(autouse=True) 
def inject_client(request, api_client): 
    """ Autouse fixture: if the test class has 'client' attribute, inject the api_client into it automatically. """ 

    if hasattr(request.node, "cls") and request.node.cls is not None: setattr(request.node.cls, "client", api_client)

@pytest.fixture(autouse=True) 
def inject_logger(request, configure_logger): 
    """ Autouse fixture: if the test class has 'logger' attribute, inject the logger into it automatically. """ 
    cls = getattr(request.node, "cls", None) 
    if cls is not None and not hasattr(cls, "logger"): setattr(cls, "logger", configure_logger)     

@pytest.fixture(scope="session") 
def data_generator(): 
    """ Provides a DataGenerator instance for all tests. Session-scoped so it's created once and reused. """

    data = DataGenerator() 
    yield data

# --- Common helpers ---

def validate_id_consistency(re_json: list, single_identifier_function):
    """ 
    To make sure GET (single) has a same entry as found in GET (all).
    "id" is the shared identifier for Carts, Products, and Users.
    """

    failures = []
    entry_map = {entry["id"]: entry for entry in re_json} 

    for id, expected_entry in entry_map.items():
        json_single = single_identifier_function(id)
        if json_single != expected_entry:
            failures.append(
                f"Mismatch for id={id}:\n"
                f"Expected: {expected_entry}\n"
                f"Got:      {json_single}\n"
            )
    return failures

def validate_unique_identifier(re_json: list, unique_identifier: str, secondary_identifier: str):
    """ Count unique_identifier and use secondary_identifier to analyze if any duplicates """

    id_counts = Counter(p[unique_identifier] for p in re_json)
    return [
            (p[unique_identifier], p.get(secondary_identifier))
            for p in re_json
            if id_counts[p[unique_identifier]] > 1
        ]
