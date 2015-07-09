import urllib, json

def distinctAPMCNames():
	fileHandle = open('./data/data1314.csv','r')
	#commodity;variety;market;arrival;minprice;maxprice;modalprice;day;month;year
	firstline = True
	names = []
	for line in fileHandle:
		if firstline:
			firstline = False
			continue
		fields = line.split(";")
		market = fields[2]
		if market not in names:
			names.append(market)

	for n in names:
		print n
	print "The distinct markets are: ", len(names)
	return names

def findLatLong(placeName):
	url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + placeName + ",+Maharashtra&region=in&components=administrative_area:MH|country:IN&key=AIzaSyDXu1bbOBWNqRMNNXUMt-Y9Zdr1HqCPGoY"
	res = urllib.urlopen(url)
	data = json.loads(res.read())
	results = data['results']
	latlong = []
	for result in results:
		latlong.append(result['geometry']['location'])
	
	return latlong

def preparePositions():
	names = distinctAPMCNames()
	ambigous = []
	fileHandle = open('latlongdataMH.csv','w')
	fileHandle.write("apmcName;latitute;longitude\n")
	for name in names:
		fileHandle.write(name + ";")
		latlong = findLatLong(name)
		if len(latlong) > 1:
			ambigous.append(name)

		for ltll in latlong:
			fileHandle.write(name + ";")
			fileHandle.write(str(ltll['lat']) + ";")
			fileHandle.write(str(ltll['lng']) + ";")
		fileHandle.write("\n")
		print "completed..", name
	fileHandle.close()
	print ambigous

if __name__ == '__main__':
	preparePositions()