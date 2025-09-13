.PHONY: build

build:
	xcrun swiftc -O -framework CoreMediaIO call_alert.swift -o call_alert
	@echo "Build complete, run ./call_alert"
