import csv, json, unicodedata
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn').strip()
P={norm(r['departamento']):r for r in csv.DictReader(open('pobreza_departamento_2015_2024.csv',encoding='utf-8'))}
F=list(csv.DictReader(open('factores_departamento.csv',encoding='utf-8')))
YRS=list(range(2015,2025))
NAC=[21.77,20.74,21.70,20.49,20.19,30.13,25.87,27.52,29.05,27.58]   # INEI cuadro 3.1, fila Nacional
def rank(v):
    s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and v[s[j+1]]==v[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2+1
        i=j+1
    return r
def pear(a,b):
    n=len(a);ma=sum(a)/n;mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/((sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5)
sp=lambda a,b: pear(rank(a),rank(b))
x=[float(r['pobreza_2015']) for r in F]; y=[float(r['cambio_2015_24']) for r in F]
n=len(x);mx=sum(x)/n;my=sum(y)/n;b=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x);a0=my-b*mx
res=[c-(a0+b*(a-mx)) for a,c in zip(x,y)]
name={}  # clave normalizada -> nombre bonito
dep={};sc={}
for r in F:
    k=norm(r['departamento']);p=P[k];nm=p['departamento'].strip();name[k]=nm
for i,r in enumerate(F):
    k=norm(r['departamento']);nm=name[k];p=P[k]
    dep[nm]={'p':[float(p[str(yv)]) for yv in YRS]}
    sc[nm]={'p15':float(p['2015']),'p24':float(p['2024']),'cambio':round(y[i],2),'res':round(res[i],2)}
LAB=[('gasto_subnac_pc','gasto regional y municipal'),('ejecucion_subnac_pct','ejecución del gasto'),('gasto_nacional_pc','gasto del gobierno nacional'),
     ('saneamiento_subnac_pc','gasto en saneamiento'),('transporte_subnac_pc','gasto en transporte'),('agropecuaria_subnac_pc','gasto agropecuario'),
     ('salud_subnac_pc','gasto en salud'),('educacion_subnac_pc','gasto en educación'),('cp_con_4g_pct','centros poblados con 4G'),
     ('zonas_criticas_x100mil','zonas críticas (por 100 mil hab.)'),('emerg_hidricas_x100mil','emergencias hídricas (por 100 mil)')]
rho=[{'l':l,'cam':round(sp([float(r[k]) for r in F],y),2),'res':round(sp([float(r[k]) for r in F],res),2)} for k,l in LAB]
G=list(csv.DictReader(open('comparacion_grupos.csv',encoding='utf-8')))
def gm(col,g): v=[float(r[col]) for r in G if r['grupo'].endswith(g)]; return sum(v)/len(v)
ing=[{'l':l,'a':round(gm(c,'MÁS'),1),'b':round(gm(c,'MENOS'),1)} for l,c in
     [('trabajo independiente','d_trab_independiente'),('trabajo dependiente','d_trab_dependiente'),('transferencias privadas','d_transf_privadas'),('transferencias públicas','d_transf_publicas'),('extraordinarios','d_extraordinarios'),('rentas','d_rentas'),('remesas del exterior','d_remesas_exterior')]]
sec_ing=[{'l':l,'a':a,'b':b} for l,a,b in [('agro',68,77),('minería',63,28),('transporte',38,16),('hoteles y restaurantes',38,19),('construcción',30,15),('comercio',29,23),('otros servicios',39,39),('manufactura',32,29)]]
sec_emp=[{'l':l,'a':a,'b':b} for l,a,b in [('agro',38,36),('otros servicios',18,17),('comercio',17,17),('transporte',7,8),('hoteles y restaurantes',7,7),('manufactura',6,6),('construcción',6,7),('minería',1,2)]]
mas=['AMAZONAS','APURIMAC','LAMBAYEQUE','ICA','SAN MARTIN','HUANCAVELICA']; menos=['LORETO','UCAYALI','TUMBES','PUNO','HUANUCO','PASCO']
D={'years':YRS,'dep':dep,'nac':NAC,'grupos':{'mas':[name[k] for k in mas],'menos':[name[k] for k in menos]},'sc':sc,'tend':[round(a0-b*mx,3),round(b,4)],'rho':rho,'ing':ing,'sec_ing':sec_ing,'sec_emp':sec_emp}
html=open('plantilla.html',encoding='utf-8').read().replace('__DATA__',json.dumps(D,ensure_ascii=False))
open('INFORME.html','w',encoding='utf-8').write(html); open('index.html','w',encoding='utf-8').write(html)
print(len(html),'bytes'); print('tend',D['tend'],'rho',[(r['l'][:14],r['cam'],r['res']) for r in rho])
