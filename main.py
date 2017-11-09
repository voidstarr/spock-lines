import requests
import re
import io
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

f = open("spock.txt","a+")

cleanr = re.compile('<.*?>')
spockln = re.compile('SPOCK: *')

def cleanhtml(raw_html):
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = re.sub(spockln, '', cleantext)
    return cleantext

def getlines(season, ep):
    if (ep < 10):
        ep = '0' + str(ep)
    r = requests.get('https://scifi.media/wp-content/uploads/t/os/s{}-{}.txt'.format(season, ep))
    script = r.text.split('\n')
    grabNext = False
    foundSpock = False
    line = ''
    for i in range(len(script)):

        if grabNext:
            line = line + ' ' + cleanhtml(script[i])
            grabNext = False
            continue

        if (script[i].find('SPOCK:') is not -1):
            line = cleanhtml(script[i])
            foundSpock = True

        if(foundSpock and (i+1 < len(script)) and (script[i+1].find(':') is -1) and len(script[i+1]) > 0):
            grabNext = True
            #print 'GN-- {}'.format(script[i+1])
        elif len(line) != 0:
            grabNext = False
            foundSpock = False
            print line
            f.write(line + '\n')
            line = ''

def doit():
    print "s:0 e:1"
    getlines(0,1)
    for i in range(1, 30):
        print "s:1 e:{}".format(i)
        getlines(1,i)
    
    for i in range(1, 26):
        print "s:2 e:{}".format(i)
        getlines(2,i)
  
    for i in range(1, 24):
        print "s:3 e:{}".format(i)
        getlines(3,i)
    
doit()
f.close()
