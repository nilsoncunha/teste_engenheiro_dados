SELECT
	ch.entry.resource.medicationCodeableConcept.text as medication,
	count(ch.entry.resource.medicationCodeableConcept.text) as qtd_medication
FROM
	clinic.main.clinic_history ch
WHERE
	ch.entry.resource.resourceType = 'MedicationRequest'
GROUP BY
	ch.entry.resource.medicationCodeableConcept.text
ORDER BY
	2 DESC
LIMIT
	10