import unittest
import data_cleaning
import numpy as np
import pandas as pd
from os import path
from datetime import datetime


class DataCleaningTestCase(unittest.TestCase): # inherit from unittest.TestCase
    # Unit testing Checking in account_class.py
    
    def test_is_drop_na_removing_na_values(self):
        
        # Set up
        data = {
                'header':['head1', 'head2', 'head3'], 
                'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
                'NumberofInstances': [2.0, np.nan, 1800],
                 'Area': ['Real', np.nan, 'Computer'],
                 'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
                 'NumberofAttributes': [18.0, np.nan, 2],
                 'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
                 'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
                 'MissingValues': ['No', np.nan, 'yes'], 
                 'NumberofWebHits': [11111, np.nan, 11]
                 } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        # is the fee correct?
        self.assertNotEqual(data_cleaning.fillna(dataframe)['DataSetCharacteristics'][2], np.nan)

    def test_create_characteristics_columns(self):

        # Set up
        data = {
                'header':['head1', 'head2', 'head3'], 
                'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
                'NumberofInstances': [2.0, np.nan, 1800],
                 'Area': ['Real', np.nan, 'Computer'],
                 'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
                 'NumberofAttributes': [18.0, np.nan, 2],
                 'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
                 'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
                 'MissingValues': ['No', np.nan, 'yes'], 
                 'NumberofWebHits': [11111, np.nan, 11]
                 } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        self.assertEqual(len(data_cleaning.create_characteristics_columns(dataframe).columns), 22)

    def test_create_attribute_columns(self):

        #setup
        data = {
        'header':['head1', 'head2', 'head3'], 
        'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
        'NumberofInstances': [2.0, np.nan, 1800],
        'Area': ['Real', np.nan, 'Computer'],
        'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
        'NumberofAttributes': [18.0, np.nan, 2],
        'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
        'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
        'MissingValues': ['No', np.nan, 'yes'], 
        'NumberofWebHits': [11111, np.nan, 11]
        } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        self.assertEqual(len(data_cleaning.create_attribute_columns(dataframe).columns), 14)



    def test_create_tasks_columns (self):
        
        #setup
        data = {
        'header':['head1', 'head2', 'head3'], 
        'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
        'NumberofInstances': [2.0, np.nan, 1800],
        'Area': ['Real', np.nan, 'Computer'],
        'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
        'NumberofAttributes': [18.0, np.nan, 2],
        'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
        'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
        'MissingValues': ['No', np.nan, 'yes'], 
        'NumberofWebHits': [11111, np.nan, 11]
        } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        self.assertEqual(len(data_cleaning.create_tasks_columns(dataframe).columns), 19)


    def test_convert_to_datetime (self):
    
        #setup
        data = {
        'header':['head1', 'head2', 'head3'], 
        'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
        'NumberofInstances': [2.0, np.nan, 1800],
        'Area': ['Real', np.nan, 'Computer'],
        'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
        'NumberofAttributes': [18.0, np.nan, 2],
        'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
        'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
        'MissingValues': ['No', np.nan, 'yes'], 
        'NumberofWebHits': [11111, np.nan, 11]
        } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        self.assertIs(type(data_cleaning.convert_to_datetime(dataframe)['DateDonated'][2]),pd._libs.tslibs.timestamps.Timestamp)


    def test_final_na_drop (self):
                
        # Set up
        data = {
                'header':['head1', 'head2', 'head3'], 
                'DataSetCharacteristics':['Multivariate, Time-Series', np.nan, 'Multivariate, Time-Series'],
                'NumberofInstances': [2.0, np.nan, 1800],
                 'Area': ['Real', np.nan, 'Computer'],
                 'AttributeCharacteristics': ['Integer, real', np.nan, 'Categorical, Integer'],
                 'NumberofAttributes': [18.0, np.nan, 2],
                 'DateDonated': ['7/29/2015',np.nan, '8/29/2014'],
                 'AssociatedTasks': ['Classification, Refression', np.nan, 'Classification, Clustering'],
                 'MissingValues': ['No', np.nan, 'yes'], 
                 'NumberofWebHits': [11111, np.nan, 11]
                 } 
  
        # Create DataFrame 
        dataframe = pd.DataFrame(data) 
        
        # Test
        # is the fee correct?
        self.assertNotEqual(data_cleaning.final_na_drop(dataframe)['DataSetCharacteristics'][2], np.nan)

    def test_add_locations (self):
        #Ensure that the proper lookup values are returned

        #setup
        data = """benedek.rozemberczki '@' gmail.com The University of Edinburgh"""
        
        self.assertEqual(data_cleaning.get_Univ_Loc_match(data), "University of Edinburgh;Edinburgh;United Kingdom;GBR")

    def test_find_small(self):
        #Ensure that only small datasets return 1 from function
        data1 = "UJIIndoorLoc-Mag-forUCI.zip,1M,1455359"
        data2 = "Index,105B,105|bezdekIris.data,4K,4551|iris.data,4K,4551|iris.names,2K,2998"
        self.assertFalse(data_cleaning.find_small(data1))
        self.assertTrue(data_cleaning.find_small(data2))

    def test_sum_file_size(self):
        #Ensure that the correct summed file size is returned
        data1 = "UJIIndoorLoc-Mag-forUCI.zip,1M,1455359"
        data2 = "Index,105B,105|bezdekIris.data,4K,4551|iris.data,4K,4551|iris.names,2K,2998"
        self.assertEqual(data_cleaning.sum_file_size(data1),1455359)
        self.assertTrue(data_cleaning.sum_file_size(data2),105+4551+4551+2998)

log_file = 'testing_package.txt'
with open(log_file, "a") as f:
    f.writelines(f"{datetime.now()} {path.realpath(__file__)}")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)

if __name__ == '__main__':
    unittest.main()