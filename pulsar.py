from qcodes import VisaInstrument
from qcodes.utils import validators
import struct

phase_bits = {
    '1_4': {
        'mux': 0x01,
        'val': 1.4
        },
    '2_8': {
        'mux': 0x02,
        'val': 2.8
        },
    '5_6': {
        'mux': 0x04,
        'val': 5.6
    },
    '11_2': {
        'mux': 0x08,
        'val': 11.2
    },
    '22_5': {
        'mux': 0x10,
        'val': 22.5
    },
    '45': {
        'mux': 0x20,
        'val': 45
    },
    '90': {
        'mux': 0x40,
        'val': 90
    },
    '180': {
        'mux': 0x80,
        'val': 180
    },
}

class Pulsar(VisaInstrument):
    def __init__(self, name, address, baudrate=9600):

        super().__init__(name, address)

        handle = self.visa_handle
        handle.baud_rate = baudrate

        self._bit_mask = 0x00

        self.add_parameter('phase_1_4',
                           label='phase_1_4',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '1_4'),
                           get_cmd=lambda: self._get_bit('1_4')
        )

        self.add_parameter('phase_2_8',
                           label='phase_2_8',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '2_8'),
                           get_cmd=lambda: self._get_bit('2_8')
        )


        self.add_parameter('phase_5_6',
                           label='phase_5_6',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '5_6'),
                           get_cmd=lambda: self._get_bit('5_6')
        )


        self.add_parameter('phase_11_2',
                           label='phase_11_2',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '11_2'),
                           get_cmd=lambda: self._get_bit('11_2')
        )


        self.add_parameter('phase_22_5',
                           label='phase_22_5',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '22_5'),
                           get_cmd=lambda: self._get_bit('22_5')
        )

        self.add_parameter('phase_45',
                           label='phase_45',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '45'),
                           get_cmd=lambda: self._get_bit('45')
        )

        self.add_parameter('phase_90',
                           label='phase_90',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '90'),
                           get_cmd=lambda: self._get_bit('90')
        )


        self.add_parameter('phase_180',
                           label='phase_180',
                           vals=validators.OnOff(),
                           val_mapping={'on': 1, 'off': 0},
                           set_cmd=lambda val: self._set_bit(val, '180'),
                           get_cmd=lambda: self._get_bit('180')
        )
        self._write()

        self.connect_message()

    def get_idn(self):
        return {"serial": 1234, "hardware_version": 4321}


    def _set_bit(self, val, bit_string):
        bit = phase_bits[bit_string]['mux']
        if val:
            self._bit_mask |= bit
        else:
            self._bit_mask &= (~bit & 0xFF)
        self._write()


    def _get_bit(self, bit_string):
        bit = phase_bits[bit_string]['mux']
        if (bit & self._bit_mask):
            return 'on'
        else:
            return 'off'

    def _write(self):
        self.visa_handle.write_raw(struct.pack("B", self._bit_mask))
        raw = self.visa_handle.read_bytes(1)
        mask = struct.unpack('B', raw)
        assert(mask == self._bit_mask)
