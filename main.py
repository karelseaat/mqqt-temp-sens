import gc
import time
import ujson

from filehelper import makefileifneed
from websettings import websettings

import network
import urequests
from machine import Pin

gc.enable()

def connection(network_name, network_password):
    attempts = 0
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network...")
        station.active(True)
        station.connect(network_name, network_password)
        while not station.isconnected():
            print("Attempts: {}".format(attempts))
            attempts += 1
            time.sleep(5)
            if attempts > 3:
                return None
                break
    print('Network Config:', station.ifconfig())
    return station


def captive_portal(websets):

    import usocket as socket
    


    existing_config = websets.test_config() 

    if not existing_config:

        from dnsquery import DNSQuery
        websets.setTemplate('set_ap.html')
        websets.setregexp(['networkname','password','mqaddress','mqname', 'mqpass'])

        websets.addTempVars({'ssid':'networkname','pass':'password','mqaddress':'mqaddress','mqname':'mqname','mqpass':'mqpass'})

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid='tempsens', authmode=1)

        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.bind(('',53))

        s = socket.socket()

        ip = ap.ifconfig()[0]
        ai = socket.getaddrinfo(ip, 80)
        
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        s.settimeout(30)

        dnss = DNSQuery()
        dnss.setUDPs(udps)
        dnss.setIP(ip)

        while True:
            dnss.DNSQnA()
            websets.WEBQnA(s)
            time.sleep_ms(1000)
        udps.close()

    else:
        from umqtt.simple import MQTTClient
        import machine
        from htu21d import HTU21D

        from machine import I2C

        connection(existing_config['networkname'],existing_config['password'])

        i2c = I2C(scl=Pin(14), sda=Pin(2))

        htu = HTU21D(i2c)


        mqc = MQTTClient("klont", existing_config['mqaddress'], user='aaps', password='kippy123')
        mqc.connect()
        mqc.publish(b"temparature/aatliving", str(htu.temperature))
        mqc.publish(b"humidity/aatliving", str(htu.humidity))
        mqc.disconnect()

        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 600000)
        machine.deepsleep()

websets = websettings()

clear = Pin(0)
if not clear.value():
	websets.clear_settings()



captive_portal(websets)