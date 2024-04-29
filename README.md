# Тестовое задание 
## Отчёт о проделанной работе

# ВАЖНО

> Для корректной работы кода нужен файл config.py, в нём хранятся 4 переменные:
>
> SERVER_NAME - это имя сервера БД
> 
> DATABASE_NAME - название БД (в моём случае SCB)
> 
> DADATA_TOKEN - токен для взаимодействия с API Dadata
> 
> DADATA_SECRET - секретный ключ для взаимодействия с API Dadata
> 
> ФАЙЛА НЕТ В РЕПОЗИТОРИИ СОГЛАСНО ПРАВИЛАМ ЗАЩИТЫ КОНФИДЕНЦИАЛЬНОЙ ИНФОРМАЦИИ
> 
> НЕОБХОДИМО СОЗДАТЬ И ЗАПОЛНИТЬ ФАЙЛ САМОСТОЯТЕЛЬНО


## Задача 1 

### Декодирование, парсинг .xml файла и запись данных в БД
#### Requirements: bs4 (для парсинга .xml), pypyodbc (для взаимодействия с БД), dadata (для стандартизации адреса)
#### База данных: MS SQL

Решение:

Код декодирования файла, создания таблиц, добавления данных можно увидеть в файле 
>main.py

В ходе анализа выявил 6 сущностей: 

* Debtor
* Publisher 
* Bank
* ObligatoryPayment 
* MonetaryObligation 
* ExtrajudicialBankruptcyMessage

Также посчитал должным выделить предыдущие имена пользователей в отдельную таблицу PreviousName

7 таблиц:

1. _Таблица Debtor:_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/DebtorStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/DebtorResult.png)
<br/><br/>
2. _Таблица PreviousName (many to many):_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/PreviousNameStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/PreviousNameResult.png)
<br/><br/>
3. _Таблица Publisher:_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/PublisherStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/PublisherResult.png)
<br/><br/>
4. _Таблица Bank (уникальность по БИК):_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/BankStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/BankResult.png)
<br/><br/>
5. _Таблица MonetaryObligation:_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/MonetaryObligationStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/MonetaryObligationResult.png)
<br/><br/>
6. _Таблица ObligatoryPayment:_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img_1.png](README_img/ObligatoryPaymentStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img_1.png](README_img/ObligatoryPaymentResult.png)
<br/><br/>
7. _Таблица ExtrajudicialBankruptcyMessage:_
    <br/><br/>
    Структура:
    <br/><br/>
    ![img.png](README_img/ExtrajudicialBankruptcyMessageStructure.png)
    <br/><br/>
    Результат:
    <br/><br/>
    ![img.png](README_img/ExtrajudicialBankruptcyMessageResult.png)
<br/><br/>
## Задача 2
### SQL запросы

Код запросов представлен в папке
>Queries

Решение:


- Запрос a:

    ![img.png](README_img/Query_a.png)
<br/><br/>
- Запрос b:

    ![img.png](README_img/Query_b.png)
<br/><br/>
- Запрос c:

    ![img.png](README_img/Query_c.png)
<br/><br/>
## Задача 3
### Визуализация данных
#### Requirements: pandas, matplotlib, seaborn

Код задач представлен в файлах
>visualization_debt_by_region.py
> 
>visualization_debt_by_region.py 

Результат 1 визуализации:

![img.png](README_img/debt_by_region_show.png)


Результат 2 визуализации:

![img.png](README_img/debt_by_age_show.png)