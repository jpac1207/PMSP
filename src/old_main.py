# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 19:10:24 2021

@author: asus
"""

import pandas as pd
from datetime import date
from model.MaintenanceEvent import MaintenanceEvent

optimizer_file = 'Mioptmizer2020.csv'
start_date = date(2020, 11, 30)
end_date = date(2020, 12, 4)

def load_data(path):
    return pd.read_csv(path, sep=";", parse_dates=['data_inicio'])

def get_interest_data(data):
    interest_collums = ['Km_inicial', 'Km_final', 'data_inicio', 'horario_inicio',
                        'tempo_atividade', 'Linha_inicio', 'Linha_fim', 'descricao_atividade',
                        'tipo_atividade']
    new_data = data[interest_collums]
    return new_data

def convert_data():
    data = load_data(optimizer_file)    
    data = get_interest_data(data)      
    data = data.set_index(['data_inicio'])    
    data.to_csv('data.csv', sep = ";", encoding='utf-8')

def parse_data(data):
    maintenance_events = []
    for index, row in data.iterrows():
        obj = MaintenanceEvent(index, row['Km_inicial'], row['Km_final'], row['horario_inicio'], 
        row['tempo_atividade'], row['Linha_inicio'], row['Linha_fim'], row['descricao_atividade'], row['tipo_atividade'])
        maintenance_events.append(obj)   
        print(obj.to_string())        
    return maintenance_events

def main():   
    data = pd.read_csv('data.csv', sep=";", parse_dates=['data_inicio'])    
    data = data.set_index(['data_inicio'])
    data = data.loc[start_date.isoformat():end_date.isoformat()]
    parse_data(data)
    
    
main()
    