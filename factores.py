import sqlite3, json, csv, unicodedata
def norm(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(ch)!='Mn').strip()
Q=sqlite3.connect('file:../quipu/data/quipu.db?mode=ro',uri=True)
D=sqlite3.connect('file:../datos-pe/data/padron.db?mode=ro',uri=True)
pob=json.load(open('../quipu/data/poblacion-2025.json',encoding='utf-8'))['pob']
dep_name={}
for u,dep in D.execute('select ubigeo,departamento from ubigeo'): dep_name[u[:2]]=norm(dep)
P={}
for u,v in pob.items(): P[dep_name[u[:2]]]=P.get(dep_name[u[:2]],0)+v
F={d:{'pob_2025':P[d]} for d in P}
# gasto 2025
q='''select e.depto, e.nivel, g.funcion, sum(case when g.mes=0 then g.pim else 0 end), sum(case when g.mes>0 then g.devengado else 0 end)
from gasto g join ejecutora e on e.id=g.ejecutora_id where g.anio=2025 group by 1,2,3'''
agg={}
for dep,niv,fn,pim,dev in Q.execute(q):
    d=norm(dep); a=agg.setdefault(d,{})
    sub = 'nac' if niv=='GOBIERNO NACIONAL' else 'sub'
    for k,v in ((f'{sub}_pim',pim),(f'{sub}_dev',dev),(f'{sub}_dev_{fn}',dev)):
        a[k]=a.get(k,0)+v
for d,a in agg.items():
    if d not in F: continue
    p=F[d]['pob_2025']
    F[d]['gasto_subnac_pc']=round(a['sub_dev']/p)
    F[d]['ejecucion_subnac_pct']=round(100*a['sub_dev']/a['sub_pim'],1)
    F[d]['gasto_nacional_pc']=round(a.get('nac_dev',0)/p)
    for fn,nm in (('18','saneamiento'),('15','transporte'),('10','agropecuaria'),('20','salud'),('22','educacion')):
        F[d][f'{nm}_subnac_pc']=round(a.get(f'sub_dev_{fn}',0)/p)
# cobertura 4G
cov={}
for dep,m in D.execute('select departamento,max_4g from cobertura_cp'):
    d=norm(dep); c=cov.setdefault(d,[0,0]); c[1]+=1; c[0]+= (m or 0)>=50
for d,(a,b) in cov.items():
    if d in F: F[d]['cp_con_4g_pct']=round(100*a/b,1); F[d]['n_centros_poblados']=b
# zonas criticas y emergencias hidricas
for dep,n in D.execute('select region,count(*) from zona_critica group by 1'):
    d=norm(dep)
    if d in F: F[d]['zonas_criticas_x100mil']=round(1e5*n/F[d]['pob_2025'],1)
for dep,n in D.execute('select departamento,count(*) from emergencia_hidrica group by 1'):
    d=norm(dep)
    if d in F: F[d]['emerg_hidricas_x100mil']=round(1e5*n/F[d]['pob_2025'],1)
# pobreza
pov={}
for r in csv.DictReader(open('pobreza_departamento_2015_2024.csv',encoding='utf-8')):
    n=norm(r['departamento'])
    if n.startswith(('LIMA','PROV. CONST')): continue
    pov[n]=r
rows=[]
for n,r in pov.items():
    f=F.get(n)
    if not f: print('SIN MATCH',n); continue
    rows.append({'departamento':r['departamento'],'pobreza_2015':r['2015'],'pobreza_2019':r['2019'],'pobreza_2024':r['2024'],
                 'cambio_2015_24':round(float(r['2024'])-float(r['2015']),1),'cv_2024':r['cv_2024'],**f})
keys=list(rows[0].keys())
for r in rows:
    for k in keys: r.setdefault(k,'')
w=csv.DictWriter(open('factores_departamento.csv','w',newline='',encoding='utf-8'),fieldnames=keys); w.writeheader(); w.writerows(rows)
print(len(rows),'departamentos; columnas:',keys)
