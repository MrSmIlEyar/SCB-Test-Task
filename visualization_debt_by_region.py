import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pypyodbc as odbs  # для работы с БД
import config

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

query = '''
    SELECT
        Debtor.region,
        SUM(MonetaryObligation.debt_sum) as total_debt
    FROM
        ExtrajudicialBankruptcyMessage
    JOIN
        MonetaryObligation
    ON
        ExtrajudicialBankruptcyMessage.id = MonetaryObligation.message_id
    JOIN
        Debtor
    ON
        Debtor.[name] = ExtrajudicialBankruptcyMessage.debtor_name
    GROUP BY
        Debtor.region
    ORDER BY
        total_debt
'''

df = pd.read_sql(query,
                 conn)  # тут возникает UserWarning, но это предупреждение говорит лишь о том, что pandas поддерживает лишь SQLAlchemy

conn.close()

plt.figure(figsize=(20, 10))  # устанавливаем размер графика

ax = sns.barplot(x='region', y='total_debt', data=df)  # создаём диаграмму на основе данных

plt.xticks(rotation=45)  # поворачиваем названия регионов на 45 градусов, чтобы они полностью вмещались

plt.title('Debt by Region')  # устанавливаем название графика
plt.ylabel('')  # устанавливаем подпись оси y

# добавляем суммы над столбцами
for p in ax.patches:
    width, height = p.get_width(), p.get_height()  # шрирна и высота столбца
    x, y = p.get_xy()  # координата столбца
    ax.text(x + width / 2,  # координата x относительно столбца
            y + height + 10,  # координата y относительно столбца
            f'{height:,.2f}',  # округляем до 2 знаков после запятой
            ha='center',  # выравнивание по центру
            va='bottom',  # выравнивание по нижнему краю
            fontsize=8)  # размер шрифта
plt.show()
