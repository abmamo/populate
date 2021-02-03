# populate ![build](https://github.com/abmamo/populate/workflows/build/badge.svg?branch=main)
generate + load data into a relational database. currently supports populating Postgres & MySQL
with random tables of varying sizes + data types

## quickstart
create virtualenv
```
    python3 -m venv env && source env/bin/activate && pip3 install --upgrade pip
```
install populate
```
    pip3 install populate @ https://github.com/abmamo/populate/archive/v0.0.1.tar.gz
```
populate database
```
    # mock data gen + insert into db
    # import populate
    from populate import Populate
    # db conn info (replace values with values for db being populated)
    connection_info = {'host': <db host>, 'port': <db port>, 'user': <db user>', 'password': <db pass>', 'database': <db_name>}
    connection_info["engine"] = "pg"
    # populate table with mock data
    Populate.populate(connection_info=connection_info)
```