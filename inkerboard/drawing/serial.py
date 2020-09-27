import enum
import serial
import struct

SYNC1 = int(0xAA).to_bytes(1, 'little')
SYNC2 = int(0x55).to_bytes(1, 'little')


class EpaperImageType(enum.IntEnum):
    IMAGE_INTERNAL = 0
    IMAGE_EXT_UNCOMPRESSED = 1
    IMAGE_EXT_COMPRESSED = 2


class EpaperOrientation(enum.IntEnum):
    NO_ROTATION = 0
    ROTATED = 1


class EpaperSerial(object):
    def __init__(self, comport: str, orientation: EpaperOrientation):
        self.baudrate = 1000000
        self.orientation = orientation

        try:
            self.ser = serial.Serial(comport, self.baudrate)
        except serial.SerialException as e:
            self.open = False
            raise e
        else:
            self.open = True

    def __del__(self):
        self.ser.close()

    @staticmethod
    def _packed_data(cmd, data):
        values = (SYNC1, SYNC2, int(cmd).to_bytes(1, 'little'), bytearray(data))
        packer = struct.Struct(f'c c c {len(data)}s')
        packed_data = packer.pack(*values)
        return packed_data

    def _write_serial(self, data):
        if self.open:
            self.ser.write(data)
        else:
            raise serial.SerialException('Serial port is not open!')

    def internal_image(self, image):
        pass

    def write_image(self, data, compressed=False):
        if compressed:
            cmd = (EpaperImageType.IMAGE_EXT_COMPRESSED << 6) | (self.orientation << 5)
        else:
            cmd = (EpaperImageType.IMAGE_EXT_UNCOMPRESSED << 6) | (self.orientation << 5)

        self._write_serial(self._packed_data(cmd, data))