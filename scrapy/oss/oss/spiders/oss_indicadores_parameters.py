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
        
        clean_dict = {}
        with open('indicadores_parameters.json','w', encoding='utf-8') as outfile:
            outfile.write(json.dumps(clean_dict))
            outfile.close()
        
        tipo_unidade_name  = get_correct_list(response.xpath("//*[@name='tipo_unidade']/option/text()").extract())
        tipo_unidade_value = get_correct_list(response.xpath("//*[@name='tipo_unidade']/option/@value").extract())

        periodo_name  = get_correct_list(response.xpath("//*[@name='periodo']/option/text()").extract())
        periodo_value = get_correct_list(response.xpath("//*[@name='periodo']/option/@value").extract())
        
        years = get_correct_list(response.xpath("//*[@name='ano']/option/text()").extract())

        # print(tipo_unidade_name)
        # print(periodo_name)
        # print(years)

        i = 0
        
        for j in range(len(tipo_unidade_value)):
            for k in range(len(periodo_value)):
                for year in years:
                    print(i)
                    
                    data = {
                            'form_name':"form_p_1",
                            'tipo_unidade':tipo_unidade_value[j],
                            'periodo':periodo_value[k],
                            'ano':year
                    }
                    header = {
                        'Content-Type':' application/x-www-form-urlencoded'
                    }
                    
                    
                    meta = {}
                    meta['i']=i
                    meta[f'data_{i}'] = {}
                    meta[f'data_{i}']['data'] = data
                    meta[f'data_{i}']['tipo_unidade_name'] = tipo_unidade_name[j]
                    meta[f'data_{i}']['periodo_name'] = periodo_name[k]

                    i+=1
                    yield scrapy.FormRequest(self.site_url, headers=header, formdata = data, callback=self.parse_months,  dont_filter=False, meta=meta)


        
        
    def parse_months(self,response):
        # print(response.text)
        # #get the columns
        r = response.text
        meta = response.meta
        
        
        unidade_name  = response.xpath("//*[@name='unidade[]']/option/text()").extract()
        unidade_value = response.xpath("//*[@name='unidade[]']/option/@value").extract()
        
        # print(unidade_value)
        i = meta['i']
        meta[f'data_{i}']['data']['unidade[]'] = unidade_value        

        with open('indicadores_parameters.json', encoding='utf-8') as feedsjson:
            parameters = json.load(feedsjson)
            
            
            
        parameters[f'data_{i}'] = meta[f'data_{i}']        
        
        
        with open('indicadores_parameters.json','w', encoding='utf-8') as outfile:
            outfile.write(json.dumps(parameters))
            outfile.close()