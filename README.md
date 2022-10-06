# DankBot
![License](https://img.shields.io/github/license/IshanManchanda/DankBot?style=flat-square&color=blue)
[![CodeFactor](https://www.codefactor.io/repository/github/ishanmanchanda/dankbot/badge?style=flat-square)](https://www.codefactor.io/repository/github/ishanmanchanda/dankbot)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/04b9d80565c44b0d9d2677bdb86897ba)](https://www.codacy.com/gh/IshanManchanda/DankBot/dashboard)
[![codebeat badge](https://codebeat.co/badges/457b7511-92e7-4286-89fb-83483cd30c94)](https://codebeat.co/projects/github-com-ishanmanchanda-dankbot-master)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg?style=flat-square)](https://saythanks.io/to/Rippr)

DankBot - A Telegram Bot that sends, generates, and **deep fries** memes.

## Why DankBot?
DankBot has been an extremely fun project to work on.
<br>
The idea itself started off as a joke - My friends and I would often reference memes
in our conversations and wishfully talk about a tool that would share memes in response 
to certain triggers. While the idea of making a bot had occurred to me, the fact
that Whatsapp, our primary communications app, didn't have a public API was discouraging.
<br>
Later when I found out about Telegram's rich bot culture, I was thrilled
and soon began this project.
<br>

Since then the project has gone through enough changes to make it nearly unrecognizable,
most notably the addition of the deep frier and the various iterative improvements to it.
It has also served as a playground for a lot of things I've explored.
This list includes CI/CD systems like Travis CI and CodeShip,
automated code quality reviews (evidenced by the several badges!),
and different face detection methods with OpenCV.

### Major Technologies Used
- Python 3
- Pillow (Python Imaging Library)
- OpenCV-Python (Python bindings for the Open Computer Vision library)
- Numba
- Python Telegram Bot (Wrapper over the Telegram API)
- Papertrail Add-on on Heroku

### Things I've Learnt
- Building stateless, event-driven bots
- Detecting text, faces, and eyes in images using OpenCV
- Manipulating images with PIL
- Extracting frames from a video and making videos from a series of frames using OpenCV + imutils
- Using Numba JIT and asynchronous execution to improve performance
- Applying binary search on discrete functions (Used to calculating optimum text size in the meme generator)
- Uploading images to Imgur with PyImgur
- Using papertrail API for centralized logging
- Using static log analysis to get stats ([DankBot-Stats](https://github.com/IshanManchanda/DankBot-Stats))
- Using CI/CD systems like Travis CI and CodeShip
- Using automated code quality reviews

## Using DankBot

### Basic Commands
Each of these commands trigger a certain response. <br>
For most commands, there are multiple responses from which one is randomly picked.

- Hmmm
- Boom son
- Just do it
- E
- Hello there
- I don't think so
- Wut / Wat / Dude what / What even / What the
- Ironic
- F / RIP
- ???

### Advanced Commands

#### ABC, not XYZ
Generates a meme using either the Robbie Rotten, Babushka, or Drake template in which ABC is chosen over XYZ.

#### Alt: ABC
Converts text that follows the colon to aLt CaSe. It deletes the trigger message if bot has admin rights.

#### Vaporize: ABC
Converts text that follows the colon to Vaporwave text. It deletes the trigger message if bot has admin rights.

#### 🅱
Replaces the first consonant group of each word with a 🅱. <br>
It doesn't replace those consonants which can (mostly) be pronounced after a B.

#### Alexa / Dankbot play Despacito \[x\]
Sends a GIF of the Despacito music video along with an audio file of Despacito. <br>
If a number x is given, certain effects are applied to the audio. <br>
If not, the audio file has a 10% chance of being extremely bass boosted. <br>

#### T: ABC B: XYZ
Creates a meme with the provided captions when the message is a reply to an image.
ABC is the top-text and XYZ is the bottom-text.
By default, the captions are converted to upper case.
Replacing T with Ts and B with Bs prevents auto-capitalization.

### Deep Fryer
The Deep Fryer fries images, GIFs, or videos (Experimental).
Frying includes increasing saturation & contrast, and adding noise, emojis, laser eyes, and bulges.

The action is triggered by replying to a message containing a media file with one of the following commands:

- Fry: 1 cycle of frying.
- Nuke: 3 cycles of frying.
- Tsar Bomba: 5 cycles of frying.

#### Additional parameters

**Deep:** High contrast and saturation increase. <br>
**Shallow:** Low contrast and saturation increase. <br><br>

**High-fat:** Emojis are increased. <br>
**Low-fat:** Emojis are reduced. <br>
**No-fat:** Emojis aren't added. <br><br>

**Heavy:** Extra bulges are added. <br>
**Light:** No bulges are added. <br><br>

**Vitamin-B:** (Experimental) Adds the B emoji on text in the image. <br>
**Chilli:** (Experimental) Adds laser eyes.
