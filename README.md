# UC Irvine Datasets 

### Making an Object from A Dataset

First we need to import the relevant project files, including the class **UC_Irvine_datasets**.

## class UC_Irvine_datasets()

An instance of the UC_Irvine_datasets() object contains a dataframe of all the datasets. 

Many methods make it easy to peruse, export, and even import the datasets inside the object.


```python
from scripts.ucidata import UC_Irvine_datasets, df_first_row_to_header
from scripts.Kip_plotly_viz import viz_stacked_tasks_time, viz_stacked_area_tasks_time, viz_webhits_data_available, worldmap

# Create an instance of the class, which loads the dataframe of UC Irvine datasets
ucid = UC_Irvine_datasets()
```

## string representation

The string property allows users to understand the current state of the class object.


```python
print(ucid)
```

![1_print_object](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/1_print_object.JPG?raw=true)

## object.list_all_datasets()

Look at what datasets area available with *list_all_datasets()*


```python
ucid.list_all_datasets()
```

![2_list_all_datasets](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/2_list_all_datasets.JPG?raw=true)

## object.limit(fieldname, value_to_match)

If you want to select only a single kind of dataset, limit to a single value with limit().


```python
ucid.limit("Area", "Business")
print(ucid)
ucid.list_all_datasets()
```

![3_limit](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/3_limit.JPG?raw=true)

## object.show_me_dataset(ID)

Wow that's too many datasets all at once. 

Let's just look at one with *show_me_dataset(ID)*


```python
ucid.show_me_dataset("wine-quality")
```

![4_show_me_dataset](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/4_show_me_dataset.JPG?raw=true)

## object.load_small_dataset_df(ID)

There's a flag set on this data set called small = 1. 

In this case that means that our team decided the dataset was sufficiently small to safely import directly as a dataframe.

You can try to import any small dataset as *load_small_dataset_df(ID)*

Note that if there are multiple datasets available, only the first dataset is loaded. 


```python
test_load_df = ucid.load_small_dataset_df("wine-quality")
print(f"There are {len(test_load_df.index)} rows")
print(test_load_df.head())
```

![5_load_small_dataset_df](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/5_load_small_dataset_df.JPG?raw=true)

## df_first_row_to_header(df)

Sometimes the datasets come with headers, and sometimes they don't. 

*df_first_row_to_header(df)* will resolve this issue.


```python
test_load_df = df_first_row_to_header(test_load_df)
print("\n\n### WITH HEADERS CORRECTED ###\n")
print(test_load_df.head())
```

![6_df_first_row_to_header](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/6_df_first_row_to_header.JPG?raw=true)

## object.small_datasets_only()

*object.small_datasets_only()* will return a new object of only "small" datasets.

Let's see what returns from using it.


```python
small_ucid = UC_Irvine_datasets().small_datasets_only()
small_uci = small_ucid.list_all_datasets()
print(small_ucid)
```

![7_small_datasets_only](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/7_small_datasets_only.JPG?raw=true)

The object can also produce simple plots from the dataframe:


```python
ucid.print_distribution("NumberofInstances")
```

![8_Histogram](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/8_Histogram.JPG?raw=true)


```python
ucid.print_barplot("year_donated","NumberofWebHits", colorcol="header")
```

![9_barplot](https://github.com/kipmccharen/UC_Irvine_Dataset_MetaAnalysis/blob/master/readme_images/9_barplot.JPG?raw=true)

