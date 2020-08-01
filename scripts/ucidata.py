import pandas as pd 
import requests
import os 
import plotly.express as px
import scripts.Kip_plotly_viz as kpv
#import Kip_plotly_viz as kpv
import ast
import operator


def df_first_row_to_header(df):
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

class UC_Irvine_datasets():

    def __init__(self):
        dirname = os.path.dirname
        basedir = dirname(dirname(os.path.abspath(__file__)))
        self.__df__ = pd.read_csv(basedir + r"\\data\cleanest_data_KMaugmented.csv")

    def __str__(self): # as str
        rows = len(self.__df__.index)
        avgage = round(self.__df__['DatasetAge'].mean(), 1)
        datapoints = round(self.__df__['DatapointCount'].median(), 1)
        sumdf = str(self.__df__[['multivariate_data', 'time_series_data', 'data_generator_data', 'domain_theory_data', 'image_data', 'relational_data', 'sequential_data', 'spatial_data', 'univariate_data', 'spatio_temporal_data', 'text_data', 'transactional_data', 'categorical_attributes', 'real_attributes', 'integer_attributes', 'no_listed_attributes', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'reccomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task', 'small']].sum())

        output = "count of datasets: ".rjust(25, " ") + f"{rows} \n" \
            + "avg age: ".rjust(25, " ") + f"{avgage} yrs \n" \
            + "median # datapoints: ".rjust(25, " ") + f"{datapoints} \n" \
            + f"\nHere are the number of rows in each category: \n\n{sumdf}"
        return output

    def __len__(self): # as integer
        return len(self.__df__.index)

    def list_all_datasets(self): # as str
        """returns string output of all dataset IDs and Titles """
        listall = self.__df__[['shortname', 'header']]
        listall.columns = ["ID", "Title1"]
        def cleanx(x):
            x = str(x)
            x = f"{x[:50]}..." if len(x) > 50 else x
            x = x.replace(" Data Set", "")
            return x
        listall['Title'] = listall['Title1'].apply(cleanx)
        listall = listall[['ID', 'Title']]
        return str(listall.to_string(index=False))
    
    def to_df(self): # as df
        """returns underlying class dataframe"""
        return self.__df__
    
    def small_datasets_only(self): # as df
        """returns all small datasets from underlying dataframe """
        self.__df__ = self.__df__[self.__df__['small'] == 1]

    def load_small_dataset_df(self, dataset_ID): # as df
        """returns df of "small" returnable  datasets 
        that can be imported as dataframes"""
        df = self.__df__[self.__df__['small'] == 1]

        def find_ok_data(list_of_lists):
            okdatatypes = [".csv", ".data", ".txt"]
            for x in ast.literal_eval(df['data_ext_url']):
                for odt in okdatatypes:
                    if odt in x[0]:
                        return x[0]

        df = df[df['shortname'] == dataset_ID].to_dict('records')[0]
        datasets = find_ok_data(ast.literal_eval(df['data_ext_url']))
        #[x for x in  if ".csv" in x[0] or ".data" in x[0]][0][0]
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases" + df['data_folder'] + datasets
        print(url)
        try:
            textval = requests.get(url).text
        except:
            print("couldnt' do that")
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
            df = df[df['shortname'] == dataset_ID].T
            df = df[(df.T != 0).any()][1:]
            return df.to_string()
        except:
            return "sorry, not a real dataset ID"


# ucid.load_small_dataset_df(self, dataset_ID) | 
    # def load_small_names_text(self, dataset_ID): #as str 
    #     """returns names text of "small" datasets"""
    #     pass

    # def download(self, dataset_ID, save_directory): # as interactive | 
    #     """returns input box prompting response here are the options, 
    #     pick one or all of them, are you sure? OK"""
    #     pass

    def limit(self, field, input): # as obj | 
        """limits self to only datasets with this field type"""
        try:
            sdf = self.__df__
            sdf = sdf[sdf[field] == input]
            self.__df__ = sdf
        except:
            print("sorry that didn't work, please try again")

    def print_distribution(self, field): # as plot | 
        """prints histogram of whatever field which is valid, binned in 20 groupings if continuous"""
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
            
            fig.show()
        else:
            print("field entered must exist and be a string")

    def print_barplot(self, xcol, ycol, colorcol=""): # as plot | 
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

            # add boarders to graph
            fig4.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig4.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig4.show()
        else:
            print("fields entered must exist and be a string")

    # def print_special_plot(self, special_plot_name): # as plot | 
    #     """based on data existing in this object, print relevant plot ['worldmap', 'stackedtasks', 'stackedareatasks', 'webhitsdatasize']"""
    #     plotdf = self.__df__
    #     if special_plot_name == 'stackedtasks':
    #         kpv.viz_stacked_tasks_time(plotdf)
    #     elif special_plot_name == 'stackedareatasks':
    #         kpv.viz_stacked_area_tasks_time(plotdf)
    #     elif special_plot_name == 'webhitsdatasize':
    #         kpv.viz_webhits_data_available(plotdf)
    #     elif special_plot_name == 'worldmap':
    #         kpv.worldmap(plotdf)
    #     else:
    #         print("not a special plot name")


if __name__ == "__main__":
    ucid = UC_Irvine_datasets()
    #ucid.print_distribution("Area")
    #ucid.print_special_plot('stackedtasks')
    #ucid.print_barplot("Area","NumberofInstances")
    #print(len(ucid.small_dataset_df().index))
    abalone = ucid.load_small_dataset_df('parkinsons')
    print(abalone.head())
    print(df_first_row_to_header(abalone).head())