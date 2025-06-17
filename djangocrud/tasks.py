from tasks.data_analyzer_engine.analyzer import df_analyzer
from celery import shared_task
import os

@shared_task
def process_file(file_path, question):
    try:
        print(f'DEBUG: Processing {file_path} with question {question}')
        result = df_analyzer(file_path, question)
        return result
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)