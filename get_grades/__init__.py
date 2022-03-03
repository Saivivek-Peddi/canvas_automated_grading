import json
import pathlib
import pandas as pd
import os
import ast
import time

from .utils import *

path = str(pathlib.Path(__file__).parents[1])
pathlib.Path(path+'/manual_inspections').mkdir(parents=True, exist_ok=True)
pathlib.Path(path+'/temp_grades').mkdir(parents=True, exist_ok=True)


with open(f'{path}/get_grades/col_names.json') as f:
    col_names = json.load(f)


class Grade:
    def __init__(self,quizzes):
        print('Grading in Progress')
        grade_config = []
        for quiz in quizzes:
            conf = {
                'id':quiz.assignment_id,
                'course_id':quiz.course_id,
                'name':quiz.title
            }
            grade_config.append(conf)
        
        with open(f'{path}/temp_grades/quiz_config.json','w') as f:
            json.dump(grade_config,f,indent=2)

        submissions = list(os.listdir(path+'/submissions'))
        groups = list(os.listdir(path+'/groups'))
        for sub in submissions:
            name = sub[:-4]
            df_sub = pd.read_csv(f'{path}/submissions/{sub}',names=col_names,header=0)
            # Getting the group name
            grp = ' '.join(sub.split(' ')[:3])
            df = pd.read_csv(f'{path}/groups/{grp}.csv')
            # name = f'{grp}_{name}'
            self.inspect(df,df_sub,name)
            print(f'Grading for is {name} complete')
        


    # df - df of groupmates
    # df_sub - df of submissions
    def inspect(self,df,df_sub,name):
        print('')
        print(f'Started Grading {name}')
        df['groupmates'] = df['groupmates'].apply(lambda x: ast.literal_eval(x))
        df['email_ids'] =  df['email_ids'].apply(lambda x: ast.literal_eval(x))

        df['name'] = df['groupmates']
        df = df.explode(['name','email_ids']).reset_index(drop=True)
        df_merged = df_sub.merge(df,how='left',on='name',indicator=True)

        df_merged[['question_1','question_2','question_3','question_4']]=df_merged[['question_1','question_2','question_3','question_4']].fillna('')
        df_merged['all_answers'] = df_merged.apply(lambda x: get_all_answers_dict([x['question_1'],x['question_2'],x['question_3'],x['question_4']]),axis = 1)

        df_merged['evaluation'] = df_merged.apply(lambda x:get_truth_score(x['name'],x['groupmates'],x['all_answers'],'all_answers',df_merged),axis=1 )

        df_merged['flag'] = df_merged.apply(lambda x: check_truth_score(x['evaluation']), axis=1)
        df_merged['score'] = df_merged.apply(lambda x: get_score(x['flag'],x['all_answers']),axis=1)
        
        print('Writing to json')
        df_merged.to_json(f'{path}/temp_grades/{name}.json', orient='records',indent=2)
        df_temp = df_merged[df_merged['flag']]
        df_temp.to_json(f'{path}/manual_inspections/{name}.json', orient='records',indent=2)
        print('Generating Summary')
        summary = {
            'number_of_tagged_students':df_temp.shape[0],
            'tagged_probably_because_of_not_listing_interactees':df_temp[df_temp.apply(lambda x:summary_score(x['evaluation']),axis=1)].shape[0],
            'must_checking_required_for':df_temp.shape[0] - df_temp[df_temp.apply(lambda x:summary_score(x['evaluation']),axis=1)].shape[0]
        }
        print('Summary Generated')
        with open(f'{path}/manual_inspections/Summary_{name}.json','w') as f:
            json.dump(summary,f,indent=2)