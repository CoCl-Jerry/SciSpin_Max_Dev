import smbus

# ------------------ for sending i2c commands to the arduino ----------------- #
# def sendCMD(cont):
#     print("sending command...\n" + cont)
#     temp = cont + "\n"
#     while True:
#         try:
#             bus = smbus.SMBus(1)
#             converted = []
#             for b in temp:
#                 converted.append(ord(b))
#             bus.write_i2c_block_data(0x08, 0x5E, converted)
#             break
#         except Exception as e:
#             General.communication_error = True
#             print(e, "communication failure,contact Jerry for support")
#         pass


# def sendCMD(cont):
#     print("sending command...\n" + cont)
#     temp = cont + "\n"
#     try:
#         bus = smbus.SMBus(1)
#         converted = []
#         for b in temp:
#             converted.append(ord(b))
#         bus.write_i2c_block_data(0x08, 0x5E, converted)
#     except Exception as e:
#         General.communication_error = True
#         print(e, "i2c Communication error, skipping command")


def sendCMD(cont):
    print("Sending command...\n" + cont)
    temp = cont + "\n"
    # Use a list comprehension for conversion
    converted = [ord(b) for b in temp]
    try:
        bus = smbus.SMBus(1)
        bus.write_i2c_block_data(0x08, 0x5E, converted)
    except IOError as e:
        # General.communication_error = True
        print("I2C communication error:", e)
    except Exception as e:
        # General.communication_error = True
        print("An unexpected error occurred:", e)


def reset_arduino():
    sendCMD("0")
