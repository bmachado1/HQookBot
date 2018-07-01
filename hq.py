from pytesseract import image_to_string
from PIL import Image
import pyscreenshot as ImageGrab
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search

startTime = datetime.now()

def getTime(checkpoint):
  print checkpoint+ ": " + str(datetime.now() - startTime)

def getSS(x1,y1,x2,y2,filename,showImg):
	im=ImageGrab.grab(bbox=(x1,y1,x2,y2))
	im.save(filename) # X1,Y1,X2,Y2
	if showImg:
		im.show()

def getText(filename):
	img=Image.open(filename)
	text = image_to_string(img)
	return text

def get_results(question, answer):
	concatinate = question + " " + answer
	print concatinate
	re = requests.get('https://www.google.com/search', params={'q':concatinate})
	soup = bs(re.text, "html.parser")
	response = soup.find('div', {'class': 'sd'})
	number = ""
	for char in range(len(response.text)):
		if response.text[char].isdigit():
			number+=str(response.text[char])
	return number

def checkEasy(question):
	print question
	re = requests.get('https://www.google.com/search', params={'q':question})
	soup = bs(re.text, "html.parser")
	response = soup.find('div', {'id' : 'search'})
	response2 = response.find('div', {'class': 'g'})
	for i in response2.find_all('div'):
		if len(i.text)>0:
			return i.text[0:20]


	
if __name__ == '__main__':
	getSS(750,200,1200,350,"hqQ.png", False)

	getSS(750,350,1150,425,"hqA1.png", False)
	getSS(750,425,1150,500,"hqA2.png", False)
	getSS(750,500,1150,575,"hqA3.png", False)

	print checkEasy(getText("hqQ.png"))

	a1 =  get_results(getText("hqQ.png"), getText("hqA1.png"))
	a2 =  get_results(getText("hqQ.png"), getText("hqA2.png"))
	a3 =  get_results(getText("hqQ.png"), getText("hqA3.png"))

	if a1>a2 and a1>a3:
		print "1"

	if a2>a1 and a2>a3:
		print "2"

	if a3>a1 and a3>a2:
		print "3"
	getTime("Done")


