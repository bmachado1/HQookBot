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

def get_results_with_question(question, answer):
	concatinate = answer + " " + question  
	re = requests.get('https://www.google.com/search', params={'q':concatinate})
	soup = bs(re.text, "html.parser")
	response = soup.find('div', {'class': 'sd'})
	number = ""
	for char in range(len(response.text)):
		if response.text[char].isdigit():
			number+=str(response.text[char])
	return number

def get_results(answer):
	re = requests.get('https://www.google.com/search', params={'q':answer})
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

def only_results(ra1,ra2,ra3):
	if ra1>ra2 and ra1>ra3:
		print "1"

	if ra2>ra1 and ra2>ra3:
		print "2"

	if ra3>ra1 and ra3>ra2:
		print "3"

# def results_ratio(rqa1,rqa2,rqa3,ra1,ra2,ra3):




	
if __name__ == '__main__':
	getSS(750,200,1200,350,"hqQ.png", False)

	getSS(750,350,1150,425,"hqA1.png", False)
	getSS(750,425,1150,500,"hqA2.png", False)
	getSS(750,500,1150,575,"hqA3.png", False)

	qtext = getText("hqQ.png")
	a1text = getText("hqA1.png")
	a2text = getText("hqA2.png")
	a3text = getText("hqA3.png")

	print checkEasy(qtext)

	qa1_results =  get_results_with_question(qtext, a1text)
	qa2_results =  get_results_with_question(qtext, a2text)
	qa3_results =  get_results_with_question(qtext, a3text)

	a1_results =  get_results(a1text)
	a2_results =  get_results(a2text)
	a3_results =  get_results(a3text)

	only_results(qa1_results,qa2_results,qa3_results)

	# results_ratio(a1,a2,a3)

	getTime("Done")


