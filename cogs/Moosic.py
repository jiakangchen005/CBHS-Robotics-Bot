import discord
from discord.ext import commands

import youtube_dl

import urllib.request
import urllib
import json

class Moosic(commands.Cog):
	playing = False

	da_queue = []

	temp = ""

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def connect(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("bruh, you're not even in a voice channel ;-;")
			return

		vc = ctx.author.voice.channel

		if ctx.voice_client is None:
			await vc.connect()
		else:
			await ctx.send("i'm busy! :aqua_cry:")

	@commands.command()
	async def add(self, ctx, url):
		self.da_queue.insert(0, url)

	@commands.command()
	async def disconnect(self, ctx):
		if ctx.voice_client is None:
			await ctx.send("i'm not in a vc")
		else:
			await ctx.voice_client.disconnect()

	async def stream(self, ctx, url):
		ctx.voice_client.stop()

		FFMPEG_ARGS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

		YT_DL_ARGS = {"format": "bestaudio"}

		vc = ctx.voice_client

		with youtube_dl.YoutubeDL(YT_DL_ARGS) as yt_dl:
			info = yt_dl.extract_info(url, download = False)
			url = info["formats"][0]["url"]
			source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_ARGS)

			self.playing = True
			vc.play(source)

	@commands.command()
	async def play(self, ctx):
		if self.playing == True:
			await ctx.send("i'm already playing music \:beluga:")
		else:
			if ctx.voice_client is None:
				await self.connect(ctx)
			
			if len(self.da_queue) == 0:
				await ctx.send("there is nothing to play as the queue is empty \:kappa:")
			else:
				await self.stream(ctx, self.da_queue.pop())

	async def get_yt_title(self, url):
		parameters = {"format": "json", "url": url}

		data_url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(parameters)

		with urllib.request.urlopen(data_url) as response:
		    text = response.read()
		    data = json.loads(text.decode())
		    self.temp = str(data['title'])
			
	@commands.command()
	async def queue(self, ctx):
		result = discord.Embed(title = "Music Queue", description = "here's the upcoming sussy music", color = discord.Color.blue())		

		await self.get_yt_title(self.da_queue[-1])

		music_titles = "1) " + self.temp

		for i in range(2, len(self.da_queue) + 1):
			await self.get_yt_title(self.da_queue[-1 * i])

			music_titles = music_titles + "\n" + str(i) + ") " + self.temp

		result.add_field(name = "Music", value = "`" + music_titles + "`", inline = False)

		if len(self.da_queue) == 0:
			await ctx.send("queue is empty :)")

		await ctx.send(embed = result)

	@commands.command()
	async def stop(self, ctx):
		if self.playing:
			self.playing = False
			await ctx.voice_client.stop()
			await ctx.send("bye! \:tips_fedora:")

	@commands.command()
	async def pause(self, ctx):
		if self.playing:
			self.playing = False

			await ctx.voice_client.pause()
			await ctx.send("ok, i pause")
		else:
			await ctx.send("i'm not playing anything \:beluga:")

	@commands.command()
	async def resume(self, ctx):
		if not self.playing:
			await ctx.voice_client.resume()
			await ctx.send("ok, i resume")

async def setup(client):
	await client.add_cog(Moosic(client))