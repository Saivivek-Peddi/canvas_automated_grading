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
            shutil.rmtree(f'{path}/manual_inspections')
            shutil.rmtree(f'{path}/submissions')
            shutil.rmtree(f'{path}/groups')
            shutil.rmtree(f'{path}/temp_grades')
            shutil.rmtree(f'{path}/final_grades')
            shutil.rmtree(f'{path}/final_tags')

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
