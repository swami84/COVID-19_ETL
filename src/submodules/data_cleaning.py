import pandas as pd
import os
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
        self.confirmed_url = self.parameter_config['confirmed_case_url']
        self.death_url = self.parameter_config['death_case_url']
        self.output_path = self.parameter_config['output_path']
        self.date_today = str(datetime.datetime.now().date())
        self.output_dataset_file_name = self.parameter_config['output_dataset_file_name']
        self.columns = self.parameter_config['columns']

        self.rename_col_name = self.parameter_config['Rename_Columns']


    def get_latest_data(self,url):
        latest_covid_data = pd.read_csv(url)

        latest_covid_data['countyFIPS'] = latest_covid_data['countyFIPS'].astype(str).str.zfill(5)
        county_file_path = self.root_dir + self.data_folder + self.county_file_name
        county_info = pd.read_csv(county_file_path)
        county_info['countyFIPS'] = county_info['countyFIPS'].astype(str).str.zfill(5)
        df_covid_county = latest_covid_data.join(county_info.set_index('countyFIPS'), on='countyFIPS',
                                                    how='inner')

        df_covid_county = df_covid_county.dropna()
        df_covid_county = df_covid_county.reset_index(drop=True)

        return df_covid_county

    def filter_data(self,df,text):

        date_cols = []
        for col in df.columns:
            if '20' in col:
                date_cols.append(col)
        columns = self.parameter_config['columns']

        columns.insert(3,date_cols[-1])

        df_filtered = df[columns].copy()
        columns.pop(3)
        df_filtered[text + ' Cases Per 1M Population'] = df_filtered[date_cols[-1]]*1e6/df_filtered['County_Population']

        self.rename_col_name[date_cols[-1]] = 'Latest ' + text + ' Cases'
        df_filtered = df_filtered.rename(columns= self.rename_col_name)

        return df_filtered


    def generate_report(self):
        active_df = self.get_latest_data(self.confirmed_url)
        death_df = self.get_latest_data(self.death_url)
        active_df_fil = self.filter_data(active_df, 'Active')
        death_df_fil = self.filter_data(death_df, 'Death')
        output_df = active_df_fil.join(death_df_fil.set_index('countyFIPS'), on = 'countyFIPS', how = 'inner', rsuffix='_right')
        for col in output_df.columns:
            if 'right' in col:
                output_df = output_df.drop(columns=[col])
        cols = output_df.columns.to_list()
        cols.insert(4, cols[-2])
        cols.pop(-2)
        output_df = output_df[cols].copy()
        output_dpath = self.root_dir + self.output_path
        output_fpath = output_dpath + self.output_dataset_file_name + '_' + self.date_today + '.csv'
        os.makedirs(output_dpath, exist_ok=True)
        output_df.to_csv(output_fpath)

