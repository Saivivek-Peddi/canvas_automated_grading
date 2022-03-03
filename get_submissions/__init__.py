import requests
import json
import pathlib
import time
from datetime import datetime

path = str(pathlib.Path(__file__).parents[1])
pathlib.Path(path+'/submissions').mkdir(parents=True, exist_ok=True)
class Submissions:
    def __init__(self,quizzes):
        self.quizzes = quizzes
        self.names = [quiz.title for quiz in self.quizzes]
        self.report_ids = []
        for quiz in quizzes:
            report = quiz.create_report('student_analysis')
            self.report_ids.append(report.id)
        start_time = datetime.now()
        print("")
        print('Generating Analysis Report this will take time.')
        elapsed = 0
        while True:
            try:
                elapsed+=10
                time.sleep(10)
                print(f'Time Elapsed: {elapsed} seconds')
                for i in range(len(quizzes)):
                    quizzes[i].get_quiz_report(self.report_ids[i]).file
                break
            except Exception as e:
                # print(e)
                pass
        end_time = datetime.now()
        print(f'Time taken for generating reports is {end_time - start_time}')

        self.urls = [quiz.create_report('student_analysis').file['url'] for quiz in quizzes]

        for i in range(len(self.urls)):
            self.download_file(self.urls[i],self.names[i])

    def download_file(self,url,name):
        local_filename = f'{path}/submissions/{name}.csv'
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)
        return local_filename
