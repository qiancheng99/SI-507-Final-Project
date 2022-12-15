import requests
import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
This file is used to generate 3 cahce files: test.json, airport_dict.json and airlines_us.json
"""

if not os.path.exists('test.json'):
	url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/airlines.json"

	headers = {
		"X-Access-Token": "undefined",
		"X-RapidAPI-Key": "6ba009b4d2msh4e252de979d76a6p11dc08jsn1f59c660d315",
		"X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers)
	json_object = json.loads(response.text)
	print(type(json_object))
	print(len(json_object))
	with open("test.json", "w") as outfile:
		outfile.write(json.dumps(json_object))

if not os.path.exists('airport_dict.json'):
	wikiurl = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States"
	response = requests.get(wikiurl)
	print(response.status_code)
	soup = BeautifulSoup(response.text, 'html.parser')
	indiatable = soup.find('table', {'class': "wikitable"})
	df = pd.read_html(str(indiatable))
	df = pd.DataFrame(df[0])
	airport_dict = {}
	states = ""
	for i in range(len(df)):
		if pd.isnull(df.loc[i]["Airport"]):
			states = df.loc[i]['City']
			continue
		if pd.isnull(df.loc[i]["IATA"]):
			continue
		airport_dict[df.loc[i]['IATA']] = [states, df.loc[i]['City'], df.loc[i]['Airport']]
	json_object = json.dumps(airport_dict, indent=4)
	with open("airport_dict.json", "w") as outfile:
		outfile.write(json_object)


if not os.path.exists('airlines_us.json'):
	f = open('airport_dict.json')
	airport_dict = json.load(f)
	for key in airport_dict.keys():
		airport_dict[key].append({})

	f = open('test.json')
	data = json.load(f)
	# print(type(data))
	i=0
	for route in data:
		if (route["departure_airport_iata"] not in airport_dict) or \
				(route["arrival_airport_iata"] not in airport_dict) or \
				(route["transfers"]>0):
			continue
		else:
			if route["arrival_airport_iata"] not in airport_dict[route["departure_airport_iata"]][-1]:
				i+=1
				if i % 10 == 0: print(i)
				url = "https://www.airmilescalculator.com/distance/"+route["arrival_airport_iata"]+"-to-"+route["departure_airport_iata"]
				# # print(url)
				response = requests.get(url)
				# print(response.status_code)
				soup = BeautifulSoup(response.text, 'html.parser')
				indiatable = soup.find_all('div', {'class': "numberline"})
				number = []
				for div in indiatable:
					number.append(div.getText().strip("\n"))
				airport_dict[route["departure_airport_iata"]][-1][(route["arrival_airport_iata"])]=number
				# print(number)
			if route["departure_airport_iata"] not in airport_dict[route["arrival_airport_iata"]][-1]:
				airport_dict[route["arrival_airport_iata"]][-1][(route["departure_airport_iata"])]=number

	keys=[]
	for key in airport_dict.keys():
		if len(airport_dict[key][-1])==0:
			keys.append(key)
	for key in keys:
		airport_dict.pop(key, None)
	print(len(airport_dict))

	json_object = json.dumps(airport_dict, indent=4)
	with open("airlines_us.json", "w") as outfile:
		outfile.write(json_object)




