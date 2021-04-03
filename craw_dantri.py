import urllib.request
import re
import json
from flask import Flask, request, jsonify

def readContentUrl(url):
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    header = {'User-Agent': userAgent}
    
    req = urllib.request.Request(url, data=None, headers=header)
    with urllib.request.urlopen(req) as response:
        thePage = response.read()
    return thePage.decode("utf-8")


def regexSearchGroup(regex, data):
    matches = re.finditer(regex, data, re.DOTALL)
 
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

post = {}

def crawDanTri(url):

    strData = readContentUrl(url)

    regexCatalogys = r"dt-breadcrumb\">(.*?)\/ul>"
    catalogys = regexSearch(regexCatalogys, strData)
    regexCatalogy = r"title=\"(.*?)\""
    post['catalogy'] = regexSearchGroup(regexCatalogy, catalogys)[1]

    regexTime = r"dt-news__time\">(.*?)<\/span>"
    post['time'] = regexSearch(regexTime, strData)

    regexTitle = r"dt-news__title\">(.*?)<\/h1"
    post['title'] = regexSearch(regexTitle, strData)

    regexSapo = r"Dân trí</span><h2>(.*?)<\/h2"
    post['sapo'] = regexSearch(regexSapo, strData)

    regexStrKeyWord = r"dt-news__tag-list\">(.*?)<\/ul>"
    strKeyWord = regexSearch(regexStrKeyWord, strData)
    regexKeyWord = r"title=\"(.*?)\" href"
    post['keyword'] =  regexSearchGroup(regexKeyWord, strKeyWord)

    regexContentAndAuthor = r"dt-news__content(.*?)<\/div>"
    contentAndAuthor = regexSearch(regexContentAndAuthor, strData)

    regexAuthor = r"strong>(.*?)<\/strong>"
    post['author'] = regexSearch(regexAuthor, contentAndAuthor)

    strContents = re.sub(r"figcaption>\n(.*?)\n<\/figcaption", "123456", contentAndAuthor)
    strContents = re.sub(r"<a.*?>", "", strContents)
    strContents = re.sub(r"<\/a>", "", strContents)
    strContents = re.sub(r"&nbsp;", "", strContents)
    strContents = re.sub(r"<\/em>", " ", strContents)
    strContents = re.sub(r"<em>", " ", strContents)

    regexContent = r"<p>(.*?)<\/p>"
    contents = regexSearchGroup(regexContent, strContents)

    content = ''
    for sub in contents:
        content += sub + "\n"

    post['content'] = content
    return post


url = "https://dantri.com.vn/xa-hoi/bo-tu-phap-noi-ve-vu-nhan-boi-thuong-oan-sai-23-ty-dong-phai-chi-900-trieu-20210402200352849.htm"
url1 = "https://dantri.com.vn/phap-luat/tra-ho-so-de-dieu-tra-bo-sung-vu-an-lien-quan-den-cuu-pho-chu-tich-tphcm-20210402211930747.htm"

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def getListPostUser():
   response = jsonify({
      'result' : crawDanTri(url)
   })
   response.headers.add('Access-Control-Allow-Origin', '*')
   return response

if __name__ == "__main__":
   app.run()
 
 