from gzip import decompress  # для декодинга
from bs4 import BeautifulSoup  # для парсинга
import pypyodbc as odbs  # для работы с БД
from dadata import Dadata  # для стандартизации адреса
import config  # конфиги

# настройка подключения к серверу БД
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = config.SERVER_NAME
DATABASE_NAME = config.DATABASE_NAME

con_str = f'''
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
'''

# подключение к БД и объявление указателя
conn = odbs.connect(con_str)
cursor = conn.cursor()

# запрос на создание таблицы для сущности Debtor
create_table_Debtor_query = '''
    CREATE TABLE Debtor (
        [name] VARCHAR(255) PRIMARY KEY,
        birth_date DATE,
        birth_place VARCHAR(255),
        postal_code VARCHAR(6) NULL,
        federal_district VARCHAR(128) NULL, 
        region VARCHAR(128) NULL,
        area VARCHAR(128) NULL,
        city VARCHAR(128) NULL,
        settlement VARCHAR(128) NULL,
        street VARCHAR(50) NULL,
        house VARCHAR(5) NULL,
        block VARCHAR(10) NULL,
        flat VARCHAR(5) NULL,
        inn VARCHAR(16) NULL
    )
'''

# запрос на создание таблицы для сущности Bank
create_table_Bank_query = '''
    CREATE TABLE Bank (
        id INT IDENTITY(1,1) PRIMARY KEY,
        [name] VARCHAR(255),
        bik VARCHAR(9)
    )
'''

# запрос на создании таблицы для сущности MonetaryObligation
create_table_MonetaryObligation_query = '''
    CREATE TABLE MonetaryObligation (
        id INT IDENTITY(1,1) PRIMARY KEY,
        message_id VARCHAR(255),
        FOREIGN KEY (message_id) REFERENCES ExtrajudicialBankruptcyMessage(id),
        creditor_name VARCHAR(255),
        content VARCHAR(255),
        basis VARCHAR(1028),
        total_sum FLOAT,
        debt_sum FLOAT NULL,
        penalty_sum FLOAT NULL,
    )
'''

# запрос на создание таблицы для сущности ObligatoryPayment
create_table_ObligatoryPayment_query = '''
    CREATE TABLE ObligatoryPayment (
        id INT IDENTITY(1,1) PRIMARY KEY,
        message_id VARCHAR(255),
        FOREIGN KEY (message_id) REFERENCES ExtrajudicialBankruptcyMessage(id),
        [name] VARCHAR(255),
        [sum] FLOAT 
    )
'''

# запрос на создание таблицы для сущности Publisher
create_table_Publisher_query = '''
    CREATE TABLE Publisher (
        [name] VARCHAR(255) PRIMARY KEY,
        inn VARCHAR(255),
        ogrn VARCHAR(255)
    )
'''

# запрос на создание таблицы для сущности PreviousName
create_table_PreviousName_query = '''
    CREATE TABLE PreviousName (
        name_now VARCHAR(255),
        previous_name VARCHAR(255)
    )
'''

# запрос на создание таблицы для сущности ExtrajudicialBankruptcyMessage
create_table_ExtrajudicialBankruptcyMessage_query = '''
    CREATE TABLE ExtrajudicialBankruptcyMessage (
        id VARCHAR(255) PRIMARY KEY,
        [number] VARCHAR(255),
        [type] VARCHAR(255),
        publish_date DATE,
        debtor_name VARCHAR(255), 
        FOREIGN KEY (debtor_name) REFERENCES Debtor([name]),
        publisher_name VARCHAR(255), 
        FOREIGN KEY (publisher_name) REFERENCES Publisher([name]),
        finish_reason VARCHAR(255)
    )
'''

# выполнение запросов
cursor.execute(create_table_Debtor_query)
cursor.execute(create_table_PreviousName_query)
cursor.execute(create_table_Publisher_query)
cursor.execute(create_table_ExtrajudicialBankruptcyMessage_query)
cursor.execute(create_table_Bank_query)
cursor.execute(create_table_MonetaryObligation_query)
cursor.execute(create_table_ObligatoryPayment_query)
# коммит изменений
conn.commit()

# открытие файла в виде потока байтов
file = open('ExtrajudicialData.xml.gz', 'rb')

# декодинг файла, получение строки
data = str(decompress(file.read()), 'utf-8')

# подготовка к парсингу
soup = BeautifulSoup(data, 'xml')

# про config -> читать README
DADATA_TOKEN = config.DADATA_TOKEN
DADATA_SECRET = config.DADATA_SECRET
dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

# парсинг сущности Debtor и добавление в таблицу каждого объекта, а также заполнение таблицы с предыдущими именами
debtors = soup.find_all('Debtor')
for debtor in debtors:
    soup_debtor = BeautifulSoup(str(debtor), 'xml')
    name = soup_debtor.find('Name').text
    birth_date = soup_debtor.find('BirthDate').text
    birth_place = soup_debtor.find('BirthPlace').text
    address = soup_debtor.find('Address').text
    clean_address = dadata.clean('address', address)
    postal_code = clean_address['postal_code']
    federal_district = clean_address['federal_district']
    region = clean_address['region']
    area = clean_address['area']
    city = clean_address['city']
    settlement = clean_address['settlement']
    street = clean_address['street']
    house = clean_address['house']
    block = clean_address['block']
    flat = clean_address['flat']
    inn = soup_debtor.find('Inn')
    inn = inn if not inn else inn.text
    previous_names = soup_debtor.find_all('PreviousName')
    cursor.execute(f'''
                INSERT INTO Debtor ([name], birth_date, birth_place, postal_code, federal_district,
                region, area, city, settlement, street, house, block, flat, inn)
                VALUES
                ('{name}', '{birth_date}', '{birth_place}', '{postal_code}', '{federal_district}', '{region}', '{area}', '{city}',
                '{settlement}', '{street}', '{house}', '{block}', '{flat}', '{inn}');

            ''')
    if previous_names:
        for previous_name in previous_names:
            soup_previous_name = BeautifulSoup(str(previous_name), 'xml')
            cursor.execute(f'''
                INSERT INTO PreviousName (name_now, previous_name)
                VALUES ('{name}', '{soup_previous_name.find('Value').text}')
            ''')
    conn.commit()

banks = soup.find_all('Bank')
for bank in banks:
    soup_bank = BeautifulSoup(str(bank), 'xml')
    name = soup_bank.find('Name').text
    bik = soup_bank.find('Bik')
    bik = bik if not bik else bik.text
    cursor.execute(f'''
        INSERT INTO Bank ([name], bik)
        SELECT '{name}', '{bik}'
        WHERE NOT EXISTS (SELECT 1 FROM Bank WHERE bik = '{bik}');
    ''')
    conn.commit()

publishers = soup.find_all('Publisher')
for publisher in publishers:
    soup_publisher = BeautifulSoup(str(publisher), 'xml')
    name = soup_publisher.find('Name').text
    inn = soup_publisher.find('Inn')
    inn = inn if not inn else inn.text
    ogrn = soup_publisher.find('Ogrn')
    ogrn = ogrn if not ogrn else ogrn.text
    cursor.execute(f'''
                    INSERT INTO Publisher ([name], inn, ogrn)
                    SELECT '{name}', '{inn}', '{ogrn}'
                    WHERE NOT EXISTS (SELECT 1 FROM Publisher WHERE [name] = '{name}');
                ''')
    conn.commit()

DADATA_TOKEN = config.DADATA_TOKEN
DADATA_SECRET = config.DADATA_SECRET
dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

messages = soup.find_all('ExtrajudicialBankruptcyMessage')
for message in messages:
    soup_message = BeautifulSoup(str(message), 'xml')
    message_id = soup_message.find('Id').text
    number = soup_message.find('Number').text
    message_type = soup_message.find('Type').text
    publish_date = soup_message.find('PublishDate').text
    soup_message_debtor = BeautifulSoup(str(soup_message.find('Debtor')), 'xml')
    debtor_name = soup_message_debtor.find('Name').text
    soup_message_publisher = BeautifulSoup(str(soup_message.find('Publisher')), 'xml')
    publisher_name = soup_message_publisher.find('Name').text
    finish_reason = soup_message.find('FinishReason')
    finish_reason = finish_reason if not finish_reason else finish_reason.text
    cursor.execute(f'''
        INSERT INTO ExtrajudicialBankruptcyMessage (id, [number], [type], publish_date, debtor_name, 
        publisher_name, finish_reason)
        VALUES ('{message_id}', '{number}', '{message_type}', '{publish_date}', '{debtor_name}', '{publisher_name}', '{finish_reason}');
    ''')
    conn.commit()
    obligatory_payments = soup_message.find_all('ObligatoryPayment')
    if obligatory_payments:
        for payment in obligatory_payments:
            soup_payment = BeautifulSoup(str(payment), 'xml')
            name = soup_payment.find('Name')
            name = name if not name else name.text
            summ = soup_payment.find('Sum')
            summ = 0.0 if not summ else float(summ.text)
            cursor.execute(f'''
                            INSERT INTO ObligatoryPayment (message_id, [name], [sum])
                            VALUES ('{message_id}', '{name}', '{summ}');
                        ''')
            conn.commit()
    monetary_obligations = soup_message.find_all('MonetaryObligation')
    if monetary_obligations:
        for obligation in monetary_obligations:
            soup_obligation = BeautifulSoup(str(obligation), 'xml')
            creditor_name = soup_obligation.find('CreditorName')
            creditor_name = creditor_name if not creditor_name else creditor_name.text
            content = soup_obligation.find('Content')
            content = content if not content else content.text
            basis = soup_obligation.find('Basis')
            basis = basis if not basis else basis.text
            total_sum = soup_obligation.find('TotalSum')
            total_sum = total_sum if not total_sum else float(total_sum.text)
            debt_sum = soup_obligation.find('DebtSum')
            debt_sum = 0.0 if not debt_sum else float(debt_sum.text)
            penalty_sum = soup_obligation.find('PenaltySum')
            penalty_sum = 0.0 if not penalty_sum else float(penalty_sum.text)
            cursor.execute(f'''
                        INSERT INTO MonetaryObligation (message_id, creditor_name, content, basis, total_sum, debt_sum, penalty_sum)
                        VALUES 
                        ('{message_id}', '{creditor_name}', '{content}', '{basis}', '{total_sum}', 
                        '{debt_sum}', '{penalty_sum}');
                    ''')
            conn.commit()

cursor.close()
conn.close()
