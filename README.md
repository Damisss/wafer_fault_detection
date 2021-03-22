Wafer Sensors Fault Detection
==============================
This project attempts to build a classification methodology to predict the quality of wafer sensors based on the given training data. The client provides data in multiple sets of files in batches. Each file contains Wafer names and 590 columns (590 sensors). Firstly, we have performed different sets of validation on the given training files and then follow by inserting all file into sqlite database. After that we have fetch all data from db into a single csv file and then perform EDA follows by some data preprocessing and then run some experimentation using jupyter notebook. 
Finally, we have written the whole in a manner that can be easily deployed.

Project Organization
------------

    ├── LICENSE
    ├── .circleci           <- Ccircle ci coonfigurations 
    ├── README.md          <- The top-level README for developers using this project.
    ├── packages
    │   ├── ml_api           <- End point to serve the ml model.
    │   └── wafer_fault_detection           <- Source code for ML project
    │       ├── tests           <- Unit tests
    │       ├── wafer_fault_detection           <- Source code for ML project
    │       │   └── app_logger          <- Write app logs to files
    │       │    └── best_model_finder           <- Models Parameters tuning and  serialization
    │       │     └── data_transformation           <- Transform data to correct formats
    │       │     └── files_from_db           <- Data fetch from db to csv
    │       │     └── logs           <- App dataLog
    │       │     └── models           <- Serialized ML models
    │       │     └── pred_data           <- Prediction test data
    │       │     └── preprocessing           <- Preprocess data and then divided it into │clusters
    │       │     └── raw_files_validation           <- Validate training batch files
    │       │     └── services           <- Database operation and it contains training_db too
    │       │     └── training_batch_files           <- Contains training raw files
    │       │     └── validated_files           <- training raw validated files
    │       │     └── utils           <- ML app config file and helper functions
    │       │     └── data_management           <- Scripts to validated raw files
    │       │     └── model_training           <- Scripts to perform training
    │       │     └── pipeline           <- ML pipeline 
    │       │     └── predict           <- Scripts to perform prediction
    │       │     └── scheam           <- Training raw files schema
    │       │     └── VERSION           <- Project version
    │       ├── tox.ini           <-  tox file with settings for running training and then all unit tests
    │       ├── setup           <- makes ML project pip installable (pip install -e .) so wafer_fault_detection can be imported
    │       ├── MANIFESTS           <- MANIFESTS with setting all icluded and excluded folders and files
    │       ├── requirements           <- The requirements file for reproducing the analysis environment
    