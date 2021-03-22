import os
import pathlib
import wafer_fault_detection

PACKAGE_ROOT = pathlib.Path(wafer_fault_detection.__file__).resolve().parent
APP_LOGS = 'wafer_fault_detection/logs'
# TRAINING_BATCH_DIR_PATH = 'wafer_fault_detection/training_batch_files'
# SCHEMA_PATH = 'wafer_fault_detection/schema.json'
# TRAINING_VALIDATED_FILES_PATH = 'wafer_fault_detection/validated_files'
# TRAINING_GOOD_DATA_PATH = os.path.join(TRAINING_VALIDATED_FILES_PATH, 'good_data')
# TRAINING_DB_PATH = 'wafer_fault_detection/services/training_wafer.db'
# TRAINING_DATA_PATH = 'wafer_fault_detection/files_from_db/data.csv'
# PLOTS_PATH = 'wafer_fault_detection/plots'
# FILE_FROM_DB = 'wafer_fault_detection/file_from_db'
# KMEANS_PATH = 'wafer_fault_detection/models/kmeans'
#TRAINING_FILE_FROM_DB = 'training_file_from_db/training_file.csv'

# PREDICTION_BATCH_FILES_PATH = 'wafer_fault_detection/prediction_batch_files'
# PREDICTION_VALIDATED_FILES_PATH = 'wafer_fault_detection/validated_files/prediction'
# PREDICTION_GOOD_DATA_PATH = os.path.join(PREDICTION_VALIDATED_FILES_PATH, 'good_data')
# PREDICTION_DB_PATH = 'wafer_fault_detection/services/training_wafer.db'
# PREDICTION_RESULTS = 'wafer_fault_detection/prediction_results/predictions.csv'
# PREDICTION_LOGS='wafer_fault_detection/prediction_logs'
# PREDICTION_DATA_PATH = 'wafer_fault_detection/files_from_db/prediction/data.csv'


DROP_FEATURES=[
  'Sensor-6',
  'Sensor-14',
  'Sensor-43',
  'Sensor-50',
  'Sensor-53',
  'Sensor-70',
  'Sensor-98',
  'Sensor-142',
  'Sensor-150',
  'Sensor-179',
  'Sensor-180',
  'Sensor-187',
  'Sensor-190',
  'Sensor-191',
  'Sensor-192',
  'Sensor-193',
  'Sensor-194',
  'Sensor-195',
  'Sensor-227',
  'Sensor-230',
  'Sensor-231',
  'Sensor-232',
  'Sensor-233',
  'Sensor-234',
  'Sensor-235',
  'Sensor-236',
  'Sensor-237',
  'Sensor-238',
  'Sensor-241',
  'Sensor-242',
  'Sensor-243',
  'Sensor-244',
  'Sensor-257',
  'Sensor-258',
  'Sensor-259',
  'Sensor-260',
  'Sensor-261',
  'Sensor-262',
  'Sensor-263',
  'Sensor-264',
  'Sensor-265',
  'Sensor-266',
  'Sensor-267',
  'Sensor-277',
  'Sensor-285',
  'Sensor-314',
  'Sensor-315',
  'Sensor-316',
  'Sensor-323',
  'Sensor-326',
  'Sensor-327',
  'Sensor-328',
  'Sensor-329',
  'Sensor-330',
  'Sensor-331',
  'Sensor-365',
  'Sensor-370',
  'Sensor-371',
  'Sensor-372',
  'Sensor-373',
  'Sensor-374',
  'Sensor-375',
  'Sensor-376',
  'Sensor-379',
  'Sensor-380',
  'Sensor-381',
  'Sensor-382',
  'Sensor-395',
  'Sensor-396',
  'Sensor-397',
  'Sensor-398',
  'Sensor-399',
  'Sensor-400',
  'Sensor-401',
  'Sensor-402',
  'Sensor-403',
  'Sensor-404',
  'Sensor-405',
  'Sensor-415',
  'Sensor-423',
  'Sensor-450',
  'Sensor-451',
  'Sensor-452',
  'Sensor-459',
  'Sensor-462',
  'Sensor-463',
  'Sensor-464',
  'Sensor-465',
  'Sensor-466',
  'Sensor-467',
  'Sensor-482',
  'Sensor-499',
  'Sensor-502',
  'Sensor-503',
  'Sensor-504',
  'Sensor-505',
  'Sensor-506',
  'Sensor-507',
  'Sensor-508',
  'Sensor-509',
  'Sensor-510',
  'Sensor-513',
  'Sensor-514',
  'Sensor-515',
  'Sensor-516',
  'Sensor-529',
  'Sensor-530',
  'Sensor-531',
  'Sensor-532',
  'Sensor-533',
  'Sensor-534',
  'Sensor-535',
  'Sensor-536',
  'Sensor-537',
  'Sensor-538',
  'Sensor-539',
  'Wafer'
]




