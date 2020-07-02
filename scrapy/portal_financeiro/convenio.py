import datetime
import pandas as pd


now = datetime.datetime.now()

for year in range(2013, now.year + 1):
    url = f'http://www.portalfinanceirodogestor.saude.sp.gov.br/consultaConvenios.asp?id=93729&mn_codmun=&ano={year}&conveniado_id=&drs_codigo=&ra_id=&prog_codigo=&subprograma_id=&natureza=&inativo=0&numero_demanda=&nis='
    
    convenio = pd.read_html(url)[0]
    convenio['ano'] = year
    
    convenio.to_csv(f'../../data/portal_financeiro/convenio/convenio_{year}.csv', index=False)
    
    print(year)
