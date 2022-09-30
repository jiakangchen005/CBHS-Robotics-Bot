from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		pass
		# bruh

	@commands.command()
	async def say(self, ctx, arg):
		await ctx.send(arg)

	@commands.command()
	async def random(self, ctx, num):
		import random
		await ctx.send(str(random.randint(1, int(num))))

async def setup(client):
	await client.add_cog(Fun(client))