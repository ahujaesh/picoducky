import board
import digitalio
import time
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import neopixel

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.15

layer_colors = [
    (255, 0, 0),
    (255, 80, 10),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (128, 0, 128),
    (200, 70, 120),
    (255, 255, 255)
]

button_pins = [board.D8, board.D6, board.D10, board.D9, board.D5, board.D2, board.D1]
layer_button_pin = board.D7

buttons = []
for pin in button_pins:
    dio = digitalio.DigitalInOut(pin)
    dio.direction = digitalio.Direction.INPUT
    dio.pull = digitalio.Pull.UP
    buttons.append(Debouncer(dio))

layer_dio = digitalio.DigitalInOut(layer_button_pin)
layer_dio.direction = digitalio.Direction.INPUT
layer_dio.pull = digitalio.Pull.UP
layer_button = Debouncer(layer_dio)

# Layer definitions, labeled with their corresponding colors from layer_colors
layers = [
    # (255, 0, 0) - Red
    [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E, Keycode.BACKSPACE, None],
    # (255, 80, 10) - Orange
    [Keycode.F, Keycode.G, Keycode.H, Keycode.I, Keycode.J, Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW],
    # (255, 255, 0) - Yellow
    [Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O, Keycode.UP_ARROW, Keycode.DOWN_ARROW],
    # (0, 255, 0) - Green
    [Keycode.P, Keycode.Q, Keycode.R, Keycode.S, Keycode.T, "VOLUME_DOWN", "VOLUME_UP"],
    # (0, 0, 255) - Blue
    [Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y, Keycode.PERIOD, Keycode.COMMA],
    # (128, 0, 128) - Purple
    [Keycode.Z, Keycode.ENTER, Keycode.SPACE, "CONTROL_TOGGLE", "SHIFT_TOGGLE", "QUESTION_MARK", Keycode.SEMICOLON],
    # (200, 70, 120) - Pink
    [Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE, Keycode.TAB, Keycode.QUOTE],
    # (255, 255, 255) - White
    [Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO, Keycode.FORWARD_SLASH, Keycode.MINUS]
]

layer = 0
pixel[0] = layer_colors[layer]

control_active = False
shift_active = False

while True:
    for b in buttons:
        b.update()
    layer_button.update()

    if layer_button.fell:
        layer = (layer + 1) % len(layers)
        print(f"Layer changed to {layer}")
        pixel[0] = layer_colors[layer % len(layer_colors)]
        
    for i, b in enumerate(buttons):
        if b.fell:
            key = layers[layer][i]
            if key == "VOLUME_DOWN":
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                print("Volume Down")
            elif key == "VOLUME_UP":
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print("Volume Up")
            elif key == "QUESTION_MARK":
                kbd.press(Keycode.SHIFT, Keycode.FORWARD_SLASH)
                kbd.release_all()
                print("Typed ?")
            elif key == "CONTROL_TOGGLE":
                if control_active:
                    kbd.release(Keycode.LEFT_CONTROL)
                    control_active = False
                    print("Control released")
                else:
                    kbd.press(Keycode.LEFT_CONTROL)
                    control_active = True
                    print("Control pressed")
            elif key == "SHIFT_TOGGLE":
                if shift_active:
                    kbd.release(Keycode.LEFT_SHIFT)
                    shift_active = False
                    print("Shift released")
                else:
                    kbd.press(Keycode.LEFT_SHIFT)
                    shift_active = True
                    print("Shift pressed")
            else:
                print(f"Pressed key: {key}")
                # kbd.release(Keycode.LEFT_CONTROL)
                # control_active = False
                # print("Control released")
                # kbd.release(Keycode.LEFT_SHIFT)
                # shift_active = False
                # print("Shift released")
                if isinstance(key, int):
                    kbd.press(key)

        if b.rose:
            key = layers[layer][i]
            if isinstance(key, int):
                kbd.release(key)

    time.sleep(0.01)
