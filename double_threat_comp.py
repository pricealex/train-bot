import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


spec_df = pd.read_csv('spec_df.csv').set_index(['class_name','spec_name'])

test_df = pd.DataFrame({'name':['Test','Test'], 'class_name':['Demon Hunter','Demon Hunter'], 'spec_name':['Havoc','Vengeance'], 'scores':[1000,2000]}).set_index(['name','class_name','spec_name'])
test_df = test_df.join(spec_df, how='left').reset_index()

ax = test_df.plot.bar(x='name', y='scores' ,stacked=True)
plt.show()