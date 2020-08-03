#imports
import pandas as pd 
import numpy as np
import os
from datetime import datetime
import re

def fillna(df):
    df['MissingValues'] = df['MissingValues'].fillna('No')
    df['NumberofInstances'] = df['NumberofInstances'].fillna(0)
    df['NumberofAttributes'] = df['NumberofAttributes'].fillna(0)
    df['AttributeCharacteristics'] = df['AttributeCharacteristics'].fillna('Other')
    df['AssociatedTasks'] = df['AssociatedTasks'].fillna('Other')
    df['Area'] = df['Area'].fillna('Other')
    return df

def create_characteristics_columns(df): 
    # force data set characteristics column to string data type
    df['DataSetCharacteristics'] = df['DataSetCharacteristics'].astype(str)

    # create a column for each data characteristic value is 1 if true, 0 if false
    df['multivariate_data'] = df['DataSetCharacteristics'].str.contains('Multivariate').astype(int)
    df['time_series_data'] = df['DataSetCharacteristics'].str.contains('Time-Series').astype(int)
    df['data_generator_data'] = df['DataSetCharacteristics'].str.contains('Data-Generator').astype(int)
    df['domain_theory_data'] = df['DataSetCharacteristics'].str.contains('Domain-Theory').astype(int)
    df['image_data'] = df['DataSetCharacteristics'].str.contains('image').astype(int)
    df['relational_data'] = df['DataSetCharacteristics'].str.contains('Relational').astype(int)
    df['sequential_data'] = df['DataSetCharacteristics'].str.contains('Sequential').astype(int)
    df['spatial_data'] = df['DataSetCharacteristics'].str.contains('Spatial').astype(int)
    df['univariate_data'] = df['DataSetCharacteristics'].str.contains('Univariate').astype(int)
    df['spatio_temporal_data'] = df['DataSetCharacteristics'].str.contains('Spatio-temporal').astype(int)
    df['text_data'] = df['DataSetCharacteristics'].str.contains('Text').astype(int)
    df['transactional_data'] = df['DataSetCharacteristics'].str.contains('Transactional').astype(int)

    #delete original data set characteristics column
    del df['DataSetCharacteristics']

    #define function to add values from all data characteristic columns in each row

    num_characteristics = lambda row: (row.multivariate_data + row.time_series_data + row.data_generator_data +
                                    row.domain_theory_data + row.image_data + row.relational_data + row.sequential_data +
                                    row.spatial_data + row.univariate_data + row.spatio_temporal_data)

    #create column to count number of data characteristics and apply lambda
    df['num_data_characteristics'] = df.apply(num_characteristics, axis=1)
    return df

def create_attribute_columns(df): 
    # force attribute characteristics column to string data type
    df['AttributeCharacteristics'] = df['AttributeCharacteristics'].astype(str)

    #ceate a column for each attribute characterstic, value is 1 if true, 0 if false
    df['AttributeCharacteristics'] = df['AttributeCharacteristics'].astype(str)
    df['categorical_attributes'] = df['AttributeCharacteristics'].str.contains('Categorical').astype(int)
    df['real_attributes'] = df['AttributeCharacteristics'].str.contains('Real').astype(int)
    df['integer_attributes'] = df['AttributeCharacteristics'].str.contains('Integer').astype(int)
    df['integer_attributes'] = df['AttributeCharacteristics'].str.contains('Integer').astype(int)
    df['no_listed_attributes'] = df['AttributeCharacteristics'].str.contains('Other').astype(int)

    #delete original attribute characteristics column
    del df['AttributeCharacteristics']

    #define function to add values from all attribute characteristic columns in each row
    num_attribute_types = lambda row: (row.categorical_attributes + row.real_attributes + row.integer_attributes +
                                        row.no_listed_attributes)

    #create column to count number of attribute characteristics and apply lambda
    df['num_attribute_characteristics'] = df.apply(num_attribute_types, axis=1)
    return df

def create_tasks_columns(df): 
    # force associated task column to string data type
    df['AssociatedTasks'] = df['AssociatedTasks'].astype(str)

    #ceate a column for each associated task, value is 1 if true, 0 if false
    df['causal_discover_task'] = df['AssociatedTasks'].str.contains('Causal-Discovery').astype(int)
    df['classification_task'] = df['AssociatedTasks'].str.contains('Classification').astype(int)
    df['regression_task'] = df['AssociatedTasks'].str.contains('Regression').astype(int)
    df['function_learning_task'] = df['AssociatedTasks'].str.contains('Function-Learning').astype(int)
    df['recomendation_task'] = df['AssociatedTasks'].str.contains('Recommendation' or
                                                                                        'Recommender-Systems').astype(int)
    df['description_task'] = df['AssociatedTasks'].str.contains('Description').astype(int)
    df['relational_learning_task'] = df['AssociatedTasks'].str.contains('Relational-Learning').astype(int)
    df['no_given_task'] = df['AssociatedTasks'].str.contains('Other').astype(int)
    df['clustering_task'] = df['AssociatedTasks'].str.contains('Clustering').astype(int)

    #delete original associated task column
    del df['AssociatedTasks']

    #define function to add values from all associated task columns in each row
    num_associated_tasks = lambda row: (row.causal_discover_task + row.classification_task + row.regression_task +
                                        row.function_learning_task + row.recomendation_task + 
                                        row.description_task +  row.relational_learning_task)

    #create column to count number of associated tasks and apply lambda
    df['num_associated_tasks'] = df.apply(num_associated_tasks, axis=1)
    return df

def final_na_drop(df):
    df1 = df.dropna()
    return df1

def get_Univ_Loc_match(rowvals):
    """ Extract University, City, and Country values from "Source"
    column of original UC Irvine dataset by using a lookup list
    developed by hand to solve this dataset problem. """

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
        tester = "|".join([";".join(x) for x in set(tuple(x) for x in tester)])
        return tester

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

if __name__ == '__main__':
    start_time = datetime.now()
    
    ######################
    #PHASE 1 CLEANING WORK
    ######################

    #Load data
    pre_cleaned_df = pd.read_csv('UC_Irvine_ML_datasets.csv')
    #select only relevant columns
    pre_cleaned_df = pre_cleaned_df[[
                                    'header', 'DataSetCharacteristics', 'NumberofInstances', 'Area',
                                    'AttributeCharacteristics', 'NumberofAttributes', 'DateDonated',
                                    'AssociatedTasks','MissingValues', 'NumberofWebHits', 
                                    'URL', 'data_folder', 'Dataset_ID', 'data_ext_url', 'Source'
                                    ]]

    #fill NA values to ensure not empty
    cleandata = fillna(pre_cleaned_df)

    #de-normalize categorical columns into indicator dummy variables
    cleandata = create_characteristics_columns(cleandata)
    cleandata = create_attribute_columns(cleandata)
    cleandata = create_tasks_columns(cleandata)

    #convert 'DateDonated' to real date value
    cleandata['DateDonated'].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True))

    #drop all records with NA values
    cleanest_data = final_na_drop(cleandata)

    #save file to csv "cleanest_data"
    cleanest_data.to_csv('cleanest_data.csv')

    ####################################################################
    
    ######################
    #PHASE 2 CLEANING WORK
    ######################
    
    #re-import the file 
    src_df = pd.read_csv('cleanest_data.csv', encoding="latin-1")

    # List of unique identifiers to search in text - lookup list
    uniquedf = pd.read_csv('uniquelist.csv', encoding="latin-1")

    # Use lookup list to find text and look for institution matches, 
    # once found append unique list of matching institution lookups
    src_df['source_institution_places'] = src_df['Source'].apply(get_Univ_Loc_match)
    
    #add year from DateDonated column
    src_df['year_donated'] = src_df['DateDonated'].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True).year)
    #additionally add the age of the dataset, subtracted from 2020
    src_df['dataset_age'] = src_df['year_donated'].apply(lambda x: 2020-x)
    
    #add column multiply rows*columns to get number of cells in dataset
    def calc_num_cells(x):
        out = x['NumberofInstances'] * x['NumberofAttributes']
        return out
    src_df['DatapointCount'] = src_df.apply(calc_num_cells, axis=1)

    #function to sum the size of all files in a dataset as sum_file_sizes
    def sum_file_size(x):
        if x in ('', "|", np.nan):
            return 0
        splitme = re.split(r',|\|', x)
        splitme = [num for num in splitme if num.isdigit()]
        return sum([int(num) for num in splitme]
    src_df['sum_file_sizes'] = src_df['data_ext_url'].apply(sum_file_size)

    # function to define which datasets are "small
    def find_small(x):
        if x == "|": #if there's no data, return 0 for no
            return 0

        x = x.split("|") #split the value
        # find the max value splitting by comma
        maxval = max([int(i.split(",")[2]) for i in x])
        # filter to get full dataset info where max size
        newval = list(filter(lambda x: x.split(",")[2] == str(maxval), x))
        # return split list version of data file
        newval = newval[0].split(",")

        # if right kind of file (csv, data, txt) and less than ~1.1MB
        # mark as small, otherwise no
        if (".csv" in newval[0] or ".data" in newval[0] or \
                ".txt" in newval[0]) and int(newval[2]) < 1100000:
            return 1
        else:
            return 0
    src_df['small'] = src_df["data_ext_url"].apply(find_small)

    # rename index to use for later
    src_df = src_df.rename(columns={"Unnamed: 0": 'Index'})

    #export finished df to new augmented file
    src_df.to_csv('cleanest_data_augmented.csv', encoding="latin-1", index=False)

    print("--- %s seconds ---" % (datetime.now() - start_time))

