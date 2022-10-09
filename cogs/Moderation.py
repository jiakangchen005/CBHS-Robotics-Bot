import discord
from discord.ext import commands

import sys

class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		pass
		# bruh

	@commands.command()
	async def clear(self, ctx, amount = sys.maxsize - 1):
		if (amount != sys.maxsize - 1):
			await ctx.channel.purge(limit = amount + 1)
		else:
			await ctx.channel.purge(limit = amount)

	# general member info
	@commands.command()
	async def whois(self, ctx, member: discord.Member = None):
		result = discord.Embed(title = "User Search", url = member.display_avatar.url, description = f"Results for {member}.", color = discord.Color.blue())

		result.set_thumbnail(url = member.display_avatar.url)

		result.add_field(name = "Username", value = f"`{member}`", inline = False)

		result.add_field(name = "Status", value = f"`{member.raw_status}`", inline = False)

		if (len(member.activities) > 0):
			result.add_field(name = "Activity(s)", value = f"`{member.activities[0].emoji} {member.activities[0].name}`", inline = False)
		else:
			result.add_field(name = "Activity(s)", value = "No Visible Activity", inline = False)

		result.add_field(name = "User ID", value = f"`{member.id}`", inline = False)

		join = member.created_at.strftime("%b %d, %Y")
		result.add_field(name = "Account Creation Date", value = f"`{join}`", inline = False)

		await ctx.send(embed = result)

	# profile pic
	@commands.command()
	async def pfp(self, ctx, member: discord.Member = None):
		await ctx.send(member.display_avatar.url)

async def setup(client):
	await client.add_cog(Moderation(client))