import json
import pathlib
import pandas as pd

path = str(pathlib.Path(__file__).parents[1])
pathlib.Path(path+'/groups').mkdir(parents=True, exist_ok=True)

with open(f'{path}/get_groups/group_names.json') as f:
    group_names=json.load(f)['group_names']

class Groups:
    def __init__(self,course):
        self.course = course
        self.groups = [item for item in self.course.get_groups()]

        print("")
        print("Generating Groups. This will take a little time.")
        for group_name in group_names:
            print(f"Group Name:{group_name}")
            fin_data = []
            for group in self.groups:
                if group_name in group.name:
                    details = {}
                    details['group_name'] = group.name
                    users = [item for item in group.get_users()]
                    details['groupmates'] = []
                    details['email_ids'] = []
                    for user in users:
                        details['groupmates'] .append(user.name)
                        details['email_ids'].append(user.integration_id)
                    fin_data.append(details)
            group_df = pd.DataFrame(fin_data)
            group_df.to_csv(f'{path}/groups/{group_name}.csv',index=False)

                    
                    

            

        
        

