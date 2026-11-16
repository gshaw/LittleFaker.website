# cspell:ignore LANCZOS
# Crops the home page's screenshot, Contact from Little Faker's 1.2 App Store screenshots,
# and makes og.jpg, for each of the site's languages from that language's shots. Wallpaper is added past the right edge so the page's rounded corners
# don't clip the menu bar. On a phone, CSS crops the left side off.
#
#   mise run shots   # reads the shots from ~/Developer/LittleFaker, writes static/screenshots/
import io
import pathlib
import subprocess

from PIL import Image

REPO = pathlib.Path.home() / "Developer/LittleFaker"
REF = "origin/main"  # LittleFaker's Assets/Screenshots/<locale>/
OUT = pathlib.Path(__file__).resolve().parent.parent / "static"
PURPLE = (104, 103, 175)  # the wallpaper
PAD = 64  # wallpaper added on the right, in screenshot pixels

# The crop (left, top, right, bottom) of the padded screenshot: 5:4, the menus on the right.
CROP = (824, 0, 2624, 1440)


# The site's languages and their App Store screenshot folders. English keeps the plain
# names, contact.jpg and og.jpg; the others are contact.de.jpg, og.de.jpg and so on.
LANGUAGES = {"en": "en-US", "de": "de-DE", "fr": "fr-FR", "ja": "ja", "zh-hans": "zh-Hans"}


def shot(locale, name):
    path = f"{REF}:Assets/Screenshots/{locale}/{name}.png"
    png = subprocess.run(["git", "-C", str(REPO), "show", path], capture_output=True, check=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGB")
    padded = Image.new("RGB", (im.width + PAD, im.height), PURPLE)
    padded.paste(im, (0, 0))
    return padded


def main():
    (OUT / "screenshots").mkdir(parents=True, exist_ok=True)
    for lang, locale in LANGUAGES.items():
        suffix = "" if lang == "en" else f".{lang}"
        contact = shot(locale, "3-contact")
        jpg = f"screenshots/contact{suffix}.jpg"
        contact.crop(CROP).save(OUT / jpg, quality=82, optimize=True, progressive=True)
        print(f"wrote static/{jpg}")
        # Open Graph: its right side, where the menus are, at 1200x630.
        og = contact.crop((1040, 0, 2624, 832)).resize((1200, 630), Image.LANCZOS)
        og.save(OUT / f"og{suffix}.jpg", quality=84, optimize=True)
        print(f"wrote static/og{suffix}.jpg")


main()
