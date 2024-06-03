# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:21:16 2024

@author: volte
"""

from google.cloud import bigquery
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import re


# Set up our GCS, NL, and BigQuery clients
storage_client = storage.Client()
nl_client = language_v1.LanguageServiceClient()
nl_client2 = language_v2.LanguageServiceClient()

# TODO: replace YOUR_PROJECT with your project id below
bq_client = bigquery.Client(project='ml-deployments-practice')

dataset_ref = bq_client.dataset('reddit_comment_data')
dataset = bigquery.Dataset(dataset_ref)
table_ref = dataset.table('raw_comment_manual_upload') # Update this if you used a different table name
table = bq_client.get_table(table_ref)

# Send article text to the NL API's classifyText method
def classify_text(article):
        response_topic = nl_client.classify_text(
                document=language_v1.types.Document(
                        content=article,
                        type_='PLAIN_TEXT'
                )
        )

        return response_topic
rows_for_bq = []  
client = bigquery.Client()
df = client.list_rows(table).to_dataframe()
#df['text'] = df['text'].str.replace(',', ' ').str.replace('\n', ' ')
print(df)
# Send files to the NL API and save the result to send to BigQuery
i=0
for ind, data in df.iterrows():
    print(i/df.shape[0])
    i=i+1
    try:
        comment_text = bytes(data['text'], 'utf-8')
        nl_topic = classify_text(comment_text)
                #if len(nl_topic.categories) > 0:
        if 1==1:
            rows_for_bq.append((str(comment_text), 
                            str(nl_topic.categories.name), nl_topic.categories.confidence))
    except Exception as e:
        print(e)

print(rows_for_bq)
print("Writing NL API article data to BigQuery...")
# Write article text + category data to BQ

output_table_ref = dataset.table('comment_sentiments')
output_table = bq_client.get_table(output_table_ref)
errors = bq_client.insert_rows(output_table, rows_for_bq)
assert errors == []