# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
import time
import numpy as np
import csv
import os
import unicodedata
from bs4 import BeautifulSoup
import datetime



class OSS(scrapy.Spider):
    name = 'oss'
    site_url = 'http://www.portaldatransparencia.saude.sp.gov.br/unidade-detalhe.php'
    # allowed_domains = ['www.fazenda.sp.gov.br/RepasseConsulta/Consulta/repasse.aspx']
    start_urls = [site_url]

    def parse(self, response):
        current_year = datetime.datetime.today().year
        years = [i for i in range(2006,current_year+1)]        

        print(years)
        for year in years:
            

            data = {
                "CONTRATO_ANO":str(year),
            }
            header = {
                'Content-Type':' application/x-www-form-urlencoded'
            }
                
            meta = {
                    'var': str(year)
                    }
                
            yield scrapy.FormRequest(self.site_url, headers=header, formdata = data, callback=self.parse_months,  dont_filter=False, meta=meta)

        
    def parse_months(self,response):
        # print(response.text)
        # #get the columns
        r = response.text
        meta = response.meta

        html = unicodedata.normalize("NFKD", r).replace('&nbsp',' ').replace('\xa0',' ').replace('CNPJ:',' CNPJ:').replace('Tipo:',' Tipo:').replace('Unidade','Unidade ').replace('Município:',' Município:')
        
        soup = BeautifulSoup(html, 'html.parser', )


        oss = soup.find_all("a", attrs={"href": "#"})
        oss = [r.text.replace(' ;','') for r in oss]

        unidades = soup.find_all("h4", attrs={"class": ""})
        unidades = [r.text for r in unidades]

        endereco_cness = soup.find_all("div", attrs={"class": "col-sm-4 invoice-col"})
        endereco = [endereco_cness[i].text for i in range(len(endereco_cness)) if i % 2 == 0]
        cnes = [endereco_cness[i].text for i in range(len(endereco_cness)) if i % 2 != 0]

        df = pd.read_html(html)
        
        
        dd_final = pd.DataFrame()
        for i in range(len(df)):
            dd = df[i]
            dd['oss'] = oss[i]
            dd['unidade'] = unidades[i]
            dd['endereco'] = endereco[i]
            dd['cnes'] = cnes[i]
            
            dd_final = pd.concat([dd_final, dd], axis=0)

        dd_final['municipio'] = dd_final['endereco'].apply(lambda x: str(x).split('Município:')[1]).str.strip()
        dd_final['endereco'] = dd_final['endereco'].apply(lambda x: str(x).split('Município:')[0]).str.strip()

        dd_final['bairro'] = dd_final['endereco'].apply(lambda x: str(x).split('Bairro:')[1]).str.strip()
        dd_final['endereco'] = dd_final['endereco'].apply(lambda x: str(x).split('Bairro:')[0]).str.replace('Endereço Unidade','').str.strip()

        dd_final['tipo'] = dd_final['cnes'].apply(lambda x: str(x).split('Tipo:')[1]).str.replace(';','').str.strip()
        dd_final['cnes'] = dd_final['cnes'].apply(lambda x: str(x).split('Tipo:')[0]).str.strip()

        dd_final['cnpj'] = dd_final['cnes'].apply(lambda x: str(x).split('CNPJ:')[1]).str.strip()
        dd_final['cnes'] = dd_final['cnes'].apply(lambda x: str(x).split('CNPJ:')[0]).str.replace('CNES:','').str.strip()

        cols = ['Tipo', 'Número', 'Ano', 'Arquivo', 'oss', 'unidade','municipio', 'endereco', 'bairro', 'tipo','cnes','cnpj']
        dd_final = dd_final[cols]
        
        
        dd_final.to_csv(f'../../../../data/oss_cidades/oss_cidades_{meta["var"]}.csv', index=False)