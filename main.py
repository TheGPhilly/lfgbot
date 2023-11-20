import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="♡"))
    await bot.tree.sync()

class SimpleView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()  # times out after 30 seconds
        # Get the member's voice channel
        voice_channel = ctx.author.voice.channel
        # Get the server (guild) ID dynamically
        server_id = ctx.guild.id
        button = discord.ui.Button(
            label='Join',
            style=discord.ButtonStyle.url,
            url=f'https://discordapp.com/channels/{server_id}/{voice_channel.id}'
        )
        self.add_item(button)

@bot.hybrid_command(name="lfg", description="look for some players.")
async def lfg(ctx, game: str, message: str):
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send(f"{ctx.author.mention}, you are not in a voice channel.", ephemeral=True)
        return

    view = SimpleView(ctx)
    
    # Get the member's avatar URL
    author_avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    
    # Get the server's (guild) icon URL
    guild_icon_url = ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty
    
    # Create an embed with the avatar icon in the title and the server avatar
    embed = discord.Embed(
        title=f"{ctx.author.name} is looking for group",
        description=f"{ctx.author.mention} {message}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild_icon_url)  # Set author's avatar in the title
    
    embed.add_field(name="Game", value=game)
    embed.add_field(name="Voice Channel", value=f"<#{ctx.author.voice.channel.id}>")
    
    # Send the embed with the view
    message = await ctx.send(embed=embed, view=view)
    view.message = message

    await view.wait()

# Bot token (replace with your own token)
bot.run(TOKEN)
