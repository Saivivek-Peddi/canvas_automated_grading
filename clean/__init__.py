import shutil
import pathlib
path = str(pathlib.Path(__file__).parents[1])

class Clean:
    def __init__(self,only_remove_flag=False):
        if not only_remove_flag:
            self.remove_and_create(f'{path}/manual_inspections')
            self.remove_and_create(f'{path}/submissions')
            self.remove_and_create(f'{path}/groups')
            self.remove_and_create(f'{path}/temp_grades')
            self.remove_and_create(f'{path}/final_grades')
            self.remove_and_create(f'{path}/final_tags')
            print('')
        else:
            self.remove(f'{path}/manual_inspections')
            self.remove(f'{path}/submissions')
            self.remove(f'{path}/groups')
            self.remove(f'{path}/temp_grades')
            self.remove(f'{path}/final_grades')
            self.remove(f'{path}/final_tags')

    def remove(self,path):
        try:
            shutil.rmtree(path)
        except:
            pass
    
    def remove_and_create(self,path):
        try:
            shutil.rmtree(path)
            f = path.split('/')[-1]
            print(f'Creating {f} folder')
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        except:
            f = path.split('/')[-1]
            print(f'Creating {f} folder')
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            pass
