import discord
from discord.ext import commands

import urllib.parse

class Robotics(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		pass
		# bruh

	# Search goBILDA website
	@commands.command()
	async def gobilda(self, ctx, command, *, query):
		if (command == "search"):
			link = "https://www.gobilda.com/search-results-page?q=" + urllib.parse.quote(
			query)
			await ctx.send(link)

	# Search REV website
	@commands.command()
	async def rev(self, ctx, command, *, query):
		if (command == "search"):
			link = "https://www.revrobotics.com/search.php?search_query=" + urllib.parse.quote(query)
			await ctx.send(link)

async def setup(client):
	await client.add_cog(Robotics(client))