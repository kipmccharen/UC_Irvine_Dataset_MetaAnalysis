import pandas as pd 
import numpy as np
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import ast
from collections import Counter

country_codes = pd.read_csv('all_country_codes.csv')

def viz_stacked_tasks_time(df, thisdir):
    
    df = df[['YearAdded', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'recomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['YearAdded'])

    df = df.groupby(['YearAdded']).sum().reset_index()
    df.columns = [x.replace("_", " ").replace(" Task", "").title() for x in list(df.columns.values)]
    # print(df)
    # quit()
    collist = list(df.columns.values)[1:]
    fig = px.bar(df, x='Yearadded', \
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

    df = df[['YearAdded', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'recomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['YearAdded'])
    df = df.groupby(['YearAdded']).sum().reset_index()
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
    fig2 = px.bar(df, x='Yearadded', \
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

    base_df = base_df[['DatasetAge', 'DatapointCount', 'NumberofWebHits']]

    base_df = base_df.groupby(['DatasetAge']).sum().reset_index().sort_values(by=['DatasetAge'])

    base_df['LogWebhits'] = base_df['NumberofWebHits'].apply(lambda x: np.log(x) +1)
    base_df['LogDatapointsAdded'] = base_df['DatapointCount'].apply(lambda x: np.log(x) +1)

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig3.add_trace(
        go.Scatter(x=base_df['DatasetAge'], 
            y=base_df['LogWebhits'], 
            name="Log of Web Hits Across Datasets",
            line_shape='spline'),
            secondary_y=False,
    )

    fig3.add_trace(
        go.Scatter(x=base_df['DatasetAge'], y=base_df['LogDatapointsAdded'], 
            name="Log of Datapoints Added",
            line_shape='spline'),
            secondary_y=True
    )

    # Add figure title
    fig3.update_layout(template="plotly_white",
        title_text="Webhits vs Count of Datapoints Added by Dataset Age on Website",
        legend=dict(
            x=0.39,
            y=0.80,
            traceorder="normal")
    )

    # Set y-axes titles
    fig3.update_yaxes(title_text="Log of Web Hits to Datasets Added", secondary_y=False)
    fig3.update_yaxes(title_text="Log of Datapoints Added", secondary_y=True)

    fig3.update_xaxes(autorange="reversed", title_text="Dataset Age / Years Since Dataset Added")
    fig3.write_html(thisdir + "viz_webhits_vs_datapoint_census.html")

    #print(base_df.head())


def worldmap(df, thisdir):
    #'multivariate_data', 'time_series_data', 'data_generator_data', 'domain_theory_data', 'image_data', 'relational_data', 'sequential_data', 'spatial_data', 'univariate_data', 'spatio_temporal_data', 'text_data', 'transactional_data'
    df = df[df['source_institution_places'].str.len() > 6]
    datasetcount = len(df.index)
    srclist = df[['source_institution_places']].values.tolist()
    countrylist = []
    for x in srclist:
        if x != [np.nan]:
            x = ast.literal_eval(x[0])
            for xsub in x:
                countrylist.append(xsub)
    df = pd.DataFrame(countrylist, columns = ['University', 'City', 'Country', 'CODE',])
    #Countrylist = list(Counter(countrylist))
    df = df.groupby(['Country', 'CODE'],as_index=False).size().reset_index()
    df.columns = [*df.columns[:-1], 'Dataset Count']
    maxcount = df['Dataset Count'].max()

    #merge dataframes
    df = df.merge(country_codes, how='right', on=['CODE'])
    df['Country'] = df['Country_y']
    df = df.drop(['Country_x', 'Country_y'], axis=1)
    df = df[df.Country != 'Antarctica']
    df=df.fillna(0)
    df['hover_text'] = 'Country: ' + df['Country'] +  '\nNumber of Datasets: ' + df['Dataset Count'].astype(str)

    def dataset_count_calc(x):
        #maxval = 15
        out = (float(x) * 100.00) / float(datasetcount)
        #out = maxval if out > maxval else out
        return out

    df['Dataset Count Pct'] = df['Dataset Count'].apply(dataset_count_calc)

    fig = go.Figure(
        data=go.Choropleth(
        locations = df['CODE'],
        z = df['Dataset Count Pct'],
        hovertext = df['hover_text'],
        colorscale = 'rdylbu',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Sourced % Datasets',
        zmin=0,
        zmax=10
    ))  
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        title_text='UC Irvine ML Dataset Analysis',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='mercator'  #eckert4, conic equal area
        ),
    #The available projections are 'equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff' and 'sinusoidal'.
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="http://archive.ics.uci.edu/ml/datasets.php">\
                UCI Machine Learning Repository</a>',
            showarrow = False
        )]
    )

    print(df)
    #fig.write_html(thisdir + "viz_worldmap_sourced_pct_datasets.html")


def mike_stacked_bar_chart(df, save_here):
    """Mike needs a stacked bar chart adding together columns. """

    sum_col_name = 'sum_int_cols' # rename this to whatever
    list_of_columns_to_sum = ['nnamed', 'header', 'berofinsta'] #??
    title_for_y_axis = "unknown sum" #??
    
    chart_title = "Sum Of Content Area ____  by Year Submitted"

    def addemtogether(x):
        summed = 0
        # Need to list columns to be summed togethert here
        for colname in list_of_columns_to_sum:
            summed = summed + int(x[colname])
        return summed

    # Apply above formula to all rows and make a new column
    df[sum_col_name] = df.apply(addemtogether, axis = 1)
    
    # Limit columns to Year, Area, and sum column, sort by year
    df = df[['year_donated', 'Area', sum_col_name]].sort_values(by=['year_donated'])
    
    # Sum together the values by year and area
    df = df.groupby(['year_donated', 'Area']).sum().reset_index()
    
    # Create the chart
    fig = px.bar(df, x='year_donated', \
        y=sum_col_name, \
        color="Area", \
        title=chart_title, \
        color_discrete_sequence=px.colors.qualitative.Set2)
    # For some reason these things have to be in update_layout
    fig.update_layout(yaxis_title=title_for_y_axis,
        legend_title="Are of Content Focus"
        ## commented below is a way to put the legend inside the graph
        # ,legend=dict(
        #     x=0.20,
        #     y=0.75,
        #     traceorder="normal"
        # )
        )
    # Safe to an html file for interactivity
    fig.write_html(save_here + "mike_stacked_bar_chart.html")

if __name__ == '__main__':
    start_time = datetime.now()

    # 1. dir path of this folder
    thisdir = os.path.dirname(os.path.abspath(__file__)) + r"\\"

    # 2. src dataset to build on -> dataframe
    src_data = thisdir + r"cleanest_data_KMaugmented.csv"
    src_df = pd.read_csv(src_data, encoding="latin-1")

<<<<<<< HEAD
    ## 3. Make visualizations
    # viz_stacked_tasks_time(src_df, thisdir)
    # viz_stacked_area_tasks_time(src_df, thisdir)
    # viz_webhits_data_available(src_df, thisdir)
    # worldmap(src_df, thisdir)
    mike_stacked_bar_chart(src_df, thisdir)
=======
    # 3. Make visualizations
    #viz_stacked_tasks_time(src_df, thisdir)
    #viz_stacked_area_tasks_time(src_df, thisdir)
    #viz_webhits_data_available(src_df, thisdir)
    worldmap(src_df, thisdir)
>>>>>>> e3b7ca22cb7a5466acf16470e826079d72b308f3

    print("--- %s seconds ---" % (datetime.now() - start_time))

