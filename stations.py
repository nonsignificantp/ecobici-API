import os
import requests
from random import shuffle
from datetime import datetime
from concurrent import futures
from pymongo import MongoClient

def getIterNumber():

    """Opens the file where the counter is, reads it and lastly adds one to it"""

    filepath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(filepath, 'data/stationsData.dat'), 'r') as file:
        num = file.read().strip()
    
    with open(os.path.join(filepath, 'data/stationsData.dat'), 'w') as file:
        file.write(str(int(num)+1))
    
    return int(num)

def run(ids):
    success = 0
    missing = []
    
    with futures.ThreadPoolExecutor() as mmeExecutioner:
        jobs = mmeExecutioner.map(fetch, ids)
        pass
    
    results = list(jobs)

    if not any(results):
        updateLog('No data after fetch. Sorry pal!')
        raise SystemExit(1)

    for index, job in enumerate(results):
        if job:
            updateDB(job)
            success += 1
            continue
        missing.append(ids[index])


    updateLog('{} registers were added, {} stations didn\'t respond'.format(success, (len(results) - success)))
    
    if any(missing):
        updateLog('{} The following stations are missing: {}'.format(u'\u21b3', missing))
        pass

def fetch(_id, flag = 0):

    """Fetch the data from the url that it is pass inside a list together with an id string"""

    try:
        url = 'http://epok.buenosaires.gob.ar/getObjectContent/?id=estaciones_de_bicicletas|{}'.format(_id)
        response = requests.get(url, timeout = 10)
        assert any(response.json())
        return [_id, response.json()]
    except:
        if not flag: # This will catch some of the timeout errors
            fetch(_id, 1)
        return None

def updateDB(taggedJson):
    
    """Inserts data inside a mongoDB"""
    
    data = parsed(taggedJson[0], taggedJson[1])
    
    try:
        connection = MongoClient()['ecobici']['stations']
        connection.insert_one(data)
        pass
    except:
        updateLog('No connection to mongo, sorry Pal!')
        raise SystemExit(1)

def parsed(station, json):
    
    """Parses the data into a dict to be used as JSON when inserted into mongo"""
    
    bicycles = json['contenido'][3]['valor']
    free_positions = json['contenido'][4]['valor']
    status = json['contenido'][1]['valor']
    
    data = {
            'id': iterNumber,
            'station': station,
            'bicycles': int(bicycles) if bicycles else 0,
            'free_positions': int(free_positions) if free_positions else 0,
            'status': status,
            'time': time
        }
    return data

def updateLog(msg):

    """Log inside ./log/ informes us about the exit value of the script"""

    filepath = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(filepath, 'log/stationsLog.txt'), 'a+') as file:
        file.write('[{}]({}): {}\n'.format(time, iterNumber, msg))
    pass

if __name__ == "__main__":    
    
    time = '{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    ids = [144,50,135,128,145,3,95,127,24,214,22,212,155,190,102,
        226,209,114,65,184,120,100,76,103,167,183,60,171,160,173,101,146,207,210,
        34,118,90,46,56,68,224,191,192,78,138,148,47,106,49,20,110,131,97,108,44,
        29,89,143,200,221,1,142,41,203,162,130,42,141,175,196,147,150,113,152,88,
        154,187,223,178,172,179,77,83,59,222,133,186,18,35,92,206,168,26,132,79,
        219,227,158,104,16,149,140,174,10,36,107,176,139,96,204,161,74,82,27,109,
        122,182,7,13,194,185,14,52,170,30,193,9,5,32,217,85,201,215,57,213,33,37,
        159,205,202,17,28,165,218,25,137,54,6,38,199,73,126,4,19,12,216,151,105,
        220,166,177,99,2,180,181,48,123,63,164,75,225,163,117,124,198,189,125,43,
        111,195,188,23,67,70,211,115,11,45,156,40,134,129,153,98,121,169,208,157]
    shuffle(ids)

    iterNumber = getIterNumber()
    run(ids)