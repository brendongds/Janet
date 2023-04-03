import discord
from discord.ext import commands
import os
import random
import youtube_dl
import keep_alive
from PIL import Image
import tempfile
import praw



client = commands.Bot(command_prefix = "Janet, ", case_insensitive=True, intents=discord.Intents.all())

reddito = praw.Reddit(client_id='Nyyc6QEEvKGZapceiaLamA',
                     client_secret='8JrjlMqc-_GXhEDvT4TlYooIllBfHQ',
                     user_agent='Janete')

#MESSAGE VARS

mão = ["concorda cmg", "concorda comigo", "concordar cmg", "concordar comigo"]
anti_mão = ["Não concordo, por favor pare de insistir.", "Eu discordo.", "Não concordo nem  discordo, muito pelo contrário.", "Concordar é uma palavra muito forte."]

kd_soso = ["cade a soso", "cade soso", "kd a soso", "kd soso", "kade soso", "kade a soso",   "cade a sonelfa", "cade sonelfa", "kd sonelfa", "kd a sonelfa", "kade sonelfa", "kade a     sonelfa", "cadê a soso", "cadê soso", "cadê a sonelfa", "cadê sonelfa", "cade a s0s0",       "cade s0s0", "kd a s0s0", "kd s0s0", "kade s0s0", "kade a s0s0", "cadê a s0s0", "cadê s0s0"]
soso = ["Eu não sei."]

#EVENTS

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('beijos pra você ♡'))
  print('A {0.user.name} está online!'.format(client))
  print("----------------------")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('Hey Janet'):
    await message.channel.send ('Olá {}, em que posso ajudar?'.format(message.author.nick or message.author.name))
 
  if any(word in message.content for word in mão):
    await message.channel.send(random.choice(anti_mão))

  if any (word in message.content for word in kd_soso):
    if message.author.id == 313481995843796992:
      await message.channel.send ('Você é a Soso.')
    else:
      await message.channel.send(random.choice(soso))

  if message.content.startswith('chonga'):
    await message.add_reaction("🍆")

  if message.content.startswith('resize'):
    if message.attachments:
      for attachment in message.attachments:
        if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.png'):
          extension = attachment.filename.split(".")[-1]
          with tempfile.NamedTemporaryFile(delete=False, suffix="."+extension) as f:
            f.write(await attachment.read())
            f.seek(0)
            image = Image.open(f.name)
            image = image.resize((image.width * 7, image.height * 7))
            image.save(f.name)
            await message.channel.send(file=discord.File(f.name))


  
  await client.process_commands(message)

#COMMANDS

@client.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Por favor, diga quantas mensagens deseja apagar.')


@client.command()
async def fala(ctx, *, text):
  if ctx.message.author.id == 290600607809536012:
    message = ctx.message
    await message.delete()
    await ctx.send(f"{text}")
  else:
    await ctx.send("Eu não vou falar isso pra eles.")

@fala.error
async def fala_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Eu preciso saber o que falar pra eles.')


##################################  COMANDOS DE MÚSICA COM LINK DO YOUTUBE ####################################
@client.command()
async def play(ctx, url : str,):
  song_there = os.path.isfile("song.mp3")
  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Espere a música atual acabar ou use o comando 'parar'")
    return

  channel = ctx.message.author.voice.channel
  if not channel:
    await ctx.send("Você não está conectado à nenhum canal de voz.")
    return
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, "song.mp3")
  voice.play(discord.FFmpegPCMAudio("song.mp3"))


################################### COMANDOS PRA ADMINISTRAR O ÁUDIO REPRODUZIDO #################################
@client.command()
async def pausar(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("Não há música tocando no momento.")

@client.command()
async def continuar(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("A música já está tocando.")

@client.command()
async def parar(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()


################################# COMANDOS DE MÚSICA DE ARQUIVOS LOCAIS ####################################
  
@client.command()
async def lofi(ctx):
  channel = ctx.message.author.voice.channel
  if not channel:
    await ctx.send("Você não está conectado à nenhum canal de voz.")
    return
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  voice.play(discord.FFmpegPCMAudio("lofi1.mp3"))


@client.command()
async def lofi2(ctx):
  channel = ctx.message.author.voice.channel
  if not channel:
    await ctx.send("Você não está conectado à nenhum canal de voz.")
    return
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  voice.play(discord.FFmpegPCMAudio("lofi2.mp3"))


@client.command()
async def gauderias(ctx):
  channel = ctx.message.author.voice.channel
  if not channel:
    await ctx.send("Você não está conectado à nenhum canal de voz.")
    return
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  voice.play(discord.FFmpegPCMAudio("gauderias.mp3"))

######################## reddit #########################

@client.command()
async def reddit(ctx, subreddit):
    # Obtenha as 10 primeiras postagens do subreddit
    posts = reddito.subreddit(subreddit).hot(limit=50)
    # Escolha uma postagem aleatória
    post = random.choice(list(posts))
    await ctx.send(post.url)

##########################################################



keep_alive.keep_alive()
client.run(os.getenv('TOKEN'))
