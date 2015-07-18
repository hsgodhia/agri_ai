#commodity;variety;market;arrival;minprice;maxprice;modalprice;day;month;year
import datetime, time
import operator, math

def average(s):
	return sum(s) * 1.0 / len(s)

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
		
	median_reports = {}
	avg_reports = {}
	std_reports = {}
	vegie_reportdist = {}
	for vegie in data:
		reports = []
		for mkt in data[vegie]:
			reports.append(len(data[vegie][mkt]))
		reports.sort()
		avg = average(reports)
		variance = map(lambda x: (x - avg)**2, reports)
		standard_deviation = math.sqrt(average(variance))

		median_reports[vegie] = reports[len(reports)/2]
		avg_reports[vegie] = avg
		std_reports[vegie] = standard_deviation
		vegie_reportdist[vegie] = reports

	#sort the 
	median_reports = sorted(median_reports.items(), key=operator.itemgetter(1))
	std_reports = sorted(std_reports.items(), key=operator.itemgetter(1))
	avg_reports = sorted(avg_reports.items(), key=operator.itemgetter(1))
	
	print avg_reports, "\n*********\n", std_reports, "\n*********\n", median_reports
	"""
	fp = open("std_reports.csv", "w")
	fp.write("commodity;standard_deviation\n")
	for vegie in std_reports:
		fp.write(str(vegie)+";"+str(std_reports[vegie])+"\n")
	fp.close()

	fp = open("avg_reports.csv", "w")
	fp.write("commodity;avg\n")
	for vegie in avg_reports:
		fp.write(str(vegie)+";"+str(avg_reports[vegie])+"\n")
	fp.close()
	"""	
	
if __name__ == '__main__':
    tsaPrep()