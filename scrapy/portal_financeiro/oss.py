import datetime
import pandas as pd


now = datetime.datetime.now()

for year in range(2013, now.year + 1):
    url = f'http://www.portalfinanceirodogestor.saude.sp.gov.br/consultaOSS.asp?id=83019&ano={year}&tipo_rel=A&oss_id=&gerenciadora_id='
    
    oss = pd.read_html(url)[0]
    oss['ano'] = year
    
    oss = oss.rename(columns={f'Contratado {year}':'Contratado', f'Pago {year}':'Pago'})
    
    oss.to_csv(f'../../data/portal_financeiro/oss/ano/oss_{year}.csv', index=False)
    
    print(year,'- ano')
    
    url = f'http://www.portalfinanceirodogestor.saude.sp.gov.br/consultaOSS.asp?id=11775&ano={year}&tipo_rel=M&oss_id=&gerenciadora_id='
    
    oss = pd.read_html(url)[0]
    oss['ano'] = year
    
    oss.to_csv(f'../../data/portal_financeiro/oss/mes/oss_{year}.csv', index=False)
    
    print(year,'- mes')



    
