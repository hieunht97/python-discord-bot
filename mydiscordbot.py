import discord
import response
import requests
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands



# async def send_message(message, user_message, is_private):
#     try:
#         response_text = response.get_response(user_message)
#         await message.author.send(response_text) if is_private else await message.channel.send(response_text)
    
#     except Exception as e:
#         print(e)
        

def run_discord_bot():
    
    #Discord bot token
    TOKEN = 'import your token here'
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    client = commands.Bot(command_prefix='!',intents=intents)
    
    #Get crypto data using CoinGecko
    def getCryptoPrices(crypto_id):
        URL = f'https://api.coingecko.com/api/v3/coins/{crypto_id}'
        params = {'vs_currency': 'usd'}
        r = requests.get(url=URL,params=params)
        data = r.json()
        
        name = data["name"]
        symbol = data["symbol"]
        price = data["market_data"]["current_price"]["usd"]
        ath = data["market_data"]["ath"]["usd"]
        
        return {"name": name, "symbol": symbol, "price": price, "ath": ath}

    #get crypto ID
    def getAllCryptoIds():
        params = {'vs_currency': 'usd'}
        response = requests.get('https://api.coingecko.com/api/v3/coins/list', params=params)
        if response.status_code == 200:
            data = response.json()
            return [coin['id'] for coin in data]
        else:
            return None
    
    #search for Artist and return artist info using Spotify API
    def search_for_artist(artist_name):
        url = "https://api.spotify.com/v1/search"
        token = 'Your token here'
        headers = {"Authorization": "Bearer " + token}
        
        # Replace spaces with %20 in the artist name
        artist_name = artist_name.replace(" ", "%20")
        
        query = f"?q={artist_name}&type=artist&limit=1"
        
        query_url = url + query
        result = requests.get(query_url, headers=headers)
        json_result = result.json()
        artist_data = json_result["artists"]["items"]
        
            
        artist_id = artist_data[0]["id"]
        artist_name = artist_data[0]["name"]
        artist_image = artist_data[0]["images"][0]["url"]
        artist_follower = artist_data[0]["followers"]["total"]
        artist_url = artist_data[0]["external_urls"]["spotify"]

        return {"id": artist_id, "name": artist_name, "img": artist_image, "follower": artist_follower, "artist_url": artist_url}
     
    #search for top 5 track of an artist in US
    def search_top_track(artist_id):
        url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US&limit=5'
        token = 'Your token here'
        headers = {"Authorization": "Bearer " + token}
        
        result = requests.get(url, headers=headers)
        data = result.json()["tracks"]
        song_names = []
        for track in data[:5]:
            song_names.append(track["name"])
        return song_names
    
        
    #Send announcemment when the bot is up and running
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        channel = client.get_channel(1076303867463082117)
        await channel.send(f'Bot is up now, hewwooooooo')
        
        try:
            synced = await client.tree.sync()
            print(f'Synced {len(synced)} commandd(s)')
        except Exception as e:
            print(e)
        
    
    #Return message based on member/user message, import response from response.py 
    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
        
    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
        
    #     print(f'{username} said: "{user_message}" ({channel})')

    #     if user_message[0] == '?':
    #         user_message = user_message[1:] 
    #         await send_message(message, user_message, is_private=True)
    #     else:
    #         await send_message(message, user_message, is_private=False)
    
    #Announce the server in a specific channel when a new member joins       
    @client.event
    async def on_member_join(member):
        print(f'{member.display_name} joined the server!')
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member.mention} Welcome to the server!')
    
    #Announce the server in a specific channel when a member leaves        
    @client.event
    async def on_member_remove(member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member.mention} Bye Baby!')
            
    #create a test button that sends messages
    class Menu(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
        
        @discord.ui.button(label='Send Message', style=discord.ButtonStyle.grey)
        async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.followup(content='xin chao')

    
    #Slash commmand 'hello'
    @client.tree.command(name='hello')
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Hey {interaction.user.mention}! This is a slash commmand, Baby!', ephemeral=True)
    
    
    #Slash command 'embed'
    @client.tree.command(name='embed')
    async def embed(interaction: discord.Interaction, member:discord.Member = None):
        if member == None:
            member = interaction.user
        
        view = Menu()
        name = member.display_name
        pfp = member.display_avatar
        data = getAllCryptoIds()
        print(type(data))
        cryptos = [f"**{item}**" for item in data[:10]]
        crypto_list = '\n'.join(cryptos)
        
        embed = discord.Embed(title="This is my embed", description="Its a very cool embed", colour=discord.Colour.green())
        embed.set_author(name=f"{name}", url='', icon_url='https://thumbs.dreamstime.com/b/two-cute-golden-retriever-puppies-playing-photo-45116795.jpg')
        embed.set_thumbnail(url=f'{pfp}')
        embed.add_field(name="Cryptocurrencies", value=crypto_list, inline=False)
        
        await interaction.response.send_message(embed=embed,view=view)
        
    #Slash command 'crypto'
    @client.tree.command(name='crypto')
    async def crypto(interaction: discord.Interaction, crypto_id: str):
        crypto_id = crypto_id.lower()
        try:
            data = getCryptoPrices(crypto_id)
        except Exception:
            await interaction.response.send_message(f"Sorry, ${crypto_id} is not a supported crypto.", ephemeral=True)
            return
        crypto_info = requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto_id}").json()
        logo_url = crypto_info["image"]["large"]
        
        embed = discord.Embed(title=data["name"], description=f"${data['symbol'].upper()}", color=0x26abff)
        embed.set_author(name=f'Check {crypto_id} price on CoinGecko', url=f"https://www.coingecko.com/en/coins/{crypto_id}", icon_url='https://static.coingecko.com/s/thumbnail-d5a7c1de76b4bc1332e48227dc1d1582c2c92721b5552aae76664eecb68345c9.png')
        embed.set_thumbnail(url=logo_url)
        embed.add_field(name="Price (USD)", value=f"${data['price']:.2f}")
        embed.add_field(name='All Time High (USD)', value=f"${data['ath']:2f}")
        embed.set_footer(text='Powered by YanCanCook')
        
        await interaction.response.send_message(embed=embed)
        
    #Slash command 'artist'
    @client.tree.command(name='artist')
    async def artist(interaction: discord.Interaction, artist_name: str):
        try:
            data = search_for_artist(artist_name)
        except Exception:
            await interaction.response.send_message(f"Sorry, ${artist_name} does not exist.", ephemeral=True)
            return
        
        logo_url = data["img"]
        song_names = search_top_track(data["id"])
        
        if data["follower"] >= 1000000:
            data["follower"] //= 1000000
            follower = f"{data['follower']}M Followers"
        elif data["follower"] >= 1000:
            follower_formatted = "{:,}".format(data["follower"])
            follower = f"{follower_formatted} Followers"
        else:
            follower = data["follower"]
        
        embed = discord.Embed(title=data["name"], description=follower, color=0x00ff00)
        embed.set_author(name=f'Check out {data["name"]} on Spotify', url=data["artist_url"], icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/991px-Spotify_icon.svg.png')
        embed.set_thumbnail(url=logo_url)
        embed.add_field(name="Top tracks", value="\n".join(song_names), inline=False)
        embed.set_footer(text='Powered by YanCanCook')
        
        await interaction.response.send_message(embed=embed)
    
    client.run(TOKEN)