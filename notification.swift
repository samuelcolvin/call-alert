#!/usr/bin/swift

import Foundation

let script = """
    display notification "Hello, World!" with title "Call Alert" sound name "default"
    """

let task = Process()
task.launchPath = "/usr/bin/osascript"
task.arguments = ["-e", script]

do {
    try task.run()
    task.waitUntilExit()
    if task.terminationStatus == 0 {
        print("Notification sent successfully!")
    } else {
        print("Failed to send notification")
    }
} catch {
    print("Error running AppleScript: \(error)")
}
