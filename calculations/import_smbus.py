import smbus

bus = smbus.SMBus(1)

for address in range(0, 128):
    try:
        bus.read_byte(address)
        print("Device found at address 0x{:02X}".format(address))
    except:
        pass
