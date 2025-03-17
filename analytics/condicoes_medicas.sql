SELECT
  ch.entry.resource.code.text AS CONDITION,
  count(ch.entry.resource.code.text) AS qtd_condition
FROM
  clinic.main.clinic_history ch
WHERE
  ch.entry.resource.resourceType = 'Condition'
GROUP BY
  ch.entry.resource.code.text
ORDER BY
  2 DESC
LIMIT
  10