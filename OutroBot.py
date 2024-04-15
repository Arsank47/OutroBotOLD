import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
from datetime import datetime, timedelta
import json
import os

#Insert your discord bot token below from the developer portal/applications/bot page
token = ''

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client1 = commands.Bot(
    command_prefix='!', intents=intents
)  # This only works if u create aysync functions using client.command so disable this if you would like it.

voice_client = None
disconnect_flag = True

# Dictionary to store available commands and their descriptions
commands_dict = {
    "!outro_help":
    "Display the available commands.",
    "!outro":
    "Play the outrobot but disconnect users at a normal pace.",
    "!outro_short":
    "Play the outrobot but disconnect users at a faster pace.",
    "!outro_long":
    "Play the outrobot but disconnect users at a slower pace WITH A SURPRISE ;)",
    "!outro_gillette":
    "!outro_game":
    "Ask the bot minimum two questions or games and the bot will pick a random option.",
    "!outro_test":
    "Use this command to test whether the bot is working.",
    "!outro_pause":
    "Pause the bot however this is an experimental feature and does not work properly.",
    "!outro_resume":
    "Resumes the bot if paused, however this is an experimental feature and does not work properly.",
    "!outro_request":
    "Allows the user to add a feature request of maximum of 200 words",
    "how to delete a outrorequest?":
    "sed -i '/^12345:/d' user_requests.txt OR sed -i `'/^Username: <discord username>:/d' user_request.txt",
    "!outro_list_requests":
    "This will list all of the current requests that have been recorded",
}

# Define a dictionary to store user requests
user_requests = {}


@client.event
async def on_message(message):
  global voice_client
  disconnect_flag = True  # Declare disconnect_flag variable here
  first_member_disconnected = None  # Declare first_member_disconnected variable here

  if message.author == client.user:
    return  # Ignore messages from the bot itself

  if message.content == '!outro_help':
    # Create an embedded message to display commands and descriptions
    embed = discord.Embed(title="Available Commands",
                          description="Here are the available commands:")

    for command, description in commands_dict.items():
      embed.add_field(name=command, value=description, inline=False)

    # Send the embedded message to the user
    await message.channel.send(embed=embed)

  if message.content == '!outro_short':
    # Check if the user is in a voice channel
    if message.author.voice:
      # Get the voice channel
      voice_channel = message.author.voice.channel

      # Play the sound file to all users in the voice channel
      sound_file = discord.FFmpegPCMAudio(
          'home/ubuntu/OutroBot/outro_music.mp3', executable='/usr/bin/ffmpeg')
      voice_client = await voice_channel.connect()
      while not voice_client.is_connected():
        await asyncio.sleep(0.1)
      voice_client.play(sound_file)

      await asyncio.sleep(15.5)  # Wait 16 seconds

      # Disconnect all users from the voice channel one at a time
      members = list(
          voice_channel.members)  # Make a copy of the list of members
      members = [m for m in members
                 if m.name != "OutroBot"]  # exclude OutroBot400 from the list
      random.shuffle(members)  # Shuffle the list of members
      for member in members:
        await member.edit(voice_channel=None)
        await asyncio.sleep(
            7)  # Wait 1 second before disconnecting the next user

      # Disconnect OutroBot
      for member in voice_channel.members:
        if member.name == "OutroBot":
          await member.edit(voice_channel=None)
          await asyncio.sleep(3)

          await voice_client.disconnect()
      disconnect_flag = True  # Reset the disconnect flag
    else:
      await message.channel.send('You are not in a voice channel!')

  if message.content == '!outro':
    # Check if the user is in a voice channel
    if message.author.voice:
      # Get the voice channel
      voice_channel = message.author.voice.channel

      # Play the sound file to all users in the voice channel
      sound_file = discord.FFmpegPCMAudio(
          '/home/ubuntu/OutroBot/outro_music.mp3',
          executable='/usr/bin/ffmpeg')
      voice_client = await voice_channel.connect()
      while not voice_client.is_connected():
        await asyncio.sleep(0.1)
      voice_client.play(sound_file)

      await asyncio.sleep(30)  # Wait 16 seconds

      # Disconnect all users from the voice channel one at a time
      members = list(
          voice_channel.members)  # Make a copy of the list of members
      members = [m for m in members
                 if m.name != "OutroBot"]  # exclude OutroBot from the list
      random.shuffle(members)  # Shuffle the list of members
      for member in members:
        if disconnect_flag:
          await member.edit(voice_channel=None)
          if not first_member_disconnected:
            first_member_disconnected = member.name
            # Wait 30 seconds before sending the message
            await asyncio.sleep(5)
            await message.channel.send(
                f"{first_member_disconnected} is the worst person in the world, as they was disconnected first."
            )
            await asyncio.sleep(
                3)  # Wait 7 seconds before disconnecting the next user

      # Disconnect OutroBot
      for member in voice_channel.members:
        if member.name == "OutroBot":
          if disconnect_flag:
            await member.edit(voice_channel=None)
            await asyncio.sleep(3)

      await voice_client.disconnect()
      disconnect_flag = True  # Reset the disconnect flag
    else:
      await message.channel.send('You are not in a voice channel!')

  if message.content == '!outro_long':
    # Check if the user is in a voice channel
    if message.author.voice:
      # Get the voice channel
      voice_channel = message.author.voice.channel

      # Play the sound file to all users in the voice channel
      sound_file = discord.FFmpegPCMAudio(
          'home/ubuntu/OutroBot/outro_music.mp3', executable='/usr/bin/ffmpeg')
      voice_client = await voice_channel.connect()
      while not voice_client.is_connected():
        await asyncio.sleep(0.1)
      voice_client.play(sound_file)

      await asyncio.sleep(45)  # Wait 16 seconds

      # Disconnect all users from the voice channel one at a time
      members = list(
          voice_channel.members)  # Make a copy of the list of members
      members = [m for m in members
                 if m.name != "OutroBot"]  # exclude OutroBot from the list
      random.shuffle(members)  # Shuffle the list of members
      for member in members:
        if disconnect_flag:
          await member.edit(voice_channel=None)
          if not first_member_disconnected:
            first_member_disconnected = member.name
            # Wait 30 seconds before sending the message
            await asyncio.sleep(5)
            await message.channel.send(
                f"{first_member_disconnected} is the worst person in the world, as they was disconnected first."
            )
            await asyncio.sleep(3)

      # Disconnect OutroBot
      for member in voice_channel.members:
        if member.name == "OutroBot":
          if disconnect_flag:
            await member.edit(voice_channel=None)
            await asyncio.sleep(3)

            disconnect_flag = True  # Reset the disconnect flag
    else:
      await message.channel.send('You are not in a voice channel!')

  # Specify the directory containing images
    images_directory = '/home/ubuntu/images'

    # List all files in the directory
    image_files = [
        f for f in os.listdir(images_directory)
        if os.path.isfile(os.path.join(images_directory, f))
    ]

    # Choose a random image file
    chosen_image = random.choice(image_files)

    # Create a file object for the chosen image
    file_path = os.path.join(images_directory, chosen_image)
    file = discord.File(file_path, filename=chosen_image)

    await asyncio.sleep(20)  # Wait 16 seconds

    # Send a message with the attached random image
    await message.channel.send(f'Have a meme/funny picture: {chosen_image}',
                               file=file)
    await voice_client.disconnect()

  if message.content == '!outro_gillette':
    # Check if the user is in a voice channel
    if message.author.voice:
      # Get the voice channel
      voice_channel = message.author.voice.channel

      # Play the sound file to all users in the voice channel
      sound_file = discord.FFmpegPCMAudio(
          'home/ubuntu/OutroBot/outro_music.mp3',
          executable='/usr/bin/ffmpeg'),
      voice_client = await voice_channel.connect()
      while not voice_client.is_connected():
        await asyncio.sleep(0.1)
      voice_client.play(sound_file)

      await asyncio.sleep(60)  # Wait 16 seconds

      # Disconnect all users from the voice channel one at a time
      members = list(
          voice_channel.members)  # Make a copy of the list of members
      members = [m for m in members
                 if m.name != "OutroBot"]  # exclude OutroBot from the list
      random.shuffle(members)  # Shuffle the list of members
      for member in members:
        if disconnect_flag:
          await member.edit(voice_channel=None)
          if not first_member_disconnected:
            first_member_disconnected = member.name
            # Wait 30 seconds before sending the message
            await asyncio.sleep(5)
            await message.channel.send(
                f"{first_member_disconnected} is the worst person in the world, as they was disconnected first."
            )
            await asyncio.sleep(
                7)  # Wait 7 seconds before disconnecting the next user

      # Disconnect OutroBot
      for member in voice_channel.members:
        if member.name == "OutroBot":
          if disconnect_flag:
            await member.edit(voice_channel=None)
            await asyncio.sleep(3)

            disconnect_flag = True  # Reset the disconnect flag
    else:
      await message.channel.send('You are not in a voice channel!')

  # Specify the directory containing images
    images_directory = '/home/ubuntu/images'

    # List all files in the directory
    image_files = [
        f for f in os.listdir(images_directory)
        if os.path.isfile(os.path.join(images_directory, f))
    ]

    # Choose a random image file
    chosen_image = random.choice(image_files)

    # Create a file object for the chosen image
    file_path = os.path.join(images_directory, chosen_image)
    file = discord.File(file_path, filename=chosen_image)

    await asyncio.sleep(20)  # Wait 16 seconds

    # Send a message with the attached random image
    await message.channel.send(f'Have a meme/funny picture: {chosen_image}',
                               file=file)
    await voice_client.disconnect()

  elif message.content.startswith('!outro_game'):
    # Get the list of games entered
    game_list = message.content.split()[1:]

    # Check if the minimum number of games is met
    if len(game_list) < 2:
      await message.channel.send('Please provide at least two games.')
      return

    max_request_length = 200  # You can adjust this limit
    if len(user_request) > max_request_length:
      await message.channel.send(
          f'Sorry, {message.author.mention}! Your request is too long.')
      return

    # Randomly pick a game
    chosen_game = random.choice(game_list)

    # Create suspense by sending filler lines
    await message.channel.send('Analyzing game options...')
    await asyncio.sleep(2)
    await message.channel.send('Generating probabilities...')
    await asyncio.sleep(3)
    await message.channel.send('Processing player preferences...')
    await asyncio.sleep(2)

    # Send the chosen game as a response
    await message.channel.send(f'The chosen game is: {chosen_game}')

  #elif message.content == '!outrotest':
  #await message.channel.send('OutroBot is online and ready to serve!')

  elif message.content == '!outrotest':
    # List of possible responses
    responses = [
        'OutroBot is online and ready to serve!',
        'OutroBot is online and ready to purge someone from the VC!',
        'OutroBot is online and ready to throw someone into the fighting pits in the Collesseum'
    ]

    # Choose a random response from the list
    response = random.choice(responses)

    await message.channel.send(response)
    """ await asyncio.sleep(4)

        embed = discord.Embed(title="Available Commands", description="Here are the available commands:")

        for command, description in commands_dict.items():
            embed.add_field(name=command, value=description, inline=False)

        # Send the embedded message to the user
        await message.channel.send(embed=embed) """

  elif message.content == '!outro_pause':
    if voice_client and voice_client.is_playing():
      voice_client.pause()
      disconnect_flag = False
      await message.channel.send('OutroBot has been paused.')
    else:
      await message.channel.send('OutroBot is not currently playing.')

  elif message.content == '!outro_resume':
    if voice_client and voice_client.is_paused():
      voice_client.resume()
      disconnect_flag = True
      await message.channel.send('OutroBot has been resumed.')
    else:
      await message.channel.send('OutroBot is not currently paused.')

  elif message.content.startswith('!outro_request'):
    # Extract the user's request from the message
    user_request = message.content[len('!outrorequest'):].strip()

    # Check if the user's request is within a reasonable length limit
    max_request_length = 200  # You can adjust this limit
    if len(user_request) > max_request_length:
      await message.channel.send(
          f'Sorry, {message.author.mention}! Your request is too long.')
      return

    # Store the user's request along with their username in the user_requests dictionary
    user_requests[message.author.id] = {
        'username': message.author.name,
        'request': f'**{user_request}**'  # Add double asterisks for bold text
    }

    # Save the requests to a text file (you can specify the file path)
    with open('user_requests.txt', 'a') as file:
      file.write(
          f'Username: {message.author.name}, User ID: {message.author.id}, Request: **{user_request}**\n'
      )

    await message.channel.send(
        f'Thank you, {message.author.mention}! Your request has been recorded.'
    )

  #The below version is used if u want the bot to provide DMs to the user
  #elif message.content == '!outrolistrequests':
  #try:
  # Read the contents of the user_requests.txt file
  #with open('user_requests.txt', 'r') as file:
  #requests = file.read()
  #await message.author.send(requests)  # Send the requests to the user via DM
  #except FileNotFoundError:
  #await message.channel.send('No requests found.')
  elif message.content == '!outro_list_requests':
    try:
      # Read the contents of the user_requests.txt file
      with open('user_requests.txt', 'r') as file:
        requests = file.read()
        if requests:
          # Create an embedded message to display the requests
          embed = discord.Embed(title="User Requests",
                                description="Here are the user requests:")
          embed.add_field(name="Requests", value=requests, inline=False)
          await message.channel.send(embed=embed)  # Send the embedded message
        else:
          await message.channel.send('No requests found.')
    except FileNotFoundError:
      await message.channel.send('No requests found.')


@client.event
async def on_disconnect():
  global voice_client
  print('Bot is offline and not working.')
  if voice_client:
    await voice_client.disconnect()


client.run(token)
