from concurrent.futures import process
from Quartz import (
  CGWindowListCopyWindowInfo,
  CGWindowListCreateImage,
  kCGWindowListOptionOnScreenOnly,
  kCGWindowImageDefault,
  kCGNullWindowID,
  CGImageGetDataProvider,
  CGDataProviderCopyData,
  CGRect,
  CGPoint,
  CGSize,
  CGImageDestinationCreateWithURL,
  kCGImagePropertyDPIWidth,
  kCGImagePropertyDPIHeight,
  CGImageDestinationAddImage,
  CGImageDestinationFinalize
)
from AppKit import (
  NSWorkspace
)
from Cocoa import (
  NSURL
)
from PIL import (
  Image
)
import LaunchServices
import time
import overlay
import tkinter as tk

# Needs white and orange
COLOR_ONE_PIXEL_MAP = {
  (124, 169, 192): "blue_",
  (98, 98, 98): "black_",
  (192, 177, 105): "yellow_",
  (105, 192, 107): "green_",
  (153, 124, 192): "purple_",
  (192, 77, 86): "red_",
  (192, 192, 192): "white_"
}

COLOR_TWO_PIXEL_MAP = {
  (50, 106, 162): "blue",
  (196, 199, 200): "white",
  (186, 155, 39): "orange",
  (87, 150, 78): "green",
  (180, 183, 76): "yellow",
  (136, 34, 25): "red",
  (38, 38, 38): "black",
  (106, 46, 150): "purple"
}

COLOR_PATTERN_MAP = {
  "black_black": "YY RR GG",
  "black_blue": "RR GG BB",
  "black_green": "YY BB GG",
  "black_orange": "GG YY BB",
  "black_purple": "GG RR BB",
  "black_red": "RR YY BB",
  "black_white": "BB RR GG",
  "black_yellow": "BB YY GG",

  "blue_black": "GG RR YY",
  "blue_blue": "BB GG RR",
  "blue_green": "GG BB YY",
  "blue_orange": "BB YY GG",
  "blue_purple": "BB RR GG",
  "blue_red": "BB YY RR",
  "blue_white": "GG RR BB",
  "blue_yellow": "GG YY BB",

  "green_black": "BB GG YY",
  "green_blue": "YY BB RR",
  "green_green": "BB RR YY",
  "green_orange": "YY RR GG",
  "green_purple": "YY BB GG",
  "green_red": "YY GG RR",
  "green_white": "YY GG BB",
  "green_yellow": "YY RR BB",

  "orange_black": "YY RR GG",
  "orange_blue": "RR GG BB",
  "orange_green": "YY BB GG",
  "orange_orange": "GG YY BB",
  "orange_purple": "GG RR BB",
  "orange_red": "RR YY BB",
  "orange_white": "BB RR GG",
  "orange_yellow": "BB YY GG",

  "purple_black": "RR BB YY",
  "purple_blue": "GG YY RR",
  "purple_green": "RR GG YY",
  "purple_orange": "RR BB GG",
  "purple_purple": "RR YY GG",
  "purple_red": "GG BB RR",
  "purple_white": "RR YY BB",
  "purple_yellow": "RR GG BB",

  "red_black": "YY GG BB",
  "red_blue": "RR BB YY",
  "red_green": "YY RR BB",
  "red_orange": "GG RR YY",
  "red_purple": "GG BB YY",
  "red_red": "RR GG YY",
  "red_white": "BB GG YY",
  "red_yellow": "BB RR YY",

  "white_black": "YY GG BB",
  "white_blue": "RR BB YY",
  "white_green": "YY RR BB",
  "white_orange": "GG RR YY",
  "white_purple": "GG BB YY",
  "white_red": "RR GG YY",
  "white_white": "BB GG YY",
  "white_yellow": "BB RR YY",

  "yellow_black": "YY BB RR",
  "yellow_blue": "RR YY GG",
  "yellow_green": "YY GG RR",
  "yellow_orange": "GG BB RR",
  "yellow_purple": "GG YY RR",
  "yellow_red": "RR BB GG",
  "yellow_white": "BB YY RR",
  "yellow_yellow": "BB GG RR",
}

COLOR_FILL_MAP = {
  "GG": "green",
  "BB": "blue",
  "RR": "red",
  "YY": "yellow"
}

COLOR_ONE_PIXEL = {
  "X": 752,
  "Y": 326
}

COLOR_TWO_PIXEL = {
  "X": 738,
  "Y": 334
}

class Window:
  def __init__(self):
    self.data = False

  def getWindow(self):
    options = kCGWindowListOptionOnScreenOnly
    windows = CGWindowListCopyWindowInfo(
      options,
      kCGNullWindowID
    )

    print("Looking for window...")

    for window in windows:
      if window["kCGWindowOwnerName"] == "Puzzle Pirates":
        self.data = window

class Overlay:
  def __init__(self, x, y):
    self.window = overlay.Window(
      size=(162, 12),
      position=(x + 143, y + 616)
    )

  def displayPattern(self, pixelOne, pixelTwo):
    colors = COLOR_ONE_PIXEL_MAP.get(pixelOne, "Undefined") + COLOR_TWO_PIXEL_MAP.get(pixelTwo, "Undefined")

    pattern = COLOR_PATTERN_MAP.get(colors, "Undefined")

    canvas = tk.Canvas(
      self.window.root,
      width=162,
      height=12,
      bd=0,
      highlightthickness=0
    )

    canvas.pack(
      padx=0,
      pady=0
    )

    if pattern != "Undefined":
      print(pattern)

      canvas.create_rectangle(-1, -1, 54, 12, fill=COLOR_FILL_MAP.get(pattern[:2]), outline=COLOR_FILL_MAP.get(pattern[:2]))
      canvas.create_rectangle(54, -1, 108, 12, fill=COLOR_FILL_MAP.get(pattern[3] + pattern[4]), outline=COLOR_FILL_MAP.get(pattern[3] + pattern[4]))
      canvas.create_rectangle(108, -1, 162, 12, fill=COLOR_FILL_MAP.get(pattern[6] + pattern[7]), outline=COLOR_FILL_MAP.get(pattern[6] + pattern[7]))

      self.window.root.update()

class Screen:
  def __init__(self, x, y, height, width):
    self.origin = CGPoint(x, y)
    self.size = CGSize(width, height)
    self.rect = CGRect(self.origin, self.size)

  def capture(self):
    image = CGWindowListCreateImage(
      self.rect,
      kCGWindowListOptionOnScreenOnly,
      kCGNullWindowID,
      kCGWindowImageDefault
    )

    provider = CGImageGetDataProvider(image)

    data = CGDataProviderCopyData(provider)

    url = NSURL.fileURLWithPath_("image.png")

    destination = CGImageDestinationCreateWithURL(
      url,
      LaunchServices.kUTTypePNG,
      1,
      None
    )

    properties = {
      kCGImagePropertyDPIWidth: 72,
      kCGImagePropertyDPIHeight: 72
    }

    CGImageDestinationAddImage(
      destination,
      image,
      properties
    )

    CGImageDestinationFinalize(destination)

class Pattern:
  def __init__(self):
    self.image = Image.open("image.png")

  def convertImageToRGB(self):
    self.image = self.image.convert("RGB")

  def getColorOnePixel(self):
    return self.image.getpixel((COLOR_ONE_PIXEL["X"], COLOR_ONE_PIXEL["Y"]))

  def getColorTwoPixel(self):
    return self.image.getpixel((COLOR_TWO_PIXEL["X"], COLOR_TWO_PIXEL["Y"]))

def proceed(x, y, height, width, _overlay):
  while True:
    screen = Screen(
      x,
      y,
      height,
      width
    )

    screen.capture()

    pattern = Pattern()
    pattern.convertImageToRGB()

    pixelOne = pattern.getColorOnePixel()
    pixelTwo = pattern.getColorTwoPixel()

    _overlay.displayPattern(pixelOne, pixelTwo)
    
    time.sleep(.5)


if __name__ == "__main__":
  window = Window()

  while True:
    while window.data == False:
      window.getWindow()

      time.sleep(.5)

    _overlay = Overlay(
      window.data["kCGWindowBounds"]["X"],
      window.data["kCGWindowBounds"]["Y"]
    )

    while window.data != False:
      overlay.Window.after(
        500, 
        proceed, 
        window.data["kCGWindowBounds"]["X"], 
        window.data["kCGWindowBounds"]["Y"], 
        window.data["kCGWindowBounds"]["Height"], 
        window.data["kCGWindowBounds"]["Width"],
        _overlay
      )

      overlay.Window.launch()