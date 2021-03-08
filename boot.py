import network


aps = dict()
aps['Wifi'] = 'password'
aps['Wifi'] = 'password'
aps['Wifi'] = 'password'

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    sta_if.active(True)
    networks = sta_if.scan()
    for net in networks:
        ssid = net[0].decode()
        if ssid in aps:  
            sta_if.connect(ssid, aps[ssid])
            while not sta_if.isconnected():
                pass
            break
del aps
print('network config:', sta_if.ifconfig())
