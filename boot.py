import gc
import network


ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    sta_if.active(True)
    sta_if.connect('WIFI', 'PASSWORD')
    while not sta_if.isconnected():
        pass

gc.collect()
