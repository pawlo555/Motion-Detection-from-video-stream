import move_detector as md
from default_values import Settings

# "https://imageserver.webcamera.pl/rec/krakow4/latest.mp4"
# "https://imageserver.webcamera.pl/rec/hotel-senacki-krakow/latest.mp4"

detector = md.MoveDetector(
    "https://imageserver.webcamera.pl/rec/krakow2/latest.mp4",
    *Settings.high)
detector.loop()
