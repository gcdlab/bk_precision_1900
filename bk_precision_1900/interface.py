#!/usr/bin/env python
import sys
import PySimpleGUI as sg
import argparse
import time
from bk1902b import BK1902B

"""
Demo Button Function Calls
Typically GUI packages in Python (tkinter, Qt, WxPython, etc) will call a user's function
when a button is clicked.  This "Callback" model versus "Message Passing" model is a fundamental
difference between PySimpleGUI and all other GUI.

There are NO BUTTON CALLBACKS in the PySimpleGUI Architecture

It is quite easy to simulate these callbacks however.  The way to do this is to add the calls
to your Event Loop
"""

layout = [[sg.Text('Demo of Button Callbacks')],
          [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
           reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
           auto_refresh=True)],
          [sg.Button('Voltage 1'), sg.Button('Voltage 20'), sg.Button('Output On'), sg.Button('Output Off')]]

window = sg.Window('Button Callback Simulation', layout)


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port", help="Path to the serial port (e.g. /dev/ttyUSB1 or COM3)"
    )
    args = parser.parse_args()

    with BK1902B(args.port) as psu:
        while True:  # Event Loop
            event, values = window.read()
            output = psu.get_display()
            print(
                f"Voltage set to 1V."
                + f"Measured: {output[0]}V @ {output[1]}A"
            )
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Voltage 1':
                psu.set_voltage(1)
            elif event == 'Voltage 20':
                psu.set_voltage(20)
            elif event == 'Output Off':
                psu.disable_output()
                output = psu.get_display()
            elif event == 'Output On':
                psu.enable_output()
                output = psu.get_display()
            elif event == "-THREAD-":
                # data1, data2 = values[event]
                # window['-DATA1-'].update(str(data1))
                # window['-DATA2-'].update(str(data2))
                print(
                    f"Voltage set to 1V."
                    + f"Measured: {output[0]}V @ {output[1]}A"
                )
        psu.disable_output()
        window.close()


if __name__ == "__main__":
    main()
