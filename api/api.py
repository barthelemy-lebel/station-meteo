import json
import requests
from app.models import History, Sensor
from datetime import datetime
from django_thread import Thread
import threading
import random
import time


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


# add request url in setting
def request_to_web_service():
    while True :
        url = "http://app.objco.com:8099/?account=MRHAOCUYL2&limit=1"
        datas = requests.get(url)
        datas.encoding
        datas=datas.text
        datas=json.loads(datas)
        i=0
        for data in datas :
            exa_code = data[1]

            #! DATE !#
            date = data[2]
            date = convert_date(date)
            #! Tag INFO !#
            tag_info_index = exa_code.index("62182")
            tag_info = exa_code[tag_info_index:tag_info_index+22]

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
                name = f"Temp-{id_capteur}"
                return id_capteur, name, sensor_type, temperature, date, rssi_signal

                sensor = Sensor(id=id_capteur, name=name, type=sensor_type, status=status, lat=random.uniform(1,14), long=random.uniform(1,14))
                sensor.save()

                sensor_data_history = History(sensor=sensor, temperature=temperature, battery_level=battery, signal_rssi=rssi_signal, update_time=date)
                sensor_data_history.save()
                
                print(id_capteur,":",name,":",temperature,":",date,":",rssi_signal)

            else :
                humidity = int(tag_info[18:20], 16)
                sensor_type = 2 #temperature and humidity
                name = f"Temp-Humid-{id_capteur}"

                sensor = Sensor(id=id_capteur, name=name, type=sensor_type, status=status, lat=random.uniform(1,14), long=random.uniform(1,14))
                sensor.save()

                sensor_data_history = History(sensor=sensor, temperature=temperature, humidity=humidity, battery_level=battery, signal_rssi=rssi_signal, update_time=date)
                sensor_data_history.save()
                
                print(id_capteur,":",name,":",temperature,":",humidity,":",date,":",rssi_signal," -- ",i)
                i+=1
        time.sleep(5*60)
autoinsert = threading.Thread(target=request_to_web_service)
autoinsert.start()