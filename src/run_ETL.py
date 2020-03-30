import sys
sys.path.append(".")
from src.submodules.data_cleaning import ETL

etl_job = ETL()
etl_job.generate_report()