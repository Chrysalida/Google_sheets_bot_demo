'''
Чтение данных из гугл-листов
Функция рабочая на 30.12.20, со второй, новой таблицей Дока

'''

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

import BB_config
from BB_config import BB2_sheet_ID, Phones_range#Читает из второй, новой таблицы


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def BB_GSh_read(Range='A1:AA1000'):#без аргументов выдает всю таблицу

    '''
    принимает диапазон, выдает его значения

    input: range as string, e.g. 'A1:AA1000'
    output: list of lists, e.g. [['Контакты'],[],['89118113939']]

    '''

    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES) #the name of downloaded JSON file with client_secret and some other data
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=BB2_sheet_ID,
                                range=Range).execute()
    values_input = result_input.get('values', [])
    #Возвращает список списков, где [0] - заголовки,а последующие списки - данные

    if not values_input and not values_expansion:
        print('No data found.')

    return values_input



###Проверка коннекта, выдает данные с листа

##a=BB_GSh_read()
##print('no args, full data: ',a)
##
##b=BB_GSh_read(Phones_range)
##print('single column: ',b)