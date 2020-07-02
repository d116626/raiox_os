import datetime
import pandas as pd


now = datetime.datetime.now()

for year in range(2013, now.year + 1):
    url = f'http://www.portalfinanceirodogestor.saude.sp.gov.br/consultaProprios.asp?id=7349&ano={year}&tipoAdm=&co_codigo=&ug_codigo=&fo_codigo='
    
    proprios = pd.read_html(url)[0]
    proprios['ano'] = year
    
    proprios.to_csv(f'../../data/portal_financeiro/proprios/proprios_{year}.csv', index=False)
    
    print(year)
