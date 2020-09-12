"""
An extremely simply example on how to read data from the SpaceMouse
and map it to application dependent commands/actions.
"""

import pyautogui as pa

from time import sleep, time
from win32gui import GetWindowText, GetForegroundWindow
from pywinusb import hid


class Handler(object):
    time = 0

    @staticmethod
    def run(data):
        if time() - Handler.time < 0.2:
            return
        Handler.time = time()

        rt_btn = data[0] == 3
        lt_btn = data[1] == 1
        x = data[2] - data[1]
        y = data[4] - data[3]
        z = data[6] - data[5]
        pitch = data[8] - data[7]
        yaw = data[10] - data[9]
        roll = data[12] - data[11]

        current_app = Handler.current_app()
        print(current_app)
        print(rt_btn, lt_btn, pitch, yaw, roll, x, y, z)

        if 'Fusion 360' in current_app:
            return  # already supported application
        elif 'Autodesk SketchBook' in current_app:
            if rt_btn: pa.hotkey('ctrl', '0')
            if roll > 50: pa.press('9')
            if roll < -50: pa.press('0')
        else:
            if roll < -50: pa.press('volumeup')
            if roll > 50: pa.press('volumedown')
            if rt_btn: pa.press('volumemute')

    @staticmethod
    def current_app():
        return GetWindowText(GetForegroundWindow())


def open_device():
    devices = hid.HidDeviceFilter(vendor_id=0x256f).get_devices()
    for device in devices:
        device.open()
        in_reports = device.find_input_reports()
        out_reports = device.find_output_reports()
        if in_reports and out_reports:
            device.set_raw_data_handler(Handler.run)
            print("Device found %s", device)
            return device
        else:
            device.close()
    print('No device found')
    return None


def list_all_devices():
    import pywinusb.hid as hid
    hids = hid.find_all_hid_devices()
    for hid in set(hids):
        print(hid)


if __name__ == '__main__':
    # list_all_devices()
    device = open_device()
    while device:
        sleep(10)
