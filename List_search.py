'''
Searches for a specific unit in the data we got from a Google sheet

'''



def phone_search(phone_number,Phones_list):
    '''
    searches for the phone number in the phone list and returns row index, which is list index+1

    Required args: phone_number as string (e.g'79119973252')
                and Phones_list as list of lists (e.g. [['телефон'], [], ['79992489059']])
    If none is found, retuns None (class 'NoneType')

    '''
    phone_number_ls=[]
    phone_number_ls.append(phone_number)

    if phone_number_ls in Phones_list: #Смотрим, есть ли полученный от юзера номер в списке
        print('victory! номер найден в первой итерации')
        idx=Phones_list.index(phone_number_ls) #Индекс найденного элемента списка
        print('row index is {}'.format(idx+1))
        return idx+1

    else:
        print('Номер не найден. Проверяю в другом формате')
        for phone in Phones_list:
            if len(phone)!=0 and len(phone[0])>9:
                raw_number=phone[0][-10:]#Будем сравнивать только последние 10 цифр номера

                if raw_number==phone_number[-10:]:
                    print('номер найден в другом формате записи')
                    idx=Phones_list.index(phone) #Индекс найденного элемента списка
                    print('row index is {}'.format(idx+1))
                    return idx+1
        print('Этого номера нет в списке')
        return None



def name_search(gotten_name,Names_list):
    '''
    searches for the gotten_name in the Names_list and returns dict of {row: 'name'}

    Required args: gotten_name (which has to be a surname) as string (e.g'Агафонова')
            and Names_list as list of lists (e.g. [['Агафонова Ольга'], ['Азанов Максим']])
    Compares gotten_name with the respective first characters of each item in the list.
    Case insensitive.

    If one match or many is found, all names and their indeces are returned as dictionary,
            where the row index is the key and the full name is the value
            (e.g: {2: 'Агафонова Ольга'}.

    If none is found, retuns None (class 'NoneType')

    '''

    name_len=len(gotten_name)
    gotten_name=gotten_name.lower()
    namesake={}

    for name in Names_list:

        if name[0][0:name_len].lower()==gotten_name:
            idx=Names_list.index(name) #Индекс найденного элемента списка
            print('Victory! \nRow index is {}'.format(idx+1))
            namesake[idx+1]=name[0]#сразу ряд в таблице, не нужно инкрементировать

    if len(namesake)!=0:
##        for item in namesake.items():
##            print(item)
##        print(namesake)
        return namesake

    else:
        print('Этой фамилии нет в списке')
        return None


