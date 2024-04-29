import pandas as pd
import pypyodbc as odbs  # для работы с БД
import matplotlib.pyplot as plt
import seaborn as sns
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

sql_query = """
    WITH DebtorAge AS (
        SELECT
            Debtor.[name],
            DATEDIFF(year, Debtor.birth_date, GETDATE()) AS age,
            MonetaryObligation.debt_sum
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
    )
    SELECT
        CASE
            WHEN age < 20 THEN '0-19'
            WHEN age < 30 THEN '20-29'
            WHEN age < 40 THEN '30-39'
            ELSE '40+'
        END AS age_group,
        SUM(debt_sum) AS total_debt
    FROM
        DebtorAge
    GROUP BY
        CASE
            WHEN age < 20 THEN '0-19'
            WHEN age < 30 THEN '20-29'
            WHEN age < 40 THEN '30-39'
            ELSE '40+'
        END
    ORDER BY
        MIN(age)
"""

df = pd.read_sql(sql_query, conn)
conn.close()
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='age_group', y='total_debt', data=df)  # создаём диаграмму на основе данных
sns.barplot(x='age_group', y='total_debt', data=df)
plt.title('Total Debt by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Total Debt')
for p in ax.patches:
    width, height = p.get_width(), p.get_height()  # ширина и высота столбца
    x, y = p.get_xy()  # координата столбца
    ax.text(x + width / 2,  # координата x относительно столбца
            y + height + 10,  # координата y относительно столбца
            f'{height:,.2f}',  # округляем до 2 знаков после запятой
            ha='center',  # выравнивание по центру
            va='bottom',  # выравнивание по нижнему краю
            fontsize=8)  # размер шрифта
plt.show()
