import serial
import sys
import time

from vitalsd.samplers import cpu

DEFAULT_SAMPLERS = [
    cpu.UptimeSampler(),
    cpu.CpuLoadSampler()
]

class Monitor(object):
    def __init__(self, delay_secs=10, serial_device='/dev/ttyGS0', speed=115200, bits=8, parity=None, rtscts=None):
        self.delay_secs = 10
        self.serial_device = serial_device
        self.speed = speed
        self.parity = parity
        self.rtscts = rtscts
        self.samplers = DEFAULT_SAMPLERS

    def run(self):
        with serial.Serial(self.serial_device, self.speed) as port:
            print('Writing to port {0}'.format(port.name))

            while True:
                print('Sending {0} samples.'.format(len(self.samplers)))
                for sampler in self.samplers:
                    sample = '{0}\n'.format(str(sampler))
                    port.write(bytes(sample, 'utf-8'))
                    port.flush()

                print('Sleeping for {0} seconds'.format(self.delay_secs))
                time.sleep(self.delay_secs)
