import os
import pandas as pd

class ManagerFiles():

    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
    
    def open_file(self):
        self.path = self.path + '\\{}'.format(self.file_name)
        if os.path.exists(self.path):
            csv_file = pd.read_csv(self.path)
            return pd.DataFrame(csv_file)
        else:
            print("Não existe o arqquivo. {}".format(self.path))
            os._exit(0)