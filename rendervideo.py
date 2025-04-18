from datetime import datetime
from io import TextIOWrapper
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
from figureoutwhere import figureoutwhere

for folder in ["log", "text", "filled", "1x", "final"]:
    os.makedirs(folder, exist_ok=True)

font = ImageFont.truetype("font/super-mario-64-mission-select.otf", 13)
log_l: list[TextIOWrapper] = []


def row_width(row: list[Image.Image]) -> int:
    return 4 * (len(row) - 1) + sum(img.width for img in row)


def runcmd(cmd: list[str]):
    #print(cmd)
    subprocess.run(cmd, check=True, stdout=log_l[0], stderr=log_l[1])


def combinerow(row: list[Image.Image]) -> Image.Image:
    W = 200
    H = max(img.height for img in row)
    X = (200 - row_width(row)) // 2

    composite = Image.new('RGB', (W, H), "white")
    for img in row:
        composite.paste(img, (X, H - img.height))
        X += img.width + 4
    return composite


def maketext(text: str, ID: str):
    words = text.replace("\n", " ").split(" ")
    wimgs: list[Image.Image] = []

    for w in words:
        img = Image.new("RGB", (200, 20), 0)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), w, font=font)
        bbox = img.getbbox()
        bbox = [*bbox] if bbox else [0, 0, 0, 0]
        bbox[2] += 1
        bbox[3] += 1
        img = ImageOps.invert(img.crop(bbox))
        wimgs.append(img)

    rows: list[list[Image.Image]] = [[]]

    while wimgs:
        row = rows[-1]
        row.append(wimgs.pop(0))
        if row_width(row) >= 200:
            rows.append([row.pop()])

    imgs = [combinerow(row) for row in rows]
    H = sum(img.height for img in imgs)
    comp = Image.new("RGB", (200, H), "white")

    y = 0
    for img in imgs:
        comp.paste(img, (0, y))
        y += img.height
    comp.save("text/%s.png" % ID)


def makefilled(COURSE: int, STAR: int, ID: str):
    overlaywidth = 200
    X = (320 - overlaywidth) // 2
    coords = (X, 80)

    cmd = [
        "ffmpeg", "-i", f"courses/{COURSE}/{STAR}.mp4", "-i",
        "text/%s.png" % ID, "-filter_complex",
        "[0:v][1:v] overlay=%d:%d" % coords, "-c:a", "copy",
        "filled/%s.mp4" % ID
    ]
    runcmd(cmd)


def makevideo(COURSE: int, ID: str):

    files = [f"courses/{COURSE}/fadein.mp4"]
    files.extend(["filled/%s.mp4" % ID] * 4)

    inputs = []
    concat = ""
    for i, f in enumerate(files):
        concat += "[%d:v]" % i
    concat += "concat=n=%d:v=1:a=0[v]" % len(files)

    files.append("courses/jingle.mp3")
    for i, f in enumerate(files):
        inputs.extend(["-i", f])

    outpath = "1x/%s.mp4" % ID
    cmd = [
        "ffmpeg", *inputs, "-filter_complex", concat, "-map", "[v]", "-map",
        "%d:a" % (len(files) - 1), outpath
    ]
    runcmd(cmd)


def upscale(ID: str):
    inpath = "1x/%s.mp4" % ID
    outpath = "final/%s.mp4" % ID

    cmd = ["ffmpeg", "-i", inpath, "-vf", "scale=1280:960", outpath]
    runcmd(cmd)


def fullprocess(text: str, flags: dict[str, str]) -> str:
    ID = hex(abs(hash(text)))
    log_l.append(open("log/%s.log" % ID, "w"))
    log_l.append(open("log/%s_ERR.log" % ID, "w"))

    COURSE, STAR = figureoutwhere(text)
    #print(f"{flags = }")
    if (C := flags.get("-c")):
        COURSE = int(C)
    if (S := flags.get("-s")):
        STAR = int(S)

    maketext(text, ID)
    makefilled(COURSE, STAR, ID)
    makevideo(COURSE, ID)
    upscale(ID)

    for path in ["text/%s.png", "filled/%s.mp4", "1x/%s.mp4"]:
        os.remove(path % ID)
    while log_l:
        log_l.pop().close()
    return ID


if __name__ == "__main__":
    sys.argv.pop(0)  # "rendervideo.py"
    flags: dict[str, str] = {}

    if sys.argv:
        while sys.argv[0].startswith("-"):
            k = sys.argv.pop(0)
            flags[k] = sys.argv.pop(0)
        text = sys.argv.pop(0)
    else:
        text = str(datetime.now()).rpartition(".")[0]

    ID = fullprocess(text, flags)
    print(ID)
