import os
os.makedirs('.kaggle', exist_ok=True)
os.environ['KAGGLE_CONFIG_DIR'] = os.path.join(os.getcwd(), '.kaggle')
import gdown
import pandas as pd
import sqlite3

class Pipeline:
    def __init__(self):
        print("Initializing Pipeline")
        self.Download_Kaggle_Token()
        # Set the correct environment variable
        from kaggle.api.kaggle_api_extended import KaggleApi as KaggleApi
        self.api = KaggleApi()
        self.api.authenticate()

    def extrat_data(self):
        print("Extracting data from source")
        if not os.path.exists('./hurricane_data_1851-2023_noaa.csv'):
            self.api.dataset_download_files("sandraroko/u-s-hurricanes-and-landfalls-1851-2023", path='./', unzip=True)
        else:
            print("Hurricane Data Already Exists")
        if not os.path.exists('./city_market_tracker.tsv000'):
            self.api.dataset_download_files("vincentvaseghi/us-cities-housing-market-data", path='./', unzip=True)
        else:
            print("Housing Data Already Exists")


        print("Data Extracted")


    def load_data(self):
        print("Loading data")
        # Try to load the data and handle possible errors
        try:
            self.hurricane_df = pd.read_csv('./hurricane_data_1851-2023_noaa.csv')
            self.housing_df = pd.read_csv('./city_market_tracker.tsv000', sep='\t')
            print("Data Loaded")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def clean_hurricane_data(self):
        print("Cleaning hurricane data...")
        self.hurricane_df = self.hurricane_df.drop_duplicates()
        self.hurricane_df['Date'] = pd.to_datetime(self.hurricane_df['Date'], errors='coerce')

        # Split states into individual rows
        self.hurricane_df = self.hurricane_df.assign(State=self.hurricane_df['States Affected Names'].str.split(', ')).explode('State')

        # Extract Year and Month
        self.hurricane_df['Year'] = self.hurricane_df['Date'].dt.year
        self.hurricane_df['Month'] = self.hurricane_df['Date'].dt.month

        # Select relevant columns
        self.hurricane_df = self.hurricane_df[['Year', 'Month', 'State', 'SS  HWS', 'Max Winds (kt)','Storm Names']]
        #print(self.hurricane_df.head())
        print("Hurricane data cleaned")

    def clean_housing_data(self):
        print("Cleaning housing data...")
        self.housing_df =self.housing_df.drop_duplicates()
        self.housing_df['period_begin'] = pd.to_datetime(self.housing_df['period_begin'], errors='coerce')

        # Extract Year and Month
        self.housing_df['Year'] = self.housing_df['period_begin'].dt.year
        self.housing_df['Month'] = self.housing_df['period_begin'].dt.month

        # Select relevant columns
        self.housing_df = self.housing_df[['Year', 'Month', 'state', 'city', 'median_sale_price', 'inventory']]
        #print(self.housing_df.head())
        print("Housing data cleaned")

    def merge_data(self):
        print("Merging datasets...")
        # Handling potential mismatch in state names by standardizing the state names
        self.hurricane_df['State'] = self.hurricane_df['State'].str.strip()
        self.housing_df['state'] = self.housing_df['state'].str.strip()

        # Left join to retain all housing data and enrich with hurricanes data
        self.merged = pd.merge(
            self.housing_df, self.hurricane_df,
            left_on=['Year', 'Month', 'state'],
            right_on=['Year', 'Month', 'State'],
            how='left'
        )
        self.merged = self.merged.drop(columns=['State'])  # Drop duplicate column
        print("Datasets merged")
        #print(self.merged.head())

    def Download_Kaggle_Token(self):
        print("Downloading Kaggle Token")
        file_path = 'https://drive.google.com/uc?id=1bj9eIGfxXw4X4loym_BNC2cgGJwdHPzm'
        output_path = '.kaggle/kaggle.json'  # Save the token file in the `.kaggle` directory
        if not os.path.exists(output_path):
            gdown.download(file_path, output_path, quiet=False)
            print("Kaggle Token Downloaded")
        else:
            print("Kaggle Token Already Exists")

    def save_to_sqlite(self):
        current_dir = os.getcwd()
        data_dir = os.path.join(current_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        db_path = os.path.join(data_dir, 'taim.sqlite')
        print(f"Saving data to SQLite database at {db_path}...")
        try:
            conn = sqlite3.connect(db_path)
            self.merged.to_sql("housing_hurricanes", conn, if_exists="replace", index=False)
            conn.close()
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data to SQLite: {e}")
            raise


def main():
    p = Pipeline()
    p.extrat_data()
    p.load_data()
    p.clean_hurricane_data()
    p.clean_housing_data()
    p.merge_data()
    p.save_to_sqlite()


if __name__ == "__main__":
    main()
