from pytesseract import image_to_string
from PIL import Image
import pyscreenshot as ImageGrab
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
import string
from bs4.element import Comment
from threading import Thread
from googlesearch import search

char_whitelist = string.digits
char_whitelist += string.ascii_lowercase
char_whitelist += string.ascii_uppercase

startTime = datetime.now()

def getTime(checkpoint):
  print (checkpoint + ": " + str(datetime.now() - startTime))

def getSS(x1,y1,x2,y2,filename,showImg):
    im=ImageGrab.grab(bbox=(x1,y1,x2,y2))
    im.save(filename) # X1,Y1,X2,Y2
    if showImg:
        im.show()

def getText(filename):
    img=Image.open(filename)

    text = image_to_string(img,config="-c tessedit_char_whitelist=%s_-." % char_whitelist)
    return text

def get_results_with_question(question, answer):
    concatinate = str(answer) + " " + str(question)
    re = requests.get('https://www.google.com/search', params={'q':concatinate})
    soup = bs(re.text, "html.parser")
    response = soup.find('div', {'class': 'sd'})
    number = ""
    for char in range(len(response.text)):
        if response.text[char].isdigit():
            number+=str(response.text[char])
    return int(number)

def get_results(answer):
    re = requests.get('https://www.google.com/search', params={'q':answer})
    soup = bs(re.text, "html.parser")
    response = soup.find('div', {'class': 'sd'})
    number = ""
    for char in range(len(response.text)):
        if response.text[char].isdigit():
            number+=str(response.text[char])
    return int(number)

def checkEasy(question):
    print (question)
    re = requests.get('https://www.google.com/search', params={'q':question})
    soup = bs(re.text, "html.parser")
    response = soup.find('div', {'id' : 'search'})
    response2 = response.find('div', {'class': 'g'})
    for i in response2.find_all('div'):
        if len(i.text)>0:
            return i.text[0:20]

def only_results(ra1,ra2,ra3):
    if ra1>ra2 and ra1>ra3:
        print ("1")

    if ra2>ra1 and ra2>ra3:
        print ("2")

    if ra3>ra1 and ra3>ra2:
        print ("3")

def results_ratio(rqa1,rqa2,rqa3,ra1,ra2,ra3):
    ra1_adjusted = 0
    ra2_adjusted = 0
    ra3_adjusted = 0
    if ra1>ra2 and ra1>ra3:
        ra2_adjusted = (ra1/ra2)*rqa2
        ra3_adjusted = (ra1/ra3)*rqa3

        ra1_adjusted = rqa1

    if ra2>ra1 and ra2>ra3:
        ra1_adjusted = (ra2/ra1)*rqa1
        ra3_adjusted = (ra2/ra3)*rqa3

        ra2_adjusted = rqa2

    if ra3>ra1 and ra3>ra2:
        ra1_adjusted = (ra3/ra1)*rqa1
        ra2_adjusted = (ra3/ra2)*rqa2

        ra3_adjusted = rqa3

    if ra1_adjusted>ra2_adjusted and ra1_adjusted>ra3_adjusted:
        print ("1")

    if ra2_adjusted>ra1_adjusted and ra2_adjusted>ra3_adjusted:
        print ("2")

    if ra3_adjusted>ra1_adjusted and ra3_adjusted>ra2_adjusted:
        print ("3")

def createURL(question):
    words = question.split()
    string_URL = ""
    for word in words:
        string_URL += word
        string_URL += "%20"
    return string_URL

def get_DuckDuckGo_filtered(answer1, answer2, answer3, question):
    a1words = answer1.split()
    a2words = answer2.split()
    a3words = answer3.split()

    print(a1words)
    print(a2words)
    print(a3words)
    qwords = [a1words,a2words,a3words]
    answerTotal = 0;
    url = 'https://duckduckgo.com/html?q=' + str(question)

    header = {
        "authority":"duckduckgo.com",
        "method":"GET",
        "path":url,
        "scheme":"https",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control":"max-age=0",
        "cookie":"ax=v125-2",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
       }
    re = requests.get(url, headers=header)
    soup = bs(re.text, "html.parser")
    answerTotal = [0,0,0]
    for i in range(0,3):
        for j in range(0, len(qwords[i])):
            answerTotal[i] += str(soup).count(str(qwords[i][j]))

    if answerTotal[0]>answerTotal[1] and answerTotal[0]>answerTotal[2]:
        print ('1')
    if answerTotal[1]>answerTotal[0] and answerTotal[1]>answerTotal[2]:
        print('2')
    if answerTotal[2]>answerTotal[0] and answerTotal[2]>answerTotal[1]:
        print ('3')

def continuousGoogle():      
    response = GoogleSearch().search("something")
    for result in response.results:
        print("Title: " + result.title)
        print("Content: " + result.getText())

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self):
        Thread.join(self)
        return self._return





    
if __name__ == '__main__':
    # getSS(700,150,1180,290,"hqQ.png", False)
    # getSS(700,300,1050,340,"hqA1.png", False)
    # getSS(700,360,1050,400,"hqA2.png", False)
    # getSS(700,420,1050,455,"hqA3.png", False)

    
    thread_qtext = ThreadWithReturnValue(target = getText, args = ("hqQ.png", ))
    thread_a1text = ThreadWithReturnValue(target = getText, args = ("hqA1.png", ))
    thread_a2text = ThreadWithReturnValue(target = getText, args = ("hqA2.png", ))
    thread_a3text = ThreadWithReturnValue(target = getText, args = ("hqA3.png", ))

    thread_qtext.start()
    thread_a1text.start()
    thread_a2text.start()
    thread_a3text.start()

    qtext = thread_qtext.join()
    a1text = thread_a2text.join()
    a2text = thread_a1text.join()
    a3text =  thread_a3text.join()

    print ("text thread finished...exiting")

    print ("results thread starting...")
    continuousGoogle()
    # get_DuckDuckGo_filtered(a1text, a2text, a3text, createURL(qtext))

    # qa1_results_thread =  ThreadWithReturnValue(target = get_results_with_question, args = (qtext, a1text, ))
    # qa2_results_thread =  ThreadWithReturnValue(target = get_results_with_question, args = (qtext, a2text, ))
    # qa3_results_thread =  ThreadWithReturnValue(target = get_results_with_question, args = (qtext, a3text, ))

    # a1_results_thread =  ThreadWithReturnValue(target = get_results, args = (a1text, ))
    # a2_results_thread =  ThreadWithReturnValue(target = get_results, args = (a2text, ))
    # a3_results_thread =  ThreadWithReturnValue(target = get_results, args = (a3text, ))

    # qa1_results_thread.start()
    # qa2_results_thread.start()
    # qa3_results_thread.start()
    # a1_results_thread.start()
    # a2_results_thread.start()
    # a3_results_thread.start()

    # qa1_results =  qa1_results_thread.join()
    # qa2_results =  qa2_results_thread.join()
    # qa3_results =  qa3_results_thread.join()

    # a1_results =  a3_results_thread.join()
    # a2_results =  a3_results_thread.join()
    # a3_results =  a3_results_thread.join()

    # only_results(qa1_results,qa2_results,qa3_results)
    # results_ratio(qa1_results,qa2_results,qa3_results, a1_results, a2_results, a3_results)

    getTime("Done")
