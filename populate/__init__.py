# mock data generation
import mock
# file 2 db extraction
import fs2db
# logging config
import logging
# set default logging level
mock.logger.setLevel(logging.WARNING)
# random string generation
import random
import string
# os
import os
# progress
from tqdm import tqdm


class Populate:
    """
        class to generate mock files & populate a
        database with the generated files
    """
    @staticmethod
    def random_string(length=5):
        """
            generate random string 

            params:
                - length: length of string generated
            returns:
                - string
        """
        # get lowercase ascii letters
        letters = string.ascii_lowercase
        # generate string from letters
        return "".join(random.choice(letters) for i in range(length))

    @staticmethod
    def random_strings(size=100):
        """
            generate list of random strings

            params:
                - size: number of random strings to generate
        """
        return [Populate.random_string() for _ in range(size)]

    @staticmethod
    def random_table_sizes(num_tables = 100, max_size=10000):
        """
            generate list of random integers which
            will be used as number of rows in tables

            params:
                - num_tables: number of random
                            numbers / table sizes to generate
                - max_size: maximum number to generate
        """
        return [random.randint(1, max_size) for _ in range(num_tables)]

    @staticmethod
    def get_generation_info(num_tables=100, max_size=10000):
        """
            generate a list of random integers (will be used as the
            number of rows in a given table) and a list of random
            strings (will be used)

            params:
                - num_tables: number of random
                            numbers / table sizes to generate
                - max_size: maximum number to generate
            returns
                - list of tuples (random_tbl_name, num_rows_in_tbl)
        """
        return list(
                    zip(
                        Populate.random_strings(
                            size=num_tables
                        ),
                        Populate.random_table_sizes(
                            num_tables=num_tables,
                            max_size=max_size
                        )
                    )
        )
    
    @staticmethod
    def generate_files(
            num_tables=25,
            max_size=10000,
            dir_path=None,
            data_types=["profile", "job"],
            file_types=["csv", "json", "xls"]
        ):
        """
            generate a file using a random string as a name
            and a random int as the number of rows in tbl
            (uses get_generation_info which returns them as a
            list of tuples)

            params:
                - num_tables: number of random
                            numbers / table sizes to generate
                - max_size: maximum number to generate
                - dir_path: local directory to store generated files
                - data_types: types of data to generate
                - file_types: file extensions to generate
        """
        # get generation info
        gen_info = Populate.get_generation_info(num_tables=num_tables, max_size=max_size)
        # iterate through each file & table size
        for file_name, data_size in tqdm(gen_info):
            # init file generator
            file_generator = mock.FileGenerator(
                data_size=data_size,
                file_types=file_types,
                data_types=[random.choice(data_types)]
            )
            # if dir path not specified
            if dir_path is None:
                # create dir path in the same directory as this file
                dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
                # if data dir doesn't exist
                if not os.path.exists(dir_path):
                    # create dir
                    os.mkdir(dir_path)
            else:
                # if user specified dir doesn't exist
                if not os.path.exists(dir_path):
                    # create dir
                    os.mkdir(dir_path)
            # store data to dir
            file_generator.store(data_dir=dir_path, file_name=file_name)
        # return dir where data was stored
        return dir_path
    
    @staticmethod
    def store(connection_info, dir_path):
        """
            store generated files to database

            params:
                - connection_info: database connection info dict
                - dir_path: directory containing files to be stored in db
        """
        # init extractor
        extractor = fs2db.FileExtractor(connection_info=connection_info)
        # run extraction
        extractor.dir2db(dir_path=dir_path)
    
    @staticmethod
    def populate(
            connection_info,
            dir_path=None,
            num_tables=50,
            max_size=10000,
            data_types=["profile", "job"],
            file_types=["csv", "json", "xls"]
        ):
        """
            populate a given database with random tables

            params:
                - connection_info: database connection info dict
                - dir_path: directory containing files to be stored in db
                - num_tables: number of random
                            numbers / table sizes to generate
                - max_size: maximum number to generate
                - dir_path: local directory to store generated files
                - data_types: types of data to generate
                - file_types: file extensions to generate
        """
        # generate files to populate db
        dir_path = Populate.generate_files(
            num_tables=num_tables,
            max_size=max_size,
            dir_path=dir_path,
            data_types=data_types,
            file_types=file_types
        )
        # insert generated files into db
        Populate.store(
            connection_info=connection_info,
            dir_path=dir_path
        )
        # return dir of generated files
        return dir_path