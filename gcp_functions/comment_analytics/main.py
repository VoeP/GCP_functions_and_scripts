import functions_framework
from nlp_scripts.topic_api import *
from datetime import date
import os

credential_path = r"C:\Users\volte\Documents\keyfile.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

if __name__=="__main__":
    assign_stats()