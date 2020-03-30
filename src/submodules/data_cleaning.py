import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import json
import datetime

class ETL:
    def __init__(self):
        self.root_dir = os.getcwd()

        parameter_json = self.root_dir + '/config/config.json'
        with open(parameter_json) as json_file:
            self.parameter_config = json.load(json_file)
        self.data_folder = self.parameter_config['input_folder']
        self.county_file_name = self.parameter_config['input_file_name']
        self.url = self.parameter_config['covid_data_url']
        self.output_path = self.parameter_config['output_path']
        self.date_today = str(datetime.datetime.now().date())
        self.output_dataset_file_name = self.parameter_config['output_dataset_file_name']
        self.columns = self.parameter_config['columns']
    #def generate_graph(self):

    def get_latest_data(self):
        latest_covid_data = pd.read_csv(self.url)
        latest_covid_data['countyFIPS'] = latest_covid_data['countyFIPS'].astype(str).str.zfill(5)
        county_file_path = self.root_dir + self.data_folder + self.county_file_name
        county_info = pd.read_csv(county_file_path)
        county_info['countyFIPS'] = county_info['countyFIPS'].astype(str).str.zfill(5)
        df_covid_county = latest_covid_data.join(county_info.set_index('countyFIPS'), on='countyFIPS',
                                                    how='inner')

        df_covid_county = df_covid_county.dropna()
        df_covid_county = df_covid_county.reset_index(drop=True)

        return df_covid_county

    def generate_report(self):

        df_covid_county = self.get_latest_data()
        df_covid_county = df_covid_county[self.columns].copy()
        output_dpath = self.root_dir + self.output_path
        output_fpath = output_dpath + self.output_dataset_file_name + '_' + self.date_today + '.csv'
        os.makedirs(output_dpath, exist_ok=True)
        df_covid_county.to_csv(output_fpath)

