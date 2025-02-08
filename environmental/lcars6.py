# SPDX-FileCopyrightText: Copyright (c) 2020 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
import adafruit_sht4x
import adafruit_bh1750
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_bitmap_font import bitmap_font

# I2C setup for SHT40
i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
sht = adafruit_sht4x.SHT4x(i2c)

# Configure the SHT40 for high-precision measurement
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
sensor = adafruit_bh1750.BH1750(i2c)

# Hopefully this stops the CLK in use error whenever a new program is downloaed.
displayio.release_displays()

# SPI setup for TFT
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)
tft_cs = board.GP1
tft_dc = board.GP26
tft_rst = board.GP27

# Load Custom Font
font = bitmap_font.load_font("/fonts/Swiss911BT-UltraCompressed-24.bdf")  # Ensure the file is on the board
font_small = bitmap_font.load_font("/fonts/Swiss911BT-UltraCompressed-14.bdf")  # Ensure the file is on the board


# Display setup for ST7735
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7735R(display_bus, width=132, height=130, rotation=90, bgr=False)

splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(128, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Build Environmental Header
roundrect_outer = RoundRect(10, 10, 130, 50, 5, fill=0xfccc95, outline=0xfccc95, stroke=6)
splash.append(roundrect_outer)

# Create Area for Temp, Humidity, and Light
roundrect_inner_right1 = RoundRect(70, 40, 70, 75, 5, fill=0x000000, outline=0x000000, stroke=6)
splash.append(roundrect_inner_right1)

# Create Lower graphic
roundrect_lower = RoundRect(10, 100, 110, 25, 5, fill=0xfccc95, outline=0xfccc95, stroke=6)
splash.append(roundrect_lower)

# Black out area for data labels
rect_cut1 = Rect(10, 50, 140, 65, fill=0x000000, outline=0x000000, stroke=6)
splash.append(rect_cut1)

# Add name of the display
temp_header = label.Label(font, text="ENVIRONMENTAL", color=0x000000, x=25, y=25)
splash.append(temp_header)

# Background for temperature data label
rect_temp_label = Rect(10, 55, 60, 15, fill=0xc28663, outline=0xc28663, stroke=6)
splash.append(rect_temp_label)

# Add the temperature data lable
temp_name = label.Label(font_small, text="Temperature", color=0xffffff, x=20, y=62)
splash.append(temp_name)

# Placeholder for the temperature data
temp_label = label.Label(font_small, text="---.- C", color=0xc28663, x=80, y=62)
splash.append(temp_label)

# Background for humidity data label
rect_humid_label = Rect(10, 75, 60, 15, fill=0xbd9b46, outline=0xbd9b46, stroke=6)
splash.append(rect_humid_label)

# Add the humidity data lable
humid_name = label.Label(font_small, text="Humidity", color=0xffffff, x=33, y=82)
splash.append(humid_name)

# Placeholder for the humidity data
humid_label = label.Label(font_small, text="---.- %", color=0xbd9b46, x=80, y=82)
splash.append(humid_label)

# Background for light level data label
rect_light_label = Rect(10, 95, 60, 15, fill=0x7682c4, outline=0x7682c4, stroke=6)
splash.append(rect_light_label)

# Add the light level data lable
light_name = label.Label(font_small, text="Light Level", color=0xffffff, x=25, y=102)
splash.append(light_name)

# Placeholder for the light level data
light_label = label.Label(font_small, text="---.- lux", color=0x7682c4, x=80, y=102)
splash.append(light_label)

while True:
    
    # Read temperature and humidity
    temp_value, rh_value = sht.measurements
    light_value = sensor.lux
    
    temp_label.text = f"{temp_value:.1f} C"
    humid_label.text = f"{rh_value:.1f} %"
    light_label.text = f"{light_value:.1f} lux"
    
    # Pause between updates
    time.sleep(2)