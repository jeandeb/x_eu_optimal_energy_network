import requests
import json
import sys 
import calendar
from datetime import tzinfo, timedelta, datetime
import csv

#libelle_fe = open('europe6h.csv') 
#libelle_fe_reader = list(csv.reader(libelle_fe))

#for l in libelle_fe_reader :
#	print(l)

def string_to_json(line):
	return json.loads(line.replace("\'", "\""))


#CREATION DICTIONNAIRE CARBON INTENSITY PAR ENERGIE
dict_carbon_intensity = dict()
dict_carbon_intensity['nuclear'] = 12
dict_carbon_intensity['geothermal'] = 38
dict_carbon_intensity['biomass'] = 230
dict_carbon_intensity['coal'] = 820
dict_carbon_intensity['wind'] = 11
dict_carbon_intensity['solar'] = 45
dict_carbon_intensity['hydro'] = 24
dict_carbon_intensity['gas'] = 490
dict_carbon_intensity['oil'] = 650
dict_carbon_intensity['unknown'] = 100
dict_carbon_intensity['hydro discharge'] = 200
dict_carbon_intensity['battery discharge'] = 20


#CREATION DICTIONNAIRE CAPACITE PAR ENERGIE PAR PAYS
dict_capacity_per_country = dict()
capacite_production_csv = open('capacite_production.csv') 
capacite_production_csv_reader = list(csv.reader(capacite_production_csv, delimiter=';'))
for row in capacite_production_csv_reader[2:26] :
	aux_data = "{'nuclear': " + str(float(row[2])*1000) +", 'geothermal': " + str(float(row[3])*1000) +", 'biomass': " + str(float(row[4])*1000) +", 'coal': " + str(float(row[5])*1000) +", 'wind': " + str(float(row[6])*1000) +", 'solar': " + str(float(row[7])*1000) +", 'hydro': " + str(float(row[8])*1000) +", 'gas': " + str(float(row[11])*1000) +", 'oil': " + str(float(row[12])*1000) +", 'unknown': 0, 'hydro discharge': " + str(float(row[9])*1000) +", 'battery discharge': " + str(float(row[10])*1000) +"}"
	dict_capacity_per_country[row[0]] = string_to_json(aux_data)


#DICT OPTIMISATION : 
optimize_production = [None] * 720

def calculator_carbon_intensity(production):
	co2 = 0
	co2 += (production['nuclear'] * dict_carbon_intensity['nuclear'])
	co2 += (production['geothermal'] * dict_carbon_intensity['geothermal'])
	co2 += (production['biomass'] * dict_carbon_intensity['biomass'])
	co2 += (production['coal'] * dict_carbon_intensity['coal'])
	co2 += (production['wind'] * dict_carbon_intensity['wind'])
	co2 += (production['solar'] * dict_carbon_intensity['solar'])
	co2 += (production['hydro'] * dict_carbon_intensity['hydro'])
	co2 += (production['gas'] * dict_carbon_intensity['gas'])
	co2 += (production['oil'] * dict_carbon_intensity['oil'])
	co2 += (production['unknown'] * dict_carbon_intensity['unknown'])
	co2 += (production['hydro discharge'] * dict_carbon_intensity['hydro discharge'])
	co2 += (production['battery discharge'] * dict_carbon_intensity['battery discharge'])
	print("production CO2" , co2)
	return co2

def switchEnergy(country, local_production, type, target):

	print("Switch de", type, "vers", target)

	if(local_production[type] == 0 or int(dict_capacity_per_country[country][target]) == 0):
		return local_production
	actual_target = local_production[target]
	#print("actual", target, actual_target)
	capacity_target = dict_capacity_per_country[country][target]
	#print("capacity_target", target, capacity_target)
	capacity = capacity_target - actual_target
	#print("capacité", capacity)

	to_change = 0
	if(capacity < local_production[type]):
		to_change = capacity
	else:
		to_change = local_production[type]
	local_production[type] -=  to_change
	local_production[target] += to_change
	return local_production


def findBetterEnergy(country, local_production, type): 

	if(type=='coal'):
		local_production = switchEnergy(country, local_production, type, 'nuclear')
		local_production = switchEnergy(country, local_production, type, 'biomass')
		local_production = switchEnergy(country, local_production, type, 'gas')
		local_production = switchEnergy(country, local_production, type, 'oil')
	if(type=='oil'):
		local_production = switchEnergy(country, local_production, type, 'nuclear')
		local_production = switchEnergy(country, local_production, type, 'biomass')
		local_production = switchEnergy(country, local_production, type, 'gas')
	if(type=='gas'): 
		local_production = switchEnergy(country, local_production, type, 'nuclear')
		local_production = switchEnergy(country, local_production, type, 'biomass')
	if(type=='biomass'):
		local_production = switchEnergy(country, local_production, type, 'nuclear')
	
	return local_production



def optimize_energy(l):
	local_production = string_to_json(l[4])
	new_local_production = findBetterEnergy(l[1], local_production,'coal')
	new_local_production = findBetterEnergy(l[1], new_local_production,'oil')
	new_local_production = findBetterEnergy(l[1], new_local_production,'gas')
	new_local_production = findBetterEnergy(l[1], new_local_production,'biomass')
	return new_local_production



libelle_fe = open('europe6hLiss.csv') 
#libelle_fe = open('europe6h.csv') 
libelle_fe_reader = list(csv.reader(libelle_fe, delimiter=';'))

production = dict();
total_production = 0

carbon_production = dict();
total_carbon_production = 0

consumption = dict();
total_consumption = 0

optimize_carbon_production = dict();
total_optimize_carbon_production = 0

#0 = date
#1 = ZONE
#2 = Carbon intensity

number_of_line = 0
for l in libelle_fe_reader[1:] :
	optimize_production = optimize_energy(l)
	number_of_line+=1
	if(l[0] in production):
		production[l[0]] = int(l[10]) + int(production[l[0]])
		consumption[l[0]] = int(l[9]) + int(consumption[l[0]])
		carbon_production[l[0]] = int(carbon_production[l[0]]) + (int(l[2]) * int(l[10]))
		optimize_carbon_production[l[0]] = int(calculator_carbon_intensity(optimize_production)) + int(optimize_carbon_production[l[0]])
	else: 
		production[l[0]] = int(l[10])
		consumption[l[0]] = int(l[10])
		carbon_production[l[0]] = (int(l[2]) * int(l[10])) 
		optimize_carbon_production[l[0]] = int(calculator_carbon_intensity(optimize_production))

print(str(len(production)) + " clé dans le dictionnaire")
with open('european_result.csv', 'w', newline='') as file:
	writer = csv.writer(file, delimiter=';')
	writer.writerow([
			"",
			"date",
			"totale production",
			"total consumption",
			"diff conso / prod (%)",
			"carbon production (kg)",
			"new carbon production (kg)"
		])
	for key in production.keys():

		aux_cons = int(consumption.get(key))
		aux_prod = int(production.get(key))
		aux_carbon_prod = int(carbon_production.get(key))
		aux_opti_carbon_prod = int(optimize_carbon_production.get(key))

		total_production = total_production + aux_prod
		total_consumption = total_consumption + aux_cons
		total_carbon_production = total_carbon_production + aux_carbon_prod
		total_optimize_carbon_production = total_optimize_carbon_production + aux_opti_carbon_prod

		writer.writerow([
			"",
			str(key),
			str(aux_prod),
			str(aux_cons),
			str(((aux_prod-aux_cons) / (aux_prod)) * 100),
			str(aux_carbon_prod),
			str(aux_opti_carbon_prod)
		])
	writer.writerow([
			"TOTAL",
			"",
			str(total_production),
			str(total_consumption),
			"",
			str(total_carbon_production),
			str(total_optimize_carbon_production)
		])








