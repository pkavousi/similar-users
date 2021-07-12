import os

import pandas as pd
import psycopg2
from flask_sqlalchemy import SQLAlchemy

from user_similarity_model.config.core import DATASET_DIR, SQL_DIR, config


def load_csv_files(filename):
    """read csv files bases on the filename

    Args:
        filename ([type]): name of the file

    Returns:
        DataFrame: A csv file
    """
    csv_file = pd.read_csv(os.path.join(DATASET_DIR, filename))
    return csv_file


def _create_tables():
    """ create tables schema in the PostgreSQL database"""
    conn = None
    try:
        conn = psycopg2.connect(**config.app_config.database_specs)
        cur = conn.cursor()
        with open(os.path.join(SQL_DIR, "tabels-schema.sql")) as file:
            query = file.read()
        cur.execute(query)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def upload_csv():
    """Upload the csv to tables in the PostgreSQL database using the
    credentials in the config.yml file
    """
    _create_tables()
    specs = config.app_config.database_specs
    engine = None
    engine = SQLAlchemy.create_engine(
        "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=require".format(
            specs["user"],
            specs["password"],
            specs["host"],
            specs["port"],
            specs["dbname"],
        )
    )
    for file in config.app_config.csv_files:
        load_csv_files(file).to_sql(file[0:-4], engine, if_exists="replace")
