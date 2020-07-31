import unittest
import data_cleaning2
import numpy as np
import pandas as pd

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
        self.assertNotEqual(data_cleaning2.fillna(dataframe)['DataSetCharacteristics'][2], np.nan)

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
        self.assertEqual(len(data_cleaning2.create_characteristics_columns(dataframe).columns), 22)

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
        self.assertEqual(len(data_cleaning2.create_attribute_columns(dataframe).columns), 14)



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
        self.assertEqual(len(data_cleaning2.create_tasks_columns(dataframe).columns), 19)


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
        self.assertIs(type(data_cleaning2.convert_to_datetime(dataframe)['DateDonated'][2]),pd._libs.tslibs.timestamps.Timestamp)


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
        self.assertNotEqual(data_cleaning2.final_na_drop(dataframe)['DataSetCharacteristics'][2], np.nan)

    def test_add_locations (self):

        #setup
        data = {
                'URL': ['http://archive.ics.uci.edu/ml/datasets/Audiology+%28Original%29'],
        	    'NumberofWebHits': [110441],
                'Source': ['Original Owner: Professor Jergen at Baylor College of Medicine Donor: Bruce Porter (porter "@" fall.cs.utexas.EDU)']
                }

        # Create DataFrame 
        dataframe = pd.DataFrame(data)
        
        self.assertEqual(data_cleaning2.add_locations(dataframe)['source_institution_places'][0][0],['University of Texas', 'Austin, TX', 'United States', 'USA'])

    def test_join_dfs (self):

        #setup
        src_df = pd.read_csv('cleanest_data.csv', encoding="latin-1")

        add_loc_df = pd.read_csv('dataset_add_Univ_City.csv', encoding="latin-1")
        add_loc_df = data_cleaning2.add_locations(add_loc_df)



        self.assertIs(type(data_cleaning2.join_dfs(add_loc_df, "source_institution_places",src_df, "NumberofWebHits")['source_institution_places'][0]),list)





if __name__ == '__main__':
    unittest.main()   