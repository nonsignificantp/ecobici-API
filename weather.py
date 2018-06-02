import os
import re
import requests
from datetime import datetime
from concurrent import futures
from pymongo import MongoClient
from bs4 import BeautifulSoup as Soup

def run():
    with futures.ThreadPoolExecutor() as mmeExecutioner:
        jobs = mmeExecutioner.map(fetch, addr)

    jobs = list(jobs)

    if not jobs:
        updateLog('No data was made available by fetch')
        raise SystemExit(1)

    for data in jobs:
        if data:
            parser(data)

    try:
        connection = MongoClient()['ecobici']['weather']
        connection.insert_one(weatherObj)
    except:
        updateLog('Mongo connection failed')
        raise SystemExit(1)

    updateLog('Success with a total of {}'.format(weatherObj['responses']))

def getIterNumber():

    """Opens the file where the counter is, reads it and lastly adds one to it"""

    filepath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(filepath, 'data/weatherData.dat'), 'r') as file:
        num = file.read().strip()
    
    with open(os.path.join(filepath, 'data/weatherData.dat'), 'w') as file:
        file.write(str(int(num)+1))
    
    return int(num)

def fetch(addr, flag=0):

    """Fetch the data from the url that it is pass inside a list together with an id string"""

    try:
        response = requests.get(addr['url'], timeout = 10)
        weatherObj['responses'] += 1
        response = Soup(response.text, 'html.parser')
        return [addr['station'], response]
    except:
        if not flag:
            fetch(addr, 1)
        return None

def parser(data):
    
    """Updates the weather object. It's this ugly since weather sites are very different with each other"""
    
    if data[0] == 'ciuUba':
        soup = data[1]
        weatherObj['stations'].append(data[0])
        weatherObj['temperature'].append(weather(soup.find_all('b')[5].text))
        weatherObj['pressure'].append(weather(soup.find_all('b')[9].text))
        weatherObj['dailyRain'].append(weather(soup.find_all('b')[13].text))
        weatherObj['rainIntensity'].append(weather(soup.find_all('b')[15].text))
        weatherObj['windVelocity'].append(weather(soup.find_all('b')[17].text))
        weatherObj['windDirection'].append(wind(soup.find_all('b')[19].text))
        weatherObj['RiseAndSet'] = riseandset(soup.find_all('b')[23].text)

    if data[0] == 'laBoca':
        soup = data[1]
        weatherObj['stations'].append(data[0])
        weatherObj['temperature'].append(weather(soup.find_all('p')[4].text))
        weatherObj['pressure'].append(weather(soup.find_all('p')[29].text))
        weatherObj['dailyRain'].append(weather(soup.find_all('p')[41].text))
        weatherObj['rainIntensity'].append(weather(soup.find_all('font')[85].text))
        weatherObj['windVelocity'].append(weather(soup.find_all('p')[33].text))
        weatherObj['windDirection'].append(wind(soup.find_all('p')[34].text))

def weather(string):
    return float(re.findall(r'\d+\{}\d+'.format('.'), string)[0])

def wind(string):
    return re.findall(r'[^\W\d]+', string.strip())[0]

def riseandset(string):
    return re.findall(r'\d+\{}\d+'.format(':'), string)

def updateLog(msg):

    """Log inside ./log/ informes us about the exit value of the script"""

    filepath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(filepath, 'log/weatherLog.txt'), 'a+') as file:
        file.write('[{}]({}): {}\n'.format(weatherObj['timestamp'], weatherObj['id'], msg))
    pass

if __name__ == '__main__':
    iterNumber = getIterNumber()
    
    weatherObj = {
        'id': iterNumber,
        'stations': [],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'responses':0,
        'temperature': [],
        'pressure': [],
        'dailyRain': [],
        'rainIntensity': [],
        'windVelocity': [],
        'windDirection': [],
        'RiseAndSet': ''
    }
    
    addr = [{
        'station':'laBoca',
        'url':'http://www.bdh.acumar.gov.ar/bdh3/meteo/boca/mb1.htm'
        },{
        'station':'ciuUba',
        'url':'http://estacion.at.fcen.uba.ar/estacion_tp.htm'
        }]

    run()