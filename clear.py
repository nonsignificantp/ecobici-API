import os

if __name__ == '__main__':
    
    """This script erase all log files and set countes inside .dat to 0"""

    # Find where I am
    
    filepath = os.path.dirname(os.path.abspath(__file__)) # Stuck in the middle with you

    # Clean logs

    with open(os.path.join(filepath, 'log/stationsLog.txt'), 'w') as file:
        pass

    with open(os.path.join(filepath, 'log/weatherLog.txt'), 'w') as file:
        pass

    # Restart counter

    with open(os.path.join(filepath, 'data/stationsData.dat'), 'w') as file:
        file.write('1')

    with open(os.path.join(filepath, 'data/weatherData.dat'), 'w') as file:
        file.write('1')