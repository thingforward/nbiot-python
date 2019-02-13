try:
    from narrowbandcore import *
except ImportError:
    from narrowband.narrowbandcore import *

class Narrowband(NarrowbandCore):

    def set_cdp(self, hostname):
        self._set_module_functionality("0")
        self._set_ncdp(hostname)
        self._set_module_functionality("1")

    def set_apn(self, apn):
        self._set_pdp_context(apn)

    def attach(self):
        self._set_signalling_connection_status("1")
        self._set_eps_network_registration_status("1")
        self._set_attach_status("1")
        while not self.net_connected or not self.net_registered or not self.net_attached:
            time.sleep(1)
            if not self.net_connected:
                self._get_signalling_connection_status()
                print("Waiting for connection...")
            if not self.net_registered:
                self._get_eps_network_registration_status()
                print("Waiting for registration...")
            if not self.net_attached:
                self._get_attach_status()
                print("Waiting for attachment...")

    def send_udp(self, remote_addr, remote_port, data):
        if self.net_attached:
            if not self.udp_socket_active:
                self._create_socket("DGRAM","17","1337")
                self.udp_socket_last_cmd = True
                self.udp_socket_active = True

            while self.udp_socket_id is -1:
                time.sleep(1)

            utfStr = data.encode('utf-8')
            hexStr = utfStr.hex()
            self._udp_send(str(self.udp_socket_id), remote_addr, remote_port, str(len(bytes.fromhex(hexStr))), hexStr)