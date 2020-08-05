import pandas as pd 
import numpy as np
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import plotly.offline as pyo

# dirname = os.path.dirname
# basedir = dirname(dirname(os.path.abspath(__file__)))
thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\"
country_codes = pd.read_csv(thisdir + r"all_country_codes.csv")

def viz_stacked_tasks_time(df): #, thisdir):
    pyo.init_notebook_mode()
    
    df = df[['year_donated', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'recomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['year_donated'])

    df = df.groupby(['year_donated']).sum().reset_index()
    df.columns = [x.replace("_", " ").replace(" Task", "").title() for x in list(df.columns.values)]
    # print(df)
    # quit()
    collist = list(df.columns.values)[1:]
    fig = px.bar(df, x='Year Donated', y=collist, \
        title="Dataset Count by ML Research Area by Year Submitted", \
        color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(yaxis_title="Count of Datasets",
        # legend_title="ML Task Appropriate to Dataset",
        # legend=dict(
        #     x=0.20,
        #     y=0.75,
        #     traceorder="normal")
        )
    #fig.write_html(thisdir + "viz_stacked_tasks_time.html")
    return fig

def viz_stacked_area_tasks_time(df): #, thisdir):
    pyo.init_notebook_mode()
    df = df[['year_donated', 'causal_discover_task', 'classification_task', 'regression_task', 'function_learning_task', 'recomendation_task', 'description_task', 'relational_learning_task', 'no_given_task', 'clustering_task']].sort_values(by=['year_donated'])
    df = df.groupby(['year_donated']).sum().reset_index()
    df.columns = [x.replace("_", " ").title().replace(" Task", "") for x in list(df.columns.values)]
    collist = list(df.columns.values)[1:]

    df['sumvals'] = df[collist].sum(axis=1).astype(float)

    def convert_to_pct(x):
        for col in collist:
            x[col] = x[col].astype(float)
            x[col] = (x[col] / x['sumvals'])
        return x

    df = df.apply(convert_to_pct, axis=1)
    
    #print(df.head())
    # quit()
    # quit()
    fig2 = px.bar(df, x='Year Donated', y=collist, \
        title="Dataset Count by ML Research Area by Year Submitted", \
        color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(yaxis_title=r"Count of Datasets as Percent of All Datasets",
        legend_title="ML Task Appropriate to Dataset",
        # legend=dict(
        #     x=0.70,
        #     y=0.17,
        #     traceorder="normal")
             )
    fig2.update_yaxes(range=[0, 1])
    fig2.layout.yaxis.tickformat = ',.1%' 
    #fig2.write_html(thisdir + "viz_stacked_area_tasks_time.html")
    return fig2


def viz_webhits_data_available(base_df): #, thisdir):
    pyo.init_notebook_mode()
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import math

    base_df = base_df[['dataset_age', 'sum_file_sizes', 'NumberofWebHits']]

    base_df = base_df.groupby(['dataset_age']).sum().reset_index().sort_values(by=['dataset_age'])

    base_df['LogWebhits'] = base_df['NumberofWebHits'].apply(lambda x: np.log(x) +1)
    base_df['LogDatapointsAdded'] = base_df['sum_file_sizes'].apply(lambda x: np.log(x) +1)

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig3.add_trace(
        go.Scatter(x=base_df['dataset_age'], 
            y=base_df['LogWebhits'], 
            name="Log of Web Hits Across Datasets",
            line_shape='spline'),
            secondary_y=False,
    )

    fig3.add_trace(
        go.Scatter(x=base_df['dataset_age'], y=base_df['LogDatapointsAdded'], 
            name="Log of Summed File Sizes Added",
            line_shape='spline'),
            secondary_y=True
    )

    # Add figure title
    fig3.update_layout(template="plotly_white",
        title_text="Webhits vs Count of Datapoints Added by Dataset Age on Website",

        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.2,
        xanchor="center",
        x=0.5
        )
        #showlegend=False
        #     x=0.39,
        #     y=0.80,
        #     traceorder="normal")

    )

    # Set y-axes titles
    #fig3.update_yaxes(title_text="Log of Web Hits to Datasets Added", secondary_y=False)
    #fig3.update_yaxes(title_text="Log of Datapoints Added", secondary_y=True)

    fig3.update_xaxes(autorange="reversed", title_text="Dataset Age / Years Since Dataset Added")
    return fig3
    #fig3.write_html(thisdir + "viz_webhits_vs_datapoint_census.html")

    #print(base_df.head())


def worldmap(df): #, thisdir):
    #pyo.init_notebook_mode()
    #'multivariate_data', 'time_series_data', 'data_generator_data', 'domain_theory_data', 'image_data', 'relational_data', 'sequential_data', 'spatial_data', 'univariate_data', 'spatio_temporal_data', 'text_data', 'transactional_data'
    df = df[df['source_institution_places'].str.len() > 6]
    datasetcount = len(df.index)
    srclist = df[['source_institution_places']].values.tolist()
    countrylist = []
    for x in srclist:
        if x != [np.nan]:
            x = x[0].split("|")
            for xsub in x:
                xsub = xsub.split(";")
                countrylist.append(xsub)
    df = pd.DataFrame(countrylist, columns = ['University', 'City', 'Country', 'CODE',])
    
    df = df.groupby(['Country', 'CODE'],as_index=False).size().reset_index()
    df.columns = [*df.columns[:-1], 'Dataset Count']

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
        colorscale = 'Blues',
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

    #print(df)
    #fig.write_html(basedir + "viz_worldmap_sourced_pct_datasets.html")
    return fig

if __name__ == '__main__':
    start_time = datetime.now()

    src_data =r"cleanest_data_augmented.csv"
    src_df = pd.read_csv(src_data, encoding="latin-1")

    # 3. Make visualizations
    #viz_stacked_tasks_time(src_df)
    #viz_stacked_area_tasks_time(src_df)
    #viz_webhits_data_available(src_df)
    worldmap(src_df).show()

    print("--- %s seconds ---" % (datetime.now() - start_time))

