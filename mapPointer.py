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

def ambigiousnames():
	fileHandle = open('./data/ambiguousnamesCorrected.csv','r')
	outHandle = open('latlongdataMH.csv','a')
	ambigous = []

	for line in fileHandle:
		line = line.strip()
		latlong = findLatLong(line)
		apmc = line.split(",", 1)[0]

		if len(latlong) > 1:
			ambigous.append(apmc)
			continue

		for ltll in latlong:
			outHandle.write( apmc + ";")
			outHandle.write(str(ltll['lat']) + ";")
			outHandle.write(str(ltll['lng']) + ";")
		outHandle.write("\n")
		print "completed..", apmc

	fileHandle.close()
	outHandle.close()
	print ambigous
	
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
			continue

		for ltll in latlong:
			fileHandle.write(str(ltll['lat']) + ";")
			fileHandle.write(str(ltll['lng']) + ";")
		fileHandle.write("\n")
		print "completed..", name
	fileHandle.close()

if __name__ == '__main__':
	preparePositions()
	ambigiousnames()