__author__ = 'guoxiao'

from serialUtils import *
from updateUtils import *
from commUtils import *
from confUtils import *

if __name__ == "__main__":
    print "start 3G port"
    #start 3G interface
    #os.system("sudo usb_modeswitch -c /etc/usb_modeswitch.d/12d1\:15ca")
    #os.system("sudo wvdial -C /etc/wvdial.conf &")
    #sync time for devies
    #print "start sync time"
    #os.system("ntpdate -u ntp.api.bz")

    duration = get_update_duration()

    ser = init_serial_port()
    ser = open_serial_port(ser)
    TProcess = CountDownExec.get_instance('serial_update', duration, exe_collection_datas, args={"serial": ser})
    UProcess = CountDownExec.get_instance('net_update', duration, exe_update)
    #CProcess = CountDownExec.get_instance('ctrl_update', CTRL_UPDATE_DURATION, exe_ctrl)

    TProcess.start()
    UProcess.start()
    #CProcess.start()

