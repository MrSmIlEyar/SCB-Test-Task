USE SCB;

SELECT
	Debtor.[name],
	Debtor.inn,
	COALESCE((SUM(ObligatoryPayment.[sum]) * 100) / SUM(MonetaryObligation.total_sum), 0) AS [percent]
FROM
	Debtor
JOIN
	ExtrajudicialBankruptcyMessage
ON
	Debtor.[name] = ExtrajudicialBankruptcyMessage.debtor_name
LEFT JOIN
	MonetaryObligation
ON
	ExtrajudicialBankruptcyMessage.id = MonetaryObligation.message_id
LEFT JOIN
	ObligatoryPayment
ON
	ExtrajudicialBankruptcyMessage.id = ObligatoryPayment.message_id
GROUP BY
	Debtor.[name],
	Debtor.inn
ORDER BY
	[percent] DESC;