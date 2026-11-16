import pandas as pd, numpy as np
df=pd.read_csv('empleo_departamento_sector_anio.csv')
mejor=['AMAZONAS','APURIMAC','LAMBAYEQUE','ICA','SAN MARTIN','HUANCAVELICA']
peor=['LORETO','UCAYALI','TUMBES','PUNO','HUANUCO','PASCO']
grupos={'MÁS (6)':mejor,'MENOS (6)':peor,'Huancavelica':['HUANCAVELICA'],'Apurímac':['APURIMAC'],'Puno':['PUNO']}
ini,fin=[2015,2016],[2023,2024]
def resumen(deps,años):
    s=df[df.dep.isin(deps)&df.anio.isin(años)&(df.sec!='sin_dato')]
    g=s.groupby('sec').apply(lambda x: pd.Series({'oc':x.ocupados.sum(),'ing':(x.ing_medio*x.ocupados).sum()/x.ocupados.sum(),'tfnr':x.tfnr.sum()}),include_groups=False)
    g['sh']=100*g.oc/g.oc.sum(); tot_ing=(g.ing*g.oc).sum()/g.oc.sum()
    return g,tot_ing,100*g.tfnr.sum()/g.oc.sum()
orden=['agro','mineria','manufactura','construccion','comercio','transporte','hoteles_rest','otros_servicios']
for nombre,deps in grupos.items():
    a,ia,ta=resumen(deps,ini); b,ib,tb=resumen(deps,fin)
    print(f'\n== {nombre}: ingreso laboral medio por ocupado S/mes {ia:.0f} -> {ib:.0f} ({100*(ib/ia-1):+.0f}%) | trabajo familiar no remunerado {ta:.0f}% -> {tb:.0f}%')
    t=pd.DataFrame({'%ocup_ini':a.sh,'%ocup_fin':b.sh,'S/_ini':a.ing,'S/_fin':b.ing}).reindex(orden).round(0)
    t['d_%ocup']=(t['%ocup_fin']-t['%ocup_ini']); t['crec_ing_%']=(100*(t['S/_fin']/t['S/_ini']-1)).round(0)
    print(t.to_string())
