#!/usr/bin/python
import requests
import urllib2
from bs4 import BeautifulSoup as BS

def scrapePage(url):
	# page = urllib2.urlopen(url)
	try:
		response=requests.get(url)
		soup=BS(response.text, 'lxml')
		bodyDict={}
		bodyDict["subject"]=str(soup.find('span', class_="w-a-title margin-lr-0 margin-tb-1875em").text.strip())
		bodyDict["word"]=str(soup.find('div', class_="word-and-pronunciation").h1.string)
		meanings=[]
		div=soup.find('div', class_="wod-definition-container")
		pElem=div.findAll('p')
		for p in pElem:
			meanings.append(p.text.strip().encode('ascii', 'ignore'))
		bodyDict["meaning"]=meanings
		return bodyDict	
	except requests.ConnectionError:
		print "No Internet Dude"	

def send_simple_message(bodyDict):
    print bodyDict
    subj = bodyDict["subject"]
    del bodyDict["subject"]
    return requests.post(
        "https://api.mailgun.net/v3/sandboxb4826aa6e193438ea9708f7b575235d9.mailgun.org/messages",
        auth=("api", "key-f7416e73175aeaeb34249e9cc27ffc28"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxb4826aa6e193438ea9708f7b575235d9.mailgun.org>",
              # "to": "anurag soni <anuragsoni39@yahoo.com>",
              "to": "<anuragiit2013@gmail.com>,<anuragsoni39@yahoo.com>",
              "subject":subj ,
              "text": [bodyDict["word"].upper() , bodyDict["meaning"]]})



if __name__ == '__main__':
	url='http://www.merriam-webster.com/word-of-the-day'
	bodyDict=scrapePage(url)
	send_simple_message(bodyDict)

