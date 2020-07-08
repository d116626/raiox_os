# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
import time
import numpy as np
import csv
import os
import json 

def get_correct_list(vector):
    return vector[int((len(vector)+1)/2)+1:]

class OSS(scrapy.Spider):
    name = 'oss'
    site_url = 'http://www.portaldatransparencia.saude.sp.gov.br/indicadores.php'
    # allowed_domains = ['www.fazenda.sp.gov.br/RepasseConsulta/Consulta/repasse.aspx']
    start_urls = [site_url]

    def parse(self, response):
        
        with open('indicadores_parameters.json', encoding='utf-8') as feedsjson:
            parameters = json.load(feedsjson)
        
        
        for key in parameters.keys():
        
            data = parameters[key]['data']

            header = {
                'Content-Type':' application/x-www-form-urlencoded'
            }
            
            
            meta=parameters[key]
            

            yield scrapy.FormRequest(self.site_url, headers=header, formdata = data, callback=self.parse_months,  dont_filter=False, meta=meta)
        
        
    def parse_months(self,response):
        # print(response.text)
        # #get the columns
        r = response.text
        meta = response.meta
        
        df = pd.read_html(r)[0]
        
        df['tipo_unidade'] = meta['tipo_unidade_name']

        df['periodo'] = meta['periodo_name']

        df['ano'] = meta['data']['ano']
        
        tipo_unidade = meta['data']['tipo_unidade']
        periodo = meta['data']['periodo']
        ano = meta['data']['ano']
        
        
        
        df.to_csv(f'../../../../data/oss_indicadores/{tipo_unidade}_{periodo}_{ano}.csv', index=False, encoding='utf-8')

        
        