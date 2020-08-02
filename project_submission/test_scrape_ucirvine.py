import unittest
import pandas as pd
from scrape_ucIrvine_ML_datasets import getparentlist, getchildpages, grab_data_file_URL

class CheckingTestCase(unittest.TestCase): # inherit from unittest.TestCase
    
    def test_getparentlist(self):
        scrape_df = getparentlist()
        self.assertIsInstance(scrape_df, pd.DataFrame) #returns dataframe
        self.assertGreater(len(scrape_df.index),500) # lots of datasets and growing
        self.assertEqual(len(scrape_df.columns),10) # captures 10 columns of data
    
    def test_getchildpages(self):# returns df
        childpageurl = "http://archive.ics.uci.edu/ml/datasets/Wine+Quality"
        df = pd.DataFrame([[childpageurl]], columns=['URL'])
        scrape_child = getchildpages(df)
        scr_dict = scrape_child.to_dict()
        self.assertIsInstance(scrape_child, pd.DataFrame) #returns dataframe
        self.assertEqual(len(scrape_child.index),1) # lots of datasets and growing
        self.assertEqual(len(scrape_child.columns),17) # captures 10 columns of data
        self.assertEqual(scr_dict['header'][0], 'Wine Quality Data Set')
    
    def test_grab_data_file_URL(self): # returns df
        

if __name__ == '__main__':
    unittest.main()