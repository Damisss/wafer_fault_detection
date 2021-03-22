import os

from wafer_fault_detection.services.db import DbOperation
from wafer_fault_detection.raw_files_validation.validation import FileValidation
from wafer_fault_detection.data_transformation.transformation import DataTransformation
from wafer_fault_detection.utils import config, file_operation

_params = file_operation.params_loader(path= os.path.join(config.PACKAGE_ROOT, 'utils/params.yaml'))
class FileValidationDbOperation ():

  def __init__(
    self, 
    batch_files_path,
    validated_filesPath, 
    good_files_path, 
    File_from_db_path, 
    db_path, 
    sql_path= _params['data_preparation']['training_sql_query'], 
    task='training', 
    log_folder_path='wafer_fault_detection/logs',
    schema=_params['data_preparation']['schema_training']
    ):

    self.batch_files_path = batch_files_path
    self.good_files_path = good_files_path
    self.File_from_db_path = File_from_db_path
    self.db_path = db_path
    self.log_folder_path = log_folder_path
    self.sql_path = sql_path
    self.validated_filesPath = validated_filesPath
    self.task = task
    self.schema = schema

  def start(self):
    try:
  
      fileValidation = FileValidation(
        self.batch_files_path,
        self.log_folder_path,
        )
      #grab schema values from schema file
      sampleFileName, lengthOfDateStampInFile, lengthOfTimeStampInFile, numberofColumns, colName =  file_operation.grab_schema_values(schema_path=self.schema)
      regex = file_operation.regex()
      #file name validation
      fileValidation.file_name_validation(regex, lengthOfDateStampInFile, lengthOfTimeStampInFile, self.validated_filesPath)
      #column number validation
      fileValidation.columns_validation(numberofColumns, self.validated_filesPath, self.task)
      #empty column validation
      fileValidation.empty_column_validation(self.validated_filesPath)
      # transform data by replacing empty value to NULL
      DataTransformation.transformation(self.good_files_path)
      # move bad files to archive
      file_operation.move_file_to_archive(base_path=os.path.join(self.validated_filesPath,'bad_data'))

      ## db operation
      db_operation = DbOperation(self.db_path, self.log_folder_path)
      db_operation.create_table(self.sql_path)
      db_operation.insert_data_to_db(self.good_files_path, 'wafer')
      db_operation.from_db_to_file('wafer', self.File_from_db_path)

    except Exception as e:
      raise e