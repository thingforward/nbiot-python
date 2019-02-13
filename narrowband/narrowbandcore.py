import time
from threading import Thread
import serial
from serial.tools import list_ports

class NarrowbandCore():

    def __init__(self, device="auto", baud="auto", out="auto", reboot=True):
        self.net_registered = False
        self.net_connected = False
        self.net_attached = False
        self.udp_socket_active = False
        self.tcp_socket_active = False
        self.udp_socket_id = -1
        self.tcp_socket_id = -1
        self.udp_socket_last_cmd = False
        self.tcp_socket_last_cmd = False
        self.udp_remote_addr = "0.0.0.0"
        self.last_cmd_ok = True
        self.verbose = True
        self.REBOOT_TIME = 10
        self.current_device = "BC95"

        if device is "auto":
            dev, baud = self.__find_device()
            if baud >= 9600:
                self.ser = serial.serial_for_url(dev, baudrate=baud, timeout=2)
            else:
                print("No NB device detected!")
                return -1
        else:
            self.ser = serial.serial_for_url(device, baudrate=baud, timeout=out)
            self.current_device = "unknown"

        thread = Thread(target=self.__listen, args=())
        thread.start()

        self._display_product_identification_information()
        while self.current_device == "":
            time.sleep(1)

        print("Found: "+self.current_device+" with baudrate "+str(baud))

        if reboot:
            if self.current_device == "BC68" or self.current_device == "BC95":
                self.reboot()
            else:
                print("Reboot not supported for this device")

        self._set_echo_mode("0")

    def __find_device(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            ser = serial.Serial(port.device)
            ser.timeout = 1
            for baudrate in ser.BAUDRATES:
                if baudrate == 9600 or baudrate == 115200:
                    print("Checking "+port.device+" with baudrate "+str(baudrate))
                    ser.baudrate = baudrate
                    ser.write(str.encode("ATI\r"))
                    resp = ser.read()
                    try:
                        if resp.decode("utf-8") != '':
                            return port.device, baudrate
                    except:
                        pass
                if ser.baudrate > 115200:
                    return "UNKNOWN",-1

        else:
            return "UNKNOWN",-1

    def __readline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    def __listen(self):
        while True:
            if self.ser.in_waiting > 0:
                data = self.__readline()
                dataStr = ""
                try:
                    dataStr = data.decode("utf-8")
                except:
                    print("\r\nUTF-8 decode error with:")
                    print(data)
                    self.last_cmd_ok = True
                    self.current_device = "unknown"
                    pass

                if dataStr and not dataStr.isspace():
                    if "CEREG:1" in dataStr:
                        if not self.net_registered:
                            print("Registered in network!")
                        self.net_registered = True
                    elif "CSCON:1" in dataStr:
                        if not self.net_connected:
                            print("Connected to network!")
                        self.net_connected = True
                    elif "CGATT:1" in dataStr:
                        if not self.net_attached:
                            print("Attached to network!")
                        self.net_attached = True
                    elif "NSONMI" in dataStr:
                        self._get_udp_socket_data(dataStr[11:])
                    elif "NPING" in dataStr:
                        print(dataStr)
                    elif "ERROR" in dataStr:
                        print(dataStr)
                        self.last_cmd_ok = True
                    elif "Revision:" in dataStr:
                        if "BC66" in dataStr:
                            self.current_device = "BC66"
                        elif "BC68" in dataStr:
                            self.current_device = "BC68"
                        elif "BC95" in dataStr:
                            self.current_device = "BC95"
                    elif "OK" in dataStr:
                        self.last_cmd_ok = True
                    elif self.udp_remote_addr in dataStr:
                        udp_response = dataStr.split(',')
                        print(bytes.fromhex(udp_response[4]).decode('utf-8'))
                    if self.verbose:
                        if not dataStr.isspace():
                            print(dataStr)
                    if self.udp_socket_last_cmd and not dataStr.isspace() and self.udp_socket_id is -1:
                        self.udp_socket_id = int(dataStr)
                        self.udp_socket_last_cmd = False
                    if self.tcp_socket_last_cmd and not dataStr.isspace() and self.udp_socket_id is -1:
                        self.tcp_socket_id = int(dataStr)
                        self.tcp_socket_last_cmd = False

    def exec_at_cmd(self, cmd):
        while not self.last_cmd_ok:
            time.sleep(1)

        if not self.ser.isOpen():
            self.ser.open()
            print('opening port\n')

        ret = self.ser.write(str.encode(cmd+"\r"))
        if self.verbose:
            print('\r\n--> {}\n'.format(repr(cmd)))

        self.last_cmd_ok = False

    def _display_product_identification_information(self):
        self.ser.write(str.encode("ATI\r"))
        print('\r\n--> {}\n'.format(repr("ATI")))

    def reboot(self):
        self.exec_at_cmd("AT+NRB")
        now = time.time()
        future = now + self.REBOOT_TIME
        while time.time() < future:
            time.sleep(1)

    def _set_echo_mode(self, status):
        if(status is "0" or status is "1"):
            self.exec_at_cmd("ATE"+status)

    def _set_module_functionality(self, status):
        self.exec_at_cmd("AT+CFUN="+status)

    def _get_module_functionality(self):
        self.exec_at_cmd("AT+CFUN?")

    def _set_plmn(self, mode, oper=None):
        if oper:
            self.exec_at_cmd("AT+COPS="+mode+",2,"+oper)
        else:
            self.exec_at_cmd("AT+COPS="+mode)

    def _get_plmn(self):
        self.exec_at_cmd("AT+COPS?")

    def _set_pdp_context(self, apn):
        self.exec_at_cmd('AT+CGDCONT=0,"IP","'+apn+'"')

    def _get_pdp_context(self):
        self.exec_at_cmd("AT+CGDCONT?")

    def _set_ncdp(self, cdp):
        self.exec_at_cmd("AT+NCDP="+cdp)

    def _get_ncdp(self, cdp):
        self.exec_at_cmd("AT+NCDP?")

    def _set_signalling_connection_status(self, status):
        self.exec_at_cmd("AT+CSCON="+status)

    def _get_signalling_connection_status(self):
        self.exec_at_cmd("AT+CSCON?")

    def _set_eps_network_registration_status(self, status):
        self.exec_at_cmd("AT+CEREG="+status)

    def _get_eps_network_registration_status(self):
        self.exec_at_cmd("AT+CEREG?")

    def _set_attach_status(self, status):
        self.exec_at_cmd("AT+CGATT="+status)

    def _get_attach_status(self):
        self.exec_at_cmd("AT+CGATT?")

    #DGRAM, STREAM // 17, 6
    def _create_socket(self, type, protocol, listenport):
        self._close_socket(0)
        self.exec_at_cmd("AT+NSOCR="+type+","+protocol+","+listenport)

    def _close_socket(self, socket):
        self.exec_at_cmd("AT+NSOCL="+str(socket))

    def _udp_send(self, socket, remote_addr, remote_port, length, data):
        self.udp_remote_addr = remote_addr
        self.exec_at_cmd("AT+NSOST="+socket+","+remote_addr+","+remote_port+","+length+","+data)

    def _ping_send(self, remote_addr, p_size=12, timeout=10000):
        self.exec_at_cmd("AT+NPING="+remote_addr+","+str(p_size)+","+str(timeout))

    def _get_udp_socket_data(self, size):
        self.exec_at_cmd("AT+NSORF="+str(self.udp_socket_id)+","+size)
