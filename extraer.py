import openpyxl, csv, sys
src='raw/anexo/Anexo Estadístico Excel/03_FGT de Pobreza 2015-2024_informe.xlsx'
wb=openpyxl.load_workbook(src,read_only=True,data_only=True)
ws=wb['3.1']
rows=list(ws.iter_rows(values_only=True))
i=[k for k,r in enumerate(rows) if r[0]=='Departamentos'][0]
out=[]
for r in rows[i+1:]:
    if r[0] is None or str(r[0]).startswith(('*','Nota','1/','2/','Fuente')): break
    out.append(r[:14])
yrs=list(range(2015,2025))
with open('pobreza_departamento_2015_2024.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['departamento']+yrs+['ic_inf_2024','ic_sup_2024','cv_2024'])
    for r in out:
        w.writerow([r[0].strip()]+[round(x,2) for x in r[1:11]]+[round(r[11],2),round(r[12],2),round(r[13],1)])
print(len(out))
