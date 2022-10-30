import discord
from discord.ext import commands

import asyncio

import youtube_dl

import requests
import json

class Moosic(commands.Cog):
	FFMPEG_ARGS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
	YT_DL_ARGS = {"format": "bestaudio"}

	playing = False

	da_queue = []

	temp = ""

	current = ""

	vc = None

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def connect(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("bruh, you're not even in a voice channel ;-;")
			return

		user_vc = ctx.author.voice.channel

		if ctx.voice_client is None:
			await user_vc.connect()
		else:
			await ctx.send("i'm busy! \:aqua_cry:")

	@commands.command()
	async def disconnect(self, ctx):
		if ctx.voice_client is None:
			await ctx.send("i'm not in a vc")
		else:
			await ctx.voice_client.disconnect()

	async def play_next(self):
		if len(self.da_queue) > 0:
			self.current = self.da_queue.pop()

			with youtube_dl.YoutubeDL(self.YT_DL_ARGS) as yt_dl:
				info = yt_dl.extract_info(self.current, download = False)
				source = await discord.FFmpegOpusAudio.from_probe(info["formats"][0]["url"], **self.FFMPEG_ARGS)

				self.playing = True

				self.vc.play(source, after = lambda e: asyncio.run(self.play_next()))
		else:
			self.playing = False

	async def play_audio(self, ctx):
		with youtube_dl.YoutubeDL(self.YT_DL_ARGS) as yt_dl:
			info = yt_dl.extract_info(self.current, download = False)
			source = await discord.FFmpegOpusAudio.from_probe(info["formats"][0]["url"], **self.FFMPEG_ARGS)

			self.playing = True

			self.vc = ctx.voice_client

			ctx.voice_client.play(source, after = lambda e: asyncio.run(self.play_next()))
			
	@commands.command(name = "play")
	async def play(self, ctx, url):
		self.da_queue.insert(0, url)

		if not self.playing:
			if ctx.voice_client is None:
				await self.connect(ctx)

			if len(self.da_queue) > 0:
				self.current = self.da_queue.pop()

				await self.play_audio(ctx)
			else:
				await ctx.send("there is nothing to play as the queue is empty \:kappa:")

	async def get_yt_title(self, url):
		data_url = "https://www.youtube.com/oembed?format=json&url=" + url

		response = requests.get(data_url)
		html = response.text
		data = json.loads(html)

		self.temp = str(data['title'])
			
	@commands.command()
	async def queue(self, ctx):
		if len(self.da_queue) == 0:
			await ctx.send("queue is empty :)")
			return

		result = discord.Embed(title = "Music Queue", description = "here's the upcoming sussy music", color = discord.Color.blue())		

		await self.get_yt_title(self.da_queue[-1])

		music_titles = "1) " + self.temp

		for i in range(2, len(self.da_queue) + 1):
			await self.get_yt_title(self.da_queue[-1 * i])

			music_titles = music_titles + "\n" + str(i) + ") " + self.temp

		result.add_field(name = "Music", value = "`" + music_titles + "`", inline = False)

		await ctx.send(embed = result)

	@commands.command()
	async def stop(self, ctx):
		if self.playing:
			self.playing = False
			ctx.voice_client.stop()
			await ctx.send("bye! \:tips_fedora:")

	@commands.command()
	async def pause(self, ctx):
		if self.playing:
			self.playing = False

			ctx.voice_client.pause()
			await ctx.send("ok, i pause")
		else:
			await ctx.send("i'm not playing anything \:beluga:")

	@commands.command()
	async def resume(self, ctx):
		if not self.playing:
			self.playing = True

			ctx.voice_client.resume()
			await ctx.send("ok, i resume")

async def setup(client):
	await client.add_cog(Moosic(client))