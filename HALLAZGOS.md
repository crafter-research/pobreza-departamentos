# Pobreza por departamento: hallazgos al 2026-11-15
Fuente pobreza: INEI, Evolución de la pobreza monetaria 2015-2024 (cuadro 3.1). Factores: quipu (gasto 2025), datos-pe (cobertura OSIPTEL, zonas críticas, emergencias hídricas). 23 departamentos (sin Lima Metropolitana, Lima 2/ ni Callao). Scripts: extraer.py, factores.py. Tabla: factores_departamento.csv.

1. Huancavelica redujo 11,8 pts (45,2→33,4 %), 3.º mayor descenso; sigue sobre el nacional (27,6 %).
2. Convergencia: cambio vs nivel inicial rho = -0,60. Quien partía más alto bajó más.
3. Descontando el nivel inicial, Huancavelica bajó 4,9 pts MÁS de lo esperado (junto a Amazonas, Apurímac, Lambayeque, Ica, San Martín). Por debajo de lo esperado: Loreto, Ucayali, Tumbes, Puno, Huánuco, Pasco.
4. Gasto subnacional per cápita 2025, ejecución, saneamiento, educación, 4G: ninguno se asocia con el cambio tras descontar el nivel inicial (|rho| < 0,26; umbral 0,41 con n=23). Único borderline: emergencias hídricas por 100 mil hab. (rho -0,40).
LÍMITES: gasto 2025 es una foto posterior al periodo; n=23; asociaciones no causales. Para explicar hacen falta microdatos ENAHO (composición del ingreso: empleo asalariado, agro, transferencias, remesas) y series de gasto 2015-2024.

## ENAHO (Sumaria 2015-2024, descargada 2026-11-15; enaho.py, comparar.py)
Validación: la pobreza recalculada con factor07*mieperho reproduce el INEI al centésimo (Huancavelica 45,16 / 36,91 / 33,40; Cajamarca, Puno, Apurímac igual). Componentes de ingreso reconstruyen ~83 % de inghog1d (el resto: imputaciones no listadas).
Comparación de 6 deptos que redujeron MÁS de lo esperado (Amazonas, Apurímac, Lambayeque, Ica, San Martín, Huancavelica) vs 6 que redujeron MENOS (Loreto, Ucayali, Tumbes, Puno, Huánuco, Pasco). Ingreso mensual per cápita (S/ nominales), promedio 2015-16 → 2023-24:
- Crecimiento del ingreso: +56 % vs +31,5 %.
- Trabajo dependiente: +116 vs +77. Trabajo independiente: +103 vs +43.
- Transferencias públicas: +10,2 vs +10,0 (iguales). Remesas del exterior: ~0 en ambos.
- Huancavelica: S/298 → S/509 (+70,7 %), +105 dependiente, +82 independiente, +10 transf. públicas.
LÍMITES: n=6 vs 6; nominal (misma inflación nacional); Sumaria no dice el sector (agro/minería/servicios): falta módulo 500 (empleo) para eso.

## ENAHO empleo (módulo 500, 2015-2024; empleo.py, comparar_empleo.py)
Ocupados (ocu500=1, fac500a), sector por CIIU rev.4 (p506r4), ingreso laboral mensual = (i524a1+i530a)/12 entre quienes declaran ingreso>0. Promedios 2015-16 → 2023-24.
- La estructura del empleo casi no cambió en ningún grupo (cambios de 1-2 pts por sector, salvo Huancavelica agro 65→59 %).
- Ingreso laboral medio por ocupado: grupo MÁS +43 % (S/806→1154); MENOS +35 % (S/727→983); Huancavelica +66 % (S/421→700).
- Fuera del agro el grupo MÁS creció mucho más: transporte +38 vs +16 %, hoteles/rest. +38 vs +19, construcción +30 vs +15, comercio +29 vs +23, minería +63 vs +28. Agro similar (+68 vs +77 %).
- Huancavelica: sigue 59 % del empleo en agro con S/377 al mes (S/208 antes); trabajo familiar no remunerado 32→23 %; comercio +106 % (S/343→705).
LÍMITES: celdas depto×sector chicas (minería ~2 % de ocupados); el ingreso medio excluye a quien no declara ingreso; nominal; asociación, no causa.
