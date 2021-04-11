"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

from __future__ import division
import numpy as np
from gnuradio import gr, blocks


# from datetime import datetime


from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui
import pmt
import time

from gnuradio import gr, gr_unittest
from gnuradio import blocks, analog
import numpy as np

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, 
                num_frequencies=4, 
                frequencies=[-3281250, -1093750 , 1093750 ,3281250], 
                dwell_time=.1,
                sample_frequency=1000000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='frequency dweller',   # will show up in GRC
            in_sig=None, # no input
            out_sig=[np.complex64]       # have a dummy output
        )
        self.samp_rate = long(sample_frequency)
        self.message_port_register_out(pmt.intern('debug'))  # port to send on

        # setup loadins
        self.frequencies = frequencies
        self.num_frequencies = num_frequencies
        self.dwell_time = dwell_time
        self.index = 0

        # setup initial frequency stuff
        self.freq = self.frequencies[0]
        self.sample_rate = 1/sample_frequency

        self.last_switch = time.time()

    def transition(self):
        now = time.time()
        if(now - self.last_switch > self.dwell_time):
            # update timer
            self.last_switch = now

            # get frequency
            self.index = self.index + 1 
            if (self.index >= self.num_frequencies):
                self.index = 0 
            self.freq = self.frequencies[self.index]
        else:
            return False

    def work(self, input_items, output_items):
        """example: multiply with constant"""

        temp = 1.0/self.samp_rate

        # Frequency Calculations -- fill in entire array
        # checks for this happen frequently
        f = 2*np.pi*self.freq
        for x in range(len(output_items[0])):
            time = x * temp
            imag = np.sin(f*time)
            real = np.cos(f*time)
            output_items[0][x] = complex(real, imag)

        # check for transition
        self.transition()

        return len(output_items[0])
