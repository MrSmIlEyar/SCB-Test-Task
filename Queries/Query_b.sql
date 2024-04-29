USE SCB;

SELECT TOP 10
    Debtor.[name] AS [name],
    Debtor.inn AS inn,
    SUM(debt_sum) AS debt
FROM
    MonetaryObligation
JOIN
    ExtrajudicialBankruptcyMessage
ON
    ExtrajudicialBankruptcyMessage.id = MonetaryObligation.message_id
JOIN
    Debtor
ON
    Debtor.[name] = ExtrajudicialBankruptcyMessage.debtor_name
GROUP BY
    Debtor.[name],
    Debtor.inn
ORDER BY
	debt DESC;

