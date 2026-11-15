# cspell:ignore LANCZOS
# Crops the home page's screenshot, Fake Info from Little Faker's 1.2 App Store screenshots,
# and makes og.jpg. Wallpaper is added past the right edge so the page's rounded corners
# don't clip the menu bar. On a phone, CSS crops the left side off.
#
#   mise run shots   # reads the shots from ~/Developer/LittleFaker, writes static/screenshots/
import io
import pathlib
import subprocess

from PIL import Image

REPO = pathlib.Path.home() / "Developer/LittleFaker"
REF = "origin/27-app-store-screenshots"  # LittleFaker PR #52; main once it merges
OUT = pathlib.Path(__file__).resolve().parent.parent / "static"
PURPLE = (104, 103, 175)  # the wallpaper
PAD = 64  # wallpaper added on the right, in screenshot pixels

# The crop (left, top, right, bottom) of the padded screenshot: 5:4, the menus on the right.
CROP = (924, 0, 2624, 1360)


def shot(name):
    path = f"{REF}:Assets/Screenshots/en-US/{name}.png"
    png = subprocess.run(["git", "-C", str(REPO), "show", path], capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGB")
    padded = Image.new("RGB", (im.width + PAD, im.height), PURPLE)
    padded.paste(im, (0, 0))
    return padded


def main():
    (OUT / "screenshots").mkdir(parents=True, exist_ok=True)
    fake_info = shot("3-fake-info")
    fake_info.crop(CROP).save(OUT / "screenshots/fake-info.jpg", quality=82, optimize=True, progressive=True)
    print("wrote static/screenshots/fake-info.jpg")
    # Open Graph: its right side, where the menus are, at 1200x630.
    og = fake_info.crop((1040, 0, 2624, 832)).resize((1200, 630), Image.LANCZOS)
    og.save(OUT / "og.jpg", quality=84, optimize=True)
    print("wrote static/og.jpg")


main()
