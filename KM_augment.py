import pandas as pd 
import numpy as np
import os
from datetime import datetime

def add_univ_city(dfsrc, uniquedf):
    """ Extract University, City, and Country values from "Source"
    column of original UC Irvine dataset by using a lookup list
    developed by hand to solve this dataset problem. """

    def get_Univ_Loc_match(rowvals):
        """ Have to use sub-function to run function on
        each row of a dataframe using apply. """

        # If encounters a number, go ahead and return nothing
        if isinstance(rowvals, float) or isinstance(rowvals, int):
            return ""
        #Inherit the lookup list from parent function
        tester = uniquedf.copy() 
        #Create boolean column to check if each lookup value exists 
        # in the column being checked, ensure all texts are stripped
        # and all text is lowercase to ensure matches work.
        tester['boole'] = tester['LookupVal'].apply(lambda x: x.strip().lower() in rowvals.strip().lower())
        tester = tester[tester['boole'] == True] #return only rows with match
        # Convert matched rows to a list which can be saved in the column
        tester = tester[['University', 'City', 'Country', 'CODE']].values.tolist()
        
        # If nothing results from lookups, return nothing
        if not tester:
            return ""
        else:
            # Otherwise return a unique list of Countries. Multiple
            # Lookups per value means could be multiple hits for 1 match
            tester = [list(x) for x in set(tuple(x) for x in tester)]
            return tester

    dfsrc['source_institution_places'] = dfsrc['Source'].apply(get_Univ_Loc_match)

    return dfsrc

def create_lookup_list(dfsrc):
    """ Original starting place for creating the lookup list.
    At first I was collecting data by hand, which turned into making this. """
    df1 = dfsrc[['University1', 'Location1']]
    df2 = dfsrc[['University2', 'Location2']]
    df3 = dfsrc[['University3', 'Location3']]
    renamecols = ['University', 'Location']

    for i,idf in enumerate([df1, df2, df3]):
        idf.columns = renamecols
        if i != 1:
            df1.append(idf, ignore_index=True, sort=False)
    
    unq = df1.groupby(renamecols).size().reset_index()
    return unq

def add_locations(updatemedf, thisdir):
    """ Add locations data to a dataframe """
    # List of unique identifiers to search in text
    unique_list_fdir = thisdir + r"uniquelist.csv"
    uniquedf = pd.read_csv(unique_list_fdir, encoding="latin-1")

    # Use lookup list to find text and look for institution matches, 
    # once found append unique list of matching institution lookups
    df = add_univ_city(updatemedf, uniquedf)
    # Output this to a file for checking and adding more values as needed
    return df

def join_dfs(cols_source_df, col_to_add, add_to_df, join_on_col):
    """ Join two dataframes together, resulting in 2 columns added. """
    List_cols_to_add = [col_to_add, join_on_col]
    cols_source_df = cols_source_df[List_cols_to_add]
    add_to_df = add_to_df.join(cols_source_df.set_index(join_on_col), on=join_on_col)
    return add_to_df

if __name__ == '__main__':
    start_time = datetime.now()

    # 1. dir path of this folder
    thisdir = os.path.dirname(os.path.abspath(__file__)) + r"\\"

    # 2. src dataset to build on -> dataframe
    src_data = thisdir + r"cleanest_data.csv" #Real dataset
    src_df = pd.read_csv(src_data, encoding="latin-1")

    add_loc_data = thisdir + r"dataset_add_Univ_City.csv" #TESTING DATA ONLY
    add_loc_df = pd.read_csv(add_loc_data, encoding="latin-1")

    # # 3. add lookup-text-search institution / location values to src
    add_loc_df = add_locations(add_loc_df, thisdir)

    # 3.5 then add those looked up values to the real cleaned dataset
    src_df = join_dfs(add_loc_df, "source_institution_places",src_df, "NumberofWebHits")
    src_df['year_donated'] = src_df['DateDonated'].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True).year)
    src_df['DatasetAge'] = src_df['year_donated'].apply(lambda x: 2020-x)
    
    def calc_num_cells(x):
        out = x['NumberofInstances'] * x['NumberofAttributes']
        return out
    src_df['DatapointCount'] = src_df.apply(calc_num_cells, axis=1)

    # # 4. export finished df to file for easy access
    src_df.to_csv(src_data.replace(".csv", "_KMaugmented.csv"), encoding="latin-1", index=False)

    print("--- %s seconds ---" % (datetime.now() - start_time))