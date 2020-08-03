import unittest
import pandas as pd
from ucidata import UC_Irvine_datasets
from os import path
from datetime import datetime

class text_ucid(unittest.TestCase): # inherit from unittest.TestCase

    def test_create_ucid(self): #test __init__ action
        #create instance and check that readme value is right
        newucid = UC_Irvine_datasets()
        self.assertIsInstance(newucid, UC_Irvine_datasets)
        self.assertEqual(newucid.readme, """Representation of UC Irvine's Machine Learning Repository Website
available here: http://archive.ics.uci.edu/ml/datasets.php""")
    
    def test_list_all_datasets(self):
        #ensure returned value of list all datasets is more than length
        #ensure when grabbing full new datasets, greater than 500 datasets
        #will grow over time if rescraped
        newucid = UC_Irvine_datasets()
        self.assertGreater(newucid.list_all_datasets().count("\n"), len(newucid))
        self.assertGreaterEqual(newucid.list_all_datasets().count("\n"), 500)

    def test_len(self):
        # ensure size of new instance is greater than 500
        newucid = UC_Irvine_datasets()
        self.assertGreaterEqual(len(newucid), 500)
    
    def test_df(self):
        #check that underlying dataframe is a dataframe
        #check that columns match expectations
        newucid = UC_Irvine_datasets()
        self.assertIsInstance(newucid.to_df(), pd.DataFrame)
        collist = ['Index', 'header', 'NumberofInstances', 'Area', 'NumberofAttributes',
       'DateDonated', 'MissingValues', 'NumberofWebHits', 'URL', 'data_folder',
       'Dataset_ID', 'data_ext_url', 'Source', 'multivariate_data',
       'time_series_data', 'data_generator_data', 'domain_theory_data',
       'image_data', 'relational_data', 'sequential_data', 'spatial_data',
       'univariate_data', 'spatio_temporal_data', 'text_data',
       'transactional_data', 'num_data_characteristics',
       'categorical_attributes', 'real_attributes', 'integer_attributes',
       'no_listed_attributes', 'num_attribute_characteristics',
       'causal_discover_task', 'classification_task', 'regression_task',
       'function_learning_task', 'recomendation_task', 'description_task',
       'relational_learning_task', 'no_given_task', 'clustering_task',
       'num_associated_tasks', 'source_institution_places', 'year_donated',
       'dataset_age', 'DatapointCount', 'sum_file_sizes', 'small']
        self.assertListEqual(list(newucid.__df__.columns), collist)
    
    def test_smalldf(self):
        """check that small df requested is appropriate size
        and there are no rows that are not small"""
        newobj = UC_Irvine_datasets()
        newobj = newobj.small_datasets_only()
        newobj = newobj.__df__
        self.assertEqual(len(newobj[newobj['small']==0].index), 0)
        self.assertLess(len(newobj.index), 150)

    def test_load_small_dataset_df(self):
        """ensure that result of loading a small dataset is real dataframe """
        newucid = UC_Irvine_datasets()
        abalone = newucid.load_small_dataset_df('abalone')
        self.assertIsInstance(abalone, pd.DataFrame)

    def test_limit(self):
        """Ensure that result of limit "query" matches expectations
        Check that nothing results from bad inputs"""
        newucid = UC_Irvine_datasets()
        newucid.limit("Area", "Computer")
        self.assertEqual(len(newucid.__df__['Area'].value_counts()), 1)
        self.assertIsNone(newucid.limit("notreal", "madeup"))
    
    def test_show_me_dataset(self):
        """Test that column name appropriate shows up in result of 
        showing values of a dataset"""
        newucid = UC_Irvine_datasets()
        newucid = newucid.show_me_dataset("abalone")
        self.assertTrue("NumberofWebHits" in newucid)

log_file = 'testing_package.txt'
with open(log_file, "a") as f:
    f.writelines(f"{datetime.now()} {path.realpath(__file__)}")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)

if __name__ == '__main__':
    unittest.main()