#!/usr/bin/python3

# This file is part of the MAVLink Router project
#
# Copyright (C) 2017  Intel Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import time
from pymavlink import mavutil

OWN_COMP_ID = 1

if len(sys.argv) != 3:
    print("Usage: %s <ip:udp_port> <system-id>" % (sys.argv[0]))
    print("Receive mavlink heartbeats on specified interface. "
          "Respond with a ping message")
    sys.exit()

srcSystem = int(sys.argv[2])
mav = mavutil.mavlink_connection('udpin:' + sys.argv[1],
                                 source_system=srcSystem,
                                 source_component=OWN_COMP_ID)

while True:
    msg = mav.recv_match(blocking=True)
    print("Message from System ID %d Component %d : %s" % (msg.get_srcSystem(), msg.get_srcComponent(), msg))
    if hasattr(msg, 'target_system'):
        if msg.target_system == 0:
            print("\tMessage sent to all")
        elif msg.target_system == srcSystem:
            print("\tMessage sent to me")
        else:
            print("\tMessage sent to other")
    else:
        print("\tMessage without target system")

    mav.mav.ping_send(int(time.time() * 1000), msg.seq, msg.get_srcSystem(),
                     msg.get_srcComponent())
