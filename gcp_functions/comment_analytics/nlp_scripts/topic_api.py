from google.cloud import bigquery
import stanza
import pandas as pd
import text2emotion as te



def assign_stats(date=None):
    stanza.download('en')  # Download the English language model
    nlp = stanza.Pipeline()
    bq_client = bigquery.Client(project='ml-deployments-practice')

    dataset_ref = bq_client.dataset('reddit_comment_data')
    dataset = bigquery.Dataset(dataset_ref)
    table_ref = dataset.table('raw_daily_hot_comments') # Update this if you used a different table name
    table = bq_client.get_table(table_ref)


    def classify_text(text):
        doc = nlp(text)
        sentiment_score = sum([sentence.sentiment for sentence in doc.sentences]) / len(doc.sentences)
        topics = list()
        for sentence in doc.sentences:
            for entity in sentence.ents:
                if entity.type != 'O':  # Exclude non-entity tokens
                    topics.append(entity.text)
        topics= ",".join(topics)
        emotions = te.get_emotion(text)
        return [sentiment_score, topics, emotions]


    rows_for_bq = []  
    client = bigquery.Client()
    df = client.list_rows(table).to_dataframe()
    #if date:
    #    df = df[df["date"] == date]
    df = df[["text", "date"]]
    df.drop_duplicates(inplace=True)
    #print(df)
    # Send files to the NL API and save the result to send to BigQuery
    i=0
    for ind, data in df.iterrows():
       # print(i/df.shape[0])
        i=i+1
        try:
            comment_text = data['text']
            nl_result = classify_text(comment_text)
            if 1==1:
                rows_for_bq.append((str(comment_text), 
                            str(nl_result[0]), str(nl_result[0]), nl_result[2]["Happy"], nl_result[2]["Angry"],
                            nl_result[2]["Sad"], nl_result[2]["Fear"]))
        except Exception as e:
            print(data['text'], e)
            pass

    print(rows_for_bq)
    print("Writing post topics to bigquery...")
    # Write article text + category data to BQ

    output_table_ref = dataset.table('comment_analytics')
    output_table = bq_client.get_table(output_table_ref)
    errors = bq_client.insert_rows(output_table, rows_for_bq)
    assert errors == []