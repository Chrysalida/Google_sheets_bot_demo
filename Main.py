'''
09.12.20:
    работающая версия

'''


# -*- coding: utf-8 -*-
import logging as log
from BB_config import TOKEN, Logpath, \
                      Full_table, Phones_range, Name_range, \
                      Medic_range, Tlg_IDs_range
import telebot
from telebot import types
import time
import GSheet_read
import List_search
import GSheet_write
import Lists_to_dispatch


bot = telebot.TeleBot(TOKEN)
log.basicConfig(filename=Logpath,level=log.INFO, format='%(asctime)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')

write_success=False #для отслеживания успеха записи данных на лист
admin_ID='ID'#Мой ID, сюда будем слать всякую важную инфу

write_ID_failed_msg='Не удалось записать пользователя {} на лист'
Start_and_Greeting = 'Добро пожаловать! \nЭтот бот нужен для всяких полезных штук.'


@bot.message_handler(commands=['start'])#Просим юзера поделиться контактом
def Start_handler(message):
    log.info(
            '\n Incoming message: '+ str(message.text) + ' from: ID '+ str(message.from_user.id) +
            ' ' + str(message.from_user.first_name) + ' @' + str(message.from_user.username ))

    print('User {} pressed "/Start" '.format(message.chat.first_name))

    keyboard2=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=False);
    requester=types.KeyboardButton("Отправить контакт",request_contact=True)
    keyboard2.add(requester)

    Confirm2='Здравствуйте!\nПожалуйста, поделитесь со мной вашим контактом, чтобы я смог найти вас в списке'
    bot.send_message(message.from_user.id,text=Confirm2, reply_markup=keyboard2)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    '''

    Берем из контакта телефонный номер, ищем его в таблице волонтеров.
    Если находим, сообщаем юзеру, кто он такой.
    Если не находим, спрашиваем фамилию, запускаем next_step_handler

    '''
    log.info('\n_ _ _ _ _ _ _ _ _ _ _ _ _ INCOMING CONTACT _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ')
    log.info(
            'Incoming contact: '+ str(message.text) + ' from: ID '+ str(message.from_user.id) +
            ' ' + str(message.from_user.first_name) + ' @' + str(message.from_user.username ))

    global phone_number;
    global Phones_list;
    global user_row

    remove_btn = types.ReplyKeyboardRemove(selective=False)

    phone_number=message.contact.phone_number
    contact_confirm='Ищу номер телефона {} в списке волонтеров...'.format(phone_number)
    bot.send_message(message.from_user.id,contact_confirm,reply_markup=remove_btn)

    Phones_list=GSheet_read.BB_GSh_read(Phones_range)#Получаем список телефонов волонтеров из Гугл-листа
    phone_result=List_search.phone_search(phone_number,Phones_list)#Ищем полученный номер в этом списке



    #ТЕПЕРЬ: если результат не None, выдаем волонтеру его имя
    #Если None - сообщаем об этом и рекомендуем обратиться к админу
    if phone_result!=None:#then it's an integer
        #БЛОК ЗНАКОМСТВА 1: КОНТАКТ НАЙДЕН

        Found_Name=GSheet_read.BB_GSh_read('Медики!A{}'.format(phone_result))[0][0]

        user_row=phone_result
        name_confirm= 'Я думаю, что вас зовут {}. Так и записываю...'.format(Found_Name)
        bot.send_message(message.from_user.id,text=name_confirm)

        user_tlg_id=str(message.from_user.id)
        id_location = "Медики!E{}".format(user_row)
        data="{}".format(user_tlg_id)
        print('User tlg data 2 be written: ',repr(id_location),repr(data))

        write_success=GSheet_write.BB_GSh_write(id_location,data)
        if write_success==False:
            bot.send_message(admin_ID,write_ID_failed_msg.format(user_tlg_id))

        bot.send_message(message.from_user.id,Start_and_Greeting)


    else:#if phone_result == None
        bot.send_message(message.from_user.id,'\
                                                Вашего телефона нет в списке.\
                                                 \nДавайте попробуем поискать по фамилии?\
                                                 \n\nПожалуйста, напишите свою фамилию')
        bot.register_next_step_handler(message,Name_handler)


def Name_handler(message):#получили от человека его фамилию
                        #ищем в фамилиях
                        #если нашли - ок, мы поняли, кто это, если нет - пусть пишет админу
                        #если однофамильцы - предлагает выбрать

    global gotten_name;
    gotten_name=message.text

    global Names_list;
    Names_list=GSheet_read.BB_GSh_read(Name_range)

    global result;
    result=List_search.name_search(gotten_name,Names_list)

    global keys_list;
    global user_row;


    if result==None:
        bot.send_message(message.from_user.id,\
        'Похоже, вас совсем-совсем нет в списке.\n Пожалуйста, сообщите об этом админу: @Admin \n\
        Вы все равно можете рассылать оповещения волонтерам, но не будете получать оповещения, отправленные другими')

        bot.send_message(message.from_user.id,Start_and_Greeting)


    elif len(result)==1:#result is like: {2: 'Агафонова Ольга'}

        #БЛОК ЗНАКОМСТВА 2: В СПИСКАХ НАЙДЕНО 1 ИМЯ

        Y_N_keyboard=types.InlineKeyboardMarkup();
        key_yes=types.InlineKeyboardButton(text="Да",callback_data='yes');
        key_no=types.InlineKeyboardButton(text="Нет",callback_data='no');
        Y_N_keyboard.add(key_yes,key_no)

        keys_list=list(result.keys())
        result_name=result[keys_list[0]]
        user_row=keys_list[0]
        name_confirm='вы {}?'.format(result_name)
        bot.send_message(message.from_user.id,text=name_confirm, reply_markup=Y_N_keyboard)

        print('Y_N_keyboard shown to user {}'.format(message.from_user.id))

        @bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data == 'no')
        def Yes_No_handler_name(call):

            if call.data=='yes':

                print('call data Yes received from user {}'.format(call.from_user.id))
                user_tlg_id=str(call.from_user.id)

                bot.send_message(call.from_user.id,'Спасибо, записываю...')
                id_location = "Медики!E{}".format(user_row)
                data="{}".format(user_tlg_id)
                print(repr(id_location),repr(data))

                write_success=GSheet_write.BB_GSh_write(id_location,data)
                if write_success==False:
                    bot.send_message(admin_ID,write_ID_failed_msg.format(user_tlg_id))



            elif call.data=='no':
                bot.send_message(call.from_user.id,\
                'Очень странно.\nПожалуйста, сообщите об этом админу: @Admin.\n\n \
                Вы все равно можете рассылать оповещения волонтерам, \
                но не будете получать оповещения, отправленные другими')

            bot.send_message(call.from_user.id,Start_and_Greeting)


    else: #Найдены 2 однофамильца и более , предлагаем выбрать себя в списке
          #result is like: {2: 'Антонова Анна',  4: 'Анохов Руслан'}

        #БЛОК ЗНАКОМСТВА 3: В СПИСКАХ НАЙДЕНО НЕСКОЛЬКО ИМЕН

        keys_list=list(result.keys())
        values_list=list(result.values())

        name_choice_text='Выберите себя в списке:'
        name_choice_kboard=types.InlineKeyboardMarkup(row_width=2);


        if len(result)==2:
            name_1=values_list[0]
            name_2=values_list[1]
            key_1=types.InlineKeyboardButton(text=name_1,callback_data='1');
            key_2=types.InlineKeyboardButton(text=name_2,callback_data='2');
            name_choice_kboard.add(key_1,key_2)
            bot.send_message(message.from_user.id,text=name_choice_text, reply_markup=name_choice_kboard)


        elif len(result)==3:
            name_1=values_list[0]
            name_2=values_list[1]
            name_3=values_list[2]

            key_1=types.InlineKeyboardButton(text=name_1,callback_data='1');
            key_2=types.InlineKeyboardButton(text=name_2,callback_data='2');
            key_3=types.InlineKeyboardButton(text=name_3,callback_data='3');
            name_choice_kboard.add(key_1,key_2,key_3)
            bot.send_message(message.from_user.id,text=name_choice_text, reply_markup=name_choice_kboard)


        elif len(result)==4:
            name_1=values_list[0]
            name_2=values_list[1]
            name_1=values_list[2]
            name_1=values_list[3]

            key_1=types.InlineKeyboardButton(text=name_1,callback_data='1');
            key_2=types.InlineKeyboardButton(text=name_2,callback_data='2');
            key_3=types.InlineKeyboardButton(text=name_3,callback_data='3');
            key_4=types.InlineKeyboardButton(text=name_4,callback_data='4');
            name_choice_kboard.add(key_1,key_2,key_3,key_4)
            bot.send_message(message.from_user.id,text=name_choice_text, reply_markup=name_choice_kboard)

        else:
            name_1=values_list[0]
            name_2=values_list[1]
            name_1=values_list[2]
            name_1=values_list[3]
            key_1=types.InlineKeyboardButton(text=name_1,callback_data='1');
            key_2=types.InlineKeyboardButton(text=name_2,callback_data='2');
            key_3=types.InlineKeyboardButton(text=name_3,callback_data='3');
            key_4=types.InlineKeyboardButton(text=name_4,callback_data='4');
            name_choice_kboard.add(key_1,key_2,key_3,key_4)

            bot.send_message(message.from_user.id,'были найдены и другие однофамильцы.\n \
                                                Напишите админу, если вашего имени нет в перечисленных.\n \
                                                Связь с админом: @Admin')

            bot.send_message(message.from_user.id,text=name_choice_text, reply_markup=name_choice_kboard)



        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):

            '''
            определяем ряд в зависимости от нажатой юзером кнопки,
            сразу и записываем Telegram-ID юзера в этот ряд
            '''
            user_tlg_id=str(call.from_user.id)

            if call.data=='1':
                user_row=keys_list[0]
                bot.send_message(user_tlg_id,'Спасибо, записываю...')


            elif call.data=='2':
                user_row=keys_list[1]
                bot.send_message(user_tlg_id,'Спасибо, записываю...')


            elif call.data=='3':
                user_row=keys_list[2]
                bot.send_message(user_tlg_id,'Спасибо, записываю...')


            elif call.data=='4':
                user_row=keys_list[3]
                bot.send_message(user_tlg_id,'Спасибо, записываю...')


            #записываем на лист:
            id_location = "Медики!E{}".format(user_row)
            data="{}".format(user_tlg_id)
            print(repr(id_location),repr(data))

            write_success=GSheet_write.BB_GSh_write(id_location,data)
            if write_success==False:
                bot.send_message(admin_ID,write_ID_failed_msg.format(user_tlg_id))

            bot.send_message(message.from_user.id,Start_and_Greeting)



@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    log.info('\n_ _ _ _ _ _ _ _ _ _ _ _ _ INCOMING MESSAGE _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ')
    log.info(
            'Incoming message: '+ str(message.text) + ' from: ID '+ str(message.from_user.id) +
            ' ' + str(message.from_user.first_name) + ' @' + str(message.from_user.username ))

    print("INCOMING MESSAGE "+ str(message.text) + ' from: ID '+ str(message.from_user.id) +
            ' ' + str(message.from_user.first_name) + ' @' + str(message.from_user.username ))

    global mess;
    mess=str(message.text)

    global author_username;
    if message.from_user.username!=None:
        author_username='@'+str(message.from_user.username)
    else:
        author_username=''


#TEST DISPATCHER
    dispatch_keyboard=types.InlineKeyboardMarkup(row_width=1);
    key_Med=types.InlineKeyboardButton(text="только медикам",callback_data='med');
    key_nonMed=types.InlineKeyboardButton(text="немедикам",callback_data='nonmed');
    key_everyone=types.InlineKeyboardButton(text="всем",callback_data='everyone');
    dispatch_keyboard.add(key_Med,key_nonMed,key_everyone)

    question ='Кому разослать ваше сообщение?'
    bot.send_message(message.from_user.id,text=question, reply_markup=dispatch_keyboard)

    print('dispatch_keyboard shown to user {}'.format(message.from_user.id))

    @bot.callback_query_handler(\
                                func=lambda call: \
                                   call.data == 'med'\
                                or call.data == 'nonmed' \
                                or call.data == 'everyone')
    def Dispatcher(call):

        if call.data=='med':

            bot.send_message(call.from_user.id,'Формирую список медиков...')
            dispatch_list=Lists_to_dispatch.lists_to_dispatch()
            dispatch_list=dispatch_list['Medics']

        elif call.data=='nonmed':

            bot.send_message(call.from_user.id,'Формирую список немедиков...')
            dispatch_list=Lists_to_dispatch.lists_to_dispatch()
            dispatch_list=dispatch_list['NonMedics']

        elif call.data=='everyone':

            bot.send_message(call.from_user.id,'Формирую список...')
            dispatch_list=Lists_to_dispatch.lists_to_dispatch()
            dispatch_list=dispatch_list['everyone']

        #НЕЗАВИСИМО ОТ РЕЗУЛЬТАТА, РАССЫЛКА ПО СПИСКУ
        recipients=0
        bot.send_message(call.from_user.id,'Рассылаю...')

        if author_username!='':#если есть юзернейм, то всем сообщаем, кто автор
            for item in dispatch_list:
                try:
                    bot.send_message(item,'Сообщение от {}:'.format(author_username))
                    bot.send_message(item,mess)
                    recipients+=1
                except:
                    bot.send_message(admin_ID,\
                    'ошибка отправки оповещения от автора {} на ID {}'.format(author_username,item))

        else: #если юзернейма нет, то только само сообщение
            for item in dispatch_list:
                try:
                    bot.send_message(item,mess)
                    recipients+=1
                except:
                    bot.send_message(admin_ID,\
                    'ошибка рассылки сообщения на ID {}'.format(item))


        bot.send_message(call.from_user.id,\
        'Ваше сообщение разослано. Получателей: {}'.format(recipients))


def start_working():
    try:
        print('Start working')
        bot.polling(none_stop=True,interval=0)
    except:
        print('Exit working')
        time.sleep(10)
        start_working()


start_working()
