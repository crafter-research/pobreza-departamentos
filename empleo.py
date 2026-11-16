import pandas as pd, glob, numpy as np
DEP={'01':'AMAZONAS','02':'ANCASH','03':'APURIMAC','04':'AREQUIPA','05':'AYACUCHO','06':'CAJAMARCA','07':'CALLAO','08':'CUSCO','09':'HUANCAVELICA','10':'HUANUCO','11':'ICA','12':'JUNIN','13':'LA LIBERTAD','14':'LAMBAYEQUE','15':'LIMA','16':'LORETO','17':'MADRE DE DIOS','18':'MOQUEGUA','19':'PASCO','20':'PIURA','21':'PUNO','22':'SAN MARTIN','23':'TACNA','24':'TUMBES','25':'UCAYALI'}
def sector(c):
    if np.isnan(c): return 'sin_dato'
    d=int(c)//100
    if d<=3: return 'agro'
    if d<=9: return 'mineria'
    if d<=33: return 'manufactura'
    if d<=39: return 'electr_agua'
    if d<=43: return 'construccion'
    if d<=47: return 'comercio'
    if d<=53: return 'transporte'
    if d<=56: return 'hoteles_rest'
    return 'otros_servicios'
rows=[]
for y in range(2015,2025):
    f=[p for p in glob.glob(f'enaho_raw/e{y}/**/enaho01a-{y}[-_]500.dta',recursive=True)][0]
    d=pd.read_stata(f,convert_categoricals=False,columns=None)
    d.columns=[c.lower() for c in d.columns]
    d=d[d['ocu500']==1].copy()
    d['dep']=d['ubigeo'].astype(str).str.zfill(6).str[:2].map(DEP)
    d['sec']=d['p506r4'].map(sector)
    d['ing']=(d['i524a1'].fillna(0)+d['i530a'].fillna(0))/12
    d['tfnr']=(d['p507']==5)
    d['w']=d['fac500a']
    for (dep,sec),s in d.groupby(['dep','sec']):
        w=s['w'].sum(); si=s[s['ing']>0]
        rows.append({'anio':y,'dep':dep,'sec':sec,'ocupados':w,'ing_medio':(si['ing']*si['w']).sum()/si['w'].sum() if len(si) else np.nan,'tfnr':(s['tfnr']*s['w']).sum()})
df=pd.DataFrame(rows); df.to_csv('empleo_departamento_sector_anio.csv',index=False); print(df.shape)
