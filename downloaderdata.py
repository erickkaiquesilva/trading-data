from tvDatafeed import TvDatafeed, Interval
import os
import MetaTrader5 as mt5
import pandas as pd

class DownloaderData():

    def __init__(self, user):
        self.user = user

    def conn_data_frame(self):
        credentials = self.user.open_credentials()
        if self.user.server_selected_user() == 'tradingview':
            self._conn_tradingview(credentials)
        elif self.user.server_selected_user() == 'metatrader':
            self._conn_metatrade(credentials)
        else:
            print("Error in connect with server. Try Again!!!")
            os.quit()

    def _conn_tradingview(self, credentials):
        self.tv = TvDatafeed(credentials['login'], credentials['password'])
        print("")
        print("===== INFORME O TICKER DO ATIVO E A EXCHANGE ONDE É LISTADO =====")
        symbol = input(f'TICKER EX(PETR4): ')
        exchange = input(f'QUAL BOLSA ESTA LISTADO O ATIVO: ')

        if symbol != None and exchange != None:
            print("")

            timeframes = self._get_timeframes_tv()
            count = 0
            for i in timeframes.values():
                print(f'[{count}] {i[1]}')
                count += 1
            
            timeframe_option = int(input(f'Selecione um timeframe: '))

            if timeframe_option <= len(timeframes) and timeframe_option >= 0:
                timeframe_selected = timeframes[timeframe_option]
                print("")
                print("Qual total de bars que deseja ver")
                bars = int(input(f'Informe quantos bars deseja retorna Max(7000): '))

                if bars <= 7000:
                    self.get_hist_symbol_tv(symbol,exchange,timeframe_selected,bars)
        else:
            print("ERROR")
            os._exit(0)

    def _conn_metatrade(self, credentials):
        if not mt5.initialize(login=int(credentials['login']), password=credentials['password'], server=credentials['server']):
            print("Failed initialie() Error={}".format(mt5.last_error()))
            mt5.shutdown()

        print("")
        print("====== INFORME O TICKER DO ATIVO QUE DESEJA OBTER DADOS ======")
        symbol = input(f'TICKER EX(PETR4): ')

        if symbol != None:
            print("Qual a data inicial que deseja buscar")
            date_from = input(f'Ex(2012/12/1): ')
            print("Qual a data final: OBS(Caso não informe uma data final iremos considerar a atual)")
            date_to = input(f'Ex(2014/12/31): ')
            timeframes = self._get_timeframes_mt5()

            print("Informe em qual timeframe deseja obter esses dados: OBS(Quanto menor o timeframe mais processamento leva para obter os dados)")
            count = 0
            for i in timeframes.values():
                print(f'[{count}] {i[1]}')
                count += 1
            opt_timeframe = int(input(f'Infome o timeframe: '))

            if opt_timeframe <= len(timeframes) and opt_timeframe >= 0:
                timeframe_selected = timeframes[opt_timeframe]
                self.get_hist_symbol_mt5(symbol, date_from, date_to, timeframe_selected)
            else:
                print("Error")
                os._exit(0)
        else: 
            print("Error")
            os._exit(0)

    def get_hist_symbol_mt5(self, symbol, data_from, date_to, timeframe):
        data_from = pd.to_datetime(data_from)
        date_to = pd.to_datetime(date_to)
        symbol_hist = mt5.copy_rates_range(symbol, timeframe[0], data_from, date_to)
        df_symbol = pd.DataFrame(symbol_hist)

        print("")
        print("Success...")
        print("Deseja salvar esses dados?")
        opt = int(input(f'[1] SIM / [2] NÃO: '))

        if opt == 1:
            file_name = symbol + timeframe[1] + '.csv'
            self.save_data(df_symbol, file_name, 'data-mt5')
        else:
            return df_symbol

    def get_hist_symbol_tv(self, symbol, exchange, interval,total_bars):
        symbol_hist = self.tv.get_hist(symbol=symbol,exchange=exchange,interval=interval[0],n_bars=total_bars)
        df_symbol = pd.DataFrame(symbol_hist)

        print("")
        print("Success...")
        print("Deseja salvar esses dados?")
        opt = int(input(f'[1] SIM / [2] NÃO: '))

        if opt == 1:
            file_name = symbol + interval[1] + '.csv'
            self.save_data(df_symbol, file_name, 'data-tv')
        else: 
            return df_symbol

    def _get_timeframes_tv(self):
        timeframe_tv = {0: [Interval.in_daily, 'Daily'],
                        1: [Interval.in_weekly, 'Week'], 
                        2: [Interval.in_monthly, 'Monthly'] ,
                        3: [Interval.in_1_minute, '1 Minute'],
                        4: [Interval.in_3_minute, '3 Minute'],
                        5: [Interval.in_5_minute, '5 Minute'],
                        6: [Interval.in_15_minute, '15 Minute'],
                        7: [Interval.in_30_minute, '30 Minute'],
                        8: [Interval.in_45_minute, '45 Minute'],
                        9: [Interval.in_1_hour, '1 Hour']}
        return timeframe_tv

    def _get_timeframes_mt5(self):
        timeframe_mt5 = {0: [mt5.TIMEFRAME_D1, 'Daily'],
                        1: [mt5.TIMEFRAME_W1, 'Week'], 
                        2: [mt5.TIMEFRAME_MN1, 'Monthly'],
                        3: [mt5.TIMEFRAME_H1, '1 Hour'], 
                        4: [mt5.TIMEFRAME_M30, '30 Minute'], 
                        5: [mt5.TIMEFRAME_M15, '15 Minute'], 
                        6: [mt5.TIMEFRAME_M10, '10 Minute'], 
                        7: [mt5.TIMEFRAME_M5, '5 Minute'],
                        8: [mt5.TIMEFRAME_M2, '2 Minute']}
        return timeframe_mt5

    def save_data(self, data_frame, file_name, paste_name):
        path = 'c:\\Users\\Erik\\Documents\\Python Scripts\\Python Basic\\Python Exercicios\\trading_manager'
        path = path + '\\{}'.format(paste_name)

        if not os.path.exists(path):
                os.makedirs(path)

        save_file_path = os.path.join(path, file_name)
        if os.path.exists(save_file_path):
            print("Já existe arquivo salvo!!!")
        else:
            data_frame.to_csv(save_file_path, index=False)