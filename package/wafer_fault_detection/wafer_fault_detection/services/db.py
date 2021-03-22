import sqlite3
import os
import pandas as pd
import logging

from wafer_fault_detection.app_logger.logger import AppLogger

_logger = logging.getLogger(__name__)

class DbOperation ():
  def __init__(self, db_name, log_path):
    self.db_name = db_name
    self.log_path = log_path

  def conntect_db(self):
    try:
      conn = sqlite3.connect(self.db_name)
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Database {self.db_name} has been successfully connected.\n'
      AppLogger.log(f, message)
      f.close()

      _logger.info(message)

      return conn

    except Exception as e:
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Something went wrong while connecting database {self.db_name}: {e}\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)
      raise e
  
  def create_table (self, path):
    try:
      conn = self.conntect_db()
      cur = conn.cursor()
      cur.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'wafer'")
      if cur.fetchone()[0] == 1:
        cur.execute('DROP TABLE IF EXISTS wafer')
        with open(path, 'r') as f:
          cur.execute(f.read())
        conn.close() 
        f = open(f'{self.log_path}/db_operation.txt', 'a+')
        message = f'Table wafer has been successfully created.\n'
        AppLogger.log(f, message)
        f.close()
        _logger.info(message)
        return

      with open(path, 'r') as f_sql:
        cur.execute(f_sql.read())
      
      conn.close()
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Table wafer has been successfully created\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)

    except sqlite3.OperationalError as se:
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Something went wrong while creating table vafer: {se}\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)
      raise se

  
  def insert_data_to_db(self, goodDataPath, tableName):
    try:
      conn = self.conntect_db()
      cur = conn.cursor()
      files = [os.path.join(goodDataPath, i) for i in os.listdir(goodDataPath)]

      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      for file in files:
        df = pd.read_csv(file)
        columns = [c.replace('-', '_') for c in df.columns]
        colNames = ','.join([c.replace('Good/Bad', 'Output') for c in columns])
  
        for _, row in df.iterrows():
          
          cur.execute(
            'INSERT INTO {} ({}) VALUES({})'.format(tableName, colNames, ','.join(['?' for s in range(len(list(df.columns)))])),  
            list(row)
            )
          conn.commit()

        message = f'file {file} has been successfully inserted to table.\n'
        AppLogger.log(f, message)
        _logger.info(message)

      f.close()
      conn.close()

    except sqlite3.OperationalError as se:
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Something went wrong while inserting data to table: {se}\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)
      raise se
  
  def from_db_to_file (self, tableName, csvPath):
    try:
      conn = self.conntect_db()
      cur = conn.cursor()
      query = f'SELECT * FROM {tableName}'
      cur.execute(query)
      results = cur.fetchall()
      colNames = [colName[0] for colName in cur.description]
      colNames = [c.replace('_', '-') for c in colNames]
      df = pd.DataFrame(results, columns=colNames)
      df.to_csv(csvPath, index=None, header=True)

      conn.close()
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Data have been successfully fetched\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)

    except sqlite3.OperationalError as se:
      f = open(f'{self.log_path}/db_operation.txt', 'a+')
      message = f'Something went wrong while fetching data from db: {se}\n'
      AppLogger.log(f, message)
      f.close()
      _logger.info(message)
      raise se


