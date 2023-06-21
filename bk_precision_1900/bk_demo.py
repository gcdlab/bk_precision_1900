import argparse
import time

from bk1902b import BK1902B


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port", help="Path to the serial port (e.g. /dev/ttyUSB1 or COM3)"
    )
    args = parser.parse_args()

    with BK1902B(args.port) as psu:
        print("Resetting output")
        psu.disable_output()
        psu.set_current(0.1)
        psu.set_voltage(1)
        time.sleep(10)
        psu.enable_output()
        for voltage in range(1, 40, 5):
            psu.set_voltage(voltage)
            time.sleep(2)
            output = psu.get_display()
            mode = "CV" if output[2] else "CC"
            print(
                f"Voltage set to {voltage}V."
                + f"Measured: {output[0]}V @ {output[1]}A {mode}"
            )
        psu.disable_output()


if __name__ == "__main__":
    main()
