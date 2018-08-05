from bs4 import BeautifulSoup
import requests
import re

data = []

def addToList(s):
	tempListStr = list(s.lower())
	if (s != "Previous Page" and s != "Next Page" and re.match(r"^[a-zA-Z0-9]+(?:\s[a-zA-Z0-9]+)?$",s.lower()) ):
		data.append(''.join(tempListStr))

sourceStartString = "http://www.umdmusic.com/default.asp?Lang=English&Letter=A&View=I&Page=1"
sourceList = list(sourceStartString)
source = requests.get("".join(sourceList)).text
soup = BeautifulSoup(source,'lxml')
table = soup.findAll('table')[1]
ALPHABET = 26

for i in range(ALPHABET):
	print("Scraping all \'" + chr(ord(sourceList[56])) + "\' band names...")
	maxPageNum = int(table.findAll('table')[2].findAll('b')[2].text[-2:])
	currentPageNum = 1
	for j in range(maxPageNum-1):
		source = requests.get("".join(sourceList)).text
		soup = BeautifulSoup(source,'lxml')
		table = soup.findAll('table')[1]
		bandList = (table.findAll('table')[3].findAll('b'))

		for k in range(len(bandList)-1):
			addToList(bandList[k].text)

		newPage = str(currentPageNum + 1)
		currentPageNum += 1
		sourceList[-1] = newPage
	newLetter = chr(ord(sourceList[56]) + 1)
	sourceList = list(sourceStartString)
	sourceList[56] = newLetter
	source = requests.get("".join(sourceList)).text
	soup = BeautifulSoup(source,'lxml')
	table = soup.findAll('table')[1]

dataFile = open("bandnames.txt","wb+")
for i in range(len(data)):
	string_for_output = (data[i] + "\n").encode('utf8', 'replace')
	dataFile.write(string_for_output)

dataFile.close()
print("Finished Scraping!")




