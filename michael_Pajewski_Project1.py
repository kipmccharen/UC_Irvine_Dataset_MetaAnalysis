#testing file for project 1 ideas
#Mike Pajewski 

import pandas as pd
import plotly.offline as pyo
import plotly.express as px


#setting notbook to run offline 
pyo.init_notebook_mode()

#import data file
df = pd.read_csv('cleanest_data.csv') 

#grouping by area of interest 
df_intrest = df.groupby(['Area']).sum()

#grouping by year and area of interest
df_year_area = df.groupby(['year_donated','Area']).count().reset_index()

#group by year take mean of each group
df_year_avg_instance = df.groupby(['year_donated','Area']).mean().reset_index()



#plot 1 plot histigram of count of area of interest
def plot1():
    fig = px.histogram(df, x="Area", title="Histogram of Area" )
    # updating plot layout 
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', 
    yaxis_title="Count",
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

    # add boarders to graph
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    return fig.show()

# plot histigram of number of web hits by area of interest
#need to clean this up 
def plot2():
    
    
    #plot
    fig2 = px.bar(df_intrest, y='NumberofWebHits', title="Histogram of Web Hits")

    # updating plot layout 
    fig2.update_layout(yaxis_title="Number of Web Hits",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # add boarders to graph
    fig2.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    return fig2.show()


#plot instance by area
def plot3():
    #plot
    fig4 = px.bar(df, x="Area", y="NumberofInstances", color="header", title="Instance by Area")

    #update layout
    fig4.update(layout_showlegend=False)
    fig4.update_layout(yaxis_title="Number of Instances",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # add boarders to graph
    fig4.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig4.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    return fig4.show()


#web hits by year data set was created grouped by year
def plot4():
    #creating plot
    fig5 = px.bar(df, x="year_donated", y="NumberofWebHits", color="header", title="Webhits by Year by Dataset")
    #updating plot layout
    fig5.update(layout_showlegend=False)
    fig5.update_layout(yaxis_title="Number of Web Hits",
        xaxis_title="Year",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # add boarders to graph
    fig5.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig5.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)



    return fig5.show()

def plot5():
    fig7 = px.bar(df_year_area, x="year_donated", y="header", color="Area", title="Data set per Year by Area")

    #update layout
    fig7.update_layout(yaxis_title="Number of Data Sets",
        xaxis_title="Year",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # add boarders to graph
    fig7.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig7.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    return fig7.show()

def plot6():
    #plot 
    fig8 = px.bar(df_year_avg_instance,
              x="year_donated", y="NumberofInstances" ,
              color = 'Area', 
              title="Number of Instances by Area")


    #update layout
    fig8.update_layout(yaxis_title="Number of Instances",
        xaxis_title="Year",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

<<<<<<< HEAD
ax1.show()
=======
    # add boarders to graph
    fig8.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig8.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig8.show()    

>>>>>>> e3b7ca22cb7a5466acf16470e826079d72b308f3

# =============================================================================
# plot1()
# plot2()
# plot3()
# plot4()
# plot5()
# plot6()
# =============================================================================
