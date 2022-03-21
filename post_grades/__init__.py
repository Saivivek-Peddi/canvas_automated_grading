import pandas as pd
import json
import os
from datetime import datetime
import time
import pathlib

from canvasapi import Canvas

config_path = str(pathlib.Path(__file__).parents[1])
with open(f'{config_path}/api_config.json') as f:
    config = json.load(f)

with open(f'{config_path}/temp_grades/quiz_config.json') as f:
    quiz_config = json.load(f)


class Post_Grades:
    def __init__(self):
        self.api_url = config['api_url']
        self.api_key = config['access_token']

        # Initialize a new Canvas object and get all the courses
        canvas = Canvas(self.api_url, self.api_key)
        for item in quiz_config:
            course = canvas.get_course(item['course_id'])
            break
        
        assignments = []
        for assignment in course.get_assignments():
            if 'Evaluation' in assignment.name:
                assignments.append(assignment)
        print('Started Posting Grades, this might take some time')
        for item in quiz_config:
            assignment = course.get_assignment(item['id'])
            for eval_item in assignments:
                if assignment.name in eval_item.name:
                    print(f'{assignment.name} ---> {eval_item.name}')
                    assignment = eval_item
                    break
            name = item['name']
            start_time = datetime.now()
            print(f'Posting started for {name}')
            self.post_grades(assignment,name)
            print(f'Posting completed for {name}')
            end_time = datetime.now()
            print(f'Time taken for posting is {end_time - start_time}')

    def post_grades(self,assignment,name):
        df = pd.read_json(f'{config_path}/temp_grades/{name}.json')
        df_flagged = pd.read_json(f'{config_path}/manual_inspections/{name}.json')

        for i in range(df_flagged.shape[0]):
            df.loc[df[df['id']==df_flagged.loc[i]['id']].index[0]]=df_flagged.loc[i]

        df['comments'] = df.apply(lambda x:self.comment(x['flag'],x['evaluation']),axis=1)
        df['grades_posted'] = df.apply(lambda x:self.post_score_and_comments(assignment,x['id'],x['score'],x['comments']),axis=1)
        df.to_json(f'{config_path}/final_grades/{name}.json',orient='records',indent=2)
        df_flagged[df_flagged['flag']][['name','sis_id','email_ids']].to_csv(f'{config_path}/final_tags/{name}.csv',index=False)
        
    def comment(self,flag,evaluation):
        if flag:
            comment = ''
            for i in range(len(evaluation['questions'])):
                comment+=f"{i+1}.{evaluation['questions'][i]['question']} "
        else:
            comment = ''
        return comment

    def post_score_and_comments(self,assignment,student_id,score,comment):
        try:
            sub = assignment.get_submission(student_id)
            cmt={}
            cmt['text_comment']=comment
            submission={}
            submission['posted_grade']=score
            sub.edit(comment=cmt,submission=submission)
            return True
        except Exception as e:
            print(e)
            return False