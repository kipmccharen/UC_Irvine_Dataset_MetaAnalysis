import plotly 
import pandas as pd 
import numpy as np
import os
from datetime import datetime
import plotly_express as px
import plotly.graph_objects as go

def add_univ_city(dfsrc, uniquedf):

    def get_Univ_Loc_match(rowvals):
        if isinstance(rowvals, float) or isinstance(rowvals, int):
            return ""
        tester = uniquedf.copy()
        tester['boole'] = tester['LookupVal'].apply(lambda x: x.strip().lower() in rowvals.strip().lower())
        tester = tester[tester['boole'] == True]
        tester = tester[['University', 'Location']].values.tolist()
        
        if not tester:
            return ""
        else:
            tester = [list(x) for x in set(tuple(x) for x in tester)]
            return tester

    dfsrc['source_institution_place'] = dfsrc['Source'].apply(get_Univ_Loc_match)

    return dfsrc

def create_lookup_list(dfsrc):
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
    # List of unique identifiers to search in text
    unique_list_fdir = thisdir + r"uniquelist.csv"
    uniquedf = pd.read_csv(unique_list_fdir, encoding="latin-1")

    # Use lookup list to find text and look for institution matches, 
    # once found append unique list of matching institution lookups
    df = add_univ_city(updatemedf, uniquedf)
    # Output this to a file for checking and adding more values as needed
    return df

def viz_stacked_tasks_time(df, thisdir):
    
    df = df[['donated_year', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'reccomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['donated_year'])

    df = df.groupby(['donated_year']).sum().reset_index()
    df.columns = [x.replace("_", " ").replace(" Task", "").title() for x in list(df.columns.values)]
    # print(df)
    # quit()
    collist = list(df.columns.values)[1:]
    fig = px.bar(df, x='Donated Year', \
        y=collist, \
        title="Dataset Count by ML Research Area by Year Submitted", \
        color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(yaxis_title="Count of Datasets",
        legend_title="ML Task Appropriate to Dataset",
        legend=dict(
            x=0.20,
            y=0.75,
            traceorder="normal"
        ))
    fig.write_html(thisdir + "viz_stacked_tasks_time.html")

def viz_stacked_area_tasks_time(df, thisdir):

    df = df[['donated_year', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'reccomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['donated_year'])
    df = df.groupby(['donated_year']).sum().reset_index()
    df.columns = [x.replace("_", " ").title().replace(" Task", "") for x in list(df.columns.values)]
    collist = list(df.columns.values)[1:]

    df['sumvals'] = df[collist].sum(axis=1).astype(float)

    def convert_to_pct(x):
        for col in collist:
            x[col] = x[col].astype(float)
            x[col] = (x[col] / x['sumvals'])
        return x

    df = df.apply(convert_to_pct, axis=1)
    
    # print(df.head())
    # quit()
    # quit()
    fig2 = px.bar(df, x='Donated Year', \
        y=collist, \
        title="Dataset Count by ML Research Area by Year Submitted", \
        color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(yaxis_title=r"Count of Datasets as Percent of All Datasets",
        legend_title="ML Task Appropriate to Dataset",
        legend=dict(
            x=0.70,
            y=0.17,
            traceorder="normal")
            )
    fig2.update_yaxes(range=[0, 1])
    fig2.layout.yaxis.tickformat = ',.1%' 
    fig2.write_html(thisdir + "viz_stacked_area_tasks_time.html")


def viz_webhits_data_available(base_df, thisdir):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import math

    def calc_num_cells(x):
        out = x['NumberofInstances'] * x['NumberofAttributes']
        return out

    base_df['total_cells'] = base_df.apply(calc_num_cells, axis=1)
    base_df = base_df[['donated_year', 'total_cells', 'NumberofWebHits']]

    base_df = base_df.groupby(['donated_year']).sum().reset_index().sort_values(by=['donated_year'])

    base_df['t_cell_cum'] = base_df['total_cells'].cumsum()
    base_df['t_cell_cum'] = np.log(base_df['t_cell_cum'])

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig3.add_trace(
        go.Scatter(x=base_df['donated_year'], 
            y=base_df['NumberofWebHits'], 
            name="Sum of Web Hits Across Datasets",
            line_shape='spline'),
            secondary_y=False,
    )

    fig3.add_trace(
        go.Scatter(x=base_df['donated_year'], y=base_df['t_cell_cum'], 
            name="Log of Accumulating Count of Available Datapoints",
            line_shape='spline'),
            secondary_y=True
    )
    # Add figure title
    fig3.update_layout(
        title_text="Webhits vs Accumulating Census of Datapoints Available",
        legend=dict(
            x=0.25,
            y=0.80,
            traceorder="normal")
    )

    # Set y-axes titles
    fig3.update_yaxes(title_text="Sum of Web Hits Across Datasets", secondary_y=False)
    fig3.update_yaxes(title_text="Log of Accumulating Count of Available Datapoints", secondary_y=True)

    fig3.write_html(thisdir + "viz_webhits_vs_datapoint_census.html")

    #print(base_df.head())

if __name__ == '__main__':
    start_time = datetime.now()

    # 1. dir path of this folder
    thisdir = os.path.dirname(os.path.abspath(__file__)) + r"\\"

    # 2. src dataset to build on -> dataframe
    src_data = thisdir + r"cleanest_data.csv" #Real dataset
    #src_data = thisdir + r"dataset_add_Univ_City.csv" #TESTING DATA ONLY
    base_df = pd.read_csv(src_data, encoding="latin-1")

    # # 3. add lookup-text-search institution / location values to src
    # base_df = add_locations(base_df, thisdir)

    # # 4. export finished df to file for easy access
    # base_df.to_csv(src_data.replace(".csv", "_KMrevised.csv"), encoding="latin-1")

    viz_stacked_tasks_time(base_df, thisdir)
    viz_stacked_area_tasks_time(base_df, thisdir)
    viz_webhits_data_available(base_df, thisdir)

    print("--- %s seconds ---" % (datetime.now() - start_time))