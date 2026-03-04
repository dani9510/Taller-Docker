# analisis.py - Analisis de incidentes CRUE en Docker

import pandas as pd
import os

print('='*60)
print('ANALISIS DE INCIDENTES CRUE - Ejecutando en Docker')
print('='*60)

# Cargar datos
df = pd.read_csv('incidentes_crue_diarios.txt', sep='\t')
df['fecha'] = pd.to_datetime(df['fecha'])

# Estadisticas descriptivas
print(f'\nTotal de registros: {len(df)}')
print(f'Periodo: {df.fecha.min()} a {df.fecha.max()}')

print(f'\nEstadisticas de incidentes:')
print(f'  Media:    {df.incidentes.mean():.2f}')
print(f'  Mediana:  {df.incidentes.median():.2f}')
print(f'  Desv Std: {df.incidentes.std():.2f}')
print(f'  Minimo:   {df.incidentes.min()} ({df.loc[df.incidentes.idxmin(), "fecha"].date()})')
print(f'  Maximo:   {df.incidentes.max()} ({df.loc[df.incidentes.idxmax(), "fecha"].date()})')

# Analisis temporal
df['dia_semana'] = df['fecha'].dt.day_name()
df['mes'] = df['fecha'].dt.month
df['anio'] = df['fecha'].dt.year

print(f'\nPromedio por anio:')
for anio, grupo in df.groupby('anio'):
    print(f'  {anio}: {grupo.incidentes.mean():.2f}')

print(f'\nDia con mas incidentes: {df.groupby("dia_semana").incidentes.mean().idxmax()}')
print(f'Mes con mas incidentes: {df.groupby("mes").incidentes.mean().idxmax()}')

# Agregar analisis por dia de la semana

print('\nPromedio por dia de la semana:')
dias_orden = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dias_esp = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']

for i, dia in enumerate(dias_orden):
    promedio = df[df['dia_semana'] == dia]['incidentes'].mean()
    print(f'  {dias_esp[i]}: {promedio:.2f}')

# Guardar resumen estadistico
resumen = df.describe()
resumen.to_csv('/app/resultados/resumen_estadistico.csv')

# Guardar datos completos
df.to_csv('/app/resultados/datos_completos.csv', index=False)

print(f'\nResumen guardado en: /app/resultados/resumen_estadistico.csv')
print(f'Datos completos guardados en: /app/resultados/datos_completos.csv')
print('='*60)
