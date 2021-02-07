# testing framework
import pytest
# os
import shutil
from pathlib import Path
# mock db
from fastdb import MockPostgres, MockMySQL
# init mock db classes
mock_mysql = MockMySQL()
mock_postgres = MockPostgres()
# start mock dbs in docker
mock_mysql.start()
mock_postgres.start()

@pytest.fixture(scope="package", autouse=True)
def test_data_dir_generation():
    # get current file dir
    base_test_dir = Path(__file__).parent.absolute()
    # join base/current file dir with name of test data dir
    test_dir_generation = base_test_dir.joinpath("generation")
    # create dir if it doesn't exist
    test_dir_generation.mkdir(parents=True, exist_ok=True)
    # yield data dir
    yield test_dir_generation
    # delete data dir after tests finish
    shutil.rmtree(str(test_dir_generation))

@pytest.fixture(scope="package", autouse=True)
def test_data_dir_population_psql():
    # get current file dir
    base_test_dir = Path(__file__).parent.absolute()
    # join base/current file dir with name of test data dir
    test_dir_population = base_test_dir.joinpath("population_psql")
    # create dir if it doesn't exist
    test_dir_population.mkdir(parents=True, exist_ok=True)
    # yield data dir
    yield test_dir_population


@pytest.fixture(scope="package", autouse=True)
def test_data_dir_population_mysql():
    # get current file dir
    base_test_dir = Path(__file__).parent.absolute()
    # join base/current file dir with name of test data dir
    test_dir_population = base_test_dir.joinpath("population_mysql")
    # create dir if it doesn't exist
    test_dir_population.mkdir(parents=True, exist_ok=True)
    # yield data dir
    yield test_dir_population


@pytest.fixture(scope="package", autouse=True)
def test_store_psql():
    # get conn info
    test_store_psql = mock_postgres.info()
    # add engine type
    test_store_psql["engine"] = "pg"
    # yield store
    yield test_store_psql
    # stop after tests finish (basically deleting docker containers)
    mock_postgres.stop()


@pytest.fixture(scope="package", autouse=True)
def test_store_mysql():
    # get conn info
    test_store_mysql = mock_mysql.info()
    # add engine type
    test_store_mysql["engine"] = "mysql"
    # yield store
    yield test_store_mysql
    # stop after tests finish (basically deleting docker containers)
    mock_mysql.stop()
