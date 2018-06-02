# Ecobici data listening

### Summary

`stations.py` send API requests for every docking station that is part of Buenos Aires' bicycle sharing system. It's purpose is to collect data on how many docked bicycles  and available positions are in each of the 198 stations. A comprehensive list of all docking stations to present can found in  `data/stations.json`

`weather.py`: gets the HTML of two weather stations sites, parses it with the use of BeautifulSoup and returns weather variables as temperature, wind, rain, etc.

Data collected by both scripts is ment to be use for docking stations usage prediction using machine learning in a latter proyect.

### How to use

Both scripts should be use with cron so they can be executed at time intervals. We suggest running `stations.py` every 5 minutes and `weather.py` every 30 minutes. For the `stations.py` add a 1 minute buffer after the 5 minute interval mark to make sure that server side data is updated since the server updates its data every five minutes. `crontab -e` file should look like this:

```
# m h  dom mon dow   command
1-59/5 * * * * python /path/to/script/stations.py
   */5 * * * * python /path/to/script/weather.py
```

Don't forget to set the appropiate permissions for both scripts.

```
sudo chmod +x script.py
```