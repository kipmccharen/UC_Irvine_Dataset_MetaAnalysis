#testing file for project 1 ideas
#Mike Pajewski 

import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.express as px

#setting notbook to run offline 
pyo.init_notebook_mode()

#import data file
df = pd.read_csv('cleanest_data.csv') 





df_year_avg_instance = df.groupby(['year_donated','Area']).mean().reset_index()



    
    



# plot histigram of count of area of interest
fig = px.histogram(df, x="Area",
                   title="Histogram of Area")
fig.show()