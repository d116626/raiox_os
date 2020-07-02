import datetime
import pandas as pd


now = datetime.datetime.now()

for year in range(2013, now.year + 1):
    url = f'http://www.portalfinanceirodogestor.saude.sp.gov.br/consultaFundoAFundo.asp?id=37248&mn_codmun=&ano={year}&drs_codigo=&ra_id=&prog_codigo=&subprograma_id=&natureza=&inativo=0&numero_demanda=&nis='
    
    fundo = pd.read_html(url)[0]
    fundo['ano'] = year
    
    fundo.to_csv(f'../../data/portal_financeiro/fundo/fundo_{year}.csv', index=False)
    
    print(year)
