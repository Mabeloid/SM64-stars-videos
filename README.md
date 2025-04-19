# what is this

the python program that generates the videos for [my funny mario 64 star select screen bot](https://bsky.app/profile/sm64starsvideos.bsky.social)

# what do i need to do before i use it

you need to have ffmpeg and python installed, then you should run `pip install -r requirements.txt` to make sure the external python libraries are installed

# how do i use it

you run the command line

`python rendervideo.py "8 Red Coins Would Fix Me"`
(replace text accordingly)

after a second or a few, it will print a hash like 0x38fa03f949546823, and a corresponding output video is in the `final/` folder

you need to put quotes around the text or it will only use the first word

if you get `python: command not found` or `'python' is not recognized as an internal or external command` you need to write `python3` instead

you can also use `-c` and/or `-s` before the text to override the automatically chosen course or star

`-c` can be 1-15 inclusive, `-s` can be 1-6 inclusive

`python rendervideo.py -c 11 -s 6 "It's a Perfectly Good World Sir"` will force the course to be #11 (wet-dry world) and the star to be the 6th one

while the font supports a lot of characters, it doesn't include, say, emojis or egyptian hieroglyphics. these will appear as blurry boxes and it's not worth it to do anything about that

this is supposed to handle edge cases even if you don't know what you're doing, so if you encounter an issue that's quote-on-quote "my fault" and it's not mentioned here, do let me know

# how do i use it in my web browser

log into GitHub, click this button, then click "Create codespace"

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Mabeloid/SM64-stars-videos)

# how does it decide which star to use

if the name of a course is in the text, it will use that and a random star

for each enemy mentioned, each course it appears in is awarded 1 point for all missions

for each word in the text, 1 point is awarded to each mission that contains the word

finally the mission with the most points is chosen (with a random tiebreaker if multiple)

# how does it make the video

first it uses PIL (python imagine library) to render each word in the text

i wrote some code that figures out where to put line breaks, and combines each line center-adjusted into one image output in `text/`

ffmpeg overlays the image on top of 30-frame loop of the star spinning in `filled/`

ffmpeg combines the course fade-in, the star spinning, and the jingle into one video in `1x/`

ffmpeg upscales it 4x from 320x240 to 1280x960 in `final/`

finally python deletes everything except the log files and the final video so that it doesn't clog up storage

if everything worked, you can delete the log files manually