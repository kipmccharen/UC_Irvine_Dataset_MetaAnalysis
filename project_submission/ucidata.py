import pandas as pd 
import requests
import os 
import plotly.express as px
import Kip_plotly_viz as kpv
#import Kip_plotly_viz as kpv
import ast
import operator
import re 
import copy
import plotly.offline as pyo
import numpy as np


def df_first_row_to_header(df):
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

class UC_Irvine_datasets():

    def __init__(self):
        thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\"
        self.__df__ = pd.read_csv(thisdir + r"cleanest_data_augmented.csv", encoding='latin-1')
        self.__df__ = self.__df__.sort_values(by=['header'])

    def __str__(self): # as str
        rows = len(self.__df__.index)
        avgage = round(self.__df__['dataset_age'].mean(), 1)
        datapoints = round(self.__df__['DatapointCount'].median(), 1)
        areasum = str(self.__df__[['Area', 'Index']].groupby('Area').count().T)

        sumdf = str(self.__df__[['multivariate_data', 'time_series_data', 'data_generator_data', 'domain_theory_data', 'image_data', 'relational_data', 'sequential_data', 'spatial_data', 'univariate_data', 'spatio_temporal_data', 'text_data', 'transactional_data', 'categorical_attributes', 'real_attributes', 'integer_attributes', 'no_listed_attributes', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'recomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task', 'small']].sum())

        output = "count of datasets: ".rjust(25, " ") + f"{rows} \n" \
            + "avg age: ".rjust(25, " ") + f"{avgage} yrs \n" \
            + "median # datapoints: ".rjust(25, " ") + f"{datapoints} \n" \
            + f"\n## Dataset content Areas: ##\n\n {areasum}\n\n" \
            + f"\n## Here are the number of rows in each category: ##\n\n{sumdf}"
        return output

    def __len__(self): # as integer
        return len(self.__df__.index)

    def list_all_datasets(self): # as str
        """returns string output of all dataset IDs and Titles """
        listall = self.__df__[['Dataset_ID', 'header']].copy()
        listall.columns = ["ID", "Title1"]
        def cleanx(x):
            x = str(x)
            x = f"{x[:50]}..." if len(x) > 50 else x
            x = x.replace(" Data Set", "")
            return x
        listall['Title'] = listall['Title1'].apply(cleanx)
        listall = listall[['ID', 'Title']]
        return f"{' '*20}there are ##  {len(listall.index)}  ## datasets returned\n\n" \
            + str(listall.to_string(index=False))+"\n\n"
    
    def to_df(self): # as df
        """returns underlying class dataframe"""
        return self.__df__
    
    def copy(self):
        new_copy = UC_Irvine_datasets()
        new_copy.__df__ = self.__df__.copy()
        return new_copy

    def small_datasets_only(self): # as df
        """returns all small datasets from underlying dataframe """
        new_copy = copy.deepcopy(self)
        new_copy.limit("small", 1)
        return new_copy

    def load_small_dataset_df(self, dataset_ID): # as df
        """returns df of "small" returnable  datasets 
        that can be imported as dataframes"""
        df = self.__df__[self.__df__['small'] == 1]

        def find_ok_data(list_of_lists):
            okdatatypes = [".csv", ".data", ".txt"]
            splitme = re.split(r',|\|', df['data_ext_url'])
            for i,x in enumerate(splitme):
                for odt in okdatatypes:
                    if odt in splitme[i]:
                        return splitme[i]

        df = df[df['Dataset_ID'] == dataset_ID]
        df = df.to_dict('records')
        df = df[0]
        datasets = find_ok_data(df['data_ext_url'])
        url1 = "https://archive.ics.uci.edu/ml/machine-learning-databases" + df['data_folder']
        url = url1 + datasets
        print(f"dataset page: {url1}\ndataset URL: {url}\n")
        try:
            textval = requests.get(url).text
        except:
            print("couldn't do that")
            return None
        delimeters = {",":0, ";":0, r"\t":0}
        for d in delimeters.keys():
            delimeters[d] = textval.count(d)
        delimiter = max(delimeters.items(), key=operator.itemgetter(1))[0]
        try:
            new_df = pd.read_csv(url, header=None, delimiter=delimiter)
            return new_df
        except:
            new_df = pd.read_csv(url, delimiter=delimiter)
            return new_df
        print("couldnt' do that")
        return None

    def show_me_dataset(self, dataset_ID):
        df = self.__df__
        try:
            df = df[df['Dataset_ID'] == dataset_ID].T
            df = df[(df.T != 0).any()][1:]
            
            output = str(df)
        except:
            output = "sorry, not a real dataset ID"
        print(output)
        return output

    def limit(self, field, input): # as obj | 
        """limits self to only datasets with this field type"""
        try:
            print(field, input)
            self.__df__ = self.__df__[self.__df__[field] == input]
        except:
            print("sorry that didn't work, please try again")

    def print_distribution(self, field): # as plot | 
        """prints histogram of whatever field which is valid, binned in 20 groupings if continuous"""
        pyo.init_notebook_mode()
        if isinstance(field, str) and field in self.__df__.columns.tolist():
            fig = px.histogram(self.__df__, x=field, title=f"Histogram of {field}" )
            # updating plot layout 
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', 
            yaxis_title="Count",
            title={
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

            # add borders to graph
            fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            
            return fig
        else:
            print("field entered must exist and be a string")

    def print_barplot(self, xcol, ycol, colorcol=""): # as plot | 
        pyo.init_notebook_mode()
        plotdf = self.__df__
        plotdf["dataset_count"] = 1
        collist = plotdf.columns.tolist()
        xtruth = isinstance(xcol, str) and xcol in collist
        ytruth = isinstance(ycol, str) and ycol in collist
        colortruth = isinstance(colorcol, str) and colorcol in collist
        if xtruth and ytruth:
            #args = list(args)
            if colorcol != "" and colortruth:
                fig4 = px.bar(plotdf, x=xcol, y=ycol, color=colorcol, title=f"{xcol} by {ycol}")
            else:
                fig4 = px.bar(plotdf, x=xcol, y=ycol, title=f"{xcol} by {ycol}")

            #update layout
            if colorcol == "header":
                fig4.update(layout_showlegend=False)
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)', 
                title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})

            # add borders to graph
            fig4.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig4.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig4.show()
        else:
            print("fields entered must exist and be a string")

    def sizecomparisonplot(self, colx, coly, colcolor = ""):
        pyo.init_notebook_mode()
        df = self.__df__.copy()
        def maxlistsize(x):
            if x in ('', "|", np.nan):
                return 0
            splitme = re.split(r',|\|', x)
            splitme = [int(num) for num in splitme if num.isnumeric()]
            return max(splitme)
            
        def sumlistsize(x):
            if x in ('', "|", np.nan):
                return 0
            splitme = re.split(r',|\|', x)
            splitme = [int(num) for num in splitme if num.isnumeric()]
            return sum(splitme)

        df['max_size'] = df['data_ext_url'].apply(maxlistsize)
        df['sum_sizes'] = df['data_ext_url'].apply(sumlistsize)
        t_sumsize = int(df['sum_sizes'].sum())
        df['Percent of Summed File Sizes in Bytes'] = df['max_size'].apply(lambda x: x / t_sumsize)
        df['Percent of Summed Row Counts'] = df['NumberofInstances'].apply(lambda x: x / df['NumberofInstances'].sum())
        df['Percent of Summed Datapoint Counts'] = df['DatapointCount'].apply(lambda x: x / df['DatapointCount'].sum())

        df.to_csv("orderthesizes.csv")
        
        if colcolor != "":
            fig = px.scatter(df, x=colx, y=coly, color=colcolor, hover_data=['header'])
        else:
            fig = px.scatter(df, x=colx, y=coly, hover_data=['header'])
        
        if 'Percent' in colx:
            fig.update_layout(xaxis_tickformat = '%')
        if 'Percent' in coly:
            fig.update_layout(yaxis_tickformat = '%')

        fig.show()

if __name__ == "__main__":

    ucid = UC_Irvine_datasets()

    #df = ucid.get_df().copy()

    #ucid.print_distribution("Area")
    #ucid.print_special_plot('stackedtasks')
    #ucid.print_barplot("Area","NumberofInstances")
    #print(len(ucid.small_dataset_df().index))

    #ucid.sizecomparisonplot('max_pct_sumsize', 'inst_pct_sumsize', 'Area')

    # df.sort_values(by='dsizes', ascending=False, axis=1)
    test_load_df = ucid.load_small_dataset_df("abalone")
    print(test_load_df)

    #df.to_csv("orderthesizes.csv")

    # abalone = ucid.load_small_dataset_df('parkinsons')
    # print(abalone.head())
    # print(df_first_row_to_header(abalone).head())