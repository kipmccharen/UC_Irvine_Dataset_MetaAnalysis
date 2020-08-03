import unittest
import pandas as pd
from scrape_ucIrvine_ML_datasets import getparentlist, getchildpages, get_dataset_url
from os import path
from datetime import datetime

class CheckingTestCase(unittest.TestCase): # inherit from unittest.TestCase
    
    def test_getparentlist(self):
        #check to ensure that parent page is correctly scraped
        scrape_df = getparentlist()
        self.assertIsInstance(scrape_df, pd.DataFrame) #returns dataframe
        self.assertGreater(len(scrape_df.index),500) # lots of datasets and growing
        self.assertEqual(len(scrape_df.columns),10) # captures 10 columns of data
    
    def test_getchildpages(self):# returns df
        #check to ensure accurate results from scraping a child page
        childpageurl = "datasets/Wine+Quality"
        df = pd.DataFrame([[childpageurl]], columns=['URL'])
        scrape_child = getchildpages(df)
        scr_dict = scrape_child.to_dict()
        print(scr_dict)
        self.assertIsInstance(scrape_child, pd.DataFrame) #returns dataframe
        self.assertEqual(len(scrape_child.index),1) # lots of datasets and growing
        self.assertEqual(len(scrape_child.columns),20) # captures 20 columns of data
        self.assertEqual(scr_dict['header'][0], 'Wine Quality Data Set')
    
    def test_get_dataset_url(self):
        #check to ensure that correct file size results returning
        data = "../00527/"
        data2 = "../00241/"
        self.assertEqual(get_dataset_url(data), "facebook_large.zip,1M,1737479")
        self.assertEqual(get_dataset_url(data2), "100%20leaves%20plant%20species.zip,35M,36764215")

log_file = 'testing_package.txt'
with open(log_file, "a") as f:
    f.writelines(f"{datetime.now()} {path.realpath(__file__)}")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)

if __name__ == '__main__':
    unittest.main()