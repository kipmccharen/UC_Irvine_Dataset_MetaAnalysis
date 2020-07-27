#testing file for project 1 ideas
#Mike Pajewski 

 
import pandas as pd
import numpy as np



#import data file
df = pd.read_csv('cleanest_data.csv') 


ax1 = df.plot.scatter(x='DateDonated',
                      y='NumberofAttributes')

ax1.set_ylim(0,100)



