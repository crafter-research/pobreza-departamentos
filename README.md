# Pobreza por departamento, Perú 2015-2024

¿Qué separa a los departamentos que reducen pobreza de los que se estancan? Informe de trabajo con datos oficiales del INEI.

**Informe:** `index.html` (autocontenido). **Resumen y límites:** `HALLAZGOS.md`.

## Resultado en corto
- Huancavelica sí redujo pobreza: 45,2 % → 33,4 % (−11,8 puntos), tercer mayor descenso.
- Quien partía más alto bajó más (ρ = −0,60). Descontado eso, Huancavelica bajó 4,9 puntos más de lo esperado.
- Gasto público por habitante, ejecución, cobertura 4G y zonas críticas no explican el cambio (ninguno sale de la banda ±0,41; emergencias hídricas y gasto agropecuario la rozan).
- La diferencia entre los 6 departamentos que redujeron más y los 6 que redujeron menos está en el ingreso por trabajo (+S/ 103 vs +S/ 43 en independiente; +S/ 116 vs +S/ 77 en dependiente), no en transferencias (+S/ 10 en ambos).
- Es una asociación con 6 contra 6 departamentos, no una causa.

## Verificación
La pobreza recalculada con microdatos ENAHO (factor07 × mieperho, `pobreza` ∈ {1,2}) reproduce las cifras oficiales del INEI al centésimo.

## Datos y cómo reproducir
Fuentes: INEI, *Evolución de la pobreza monetaria 2015-2024* (anexo estadístico, cuadro 3.1) y ENAHO 2015-2024 módulos 34 (Sumaria) y 05 (Empleo), descargados de proyectos.inei.gob.pe/microdatos (STATA; no se incluyen aquí). Gasto 2025: quipu. Cobertura, zonas críticas y emergencias hídricas: datos abiertos OSIPTEL, INGEMMET y PCM.

Orden: `extraer.py` → `factores.py` → `enaho.py` → `comparar.py` → `empleo.py` → `comparar_empleo.py` → `informe.py`. Las rutas apuntan a `raw/` y `enaho_raw/` (ignoradas por git).

## Límites
Asociaciones, no causas. 23 departamentos (sin Lima Metropolitana, Lima provincias ni Callao). Celdas departamento por sector pequeñas. Ingresos nominales. El gasto es de 2025.
