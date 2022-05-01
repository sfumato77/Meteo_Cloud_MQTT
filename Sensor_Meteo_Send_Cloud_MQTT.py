import socketserver
import json
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import time
import os
import paho.mqtt.client as mqtt


MQTT_SERVER = "192.168.0.100"
MQTT_PORT = 1883
MQTT_TOPIC = "Home/meteo/sensors"
MQTT_USER = "mqtt_user"
MQTT_PASSWORD = "mqtt_passwd"

URL_CLOUD = (
    "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
)

parametri = [
    "ID",
    "PASSWORD",
    "indoortempf",
    "tempf",
    "dewptf",
    "windchillf",
    "indoorhumidity",
    "humidity",
    "windspeedmph",
    "windgustmph",
    "winddir",
    "absbaromin",
    "baromin",
    "rainin",
    "dailyrainin",
    "weeklyrainin",
    "monthlyrainin",
    "solarradiation",
    "UV",
    "dateutc",
    "softwaretype",
    "action",
    "realtime",
    "rtfreq",
]

valori = []

json_dati = "{}"
sensori_dict = json.loads(json_dati)

json__dati_mqtt = "{}"
sensori_dict_mqtt = json.loads(json__dati_mqtt)

def prepare_date_tx_mqtt_dati():

    json__dati_mqtt = json.dumps(sensori_dict)
    sensori_dict_mqtt = json.loads(json__dati_mqtt)

    sensori_dict_mqtt["UV"] = int(sensori_dict_mqtt["UV"])
    sensori_dict_mqtt["absbaromin"] = float(sensori_dict_mqtt["absbaromin"])
    sensori_dict_mqtt["baromin"] = float(sensori_dict_mqtt["baromin"])
    sensori_dict_mqtt["dailyrainin"] = float(sensori_dict_mqtt["dailyrainin"])
    sensori_dict_mqtt["rainin"] = float(sensori_dict_mqtt["rainin"])
    sensori_dict_mqtt["dewptf"] = float(sensori_dict_mqtt["dewptf"])
    sensori_dict_mqtt["humidity"] = int(sensori_dict_mqtt["humidity"])
    sensori_dict_mqtt["indoorhumidity"] = int(sensori_dict_mqtt["indoorhumidity"])
    sensori_dict_mqtt["indoortempf"] = float(sensori_dict_mqtt["indoortempf"])
    sensori_dict_mqtt["monthlyrainin"] = float(sensori_dict_mqtt["monthlyrainin"])
    sensori_dict_mqtt["solarradiation"] = float(sensori_dict_mqtt["solarradiation"])
    sensori_dict_mqtt["tempf"] = float(sensori_dict_mqtt["tempf"])
    sensori_dict_mqtt["weeklyrainin"] = float(sensori_dict_mqtt["weeklyrainin"])
    sensori_dict_mqtt["windchillf"] = float(sensori_dict_mqtt["windchillf"])
    sensori_dict_mqtt["winddir"] = int(sensori_dict_mqtt["winddir"])
    sensori_dict_mqtt["windgustmph"] = float(sensori_dict_mqtt["windgustmph"])
    sensori_dict_mqtt["windspeedmph"] = float(sensori_dict_mqtt["windspeedmph"])
    sensori_dict_mqtt["dateutc"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensori_dict_mqtt["softwaretype"] = sensori_dict_mqtt["softwaretype"]
    sensori_dict_mqtt["rtfreq"] = int(sensori_dict_mqtt["rtfreq"])
    sensori_dict_mqtt["realtime"] = int(sensori_dict_mqtt["realtime"])
    sensori_dict_mqtt["action"] = sensori_dict_mqtt["action"]
    sensori_dict_mqtt["ID"] = sensori_dict_mqtt["ID"]
    sensori_dict_mqtt["PASSWORD"] = sensori_dict_mqtt["PASSWORD"]

    json__dati_mqtt = json.dumps(sensori_dict_mqtt, sort_keys=True, indent=4)
    sensori_dict_mqtt = json.loads(json__dati_mqtt)

    client = mqtt.Client()
    try:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.publish(MQTT_TOPIC, json__dati_mqtt)


    except:
        print("errore invio dati mqtt")


def invia_dati_al_cloud(url):

    try:
        r = requests.get(url)
        print(r.text)
    except:
        print("errore invio dati al cloud")

#da json crea url da inviare al cloud con tutti i parametri e valori
def crea_url(parametri, valori):

    url = URL_CLOUD

    for i in range(len(parametri)):
        url = url + parametri[i] + "=" + valori[i] + "&"

    if url[len(url) - 1] == "&":
        url = url[:-1]

    if " " in url:
        url = url.replace(" ", "%20")

    return url

def crea_json(parametri, valori):
    for i in range(len(parametri)):
        sensori_dict[parametri[i]] = valori[i]


def aggiusta_url_popola_valori(url):
    url = url.replace("GET /", "https://weatherstation.wunderground.com/")
    url = url.replace(" HTTP/1.1", "")

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    valori.clear()

    for i in range(len(parametri)):
        valori.append(params[parametri[i]][0])

    valori[len(parametri) - 1] = "5"

    return valori


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} write:".format(self.client_address[0]))
        # print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

        messaggio = self.data.decode("utf-8")
        aggiusta_url_popola_valori(messaggio)
        crea_json(parametri, valori)
        url_cloud = crea_url(parametri, valori)
        invia_dati_al_cloud(url_cloud)

        prepare_date_tx_mqtt_dati()


aServer = socketserver.TCPServer(("", 8077), MyTCPHandler)
aServer.serve_forever()
