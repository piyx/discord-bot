# Setup
1. Go to https://discord.com/developers/applications and create an application.
2. Get the discord token and place it inside utils/secrets.py
3. Install ffmpeg (Note: You may need to install opus if you're on linux environment) https://ffmpeg.org/download.html#build-windows
4. `pip install -r requirements.txt`
5. `python bot.py`

### Note:
* To get other features to work (weather command and reddit command) you will need to get api key and client secret and paste it in utils/secret.py
* If you just want to use discord music bot commands then you can keep these files listed below and get rid of others.   
`cogs/music.py`  
`cogs/dscrd.py`  
`utils/embeds.py`  
`utils/yt_url.py`  
`utils/secret.py`
`bot.py`  
`music/` [This is an empty folder but very important. Don't delete this]

# Bot commands

# Music

> **play [music_name]** plays the song from youtube <br> 
> **pause** pauses the current playing song <br>
> **resume** resumes the song <br>
> **stop** stops playing music <br>
> **np** displays the now playing song <br>
> **queue** displays the song queue list <br>
> **skip** skips to next song in queue <br>
> **clear** clears the queue <br>
> **volume [volume_percent]** sets the volume<br>

## Usage

## play
<div style="width:100%"><img src="imgs/play.png"/><br/>

## Queue

<div style="width:100%"><img src="imgs/q.png"/><br/>

## Volume

<div style="width:100%"><img src="imgs/volume.png"/><br/>

# Discord

> **join** Adds the bot to voice channel <br>
> **leave** Removes the bot from voice channel <br>
> **delete [amount=5]** Deletes messages <br>
> **ping** Displays the ping <br>

## Usage

<div style="width:100%"><img src="imgs/dscrd.png"/><br/>

## Questions

> **ask [question]** Answers your question<br>
> **boss** Displays owners name<br>
> **coin** Flips a coin<br> 
> **dice** Rolls a dice<br>

## Usage

<div style="width:100%"><img src="imgs/qs.png"/><br/>

## Reddit

> **reddit [subreddit_name] [category]** Displays one post from the subreddit based on category<br>

## Usage

<div style="width:100%"><img src="imgs/reddit.png"/><br/>

## Sky

> **weather [city]** Displays the city's weather<br>
> **astro [city]** Displays the city's astronomy information<br>
> **nasa** Displays astronomy picture of the day<br>

## Usage

### Weather

<div style="width:100%"><img src="imgs/weather.png"/><br/>

### Nasa
<div style="width:100%"><img src="imgs/nasa.png"/>

