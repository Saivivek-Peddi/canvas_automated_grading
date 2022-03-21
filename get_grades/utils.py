import pandas as pd
import ast

from dateutil import parser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# getting interactees 
def get_names(A):
    try:
        for i in range(len(A)-1,-1,-1):
            if A[i]+A[i-1]==',\\':
                break
        for j in range(i+1,len(A)):
            if A[j]==',':
                break
        names = A[:j].split(',')[::-1]
        fin_names = []
        for i in range(len(names)):
            if i%2!=0:
                fin_names.append(f'{names[i-1].strip()} {names[i][:-1].strip()}')
    except:
        fin_names = []
    return fin_names

# getting topics discussed
def get_topics(A):
    topics = []
    if 'Do introductions' in A:
        topics.append('Do introductions')
    if 'School-related topics' in A:
        topics.append('School-related topics')
    if 'Play a game' in A:
        topics.append('Play a game')
    if 'Non-school-related topics' in A:
        topics.append('Non-school-related topics')
    
    return topics

# time for discussion
def get_time(A):
    tt = 0
    item = str(A).strip().replace('+','').split(',')
    for i in item:
        try:
            tt+=int(i)
        except:
            pass
    return tt

# date of discussion
def get_date(A):
    date = []
    d = ''
    A = A.split(',')
    for item in A:
        try:
            int(item)
        except:
            try:
                d = parser.parse(item,dayfirst=False).strftime("%Y-%m-%d")
            except:
                pass
        
    if d!='':
        date.append(d)
    return date

# get answers_dict
def get_answers_dict(A):
    answers = {}
    answers['interacted_with'] = get_names(A)
    answers['topics'] = get_topics(A)
    answers['time'] = get_time(A)
    answers['date'] = get_date(A)
    
    return answers

# get all answers
def get_all_answers_dict(A):
    out = {"interacted_with":[],"topics":[],'time':0,'date':[]}
    # print(A)
    # print(type(A))
    for item in A:
        # print(item)
        temp = get_answers_dict(item)
        # print(temp)
        out['interacted_with']+=temp['interacted_with']
        out['topics']+=temp['topics']
        out['time']+=temp['time']
        out['date']+=temp['date']
    
    out['interacted_with']=list(set(out['interacted_with']))
    out['topics']=list(set(out['topics']))
    out['date']=list(set(out['date']))
    return out

# Comparisions
# get topic score
def topic_score(a,b):
    return fuzz.token_set_ratio(a,b)

# get time score
def time_score(a,b):
    if b==0:
        return 100
    elif a==0:
        return 0
    return (min(a,b)/max(a,b))*100

# get date score
def date_score(a,b):
    if len(b)==0:
        return 100
    elif len(a)==0:
        return 0
    return fuzz.token_set_ratio(' '.join(a),' '.join(b))

def time_check(x):
    return True if x['time']==0 else False

# Name Disagreement
def get_interactee_disagreement(a,b):
    if a in b:
        return 0
    else:
        return 1

# Topic Disagreement
def get_topic_disagreement(a,b):
    if topic_score(' '.join(a),' '.join(b))>90:
        return 0
    else:
        return 1

# Date Disagreement 
def get_date_disagreement(a,b):
    if date_score(a,b)>=90:
        return 0
    else:
        return 1

# Time Disagreement
def get_time_disagreement(a,b):
    if time_score(a,b)>60:
        return 0
    else:
        return 1

# Percentage disagreement
def get_disagreement_score(a):
    if len(a)==0:
        return 100
    else:
        return (sum(a)/len(a))*100

# Voting based truth score.
def get_truth_score(name,groupmates,answer,col,df):
    if len(answer['interacted_with'])==0:
        return {'truth_score':0,'questions':[
            {'question':'Did you not interact with anyone?','notes':['Probably did not interact with anyone']}],'additional_notes':[]}
    interactee_disagreement,topic_disagreement,date_disagreement,time_disagreement = [],[],[],[]
    questions, additional_notes = [],[]
    topics_list,date_list,time_list = [],[],[]
    for item in answer['interacted_with']:
        int_idx = df.index[df['name']==item].tolist()
        if len(int_idx)==0:
            additional_notes.append(f'{item} did not submit.')
            interactee_disagreement.append(0)
            topic_disagreement.append(0)
            topics_list.append([])
            date_disagreement.append(0)
            date_list.append([])
            time_disagreement.append(0)
            time_list.append(0)
        else:
            idx = int_idx[0]
            int_answer = df[col][idx]
            interactee_disagreement.append(get_interactee_disagreement(name,int_answer['interacted_with']))
            topic_disagreement.append(get_topic_disagreement(answer['topics'],int_answer['topics']))
            topics_list.append(int_answer['topics'])
            date_disagreement.append(get_date_disagreement(answer['date'],int_answer['date']))
            date_list.append(int_answer['date'])
            time_disagreement.append(get_time_disagreement(answer['time'],int_answer['time']))
            time_list.append(int_answer['time'])
    
    fin_truth = []
    # Name
    if get_disagreement_score(interactee_disagreement)>50:
        fin_truth.append(0)
        nam_dag = []
        for i in range(len(interactee_disagreement)):
            if interactee_disagreement[i]==1:
                nam_dag.append(answer['interacted_with'][i])
        
        name_dag = ','.join(nam_dag)
        question = {'question':f'You mentioned that you interacted with {name_dag} but they did not mention your name',
                'notes':[f'{name_dag} did not mention {name} in their interacted list']
            }
        questions.append(question)
    else:
        fin_truth.append(1)

    # Topic
    if  get_disagreement_score(topic_disagreement)>50:
        fin_truth.append(0)
        question = {
            'question':'Your topics of discussion do not match that of your teammates',
            'notes':[
                f'1s represent disagreement with the corresponding interactees in interactee list',
                {
                    'interacted_with': answer['interacted_with'],
                    'topic_disagreement_list':topic_disagreement,
                    'topics_list':topics_list
                }
            ] 
        }
        questions.append(question)
    else:
        fin_truth.append(1)
    
    # Time
    if  get_disagreement_score(time_disagreement)>50:
        fin_truth.append(0)
        question = {
            'question':'Your total time of discussion do not match that of your teammates',
            'notes':[
                f'1s represent disagreement with the corresponding interactees in interactee list',
                {
                    'interacted_with': answer['interacted_with'],
                    'time_disagreement_list':time_disagreement,
                    'time_list':time_list
                }
            ] 
        }
        questions.append(question)
    else:
        fin_truth.append(1)
    
    # Date
    if  get_disagreement_score(date_disagreement)>50:
        fin_truth.append(0)
        question = {
            'question':'Your date of discussion do not match that of your teammates',
            'notes':[
                f'1s represent disagreement with the corresponding interactees in interactee list',
                {
                    'interacted_with': answer['interacted_with'],
                    'date_disagreement_list':date_disagreement,
                    'date_list':date_list
                }
            ] 
        }
        questions.append(question)
    else:
        fin_truth.append(1)
    
    # Groupmates - Checking if interacted with same group mates.
    try:
        if topic_score(' '.join(answer['interacted_with']),' '.join(groupmates))<40:
            fin_truth.append(0)
            question = {
                'question':'Most of your interactees are not your assigned groupmates, Why?',
                'notes':[
                    f'Did not interact with many groupmates',
                    {
                        'interacted_with': answer['interacted_with'],
                        'group_mates':groupmates
                    }
                ] 
            }
            questions.append(question)
        else:
            fin_truth.append(1)
    except Exception as e:
        print('Unable to fetch groupmates')
        fin_truth.append(1)
    
    truth_score = (sum(fin_truth)/len(fin_truth))*100 
    out = {}
    out['truth_score'] = truth_score
    out['questions'] = questions
    out['additional_notes'] = additional_notes
    return out

# Flagging Function
def check_truth_score(x):
    if x['truth_score']<=60:
        if x['truth_score']==0:
            return True
        else:
            return True
    else:
        return False

def summary_score(x):
    if x['truth_score']==0:
        return True
    else:
        return False


def get_score(flag,answer):
    if flag:
        return 0
    else:
        if answer['time']>=20:
            return 6
        else:
            return 6*(answer['time']/20)
        
# def date_score(a,b):
#     if b=='':
#         return 100
#     elif a=='':
#         return 0

#     days = abs((parse(a) - parse(b)).days)
#     if days==0:
#         return 100
#     elif days==1:
#         return 60
#     elif days==2:
#         return 40
#     else:
#         return 0
