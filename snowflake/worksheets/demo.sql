SELECT * FROM anuncios_db.bronce.anuncios WHERE tipo='casa'

SELECT * FROM anuncios_db.bronce.range_table


SELECT
  tipo,
  operacion,
  SUM(costo) AS total_costo
FROM
  anuncios
WHERE
  divisa ILIKE '%MXN%'
GROUP BY
  tipo,
  operacion
ORDER BY
  total_costo DESC;