# Meteo_Cloud_MQTT
NAT Sainlogic WS3500 wunderground do MQTT Server

sends sensor data both to the site, www.wunderground.com, and to the local MQTT server


## Supported devices
In general, if the station is supplied with `EasyWeather` software (version 1.4.x, 1.5.x), it is likely that the station will work with Home Assistant coupled with the MQTT server

### Tested

* Sainlogic WS3500
* 


### WS View (WS Tool)
If supported by your PWS, connect your PWS with `WS View` (and also the 'older' `WS Tool`) to your router by wifi, so that your PWS can upload weather data to Domoticz.

1. Install `WS View` on your mobile device
    * [Google Play Store](https://play.google.com/store/apps/details?id=com.ost.wsview)
    * [Apple App Store](https://apps.apple.com/us/app/ws-view/id1362944193)
1. , or `WS Tool`
    * [Google Play Store](https://play.google.com/store/apps/details?id=com.dtston.wstool)
    * [Apple App Store](https://apps.apple.com/nl/app/ws-tool/id1125344077)
1. Follow the instructions to connect your PWS to your router
1. Goto to Device List in Menu and choose your PWS
1. Click on Next untill you are on on the `Customized` page
1. Choose `Enable`
1. For `Protocol Type Same As` choose `Wunderground` (preferred)
1. For `Server IP / Hostname` enter your Domoticz Server ip address, eg. 192.168.0.10
1. If you choose for `Wunderground` protocol:
    * Fill in `Station ID` with a value
    * Fill in `Station Key` with a value
1. `Port` enter a free port number, eg. `8077`
1. `Upload Interval`, leave it `16` seconds
1. Click on `Save`


![Screenshot](https://github.com/Xorfor/Domoticz-PWS-Plugin/blob/master/images/screendump3.png)  ![Screenshot](https://github.com/Xorfor/Domoticz-PWS-Plugin/blob/master/images/screendump2.png)



### Init
Register a new device on the site https://www.wunderground.com
Copy
Station ID:XXXXXXXXXX
Station Key:XXXXXXXX
### Attention TCP PORT 8077

### Add  Home Assistant
to add sensor data to Home Assistant 
edit the file configuration.yaml 

add in section sensor:

<ul>
   sensor:<br/>   
     - platform: mqtt<br/></li>
       name: "Temperatura Esterna"<br/>
       state_topic: "Home/meteo/sensors"<br/>
       value_template: "{{ value_json.tempf }}"<br/>
       unit_of_measurement: '°F'<br/>
       device_class: temperature<br/>
      force_update: true<br/>
</ul>


it is possible to do for all parameters contained in parametri[]<br/>
value_json.indoortempf<br/>
value_json.tempf<br/>
value_json.dewptf<br/>
value_json.baromin ecc.. ecc...<br/>

