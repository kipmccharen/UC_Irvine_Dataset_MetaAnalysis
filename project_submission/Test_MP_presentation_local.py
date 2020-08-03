#michael Pajewski CS 5010 Project Testing
#mtp9k 7/30/2020 

import pandas as pd
import unittest
from MP_presentation_local import *
from os import path
from datetime import datetime


class PojectTestCase(unittest.TestCase): # inherit from unittest.TestCase
    # Unit testing project portion
    
    def test_data_is_imported_correctly(self):
        #testing that the orginial df is the correct size of 472 x 38 
        #checking all data is imported from csv
        self.assertEqual(len(df), 516) 
        self.assertEqual(len(df.columns), 42) 
        
    def test_df_types_correct(self):
        #test that df data types are correct
        self.assertEqual(df['NumberofInstances'].dtype, 'int64')
        self.assertEqual(df['DateDonated'].dtype, 'object')
        self.assertEqual(df['NumberofWebHits'].dtype, 'int64')
    
    def test_df_types_after_Transformation_correct(self):
        #testing that after the sum transformation everything should be integer 
        self.assertEqual(df_intrest['NumberofInstances'].dtype, 'int64')
        self.assertEqual(df_intrest['NumberofWebHits'].dtype, 'int64')
        self.assertEqual(df_intrest['text_data'].dtype, 'int64')
        
        #testing df_year_area trabsformation
        self.assertEqual(df_year_area['NumberofInstances'].dtype, 'int64')
        self.assertEqual(df_year_area['NumberofWebHits'].dtype, 'int64')
        self.assertEqual(df_year_area['text_data'].dtype, 'int64')
        
        # testing the df_year_avg_instance df transformation
        self.assertEqual(df_year_avg_instance['NumberofInstances'].dtype, 'float64')
        self.assertEqual(df_year_avg_instance['NumberofWebHits'].dtype, 'float64')
        self.assertEqual(df_year_avg_instance['text_data'].dtype, 'float64')

log_file = 'testing_package.txt'
with open(log_file, "a") as f:
    f.writelines(f"{datetime.now()} {path.realpath(__file__)}")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)

if __name__ == '__main__':
    unittest.main()