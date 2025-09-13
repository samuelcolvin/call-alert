import CoreMediaIO
import Foundation

func getBool(_ objectID: CMIOObjectID, _ selector: UInt32) -> Bool? {
    var addr = CMIOObjectPropertyAddress(
        mSelector: CMIOObjectPropertySelector(selector),
        mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeWildcard),
        mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementWildcard)
    )
    var size: UInt32 = 0
    guard CMIOObjectHasProperty(objectID, &addr),
        CMIOObjectGetPropertyDataSize(objectID, &addr, 0, nil, &size) == 0,
        size == UInt32(MemoryLayout<UInt32>.size)
    else { return nil }
    var val: UInt32 = 0
    var s = size
    guard CMIOObjectGetPropertyData(objectID, &addr, 0, nil, s, &s, &val) == 0 else { return nil }
    return val != 0
}

func getCFString(_ objectID: CMIOObjectID, _ selector: UInt32) -> String {
    var addr = CMIOObjectPropertyAddress(
        mSelector: CMIOObjectPropertySelector(selector),
        mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeWildcard),
        mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementWildcard)
    )
    var size: UInt32 = 0
    guard CMIOObjectHasProperty(objectID, &addr),
        CMIOObjectGetPropertyDataSize(objectID, &addr, 0, nil, &size) == 0
    else { return "" }
    var cfstr: Unmanaged<CFString>? = nil
    var s = size
    if CMIOObjectGetPropertyData(objectID, &addr, 0, nil, s, &s, &cfstr) == 0,
        let cf = cfstr?.takeUnretainedValue()
    {
        return cf as String
    }
    return ""
}

let system = CMIOObjectID(kCMIOObjectSystemObject)
var addr = CMIOObjectPropertyAddress(
    mSelector: CMIOObjectPropertySelector(kCMIOHardwarePropertyDevices),
    mScope: CMIOObjectPropertyScope(kCMIOObjectPropertyScopeWildcard),
    mElement: CMIOObjectPropertyElement(kCMIOObjectPropertyElementWildcard)
)

var size: UInt32 = 0
guard CMIOObjectGetPropertyDataSize(system, &addr, 0, nil, &size) == 0 else {
    fputs("Failed to query CMIO devices\n", stderr)
    exit(1)
}
let count = Int(size) / MemoryLayout<CMIOObjectID>.size
var ids = [CMIOObjectID](repeating: 0, count: count)
guard CMIOObjectGetPropertyData(system, &addr, 0, nil, size, &size, &ids) == 0 else {
    fputs("Failed to get CMIO devices\n", stderr)
    exit(1)
}

var anyInUseByOther = false
for id in ids {
    let name = getCFString(id, UInt32(kCMIOObjectPropertyName))
    // Running (this process) vs RunningSomewhere (any process)
    let running = getBool(id, UInt32(kCMIODevicePropertyDeviceIsRunning)) ?? false
    let somewhere = getBool(id, UInt32(kCMIODevicePropertyDeviceIsRunningSomewhere)) ?? false

    let status: String
    if somewhere && !running {
        status = "in use by another process"
    } else if running {
        status = "in use by this process"
    } else {
        status = "free"
    }

    if somewhere && !running { anyInUseByOther = true }
    print("\(name.isEmpty ? "Camera \(id)" : name): \(status)")
}
exit(anyInUseByOther ? 2 : 0)
