from scapy.all import *

def show_packet(packet):
    print(packet.show())


sniff(filter="tcmp", ifaces="en0",prn=show_packet,count=10)