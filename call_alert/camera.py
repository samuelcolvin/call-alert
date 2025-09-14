import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    class CoreMediaIO:
        kCMIODevicePropertyDeviceIsRunningSomewhere: object

        @classmethod
        def CMIOObjectGetPropertyData(cls, *_: object) -> tuple[int, bytes, int, bytes | object]: ...
        @classmethod
        def CMIOObjectPropertyAddress(cls, _: object) -> object: ...

    class Camera:
        def connectionID(self) -> object: ...

    AVMediaTypeVideo = object

    class AVCaptureDevice:
        @classmethod
        def devicesWithMediaType_(cls, _: AVMediaTypeVideo) -> list[Camera]: ...


else:
    import CoreMediaIO
    from AVFoundation import AVCaptureDevice, AVMediaTypeVideo


def camera_active() -> bool:
    property_address = CoreMediaIO.CMIOObjectPropertyAddress(CoreMediaIO.kCMIODevicePropertyDeviceIsRunningSomewhere)

    for camera in AVCaptureDevice.devicesWithMediaType_(AVMediaTypeVideo):
        result = CoreMediaIO.CMIOObjectGetPropertyData(
            camera.connectionID(),
            property_address,
            0,
            None,
            struct.calcsize('I'),
            None,
            None,
        )
        raw = result[3]
        if result[0] == 0 and isinstance(raw, bytes) and struct.unpack('I', raw[:4])[0]:
            return True

    return False
