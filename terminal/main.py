__author__ = 'guoxiao'

from serialUtils import *
from updateUtils import *
from commUtils import *
# from confUtils import *
import os, time
import gpio
import redis

if __name__ == "__main__":
    print "start 3G port"
    #start 3G interface
    os.system("sudo usb_modeswitch -c /etc/usb_modeswitch.d/12d1\:15ca")
    time.sleep(60)
    os.system("sudo wvdial -C /etc/wvdial.conf &")
    time.sleep(120)
    ip = get_ip_address('ppp0')
    cmd = "sudo route add default gw %s" % (ip)
    #print cmd
    os.system(cmd)

    #sync time for devies
    print "start sync time"
    os.system("ntpdate -u ntp.api.bz")

    # duration = get_update_duration()
    
    r=redis.Redis()
    duration = r.get('duration')
    if duration:
        duration = int(duration)
    else:
       duration = 10

    gpio.pin_mode(2,gpio.OUTPUT)
    ser = init_serial_port()
    ser = open_serial_port(ser)
    TProcess = CountDownExec.get_instance('serial_update', duration, exe_collection_datas, args={"serial": ser})
    UProcess = CountDownExec.get_instance('net_update', duration, exe_update)
    CProcess = CountDownExec.get_instance('ctrl_update', CTRL_UPDATE_DURATION, exe_ctrl)

    TProcess.start()
    UProcess.start()
    CProcess.start()
