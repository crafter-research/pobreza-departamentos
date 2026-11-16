import pandas as pd
df=pd.read_csv('enaho_departamento_anio.csv')
G=['trab_dependiente','trab_independiente','transf_publicas','transf_privadas','remesas_exterior','rentas','extraordinarios']
mejor=['AMAZONAS','APURIMAC','LAMBAYEQUE','ICA','SAN MARTIN','HUANCAVELICA']
peor=['LORETO','UCAYALI','TUMBES','PUNO','HUANUCO','PASCO']
a=df[df.anio.isin([2015,2016])].groupby('dep').mean(numeric_only=True)
b=df[df.anio.isin([2023,2024])].groupby('dep').mean(numeric_only=True)
a['tot']=a[['pc_'+g for g in G]].sum(axis=1); b['tot']=b[['pc_'+g for g in G]].sum(axis=1)
rows=[]
for dep in mejor+peor:
    r={'dep':dep,'grupo':'redujo MÁS' if dep in mejor else 'redujo MENOS','pc_2015-16':round(a.loc[dep,'tot']),'pc_2023-24':round(b.loc[dep,'tot']),'crec_%':round(100*(b.loc[dep,'tot']/a.loc[dep,'tot']-1),1)}
    for g in G: r['d_'+g]=round(b.loc[dep,'pc_'+g]-a.loc[dep,'pc_'+g])
    r['juntos15']=round(a.loc[dep,'hogares_juntos_pct']); r['juntos24']=round(b.loc[dep,'hogares_juntos_pct'])
    rows.append(r)
t=pd.DataFrame(rows); pd.set_option('display.width',250)
print(t.to_string(index=False))
print()
print(t.groupby('grupo')[['crec_%']+['d_'+g for g in G]+['juntos15','juntos24']].mean().round(1).T.to_string())
t.to_csv('comparacion_grupos.csv',index=False)
