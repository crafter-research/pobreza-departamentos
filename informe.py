import csv, html, unicodedata
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn').strip()
P={norm(r['departamento']):r for r in csv.DictReader(open('pobreza_departamento_2015_2024.csv',encoding='utf-8'))}
F={norm(r['departamento']):r for r in csv.DictReader(open('factores_departamento.csv',encoding='utf-8'))}
NAC=[21.77,20.74,21.70,20.49,20.19,30.13,25.87,27.52,29.05,27.58]
YRS=list(range(2015,2025))
CSS="""
:root{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--grid:#e4e3df;--b:#2a78d6;--o:#eb6834;--g:#8a8984}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--grid:#34332f;--b:#3987e5;--o:#d95926;--g:#8f8e86}}
body{background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif;margin:0;padding:24px 16px}
main{max-width:760px;margin:auto}h1{font-size:26px;line-height:1.2}h2{font-size:19px;margin-top:40px}
p,li{color:var(--ink)}.m{color:var(--ink2);font-size:14px}svg{width:100%;height:auto;display:block}
text{fill:var(--ink2);font:12px system-ui,sans-serif}.l{fill:var(--ink)}.t{font-size:13px}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:6px 8px;border-bottom:1px solid var(--grid);text-align:right}td:first-child,th:first-child{text-align:left}
.k{background:var(--grid);padding:12px 16px;border-radius:8px}
"""
def line_chart():
    W,H,L,R,T,B=720,340,44,150,16,30
    x=lambda i:L+(W-L-R)*i/9; y=lambda v:T+(H-T-B)*(1-v/50)
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Pobreza monetaria 2015-2024: Huancavelica, Apurímac, Cajamarca, Puno y nacional">']
    for v in range(0,51,10): s.append(f'<line x1="{L}" x2="{W-R}" y1="{y(v)}" y2="{y(v)}" stroke="var(--grid)"/><text x="{L-6}" y="{y(v)+4}" text-anchor="end">{v}</text>')
    for i,yr in enumerate(YRS): s.append(f'<text x="{x(i)}" y="{H-8}" text-anchor="middle">{yr}</text>')
    series=[('Huancavelica',[float(P['HUANCAVELICA'][str(k)]) for k in YRS],'var(--b)',3,''),
            ('Apurímac',[float(P['APURIMAC'][str(k)]) for k in YRS],'var(--o)',2,''),
            ('Puno',[float(P['PUNO'][str(k)]) for k in YRS],'var(--ink2)',2,''),
            ('Cajamarca',[float(P['CAJAMARCA'][str(k)]) for k in YRS],'var(--ink2)',2,'5 4'),
            ('Nacional',NAC,'var(--g)',1.5,'2 3')]
    ends=[]
    for n,v,c,w,d in series:
        pts=' '.join(f'{x(i):.1f},{y(a):.1f}' for i,a in enumerate(v))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{d}" stroke-linejoin="round"><title>{n}</title></polyline>')
        ends.append((y(v[-1]),n,v[-1],c))
    ends.sort(); last=-99
    for yy,n,v,c in ends:
        yy=max(yy,last+14); last=yy
        s.append(f'<text class="l t" x="{W-R+8}" y="{yy+4:.1f}">{n} {v:.0f} %</text>')
    s.append('</svg>'); return ''.join(s)
def scatter():
    W,H,L,R,T,B=720,460,48,50,30,40
    xs=[float(P[k]['2015']) for k in P if k in F]; 
    x=lambda v:L+(W-L-R)*(v-0)/58; y=lambda v:T+(H-T-B)*(1-(v+20)/(20+6))  # y in -20..+6? changes from -17 to +9
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Cambio de pobreza 2015-2024 frente a pobreza inicial">']
    y=lambda v:T+(H-T-B)*(1-(v+20)/45)
    for v in range(-20,26,10): s.append(f'<line x1="{L}" x2="{W-R}" y1="{y(v)}" y2="{y(v)}" stroke="var(--grid)"/><text x="{L-6}" y="{y(v)+4}" text-anchor="end">{v:+d}</text>')
    for v in range(0,56,10): s.append(f'<text x="{x(v)}" y="{H-20}" text-anchor="middle">{v}</text>')
    s.append(f'<text x="{(L+W-R)/2}" y="{H-4}" text-anchor="middle">Pobreza en 2015 (%)</text><text x="12" y="{T-14}" >Cambio 2015-2024 (puntos)</text>')
    pts=[(float(P[k]['2015']),float(P[k]['2024'])-float(P[k]['2015']),k) for k in F if k in P]
    n=len(pts);mx=sum(p[0] for p in pts)/n;my=sum(p[1] for p in pts)/n
    b=sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts); a=my-b*mx
    s.append(f'<line x1="{x(3)}" y1="{y(a+b*3)}" x2="{x(52)}" y2="{y(a+b*52)}" stroke="var(--g)" stroke-dasharray="5 4"/>')
    for xv,yv,k in pts:
        hl=k=='HUANCAVELICA'; c='var(--b)' if hl else 'var(--ink2)'
        s.append(f'<circle cx="{x(xv):.1f}" cy="{y(yv):.1f}" r="{7 if hl else 5}" fill="{c}" stroke="var(--bg)" stroke-width="2"><title>{html.escape(P[k]["departamento"])}: {xv:.1f} % en 2015, {yv:+.1f} pts</title></circle>')
        if hl or k in ('AMAZONAS','APURIMAC','CAJAMARCA','PUNO','LORETO','TUMBES','UCAYALI','ICA','PASCO'):
            s.append(f'<text class="l" x="{x(xv)+9:.1f}" y="{y(yv)+4:.1f}">{html.escape(P[k]["departamento"])}</text>')
    s.append('</svg>'); return ''.join(s)
def bars():
    data=[('Agro',68,77),('Minería',63,28),('Transporte',38,16),('Hoteles y restaurantes',38,19),('Construcción',30,15),('Comercio',29,23),('Otros servicios',39,39),('Manufactura',32,29)]
    W,H,L,T=720,300,170,8; rh=34
    s=[f'<svg viewBox="0 0 {W} {T+len(data)*rh+30}" role="img" aria-label="Crecimiento del ingreso laboral por sector">']
    sc=(W-L-50)/90
    for i,(n,a,bm) in enumerate(data):
        yy=T+i*rh
        s.append(f'<text class="l" x="{L-10}" y="{yy+18}" text-anchor="end">{n}</text>')
        s.append(f'<rect x="{L}" y="{yy+2}" width="{a*sc:.1f}" height="12" rx="3" fill="var(--b)"><title>{n}, redujeron más: +{a} %</title></rect><text x="{L+a*sc+6:.1f}" y="{yy+13}">+{a} %</text>')
        s.append(f'<rect x="{L}" y="{yy+16}" width="{bm*sc:.1f}" height="12" rx="3" fill="var(--o)"><title>{n}, redujeron menos: +{bm} %</title></rect><text x="{L+bm*sc+6:.1f}" y="{yy+27}">+{bm} %</text>')
    yy=T+len(data)*rh+14
    s.append(f'<rect x="{L}" y="{yy-9}" width="10" height="10" rx="2" fill="var(--b)"/><text x="{L+16}" y="{yy}">Redujeron más (6)</text><rect x="{L+150}" y="{yy-9}" width="10" height="10" rx="2" fill="var(--o)"/><text x="{L+166}" y="{yy}">Redujeron menos (6)</text></svg>')
    return ''.join(s)
html_doc=f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pobreza por departamento</title><style>{CSS}</style></head><body><main>
<h1>Qué separa a los departamentos que reducen pobreza de los que se estancan</h1>
<p class="m">Perú 2015-2024 · Fuente: INEI (pobreza monetaria y ENAHO) · Informe de trabajo, 15-nov-2026</p>
<div class="k"><b>En corto.</b> Huancavelica no se quedó atrás: bajó de 45,2 % a 33,4 % (−11,8 puntos), el tercer mayor descenso. Lo que separa a los departamentos que reducen de los que se estancan no es el gasto público ni las transferencias, sino el crecimiento del ingreso por trabajo, sobre todo fuera del agro. Es una asociación con 6 departamentos contra 6, no una causa demostrada.</div>
<h2>1. Huancavelica sí redujo pobreza</h2>{line_chart()}
<p class="m">Pobreza monetaria (% de la población). 2024: Huancavelica 33,4 % (intervalo de confianza 29,1–37,7). Puno terminó peor que en 2015 (34,6 % → 39,9 %); Cajamarca bajó menos (50,8 % → 45,0 %) y repuntó desde 2019. Lima y Callao se excluyen del análisis: su alza es pobreza urbana tras la pandemia.</p>
<h2>2. Los más pobres bajaron más, y Huancavelica más de lo esperado</h2>{scatter()}
<p class="m">23 departamentos (sin Lima Metropolitana, Lima provincias ni Callao). Quien partía más alto bajó más (correlación −0,60). Descontado ese efecto, Huancavelica bajó 4,9 puntos más de lo esperado, junto a Amazonas, Apurímac, Lambayeque, Ica y San Martín. Loreto, Ucayali, Tumbes, Puno, Huánuco y Pasco bajaron menos de lo esperado.</p>
<h2>3. El gasto público no lo explica</h2>
<p>Gasto regional y municipal por habitante (2025), ejecución, saneamiento, educación, cobertura 4G y zonas críticas: ninguno se asocia con el cambio una vez descontado el nivel inicial (|ρ| &lt; 0,26; con 23 departamentos hace falta 0,41). El gasto es de 2025, posterior al periodo, así que solo descarta asociaciones simples.</p>
<h2>4. La diferencia está en el ingreso por trabajo</h2>
<table><tr><th>Ingreso mensual per cápita, 2015-16 → 2023-24 (S/)</th><th>Más</th><th>Menos</th></tr>
<tr><td>Crecimiento total</td><td>+56 %</td><td>+31 %</td></tr><tr><td>Trabajo independiente</td><td>+103</td><td>+43</td></tr><tr><td>Trabajo dependiente</td><td>+116</td><td>+77</td></tr><tr><td>Transferencias públicas</td><td>+10</td><td>+10</td></tr><tr><td>Remesas del exterior</td><td>~0</td><td>~0</td></tr></table>
<p class="m">Grupo «más»: Amazonas, Apurímac, Lambayeque, Ica, San Martín, Huancavelica. Grupo «menos»: Loreto, Ucayali, Tumbes, Puno, Huánuco, Pasco. Montos nominales.</p>
<h2>5. Y es un ingreso que creció en varios sectores, no solo en el agro</h2>{bars()}
<p class="m">Crecimiento del ingreso laboral medio por ocupado, 2015-16 → 2023-24. El agro creció parecido en ambos grupos. La estructura del empleo casi no cambió: la diferencia viene del ingreso dentro de cada sector. La minería es ~2 % de los ocupados: esa cifra es frágil.</p>
<h2>Huancavelica en 2023-24</h2>
<ul><li>Ingreso laboral medio por ocupado: S/ 421 → S/ 700 (+66 %).</li><li>59 % de los ocupados sigue en el agro, con S/ 377 al mes (antes S/ 208).</li><li>Trabajo familiar no remunerado: 32 % → 23 %. No sé con estos datos si esas personas pasaron a un empleo pagado.</li><li>Comercio: +106 % (S/ 343 → S/ 705), desde una base baja.</li></ul>
<h2>Qué no se puede afirmar</h2>
<ul><li>Causalidad. Son asociaciones entre 6 y 6 departamentos (23 en total).</li><li>Cada celda departamento por sector es pequeña; el ingreso medio excluye a quien no declara ingreso; los montos son nominales.</li><li>Muchas diferencias de pobreza entre departamentos no son estadísticamente significativas (CV de 5 a 20 %).</li></ul>
<p class="m">Verificación: recalculé la pobreza con los microdatos ENAHO y reproduce las cifras oficiales del INEI al centésimo (Huancavelica 45,16 / 36,91 / 33,40). Datos y scripts: carpeta <code>pobreza-departamentos</code>.</p>
</main></body></html>"""
open('INFORME.html','w',encoding='utf-8').write(html_doc); print(len(html_doc))
