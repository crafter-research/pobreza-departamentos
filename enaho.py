import pandas as pd, glob, unicodedata, csv
DEP={'01':'AMAZONAS','02':'ANCASH','03':'APURIMAC','04':'AREQUIPA','05':'AYACUCHO','06':'CAJAMARCA','07':'CALLAO','08':'CUSCO','09':'HUANCAVELICA','10':'HUANUCO','11':'ICA','12':'JUNIN','13':'LA LIBERTAD','14':'LAMBAYEQUE','15':'LIMA','16':'LORETO','17':'MADRE DE DIOS','18':'MOQUEGUA','19':'PASCO','20':'PIURA','21':'PUNO','22':'SAN MARTIN','23':'TACNA','24':'TUMBES','25':'UCAYALI'}
G={'trab_dependiente':['ingbruhd','pagesphd','insedthd'],
   'trab_independiente':['ingindhd','ingauthd','ingseihd'],
   'transf_publicas':['ingtpuhd'],
   'transf_privadas':['ingtprhd'],
   'remesas_exterior':['ingtexhd'],
   'rentas':['ingrenhd'],
   'extraordinarios':['ingexthd','ingoexhd']}
out=[]
for y in range(2015,2025):
    f=[p for p in glob.glob(f'enaho_raw/s{y}/**/sumaria-{y}.dta',recursive=True)][0]
    d=pd.read_stata(f,convert_categoricals=False)
    d.columns=[c.lower() for c in d.columns]
    d['dep']=d['ubigeo'].astype(str).str.zfill(6).str[:2]
    d['w']=d['factor07']*d['mieperho']
    d['pob']=d['pobreza'].isin([1,2]).astype(float)
    d['ingtot']=d['inghog1d']
    for g,cols in G.items():
        d[g]=sum(d[c].fillna(0) for c in cols if c in d.columns)
    missing=[c for cs in G.values() for c in cs if c not in d.columns]
    for dep,s in d.groupby('dep'):
        w=s['w'].sum(); hw=s['factor07'].sum()
        row={'anio':y,'dep':DEP[dep],'n_hogares':len(s),'pobreza_enaho':round(100*(s['pob']*s['w']).sum()/w,2)}
        tot=sum((s[g]*s['factor07']).sum() for g in G)
        for g in G:
            row['sh_'+g]=round(100*(s[g]*s['factor07']).sum()/tot,1)
            row['pc_'+g]=round((s[g]*s['factor07']).sum()/w/12,1)
        row['recon_vs_inghog1d']=round(100*tot/(s['ingtot']*s['factor07']).sum(),1)
        jc='ingtpu01' if 'ingtpu01' in s.columns else None
        if jc: row['hogares_juntos_pct']=round(100*(s['factor07']*(s[jc].fillna(0)>0)).sum()/hw,1)
        out.append(row)
    if missing: print(y,'faltan',missing)
df=pd.DataFrame(out); df.to_csv('enaho_departamento_anio.csv',index=False)
print(df.shape)
# validación vs INEI
off=pd.read_csv('pobreza_departamento_2015_2024.csv')
def nm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn').strip()
off['dep']=off['departamento'].map(nm)
for dep in ['HUANCAVELICA','CAJAMARCA','PUNO','APURIMAC']:
    o=off[off.dep==dep].iloc[0]
    print(dep,[(y,float(o[str(y)]),float(df[(df.anio==y)&(df.dep==dep)].pobreza_enaho.iloc[0])) for y in (2015,2019,2024)])
import sys; sys.exit(0)
print(df[df.dep=='HUANCAVELICA'][['anio','pobreza_enaho','recon_vs_inghog1d']+['sh_'+g for g in G]+['hogares_juntos_pct']].to_string())
