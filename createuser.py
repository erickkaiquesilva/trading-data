import os
from downloaderdata import DownloaderData
import json

class CreateUsers():

    def __init__(self, login, password, option, server=None):
        self.login = login
        self.password = password
        self.server = server
        self.option = option
        self.researcher_data = ['tradingview', 'metatrader'] 
        self.file_credentials = {'login': self.login,
                                'password': self.password,
                                'server': self.server
                                }
        self._save_credentials()

    def _create_file_credentials(self, path):
        nm_server = self.researcher_data[self.option]
        nm_file = nm_server + 'credentials.json'
        save_file_path = os.path.join(path, nm_file)
        if os.path.exists(save_file_path):
            print("Já existe arquivo salvo!!!")
        else:
            with open(save_file_path, "w") as arquivo:
                json.dump(self.file_credentials, arquivo)

    def open_credentials(self):
        path = 'c:\\Users\\Erik\\Documents\\Python Scripts\\Python Basic\\Python Exercicios\\trading_manager\\credentials'
        file_path_nm = path + '\\{}credentials.json'.format(self.researcher_data[self.option])
        with open(file_path_nm) as f:
            data = json.load(f)
        return data

    def _save_credentials(self):
        path = 'c:\\Users\\Erik\\Documents\\Python Scripts\\Python Basic\\Python Exercicios\\trading_manager\\credentials'
        if not os.path.exists(path):
            os.makedirs(path)
        self._create_file_credentials(path) 

    def server_selected_user(self):
        return self.researcher_data[self.option] 