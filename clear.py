if __name__ == '__main__':
    
    """This script erase all log files and set countes inside .dat to 0"""

    # Clean logs

    with open('./log/stationsLog.txt', 'w') as file:
        pass

    with open('./log/weatherLog.txt', 'w') as file:
        pass

    # Restart counter

    with open('./data/stationsData.dat', 'w') as file:
        file.write('0')

    with open('./data/weatherData.dat', 'w') as file:
        file.write('0')

