from tasks.data_analyzer_engine.analyzer import df_analyzer
from celery import shared_task

@shared_task
def process_file(file_path, question):
    print(f'DEBUG: Processing {file_path} with question {question}')
    return df_analyzer(file_path, question)