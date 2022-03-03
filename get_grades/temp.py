
get_truth_score(temp['name'],temp['groupmates'],temp['answers_1'],'answers_1',df_merged)


temp = df_merged.loc[175].to_dict()

(parse('2022-01-03') - parse('2022-02-02')).days
df_merged['question_1']=df_merged['question_1'].fillna('')
df_merged['answers_1'] = df_merged.apply(lambda x: get_answers_dict(x['question_1']),axis = 1)

df_merged['evaluation'] = df_merged.apply(lambda x:get_truth_score(x['name'],x['groupmates'],x['answers_1'],'answers_1',df_merged),axis=1 )

df_merged['evaluation'] = df_merged.apply(lambda x:get_truth_score(x['name'],x['groupmates'],x['all_answers'],'all_answers',df_merged),axis=1 )




parse('2022-01-03') - parse('2022-01-02') 
with open('temp3.json','w') as f:
    json.dump(df_merged.loc[9].to_dict(),f,indent=2)

with open('temp4.json','w') as f:
    json.dump(df_merged.loc[11].to_dict(),f,indent=2)

