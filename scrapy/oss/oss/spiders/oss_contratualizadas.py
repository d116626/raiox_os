# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
import time
import numpy as np
import csv
import os



class OSS(scrapy.Spider):
    name = 'oss'
    site_url = 'http://www.portaldatransparencia.saude.sp.gov.br/unidades.php'
    # allowed_domains = ['www.fazenda.sp.gov.br/RepasseConsulta/Consulta/repasse.aspx']
    start_urls = [site_url]

    def parse(self, response):
        years = response.xpath("//*[@name='CONTRATO_ANO']/option/text()").extract()[1:]
        
        organizacoes_names  =  response.xpath("//*[@name='COD_OSS']/option/text()").extract()[1:]
        organizacoes_values =  response.xpath("//*[@name='COD_OSS']/option/@value").extract()[1:]

        municipios_oss_names  =  response.xpath("//*[@name='MUNICIPIO_OSS']/option/text()").extract()[1:]
        municipios_oss_values =  response.xpath("//*[@name='MUNICIPIO_OSS']/option/@value").extract()[1:]

        print(organizacoes_values)
        

        for year in years:
            data = {
                'async': 't',
                'list_type': 'lista_simples',
                "CONTRATO_ANO":year,
            }
            header = {
                'Content-Type':' application/x-www-form-urlencoded'
            }
            
            meta = {
                    'tipo': 'year',
                    'var': year
                    }
            
            yield scrapy.FormRequest(self.site_url, headers=header, formdata = data, callback=self.parse_months,  dont_filter=False, meta=meta)

        for i in range(len(organizacoes_values)):
            data = {
                'async': 't',
                'list_type': 'lista_simples',
                "COD_OSS":organizacoes_values[i],
            }
            header = {
                'Content-Type':' application/x-www-form-urlencoded'
            }
            
            meta = {
                    'tipo': 'organizacao',
                    'var': organizacoes_names[i]
                    }
            
            yield scrapy.FormRequest(self.site_url, headers=header, formdata = data, callback=self.parse_months,  dont_filter=False, meta=meta)

        
        
        
    def parse_months(self,response):
        # print(response.text)
        # #get the columns
        r = response.text
        meta = response.meta
        
        df = pd.read_html(r)[0]
        
        df[meta['tipo']] = meta['var']
        
        
        if meta['tipo'] == 'year':
            year = meta['var']
            df.to_csv(f'../../../../data/oss_contratualizadas/years/{year}.csv', index=False)
        elif meta['tipo'] == 'organizacao':
            organizacao = meta['var']
            df.to_csv(f'../../../../data/oss_contratualizadas/organizacoes/{organizacao}.csv', index=False)
        
        
        
        
        
