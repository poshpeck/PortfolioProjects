#!/usr/bin/env python
# coding: utf-8

# # Retail Association Rule Minig

# Objective: Through different transactions and attributes related to the online customer shopping in a retail store, we will find the likelihood of customers purchasing products with the combination of other products.

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


import matplotlib.pyplot as plt


# In[3]:


dataframe_ =  pd.read_excel('retail.xlsx')
dataframe = dataframe_.copy()


# In[4]:


dataframe_


# In[5]:


dataframe_.shape


# In[6]:


dataframe_.info()


# In[7]:


dataframe_.isna().sum()


# There are 541909 rows and 8 columns in the dataset. </br>
# The columns are of mixed data types. </br>
# There are null values in some of the columns like CustomerId and Description. </br>

# In[8]:


# Removing all the transactions that has null values in them.
dataframe.dropna(inplace=True)


# In[9]:


dataframe.isna().sum()


# In[10]:


dataframe.shape


# After removing null rows, we are left with 4086829 rows.

# In[11]:


# Visualising customers Shopping Trend


# In[12]:


month_dataframe = pd.DataFrame()
month_dataframe['InvoiceNo'] = dataframe['InvoiceNo']
month_dataframe['month'] = pd.to_datetime(dataframe['InvoiceDate']).dt.month_name()
month_dataframe.groupby('month').count().plot(kind='bar', figsize=(12,6), legend=False)


# Most of the customers shop around November, December and October. This could be possibly because of the different reasons such as Black Friday and Cyber Monday in November and Christmas in December.

# In[13]:


# Visualising Country wise transactions.


# In[14]:


dataframe[['InvoiceNo', 'Country']].groupby('Country').count().plot(kind='bar', figsize=(12,6), legend=False)


# Maximum and majority amount of the transactions are done by the customers based in the United Kingdom. We will analyse the rules for the items purchased by the United Kingdom customers.

# In[15]:


uk_dataframe = dataframe.loc[dataframe.Country=='United Kingdom']
uk_dataframe.head()


# In[16]:


# Most Frequent Items Purchased by the customers in the UK.


# In[17]:


uk_dataframe[['InvoiceNo', 'Description']].groupby('Description').count().sort_values(by='InvoiceNo', ascending=False).head(20).plot(kind='bar', figsize=(12,6), legend=False)


# These are the top 20 items purchased by the customers in the United Kingdom. WHITE HANGING HEART T-LIGHT HOLDER, JUMBO BAG RED RETROSPOT AND REGENCY CAKESTAND 3 TIER are few of the top shopped items in the online store.

# In[18]:


# Data preparation


# In[19]:


# Removing all those rows where InvoiceNo starts with C as they are of no use to us because these transactions are based on credits
dataframe['InvoiceNo'] = dataframe['InvoiceNo'].astype('str')
dataframe = dataframe[~dataframe['InvoiceNo'].str.contains('C')]


# In[20]:


np.random.seed(11)


# In[21]:


groupby_df = dataframe.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo')


# In[22]:


groupby_df.head()


# In[23]:


groupby_df = groupby_df.applymap(lambda x: 0 if x<=0 else 1)
groupby_df.head()


# In[24]:


# Training Apriori Model


# In[27]:


conda install mlxtend


# In[26]:


from mlxtend.frequent_patterns import apriori, association_rules
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_colwidth', None)


# In[ ]:


itemset = apriori(groupby_df, min_support=0.025, use_colnames=True)


# In[ ]:


itemset.sort_values("support",ascending=False)


# Item WHITE HANGING HEART T-LIGHT HOLDER is purchased in approximately 10.5% of the overall transactions in the United Kingdom.

# In[ ]:


rules = association_rules(itemset, metric ="lift", min_threshold = 1)


# In[ ]:


rules = rules.sort_values(by='lift', ascending =False)


# In[ ]:


rules.head(10)


# consequents means something that happens or follows as a result of something else.</br>
# antecedents means a thing or an event that exists or comes before another, and may have influenced it.

# # Conclusion

# With the help of Apriori algoritm, we can perform rule mining that helps us to find the relationship among purchased items and likelihood of a customer buying other items together.</br>
# 
# Item ROSES REGENCY TEACUP AND SAUCER is purchased in around 30% of the transactions with a lift of 18.53. This also helps us to find the customers buying this item will also buy GREEN REGENCY TEACUP AND SAUCER as the confidence score for the suggested purchase is 69%.</br>
# 
# Item ALARM CLOCK BAKELIKE RED can be considered as a good recommendation for the buyers purchasing ALARM CLOCK BAKELIKE GREEN as the confidence score for this purchase is approx 67%.</br>
# 
# Theses rules can be applied by the online stores to recommend and suggest other shopping items to the customers to increase the sale of the company.

# In[ ]:





# In[ ]:




