from splinter import Browser
from lxml import etree
from splinter.exceptions import ElementDoesNotExist

htmldata = []
fileHandle = open('data.csv','w')
fileHandle.write('commodity;variety;market;arrival;minprice;maxprice;modalprice;day;month;year\n')

def browserDataAutomation():    
    yc = 0
    with Browser() as browser:
        for month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March']:
            yc += 1
            if yc > 9:
                year = '2015'
            else:
                year = '2014'
                
            for day in xrange(1,32):
                url = 'http://agmarknet.nic.in/agnew/NationalBEnglish/CommodityDailyStateWise.aspx?ss=2'
                browser.visit(url)
                element = browser.find_by_name('cboState')
                element.select('Maharashtra')
                element = browser.find_by_name('cboMonth')
                element.select(month)
                element = browser.find_by_name('cboYear')
                element.select(year)  
                try:
                    browser.click_link_by_text(str(day))
                    browser.find_by_name('btnSubmit').first.click()
                    htmldata.append(browser.html)
                    table = browser.find_by_id('gridRecords')
                    singleHtmlExtractor(table.html, day, month, year)
                except ElementDoesNotExist:
                    print 'did not process', day, "-", month, "-", year
            

def singleHtmlExtractor(tableHtml, day, month, year):
    print "processing....", day, "-", month, "-", year
    commodity, prevMarket, separator = '', '', ';'
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
            fileHandle.write(commodity)
            fileHandle.write(separator)
            
            if info['Variety'] is not None:
                fileHandle.write(info['Variety'])
            fileHandle.write(separator)

            if info['Market'] is not None:
                fileHandle.write(info['Market'])
                prevMarket = info['Market']
            else:
                fileHandle.write(prevMarket)
            fileHandle.write(separator)

            if info['Arrivals'] is not None:
                fileHandle.write(info['Arrivals'])
            fileHandle.write(separator)
            
            if info['Minimum Prices'] is not None:
                fileHandle.write(info['Minimum Prices'])
            fileHandle.write(separator)

            if info['Maximum Prices'] is not None:
                fileHandle.write(info['Maximum Prices'])
            fileHandle.write(separator)
        
            if info['Modal  Prices'] is not None:
                fileHandle.write(info['Modal  Prices'])
            fileHandle.write(separator)

            fileHandle.write(str(day) + separator + str(month) + separator + str(year) + "\n")
            
if __name__ == '__main__':
    browserDataAutomation()
    fileHandle.close()