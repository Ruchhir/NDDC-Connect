from services.mikrotik import authorize_mac

print("Starting MikroTik test...")

authorize_mac("AA:BB:CC:DD:EE:FF", 1)

print("Test finished.")