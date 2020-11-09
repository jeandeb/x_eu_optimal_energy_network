import requests
import json
import sys 
import calendar
from datetime import tzinfo, timedelta, datetime
import csv

date = datetime(2020, 1	, 1, 0)
hours_added = timedelta(hours = 3)
days = 60

#zones = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','NL','SI','ES','SE']
#Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden

#zones = ['FR','DE','SE','IT','PL','ES']

zones = ['IT-CNO','IT-CSO','IT-NO','IT-SAR','IT-SIC','IT-SO']
#url = 'https://api.electricitymap.org/v3/power-breakdown/past?zone=FR&datetime=2020-01-04T00:00:00Z'
#response = requests.get(url, headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})
#json_data = response.json()

#print(json_data['powerConsumptionBreakdown']['nuclear'])
#sys.exit("Exit")




with open('italia.csv', 'w', newline='') as file:
	writer = csv.writer(file, delimiter=';')
	writer.writerow(["Date","Zone", "Carbon Intensity", "consumption", "production", "import", "export", "fossilFreePercentage", "renewablePercentage", "powerConsumptionTotal", "powerProductionTotal", "powerImportTotal", "powerExportTotal"])
	print("Début du siphonnage de l'API")

	for zone in zones :
		for i in range(8 * days):
			url_CI = "https://api.electricitymap.org/v3/carbon-intensity/past?zone=" + zone + "&datetime=" + date.strftime("%Y-%m-%dT%H:%M:%SZ")
			response_CI = requests.get(url_CI, headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})
			json_data_CI = response_CI.json()
			url_PB = "https://api.electricitymap.org/v3/power-breakdown/past?zone=" + zone + "&datetime=" + date.strftime("%Y-%m-%dT%H:%M:%SZ")
			response_PB = requests.get(url_PB, headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})
			json_data_PB = response_PB.json()
			if('error' in json_data_CI or 'error' in json_data_PB):
				print("\033[1;31;40mAucune données disponible pour la zone " + zone + " à la date " + str(date))
			else:	
				print("\033[1;32;40mEcriture des données pour la zone " + str(zone) + " à la date " + str(date))
				writer.writerow([
					str(date),
					str(json_data_CI['zone']),
					str(json_data_CI['carbonIntensity']),
					str(json_data_PB['powerConsumptionBreakdown']),
					str(json_data_PB['powerProductionBreakdown']),
					str(json_data_PB['powerImportBreakdown']),
					str(json_data_PB['powerExportBreakdown']),
					str(json_data_PB['fossilFreePercentage']),
					str(json_data_PB['renewablePercentage']),
					str(json_data_PB['powerConsumptionTotal']),
					str(json_data_PB['powerProductionTotal']),
					str(json_data_PB['powerImportTotal']),
					str(json_data_PB['powerExportTotal']),
				])
			date = date + hours_added
		date = datetime(2020, 1	, 1, 0)

sys.exit("Exit")
	





#URL = 'https://api.electricitymap.org/v3/zones'
#response = requests.get(URL)
#response = requests.get('https://api.electricitymap.org/v3/power-breakdown/past?zone=FR-COR&datetime=2020-01-04T01:00:00Z', headers={'auth-token': 'YNsWZ2OdljXUX2RkgmaFq5uD'})




for city, value in json_data.items() : 
	print(city, value)