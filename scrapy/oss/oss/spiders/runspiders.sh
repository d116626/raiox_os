#!/bin/bash
echo "oss_qualificadas"
echo " "
scrapy runspider oss_qualificadas.py
echo " "
echo " "
echo " "
echo " "

echo "oss_contratualizadas"
echo " "
scrapy runspider oss_contratualizadas.py
echo " "
echo " "
echo " "
echo " "

echo "oss_indicadores_parameters"
echo " "
scrapy runspider oss_indicadores_parameters.py
echo " "
echo " "
echo " "
echo " "

echo "oss_indicadores_tables"
echo " "
scrapy runspider oss_indicadores_tables.py
echo " "
echo " "
echo " "
echo " "


echo "oss_convocacoes_publicas"
echo " "
python oss_convocacoes.py
echo " "
echo " "
echo " "
echo " "

