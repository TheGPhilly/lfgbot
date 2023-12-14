import discord
from discord.ext import commands
from discord.ui import View, Button
from config import TOKEN

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="♡"))
    await bot.tree.sync()

@bot.hybrid_command(name="lfg", description="Look for some players.")
async def lfg(ctx, game: str, *, message: str):
    # Check if the user is in a voice channel
    if not ctx.author.voice:
        await ctx.send(f"{ctx.author.mention}, you are not in a voice channel.", ephemeral=True)
        return
    
    # Get the member's avatar URL
    author_avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    
    # Get the server's (guild) icon URL
    guild_icon_url = ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty
    
    # Create an embed with the avatar icon in the title and the server avatar
    embed = discord.Embed(
        title=f"{ctx.author.name} is looking for a group",
        description=f"{ctx.author.mention} {message}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=guild_icon_url)  # Set author's avatar in the title
    embed.add_field(name="Game", value=game)
    
    # Get the user's current voice channel
    voice_channel = ctx.author.voice.channel
    
    # Create an invite link to the voice channel
    invite = await voice_channel.create_invite()
    invite_url = invite.url
    
    # Update the embed with the invite link
    embed.add_field(name="Voice Channel Invite", value=f"[Join]({invite_url})", inline=False)
    
    # Send the updated embed
    await ctx.send(embed=embed)

# Bot token (replace with your own token)
bot.run(TOKEN)
