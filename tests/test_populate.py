# populate db class
from populate import Populate
# db middleware (Postgres + MySQL)
from fs2db.connectors.rdb import RDBMiddleware
# random
import random
# testing
import pytest
# os
import os


@pytest.fixture(scope="module")
def test_populate_obj():
    # init populate
    populate_obj = Populate()
    # return populate object
    return populate_obj

def test_populate_random_string_default(test_populate_obj):
    # generate random string
    rand_str = test_populate_obj.random_string()
    # assert type & length
    assert len(rand_str) == 5
    assert isinstance(rand_str, str)


def test_populate_random_string_parametric(test_populate_obj):
    # define custom length
    custom_len = 10
    # generate random string
    rand_str = test_populate_obj.random_string(length=custom_len)
    # assert type & length
    assert len(rand_str) == custom_len
    assert isinstance(rand_str, str)

def test_populate_random_string_randomness(test_populate_obj):
    # generate list of random strings
    random_strs = [test_populate_obj.random_string() for i in range(50)]
    # assert uniqueness
    assert len(set(random_strs)) == len(random_strs)

def test_populate_random_strings(test_populate_obj):
    # call static method random_strings
    random_strs = test_populate_obj.random_strings()
    # assert uniqueness
    assert len(set(random_strs)) == len(random_strs)

def test_random_table_sizes(test_populate_obj):
    num_tables, max_size = 10, 100
    # call static method random_table_sizes
    tbl_sizes = test_populate_obj.random_table_sizes(
        num_tables=num_tables,
        max_size=max_size
    )
    # assert length of generated 
    assert len(tbl_sizes) == num_tables
    assert all([tbl_size <= max_size for tbl_size in tbl_sizes])

def test_get_generation_info(test_populate_obj):
    num_tables, max_size = 10, 100
    # call static method get_generation_info
    generation_info = test_populate_obj.get_generation_info(
        num_tables=num_tables,
        max_size=max_size
    )
    # asser generation info matches num-tables + max siez
    assert all(len(gen_info[0]) == 5 and gen_info[1] <= max_size for gen_info in generation_info)

def test_generate_files(test_populate_obj, test_data_dir_generation):
    # generation info
    # num files to generate & their sizes
    num_tables, max_size = 10, 100
    # generate files
    test_populate_obj.generate_files(
        num_tables=num_tables,
        max_size=max_size,
        dir_path=str(test_data_dir_generation)
    )
    # get number of files generated
    num_files = len([name for name in os.listdir(test_populate_obj.dir_path)])
    # assert number of files generated = num_tables
    assert num_files == num_tables
    # assert dir_path specified by us is used
    assert test_populate_obj.dir_path == str(test_data_dir_generation)
    

def test_populate_psql(test_populate_obj, test_data_dir_population_psql, test_store_psql):
    # generation info
    # num files to generate & their sizes
    num_tables, max_size = 10, 100
    # populate db from files
    test_populate_obj.populate(
        connection_info=test_store_psql,
        dir_path=str(test_data_dir_population_psql),
        num_tables=num_tables,
        max_size=max_size
    )
    # get names of files
    file_names = [name for name in os.listdir(test_populate_obj.dir_path)]
    # get number of files generated
    num_files = len(file_names)
    # assert number of files generated = num_tables
    assert num_files == num_tables
    # assert dir_path specified by us is used
    assert test_populate_obj.dir_path == str(test_data_dir_population_psql)
    # assert tables exist
    rdb_middleware = RDBMiddleware(connection_info=test_store_psql)
    assert len(rdb_middleware.get_tables()) == num_files
    assert all(rdb_middleware.table_exists(file_name) for file_name in file_names)


def test_populate_mysql(test_populate_obj, test_data_dir_population_mysql, test_store_mysql):
    # generation info
    # num files to generate & their sizes
    num_tables, max_size = 10, 100
    # generate files
    test_populate_obj.populate(
        connection_info=test_store_mysql,
        dir_path=str(test_data_dir_population_mysql),
        num_tables=num_tables,
        max_size=max_size
    )
    # get names of files
    file_names = [name for name in os.listdir(test_populate_obj.dir_path)]
    # get number of files generated
    num_files = len(file_names)
    # assert number of files generated = num_tables
    assert num_files == num_tables
    # assert dir_path specified by us is used
    assert test_populate_obj.dir_path == str(test_data_dir_population_mysql)
    # assert tables exist
    rdb_middleware = RDBMiddleware(connection_info=test_store_mysql)
    assert len(rdb_middleware.get_tables()) == num_files
    assert all(rdb_middleware.table_exists(file_name) for file_name in file_names)