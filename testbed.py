#!/usr/bin/env python

# Copyright (c) 2021, Stephen Goadhouse <sgoadhouse@virginia.edu>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Neotion nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL NEOTION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#-------------------------------------------------------------------------------
#  Get a screen capture from Agilent/KeySight MSO3034A scope and save it to a file
#
# Using new MSOX3000 Class

# pyvisa 1.6 (or higher) (http://pyvisa.sourceforge.net/)
# pyvisa-py 0.2 (https://pyvisa-py.readthedocs.io/en/latest/)
#
# NOTE: pyvisa-py replaces the need to install NI VISA libraries
# (which are crappily written and buggy!) Wohoo!
#
#-------------------------------------------------------------------------------

# For future Python3 compatibility:
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random
import pyvisa as visa
import sys
from time import sleep

# Set to the IP address of the oscilloscope
# agilent_msox_3034a = os.environ.get('MSOX3000_IP', 'TCPIP0::172.16.2.13::INSTR')

import argparse
parser = argparse.ArgumentParser(description='Get a screen capture from Agilent/KeySight MSO3034A scope and save it to a file')
parser.add_argument('ofile', nargs=1, help='Output file name')
args = parser.parse_args()

fn_ext = ".png"
pn = "/Downloads"
fn = pn + "/" + args.ofile[0]

while os.path.isfile(fn + fn_ext):
     fn += "-" + random.choice("abcdefghjkmnpqrstuvwxyz")

fn += fn_ext

from msox3000 import MSOX3000
rm = visa.ResourceManager('@py')
resources = rm.list_resources()
print(resources)

## Connect to the Power Supply with default wait time of 100ms
scope = MSOX3000(resources[0])
scope.open()

print(scope.idn())

# print("Output file: %s" % fn )
# scope.hardcopy(fn)
# scope.waveform(fn+"_1.csv", '1')
# scope.waveform(fn+"_2.csv", '2')
# scope.waveform(fn+"_3.csv", '3')
# scope.waveform(fn+"_4.csv", '4')

chan = '1'
print("Ch.{}: {}V ACRMS".format(chan,scope.measureDVMacrms(chan)))
print("Ch.{}: {}V DC".format(chan,scope.measureDVMdc(chan)))
print("Ch.{}: {}V DCRMS".format(chan,scope.measureDVMdcrms(chan)))
print("Ch.{}: {}Hz FREQ".format(chan,scope.measureDVMfreq(chan)))

# scope.setupSave(fn+".stp")
#
# scope.setupAutoscale('1')
# scope.setupAutoscale('2')
# scope.setupAutoscale('3')
#
# scope.setupLoad(fn+".stp")

if True:
    wait = 0.5 # just so can see if happen
    for chan in range(1,5):
        scope.outputOn(chan,wait)

        for chanEn in range(1,5):
            if (scope.isOutputOn(chanEn)):
                print("Channel {} is ON.".format(chanEn))
            else:
                print("Channel {} is off.".format(chanEn))
        print()
        
    for chan in range(1,5):
        scope.outputOff(chan,wait)

        for chanEn in range(1,5):
            if (scope.isOutputOn(chanEn)):
                print("Channel {} is ON.".format(chanEn))
            else:
                print("Channel {} is off.".format(chanEn))
        print()
                
    scope.outputOnAll(wait)
    for chanEn in range(1,5):
        if (scope.isOutputOn(chanEn)):
            print("Channel {} is ON.".format(chanEn))
        else:
            print("Channel {} is off.".format(chanEn))
    print()

    scope.outputOffAll(wait)
    for chanEn in range(1,5):
        if (scope.isOutputOn(chanEn)):
            print("Channel {} is ON.".format(chanEn))
        else:
            print("Channel {} is off.".format(chanEn))
    print()


chan = '3'
if (not scope.isOutputOn(chan)):
    scope.outputOn(chan)    
print(scope.measureVoltAmplitude('1',install=True))
print(scope.measureVoltMax('1',install=True))
print(scope.measureVoltMax(install=False))

stats = scope.measureStatistics()
print(stats)
print('Done')

scope.close()
