import requests, json
from datetime import *
import time

url = "http://app.objco.com:8099/?account=MRHAOCUYL2&limit=1"
datas = requests.get(url)
datas.encoding
datas=datas.text
datas=json.loads(datas)


def convert_date(date):
    """
    Convertis la date recupéré dans le format attendu en base de donnée.

    Args:
        date (str): date recupéré dans la requête

    Returns:
        date (str): date dans le bon format
    """
    date_object = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
    # Formatter la date au format ISO 8601
    iso_date = date_object.strftime('%Y-%m-%d %H:%M:%S')
    return iso_date

def get_sensor_info():
    for data in datas :
        exa_code = data[1]
        
        #! DATE !#
        date = data[2]
        date = convert_date(date)
        
        #! Tag INFO !#    
        tag_info_index = exa_code.index("62182")
        tag_info = exa_code[tag_info_index:tag_info_index+22]
        print(tag_info)
        id_capteur = tag_info[0:7]
        status = int(tag_info[8:9], 16)
        battery = int(tag_info[10:14], 16)
        battery = battery / 1000
        battery = (battery - 3.32) // 0.083
        temperature = int(tag_info[14:18], 16)
        temperature = temperature / 10
        rssi_signal = int(tag_info[20:22], 16)
        
        
        if id_capteur == "62182660" :
            sensor_type = 1 #temperature
            return id_capteur, sensor_type, temperature, date, rssi_signal
            
        else :
            humidity = int(tag_info[18:20], 16)
            sensor_type = 2 #temperature and humidity
            return id_capteur, sensor_type, temperature, humidity, date, rssi_signal
while True :
    print(get_sensor_info())
    time.sleep(60*5)