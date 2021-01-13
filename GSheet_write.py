'''
Запись данных на гугл-лист
Функция рабочая на 30.12.20, со второй, новой таблицей Дока

'''

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

import BB_config
from BB_config import BB2_sheet_ID, My_sheet_ID

Sheet_to_write=BB2_sheet_ID #чтобы менять лист для записи только в одном месте,
                            #! при замене менять и строку принта внизу

#print('Document to write: BB2_sheet_ID')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def BB_GSh_write(cell="Лист1!Z1",data="WORKED"):
    '''
    writes given data into the specified cell

    cell as double-quoted string, e.g. "Лист1!B2:D5"
    data as double-quoted string, e.g. "=sin(3,14/2)"
    '''

    global service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    try:
        print('trying: writing to the GoogleSheet')
        results = sheet.values().batchUpdate(spreadsheetId = Sheet_to_write, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": cell,
                 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                 "values": [[data]]}
            ]
        }).execute()
        print("YEASSS BITCHES")
        return True
        #print(results)#operation summary

    except:
        print('WHATTA FUCK')
        return False

#BB_GSh_write()

#РАБОТАЮЩИЙ ПАК НА ЗАПОЛНЕНИЕ НЕСКОЛЬКИХ ЯЧЕЕК
##    service = build('sheets', 'v4', credentials=creds)
##
##    sheet = service.spreadsheets()
##        results = sheet.values().batchUpdate(spreadsheetId = Sheet_to_write, body = {
##            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
##            "data": [
##                {"range": "Лист1!B2:D5",
##                 "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
##                 "values": [
##                            ["Ячейка B2", "Ячейка C2", "Ячейка D2"], # Заполняем первую строку
##                            ['25', "=6*6", "=sin(3,14/2)"]  # Заполняем вторую строку
##                           ]}
##            ]
##        }).execute()