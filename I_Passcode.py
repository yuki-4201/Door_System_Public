from adafruit_rgb_display.rgb import color565 # type: ignore
from adafruit_rgb_display.ili9341 import ILI9341

from busio import SPI
from digitalio import DigitalInOut
import board

from PIL import Image, ImageDraw, ImageFont

def passcode (passcode1,passcode2):
    # Pin Configuration
    cs_pin = DigitalInOut(board.D8)
    dc_pin = DigitalInOut(board.D25)
    rst_pin = DigitalInOut(board.D24)

    # Set up SPI bus
    spi = SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # Create the ILI9341 display:
    disp = ILI9341(
        spi,
        cs=cs_pin, dc=dc_pin, rst=rst_pin,
        width=240, height=320,
        rotation=90,
        baudrate=24000000
    )

    # Define image size (320x240, rotated)
    IMAGE_SIZE = (disp.height, disp.width)

    # Define fonts
    FONT_ROBOTO = ImageFont.truetype("Roboto-Medium.ttf", 15)
    FONT_NOTO = ImageFont.truetype("NotoSansCJK-Regular.ttc", 28)
    FONT_NOTO_SMALL = ImageFont.truetype("NotoSansCJK-Regular.ttc", 20)

    # Define colors
    COLOR_WHITE = (236, 239, 241)
    COLOR_PURPLE = (239, 154, 154)

    # Create an image with black background
    image = Image.new("RGB", IMAGE_SIZE, (0, 0, 0))

    # Draw some text
    draw = ImageDraw.Draw(image)
    text = f"""\


    解錠用パスコードです。

    {str(passcode1)} or {str(passcode2)}"""

    for i, line in enumerate(text.split("\n")):
        draw.text((0, 24*i), line, font=FONT_NOTO, fill=COLOR_WHITE)

    draw.text((40, 200), "縣陵探究ラボ \n", font=FONT_NOTO_SMALL, fill=COLOR_PURPLE)

    # Show it on display
    disp.image(image)