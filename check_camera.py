# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyobjc==11.0",
#   "requests==2.32.3"
# ]
# ///
import multiprocessing as mp
import socket
import struct
import time

import CoreMediaIO
from AVFoundation import AVCaptureDevice, AVMediaTypeVideo
from requests import Session

requests = Session()


def worker():
    property_address = CoreMediaIO.CMIOObjectPropertyAddress(
        CoreMediaIO.kCMIODevicePropertyDeviceIsRunningSomewhere
    )

    for camera in AVCaptureDevice.devicesWithMediaType_(AVMediaTypeVideo):
        result = CoreMediaIO.CMIOObjectGetPropertyData(
            camera.connectionID(),
            property_address,
            0,
            None,
            struct.calcsize("I"),
            None,
            None,
        )
        status = result[0]
        raw = result[-1]
        if status != 0 or not isinstance(raw, (bytes, bytearray)):
            continue
        if struct.unpack("I", raw[:4])[0]:
            status = "on"
            break
    else:
        status = "off"

    print(status)


if __name__ == "__main__":
    while True:
        worker()
        time.sleep(1)
