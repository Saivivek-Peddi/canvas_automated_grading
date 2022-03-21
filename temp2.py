def get_truth_score(name,groupmates,answer,col,df):
    interactee_disagreement,topic_disagreement,date_disagreement,time_disagreement = [],[],[],[]
    qeustions, notes = [],[]
    for item in answer['interacted_with']:
        int_idx = df.index[df['name']==item].tolist()
        if len(int_idx)==0:
            notes.append(f'{item} did not submit.')
            interactee_disagreement.append(0)
            topic_disagreement.append(0)
            date_disagreement.append(0)
            time_disagreement.append(0)
        else:
            idx = int_idx[0]
            int_answer = df[col][idx]
            interactee_disagreement.append(get_interactee_disagreement(name,int_answer['interacted_with']))
            topic_disagreement.append(get_topic_disagreement(answer['topics'],int_answer['topics']))
            date_disagreement.append(get_date_disagreement(answer['date'],int_answer['date']))
            time_disagreement.append(get_time_disagreement(answer['time'],int_answer['time']))
    
    fin_truth = []
    # Name
    if get_disagreement_score(interactee_disagreement)>50:
        fin_truth.append(0)
        nam_dag = []
        for i in range(len(interactee_disagreement)):
            if interactee_disagreement[i]==1:
                nam_dag.append(answer['interacted_with'][i])
        
        name_dag = ','.join(nam_dag)
        questions.append(f'You mentioned that you interacted with {name_dag} but they did not mention your name')
    else:
        fin_truth.append(1)
    
    # Topic
    if  get_disagreement_score(topic_disagreement)>50:
        fin_truth.append(0)
        questions.append('Your topics of discussion do not match that of your teammates')
    else:
        fin_truth.append(1)
    
    # Time
    if  get_disagreement_score(topic_disagreement)>50:
        fin_truth.append(0)
        questions.append('Your total time of discussion do not match that of your teammates')
    else:
        fin_truth.append(1)
    
    # Date
    if  get_disagreement_score(topic_disagreement)>50:
        fin_truth.append(0)
        questions.append('Your date of discussion do not match that of your teammates')
    else:
        fin_truth.append(1)
    
    # Groupmates - Checking if interacted with same group mates.
    if topic_score(' '.join(answer['interacted_with']),' '.join(groupmates))>40:
        fin_truth.append(0)
        questions.append('Most of your interactees are not your assigned groupmates, Why?')
    else:
        print(topic_score(' '.join(answer['interacted_with']),' '.join(groupmates)))
        fin_truth.append(1)
    
    truth_score = (sum(fin_truth)/len(fin_truth))*100 
    out = {}
    print(truth_score)
    out['truth_score'] = truth_score
    out['questions_to_students'] = questions
    out['notes'] = notes
    print('Done')
    return out