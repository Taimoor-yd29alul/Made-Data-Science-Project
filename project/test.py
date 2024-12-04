import unittest
import os
from pipeline import Pipeline
import pandas as pd
import sqlite3
import shutil

class TestPipeline(unittest.TestCase):


    def print_success_message(self):
        print("Test passed successfully.\n")

    def test_table_Creation(self):
        print("...Testing table creation....\n")

        self.addCleanup(self.print_success_message)

        conn = sqlite3.connect('./data/taim.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name = 'housing_hurricanes';")
        table=cursor.fetchone()
        self.assertIsNotNone(table, "Table housing_hurricanes does not exist in the database")
        conn.close()

    def test_pipeline_execution(self):
        print("\n....Testing pipeline execution....\n")
        pipeline = Pipeline()
        pipeline.extrat_data()
        pipeline.load_data()
        pipeline.clean_hurricane_data()
        pipeline.clean_housing_data()
        pipeline.merge_data()
        pipeline.save_to_sqlite()
        self.addCleanup(self.print_success_message)
        self.assertIsInstance(pipeline.hurricane_df, pd.DataFrame)
        self.assertIsInstance(pipeline.housing_df, pd.DataFrame)
        self.assertTrue(pipeline.hurricane_df.shape[0] > 0)
        self.assertTrue(pipeline.housing_df.shape[0] > 0)

        self.assertTrue(os.path.exists("./data"), "Output directory does not exist.")
        self.assertTrue(os.path.exists("./data/taim.sqlite"), "Output database file was not created.")

    def test_table_data(self):
        print("...Testing table data....\n")
        self.addCleanup(self.print_success_message)

        conn = sqlite3.connect('./data/taim.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM housing_hurricanes;")
        rows = cursor.fetchone()[0]
        self.assertTrue(rows > 0, "Table housing_hurricanes is empty")
        conn.close()



def delete_files():
    if os.path.exists("./.Kaggle"):
        shutil.rmtree("./.Kaggle")
    
    if os.path.exists("./hurricane_data_1851-2023_noaa.csv"):
        os.remove("./hurricane_data_1851-2023_noaa.csv")

    if os.path.exists("./city_market_tracker.tsv000"):
        os.remove("./city_market_tracker.tsv000")


if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPipeline)
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite) 
    delete_files()
