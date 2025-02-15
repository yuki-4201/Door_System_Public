import board # type: ignore
from adafruit_rgb_display.ili9341 import ILI9341 # type: ignore
from adafruit_rgb_display.rgb import color565 # type: ignore
from busio import SPI # type: ignore
from digitalio import DigitalInOut # type: ignore
from PIL import Image, ImageDraw, ImageFont # type: ignore


def passcode (passcode1,passcode2):

    # ピン番号の設定
    cs_pin = DigitalInOut(board.D8)
    dc_pin = DigitalInOut(board.D25)
    rst_pin = DigitalInOut(board.D24)

    # SPIのセットアップ
    spi = SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # LI9341 displayの設定
    disp = ILI9341(
        spi,
        cs=cs_pin, dc=dc_pin, rst=rst_pin,
        width=240, height=320,
        rotation=90,
        baudrate=24000000
    )

    # 表示サイズの定義
    IMAGE_SIZE = (disp.height, disp.width)

    # フォント・フォントサイズの定義
    FONT_NOTO = ImageFont.truetype("NotoSansCJK-Regular.ttc", 25)
    FONT_NOTO_SMALL = ImageFont.truetype("NotoSansCJK-Regular.ttc", 16)
    FONT_NOTO_S = ImageFont.truetype("NotoSansCJK-Regular.ttc", 15)
    FONT_SMALL = ImageFont.truetype("NotoSansCJK-Regular.ttc", 15)

    # 色を定義
    COLOR_WHITE = (236, 239, 241)
    COLOR_PURPLE = (239, 154, 154)
    COLOR_RED = (71, 131, 132)

    # 背景色の定義
    image = Image.new("RGB", IMAGE_SIZE, (0, 0, 0))

    # 表示テキストの定義
    draw = ImageDraw.Draw(image)
    draw.text((20,20),f"解錠用パスコードです。\n{str(passcode2)}",font=FONT_NOTO, fill=COLOR_WHITE)
    draw.text((20,100),"※アプリにコードを入力してください。",font=FONT_SMALL, fill=COLOR_RED)
    draw.text((30, 170), "link : https://kenryolab.vercel.app/", font=FONT_NOTO_S, fill=COLOR_PURPLE)
    draw.text((20, 200), "KENRYO STEAM LAB. \n", font=FONT_NOTO_SMALL, fill=COLOR_PURPLE)

    # ディスプレイに表示する
    disp.image(image)