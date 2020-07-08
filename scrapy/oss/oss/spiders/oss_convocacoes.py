# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
import time
import numpy as np
import csv
import os

df = pd.read_html('http://www.portaldatransparencia.saude.sp.gov.br/convocacoes.php')[0]
df.columns=df.columns.get_level_values(1)

df.to_csv('../../../../data/oss_convocacoes/convocacoes_publicas.csv', index=False, encoding='utf-8')
