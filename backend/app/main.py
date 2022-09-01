from flask import Flask
from sqlalchemy.engine import URL, create_engine
import pandas as pd
import pyodbc

app = Flask(__name__)

app.config.from_object(__name__)

server = 'localhost'
database = 'AIFMRM_ERS'
username = 'sa'
password = 'pohtoj-Jewtix-vudko9'

cnxn_str = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cnxn_url = URL.create("mssql+pyodbc", query={"odbc_connect": cnxn_str})

engine = create_engine(cnxn_url)
class Database_df:
    def __init__(self, tables_df=pd.DataFrame(), table_name_list=[], select_template='', frames_dict={}):
        self.tables_df = tables_df
        self.table_name_list = table_name_list
        self.select_template = select_template
        self.frames_dict = frames_dict

    def create_dataframes(self, engine):
        # initialise connection via context manager           
        with engine.connect() as cnxn:
            self.tables_df = pd.read_sql('SELECT [name] AS [table_name] FROM sys.tables', cnxn)
            self.table_name_list = self.tables_df.table_name
            self.select_template = 'SELECT * FROM {table_name}'
            # Dictionary of table names and their respective SQL queries
            self.frames_dict = {}
            for tname in self.table_name_list:
                query = self.select_template.format(table_name = tname)
                self.frames_dict[tname] = pd.read_sql(query, cnxn)

            cnxn.close()
            
            return self.frames_dict

frames_dict = Database_df().create_dataframes(engine)

from app import routes, indices , sectors, shares, weights_and_ics