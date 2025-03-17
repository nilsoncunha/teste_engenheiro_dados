SELECT
	ch.entry.resource.gender as gender,
	count(ch.entry.resource.gender) as qtd_gender
FROM
	clinic.main.clinic_history ch
WHERE
	ch.entry.resource.resourceType = 'Patient' and
	ch.entry.resource.gender = 'male'
GROUP BY
	ch.entry.resource.gender
ORDER BY
	2 DESC
LIMIT
	10