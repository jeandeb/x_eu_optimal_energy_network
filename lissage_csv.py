import requests
import json
import sys 
import calendar
from datetime import tzinfo, timedelta, datetime
import csv

date = datetime(2020, 1	, 1, 0)
hours_added = timedelta(hours = 6)
days = 180

#zones = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','NL','SI','ES','SE']
#Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden

#zones = ['FR','DE','SE','IT','PL','ES']
#url = 'https://api.electricitymap.org/v3/power-breakdown/past?zone=FR&datetime=2020-01-04T00:00:00Z'
#response = requests.get(url, headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})
#json_data = response.json()

#print(json_data['powerConsumptionBreakdown']['nuclear'])
#sys.exit("Exit")

libelle_fe = open('europe6h.csv') 
#libelle_fe = open('europe6h.csv') 
libelle_fe_reader = list(csv.reader(libelle_fe, delimiter=';'))

line_before = libelle_fe_reader[1]

for line in libelle_fe_reader[1:] :
	#print('Date CSV : ', str(line[0]))
	#print('Datetime : ', date.strftime("%d/%m/%Y %H:%M"))

	if(str(date.strftime("%d/%m/%Y %H:%M")) != line[0]):
		print('Recalibrage des dates')
		with open('line_to_add.csv', 'a', newline='') as file:
				writer = csv.writer(file, delimiter=';')
				writer.writerow([''])
		#print('Date attendu : ' + line[0])
		#print('Date actuelle : ' + date.strftime("%d/%m/%Y %H:%M"))


		while (str(date.strftime("%d/%m/%Y %H:%M")) != line[0]) :
			aux_line = line.copy()
			with open('line_to_add.csv', 'a', newline='') as file:
				writer = csv.writer(file, delimiter=';')
				aux_line[0] = str(date)
				writer.writerow(aux_line)
			print('Missing date : ',date, '- Country : ',line[1])
			#print('Date CSV : ', str(line[0]))
			#print('Datetime : ', date.strftime("%d/%m/%Y %H:%M"))
			date = date + hours_added
			#print('Date attendu : ' + line[0])
			#print('Date actuelle : ' + date.strftime("%d/%m/%Y %H:%M"))
	if(date.strftime("%d/%m/%Y %H:%M") == "28/06/2020 18:00") : 
		date = datetime(2020, 1	, 1, 0)
	else :
		date = date + hours_added
	
	





#URL = 'https://api.electricitymap.org/v3/zones'
#response = requests.get(URL)
#response = requests.get('https://api.electricitymap.org/v3/power-breakdown/past?zone=FR-COR&datetime=2020-01-04T01:00:00Z', headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})