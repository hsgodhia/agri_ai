#commodity;variety;market;arrival;minprice;maxprice;modalprice;day;month;year
import datetime, time

def tsaPrep():
	infile = open("./data/data1415.csv", "r")
	fmt = "%d %B %Y"
	firstline = True
	data = {}
	for line in infile:
		if firstline:
			firstline = False
			continue
		ld = line.split(";")
		if ld[0] not in data:
			data[ld[0]] = {}
		if ld[2] not in data[ld[0]]:
			data[ld[0]][ld[2]] = {}

		dtstr = ld[7].strip()+" "+ld[8].strip()+" "+ld[9].strip()#datetime.date(int(ld[9]),int(ld[8]), int(ld[7]))
		dt = time.strptime(dtstr, fmt)
		data[ld[0]][ld[2]][dt] = ld[6]
		
	for vegie in data:
			for mkt in data[vegie]:
				if len(data[vegie][mkt]) > 291:
					print mkt +","+vegie+",",len(data[vegie][mkt])

if __name__ == '__main__':
    tsaPrep()