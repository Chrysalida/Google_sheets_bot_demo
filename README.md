Бот для действующей благотворительной медицинской организации, (порядка 160 человек).
Задача: получение данных из Гугл-таблиц и запись в таблицы прямо из Телеграма. 
Это публичная версия модулей, отсутствует вся чувствительная информация. 

Реализованные функции: 
1. Знакомство: бот спрашивает ваши контакты, по ним находит вас в списке волонтеров, записывает в список ваш ID
2. Рассылка по различным спискам: Вы отправляете боту сообщение, он предлагает разослать по следующим спискам: медики, немедики, все. 
В зависимости от выбора пользователя бот формирует список (по Гугл-таблице проверяя актуальную медицинскую категорию участников) и рассылает сообщение. 
После рассылки отчитывается автору о количестве получателей. Об ошибках отчитывается админу. Работа логгируется.

В процессе разработки: связь с чатами Вконтакте. 
