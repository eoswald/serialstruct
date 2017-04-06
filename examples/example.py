import struct

import serial
import serialstruct
import time


PACKET_STRUCT = struct.Struct("<IxIx")

class MyPacket(serialstruct.StructuredPacket):

    DATA_SIZE = 10 # Excluding header: 4+1+4+1

    def __init__(self):
        super(MyPacket, self).__init__(self.DATA_SIZE)

    def handle_packet(self, packet):
        print(PACKET_STRUCT.unpack(packet))

    def send_packet(self, packet):
        self.transport.write(self.HEADER)
        self.transport.write(packet)


ser = serial.serial_for_url("loop://", baudrate=115200, timeout=1)
with serial.threaded.ReaderThread(ser, MyPacket) as protocol:
    # unsigned int, pad, unsigned int, pad; with no alignment
    packet = PACKET_STRUCT.pack(1, 2)
    protocol.send_packet(packet)
    time.sleep(1)
