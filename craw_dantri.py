import urllib.request
import re

def readContentUrl(url):
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    header = {'User-Agent': userAgent}
    
    req = urllib.request.Request(url, data=None, headers=header)
    with urllib.request.urlopen(req) as response:
        thePage = response.read()
    return thePage.decode("utf-8")
url = "https://dantri.com.vn/xa-hoi/bo-tu-phap-noi-ve-vu-nhan-boi-thuong-oan-sai-23-ty-dong-phai-chi-900-trieu-20210402200352849.htm"

def regexSearchGroup(regex, data):
    matches = re.finditer(regex, data, re.MULTILINE)
 
    listData = []
    for matchNum, match in enumerate(matches, start=1):
        #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            listData.append(data[match.start(groupNum) : match.end(groupNum)])
            #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
 
    return listData
   
def regexSearch(regex, data):
    matches = re.search(regex, data, re.DOTALL)
    if matches: 
        result = data[matches.start(1): matches.end(1)]
    else: 
        result = None
    return result

strData = readContentUrl(url)

post = {}

regexCatalogys = r"dt-breadcrumb\">(.*?)\/ul>"
catalogys = regexSearch(regexCatalogys, strData)
regexCatalogy = r"title=\"(.*?)\""
post['catalogy'] = regexSearchGroup(regexCatalogy, catalogys)[1]

regexTime = r"dt-news__time\">(.*?)<\/span>"
post['time'] = regexSearch(regexTime, strData)

regexTitle = r"dt-news__title\">(.*?)<\/h1"
post['title'] = regexSearch(regexTitle, strData)

regexSampo = r"Dân trí</span><h2>(.*?)<\/h2"
post['sampo'] = regexSearch(regexSampo, strData)

regexAuthor = r"strong>(.*?)<\/strong>"
post['author'] = regexSearchGroup(regexAuthor, strData)[0]

regexStrKeyWord = r"dt-news__tag-list\">(.*?)<\/ul>"
strKeyWord = regexSearch(regexStrKeyWord, strData)
regexKeyWord = r"title=\"(.*?)\" href"
post['keyword'] =  regexSearchGroup(regexKeyWord, strKeyWord)

print(post['keyword'])