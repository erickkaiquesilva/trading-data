from downloaderdata import DownloaderData
from createuser import CreateUsers
from managerfiles import ManagerFiles


base_path = 'c:\\Users\\Erik\\Documents\\Python Scripts\\Python Basic\\Python Exercicios\\trading_manager\\data-mt5'
file_name = 'PETR4Week.csv'
manager_file = ManagerFiles(base_path,file_name)
df_1 = manager_file.open_file()