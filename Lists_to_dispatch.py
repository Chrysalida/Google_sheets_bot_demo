import GSheet_read
import BB_config
from BB_config import Medic_range, Tlg_IDs_range

#given cryteria:
#на данный момент (10.12.20) немедики - это все типы со словом "ассистент". Так и будем проверять.
#координаторы - все кто "координатор"
#медики - это все кроме ассистентов

def lists_to_dispatch():
    '''
    forms 4 lists of tlg IDs to dispatch: medics, NonMedics, Coords & everyone

    takes no args,
    returns a dictionary dispatch_lists_dict of 4 items:
    keys are 'Medics', 'NonMedics', 'Coords' & 'everyone',
    values are lists of Tlg IDs
    '''

    #all volunteers data from Google Sheet
    ID_list=GSheet_read.BB_GSh_read(Tlg_IDs_range)
    status_list=GSheet_read.BB_GSh_read(Medic_range)

    #objects to be formed:

    everyone=[]# это списки непосредственно ID, а не индексов
    Medics_list=[]
    NonMedics_list=[]
    Coord_list=[]

    dispatch_lists_dict={}

    ##print(ID_list)
    ##print('status_list[14][0] =',status_list[14][0])


    for ID in ID_list[1::]: #отсекли нулевой итем, т.к. это заголовок столбца
        if ID!=[]:

            everyone.append(ID[0])
            if status_list[ID_list.index(ID)]!=[]:#если в столбце мед.статуса вообще хоть что-то есть:

                if 'ассист' in status_list[ID_list.index(ID)][0]:
                    NonMedics_list.append(ID[0])
                    if 'коорд' in status_list[ID_list.index(ID)][0]:#ловим тех, кто и коорд и ассист
                        Coord_list.append(ID[0])

                elif 'коорд' in status_list[ID_list.index(ID)][0]:
                    Coord_list.append(ID[0])

                else:
                    Medics_list.append(ID[0])

    dispatch_lists_dict['everyone']=everyone
    dispatch_lists_dict['Medics']=Medics_list
    dispatch_lists_dict['NonMedics']=NonMedics_list
    dispatch_lists_dict['Coords']=Coord_list

##    проверочные принты:
##    print('\neveryone =',everyone)
##    print('\nMedics_list =',Medics_list)
##    print('\nNonMedics_list =',NonMedics_list)
##    print('\nCoord_list =',Coord_list)

    return dispatch_lists_dict




##Проверка функции
##a=lists_to_dispatch()
##print(a)
