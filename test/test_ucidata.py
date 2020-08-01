import unittest
import sys 
import os 
import pandas as pd

dirname = os.path.dirname
thisdir = dirname(dirname(os.path.abspath(__file__))) + "\\"
sys.path.append(thisdir)

from scripts.ucidata import UC_Irvine_datasets

class CheckingTestCase(unittest.TestCase): # inherit from unittest.TestCase


    def test_create_ucid(self): #test __init__ action
        newucid = UC_Irvine_datasets()
        self.assertIsInstance(newucid.__df__, pd.DataFrame)
    
    def test_list_all_datasets(self):
        newucid = UC_Irvine_datasets()
        self.assertIsNotNone(newucid.list_all_datasets().count("\n"))

    def test_len(self):
        newucid = UC_Irvine_datasets()
        self.assertEqual(len(newucid), 471)
    
    def test_df(self):
        newucid = UC_Irvine_datasets()
        self.assertIsInstance(newucid.to_df(), pd.DataFrame)
    
    def test_smalldf(self):
        newucid = UC_Irvine_datasets()
        newucid.small_datasets_only()
        self.assertLess(len(newucid.to_df().index), 150)

    def test_load_small_dataset_df(self):
        newucid = UC_Irvine_datasets()
        abalone = newucid.load_small_dataset_df('abalone')
        self.assertIsInstance(abalone, pd.DataFrame)

    def test_limit(self):
        newucid = UC_Irvine_datasets()
        newucid.limit("Area", "Computer")
        self.assertEqual(len(newucid.__df__['Area'].value_counts()), 1)
        self.assertIsNone(newucid.limit("notreal", "madeup"))
    
    def test_show_me_dataset(self):
        newucid = UC_Irvine_datasets()
        newucid = newucid.show_me_dataset("abalone")
        self.assertTrue("NumberofWebHits" in newucid)

if __name__ == '__main__':
    unittest.main()