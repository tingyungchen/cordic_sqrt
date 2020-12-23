from __future__ import print_function

import sys
import numpy as np
from time import time
import random
import matplotlib.pyplot as plt

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPBitFile/yclin/CORDIC_SQRT.bit")
    ipFIRN11 = ol.top_process_magnitude_0

    numSamples = 256
    ground_truth = np.zeros(numSamples)
    real_data_buffer = allocate(shape=(numSamples,), dtype=np.int32)
    imag_data_buffer = allocate(shape=(numSamples,), dtype=np.int32)
    output_data_buffer = allocate(shape=(numSamples,), dtype=np.int32)
    for i in range(numSamples):
        real_part = random.randint(0,32768)
        imag_part = random.randint(0,32768)
        real_data_buffer[i] = real_part
        imag_data_buffer[i] = imag_part
        ground_truth[i] = np.sqrt(imag_part*imag_part + real_part*real_part)

    ipFIRN11.write(0x10, real_data_buffer.device_address)
    ipFIRN11.write(0x18, imag_data_buffer.device_address)
    ipFIRN11.write(0x20, output_data_buffer.device_address)
    ipFIRN11.write(0x00, 0x01)
    while (ipFIRN11.read(0x00) & 0x4) == 0x0:
        continue

    error = np.abs(ground_truth-output_data_buffer)
    for i in range(10):
        print("error idx:", i)
        print("error value:",error[i])

    print("============================")
    print("Exit process")