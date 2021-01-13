import GSheet_read
import BB_config
from BB_config import Medic_range, Tlg_IDs_range

#given cryteria:
#на данный момент (10.12.20) немедики - это все типы со словом "ассистент". Так и будем проверять.
##nonmedic_types=['ассистент (+студенты мед.вузов до 4 курса)','координатор-ассистент (+студенты мед.вузов до 4 курса)']
##medic_types=[]# = все типы, если не пусто и не ассистент

def lists_to_dispatch():
    '''
    forms 3 lists of tlg IDs to dispatch: medics, NonMedics & everyone

    takes no args,
    returns a dictionary dispatch_lists_dict of 3 items:
    keys are 'Medics', 'NonMedics' & 'everyone',
    values are lists of Tlg IDs
    '''

    #all volunteers data from Google Sheet
    ID_list=GSheet_read.BB_GSh_read(Tlg_IDs_range)
    status_list=GSheet_read.BB_GSh_read(Medic_range)

    #objects to be formed:
##    #indexes=[]# порядковые индексы итемов ссписка, возможно, это лишний список

    everyone=[]# это списки непосредственно ID, а не индексов
    Medics_list=[]
    NonMedics_list=[]

    dispatch_lists_dict={}

    ##print(ID_list)
    ##print('status_list[14][0] =',status_list[14][0])


    for ID in ID_list[1::]: #отсекли нулевой итем, т.к. это заголовок столбца
        if ID!=[]:
##            #indexes.append(ID_list.index(ID))#возможно, это лишняя строка
            everyone.append(ID[0])
            if status_list[ID_list.index(ID)]!=[]:
                if 'ассист' in status_list[ID_list.index(ID)][0]:
                    NonMedics_list.append(ID[0])

                else:
                    Medics_list.append(ID[0])

    dispatch_lists_dict['everyone']=everyone
    dispatch_lists_dict['Medics']=Medics_list
    dispatch_lists_dict['NonMedics']=NonMedics_list

    return dispatch_lists_dict



##проверочные принты:
##print('indexes =',indexes)
##print('everyone =',everyone)
##print('Medics_list =',Medics_list)
##print('NonMedics_list =',NonMedics_list)
##
##print('\ndispatch_lists_dict =',dispatch_lists_dict)
##print(dispatch_lists_dict['Medics'])
##for medic in dispatch_lists_dict['Medics']:
##    print(medic)


##Проверка функции
##a=lists_to_dispatch()
##print(a)



