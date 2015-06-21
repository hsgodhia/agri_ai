from splinter import Browser
from lxml import etree

htmldata = []
fileHandle = open('data.csv','w')
fileHandle.write('commodity, market, arrival, minprice, maxprice, modalprice, day, month, year\n')

def browserDataAutomation():    
    month, year = 1, 2014
    with Browser() as browser:
        for day in xrange(1,31):
            url = 'http://agmarknet.nic.in/agnew/NationalBEnglish/CommodityDailyStateWise.aspx?ss=2'
            browser.visit(url)
            element = browser.find_by_name('cboState')
            element.select('Maharashtra')
            element = browser.find_by_name('cboMonth')
            element.select('January')
            element = browser.find_by_name('cboYear')
            element.select('2014')  
            browser.click_link_by_text(str(day))
            browser.find_by_name('btnSubmit').first.click()
            htmldata.append(browser.html)

            table = browser.find_by_id('gridRecords')
            singleHtmlExtractor(table.html, day, month, year)
            

def singleHtmlExtractor(tableHtml, day, month, year):
    print "...html parsing in progress~~"
    commodity = ''
    table = etree.XML(tableHtml)
    rows = iter(table)
    headers = [col.text for col in next(rows)]
    for row in rows:
        values = [col.text for col in row]
        info = dict(zip(headers, values))
        if len(info.keys()) == 1:
            val = info['Market']
            val = val.strip()
            if len(val.split(":")) == 1 and val != '':
                commodity = val
        if len(info.keys()) > 5:
            fileHandle.write(commodity + ",")
            if info['Market'] is not None:
                fileHandle.write(info['Market'] + ",")
            else:
                fileHandle.write(",")

            if info['Arrivals'] is not None:
                fileHandle.write(info['Arrivals'] + ",")
            else:
                fileHandle.write(",")
            
            if info['Minimum Prices'] is not None:
                fileHandle.write(info['Minimum Prices'] + ",")
            else:
                fileHandle.write(",")   

            if info['Maximum Prices'] is not None:
                fileHandle.write(info['Maximum Prices'] + ",")
            else:
                fileHandle.write(",")
        
            if info['Modal  Prices'] is not None:
                fileHandle.write(info['Modal  Prices'] + ",")
            else:
                fileHandle.write(",")

            fileHandle.write(str(day) + "," + str(month) + "," + str(year) + "\n")
            
if __name__ == '__main__':
    browserDataAutomation()
    fileHandle.close()