NUM_LEDS = 288

RED = 255
GREEN = 255
BLUE = 255

for i in range(NUM_LEDS):
    hex_value = hex(i)[2:].zfill(4)
    byte1 = hex_value[:2]
    byte2 = hex_value[2:]
    
    print(f"0x{byte1} 0x{byte2} {hex(RED)} {hex(GREEN)} {hex(BLUE)}", end=" ")