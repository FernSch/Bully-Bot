import discord
import time
from discord import Spotify
import random
from discord import Embed
from rights import rights
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
#from googleapiclient.discovery import build
#from discord.app import Option
from keep_alive import keep_alive
from dislash import slash_commands
from dislash.interactions import *
from lists import *
from lists import stealfail, piss, iShame, spamchoice
import os
from ids import test_guilds
import json
import requests
import urllib.request
import wikipedia
from time import perf_counter
from discord import File, Member

url = "https://static.wikia.nocookie.net/jummys-rbossfight/images/0/0e/That_One_Pikachu_Costume_that_Someone_Inevitably_Puts_on_Every_Single_Year.png/revision/latest?cb=20191102121032"

week = 10080
workplace = [
    "jewelry Store", "farmers market", "school",
    "software development company", "indie startup", "yard sale", "college",
    "university", "reserach lab", "underground government military base",
    "place im too lazy to specify", "non specific place"
]

client = commands.Bot(command_prefix="?", case_sensetive=False)
slash = slash_commands.SlashClient(client)
whitelist = []
emoji1 = "<:bully_bot:842952171792498750>"
emoji2 = "<:lmfao:893455160423100467> "
rub_check = f"https://free.currconv.com/api/v7/convert?q=RUB_USD&compact=ultra&apiKey={currency_api}"
#os.chdir("bank.json")
client.remove_command("help")
client.lava_nodes = [{
    'host': 'lava.link',
    'port': '80',
    'rest_url': 'https://lava.link:80',
    'identifier': 'MAIN',
    'password': 'anything',
    'region': 'singapore'
}]


async def open_account(user):
    users = await get_bal()

    with open("bank.json", "r") as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bal():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users



def get_story():
  data = requests.get(f"https://gnews.io/api/v4/search?q=cnn&token={news}").json()

  return data['articles'][0]




@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        msg = '**Command Still on Cooldown**, please try again in {:.2f}s'.format(
            error.retry_after)
        await ctx.send(msg)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(f'back online?!?!'))
    print("ready!")
    #client.load_extension('dismusic')

@slash.command(name='bal',
               description="check bank balance",
               
               options=[
                   Option(name="member",
                          description="user to get bal of, defaults to you",
                          required=False,
                          type=6)
               ])
async def bal(ctx, member=None):

    if not member:
        member = ctx.author
    await open_account(ctx.author)
    users = await get_bal()

    wallet = users[str(member.id)]["wallet"]
    bank = users[str(member.id)]["bank"]

    total = wallet + bank

    embed = discord.Embed(title=f"{member.name}'s Balance",
                          color=discord.Color.blurple())
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.add_field(name="Wallet", value=wallet)
    embed.add_field(name="Bank", value=bank)

    await ctx.send(embed=embed)


@slash.command(name="earn", description="earn money", )
@cooldown(1, 30, BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bal()

    earnings = random.choice(begearn)
    if earnings == 66:
        earnings = random.choice(beg1)
    workplacechoice = random.choice(workplace)
    await ctx.send(
        f"you worked at  a {workplacechoice} and earned {earnings} coins!")
    if workplacechoice == "school" and earnings >= 100:
        await ctx.send("thats a lot for working at a school ... 💀")

    users[str(user.id)]["wallet"] += earnings
    with open("bank.json", "w") as f:
        json.dump(users, f)

@slash.command(
  name="ping", 
  description="get bot latency",
  
)
async def ping(ctx):
  start = time.perf_counter()
  message = await ctx.send("Pinging...")
  end = time.perf_counter()
  await message.edit(contents=f"Pong! :ping_pong: ({end - start}ms)")
  



@slash.command(name="pay",
               description="pay someone an amount of money",
               
               options=[
                   Option(name="user",
                          description="user to pay",
                          required=True,
                          type=6),
                   Option(name="amount",
                          description="amount of pay the user",
                          required=True,
                          type=Type.INTEGER)
               ])
async def pay(ctx, user, amount):
    await open_account(ctx.author)
    users = await get_bal()
    if str(user.id) in users:
        if user == ctx.author:
            await ctx.send("you can't pay yourself dumbass")
        else:
            if users[str(ctx.author.id)]["wallet"] < amount:
                await ctx.send(
                    "Error! you do not have enough money to pay that amount!")
            else:
                await open_account(ctx.author)
                users[str(user.id)]["wallet"] += amount
                users[str(ctx.author.id)]["wallet"] -= amount
                with open("bank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(
                    f"{ctx.author} just paid {user.mention} {amount} coins")
    else:
        await open_account(user)
        if user == ctx.author:
            await ctx.send("you cant pay yourself ")
        else:
            if users[str(ctx.author.id)]["wallet"] < amount:
                await ctx.send(
                    "Error! you do not have enough money to pay that amount!")
            else:
                await open_account(ctx.author)
                await open_account(user)
                users[str(user.id)]["wallet"] += amount
                users[str(ctx.author.id)]["wallet"] -= amount
                with open("bank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(
                    f"{ctx.author} just paid {user.mention} {amount} coins")


@slash.command(name="deposit",
               description="transfer money from your wallet to your bank",
               
               options=[
                   Option(name="amount",
                          description="Amount to deposit",
                          required=True,
                          type=Type.INTEGER)
               ])
async def deposit(ctx, amount):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bal()

    if amount < 0:
      await ctx.send("Error! You cannot deposit negative money!")
     
    elif users[str(ctx.author.id)]["wallet"] < amount:
        await ctx.send(
            "Error! you do not have enough money to deposit that amount!")
    else:
        users[str(user.id)]["wallet"] -= amount
        users[str(user.id)]["bank"] += amount
        with open("bank.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"{amount} coin(s) have been added to your bank")


@slash.command(name="withdraw",
               description="transfer money from your bank to your wallet",
               
               options=[
                   Option(name="amount",
                          description="Amount to withdraw",
                          required=True,
                          type=Type.INTEGER)
               ])
async def withdraw(ctx, amount):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bal()

    if amount < 0:
      await ctx.send("Error! you cannot withdraw negative money")
   
    elif users[str(ctx.author.id)]["bank"] < amount:
        await ctx.send(
            "Error! you do not have enough money to withdraw that amount!")
    else:
        users[str(user.id)]["bank"] -= amount
        users[str(user.id)]["wallet"] += amount
        with open("bank.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"{amount} coin(s) have been added to your wallet")


@slash.command(name="supporter",
               description="buy the supporter role",
               )
async def supporter(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bal()

    if users[str(ctx.author.id)]["wallet"] < 100000:
        await ctx.send(
            "Error! you do not have enough coins to buy the supporter role. If you think you do, please check that the coins are in your wallet and not your bank."
        )
    else:
        users[str(user.id)]["wallet"] -= 100000
        with open("bank.json", "w") as f:
            json.dump(users, f)
        role = discord.utils.get(ctx.guild.roles, name="Supporter")
        await ctx.author.add_roles(role, reason="purchased Supporter Role")
        await ctx.send(
            "100,000 Coins have Been deducted from your Wallet and the role of Supporter has been added!"
        )


@slash.command(
    name="give",
    description="give yourself money",
    
    options=[
        Option(name="amount",
               description="amount to get",
               required=True,
               type=Type.INTEGER),
        Option(name="choice",
               description=
               "wether to put in bank or wallet (type either bank or wallet)",
               required=True,
               type=Type.STRING),
        Option(name="user",
               description="user to give to",
               type=6,
               required=True)
    ])
async def give(ctx, amount, choice, user):
    users = await get_bal()
    if ctx.author.id != 399385792897744918:
        await ctx.send("Error. you aint fern ")
    else:
        users[str(user.id)][choice] += amount
        with open("bank.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"Added {amount} coins to bal")


@slash.command(
    name="take",
    description="take away money",
    
    options=[
        Option(name="amount",
               description="amount to take",
               required=True,
               type=Type.INTEGER),
        Option(name="choice",
               description=
               "wether to put in bank or wallet (type either bank or wallet)",
               required=True,
               type=Type.STRING),
        Option(name="user",
               description="user to give to",
               type=6,
               required=True)
    ])
async def take(ctx, amount, choice, user):
    users = await get_bal()
    if ctx.author.id != 399385792897744918:
        await ctx.send("Error. you aint fern ")
    else:
        users[str(user.id)][choice] -= amount
        with open("bank.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"took {amount} coins from {user.mention}")


@slash.command(
    name="leaderboard",
    description=
    "Get top however many people you want based off of total balance",
    
    options=[
        Option(name="amount",
               description=
               "how many people you want to show (e.g. 5 for top 5 people)",
               required=True,
               type=Type.INTEGER)
    ])
async def leaderboard(ctx, amount):
    users = await get_bal()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    embed = discord.Embed(title=f"Top {amount} richest People",
                          description="By Total balance",
                          color=discord.Color.blurple())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        mem = await client.fetch_user(id_)
        name = mem.name
        embed.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == amount:
            break
        else:
            index += 1

    await ctx.send(embed=embed)


@slash.command(name="steal",
               description="attempt to steal coins from another user",
               
               options=[
                   Option(name="user",
                          description="user to attempt to steal from",
                          required=True,
                          type=6)
               ])
async def steal(ctx, user):
    users = await get_bal()
    attempt = random.choice(asteal)
    print(attempt)
    if user == ctx.author:
        await ctx.send("Error! you Cannot steal from youself")
    else:
        if users[str(user.id)]["wallet"] == 0:
            await ctx.send("Error User does not have any coins in their wallet"
                           )
        else:
            if attempt == 0:
                await ctx.send(random.choice(stealfail))

            else:
                wallet_amt = users[str(user.id)]["wallet"]
                amount = random.randint(0, wallet_amt)
                users[str(user.id)]["wallet"] -= amount
                users[str(ctx.author.id)]["wallet"] += amount
                await ctx.send(
                    f"Success! You stole {amount} coins from {user.mention}")
                with open("bank.json", "w") as f:
                    json.dump(users, f)


@slash.command(
    name="depositall",
    description="desposit all coins from wallet to bank",
    
)
async def depositall(ctx):
    users = await get_bal()
    user = ctx.author
    users[str(ctx.author.id)]["bank"] += users[str(user.id)]["wallet"]
    users[str(user.id)]["wallet"] = 0
    with open("bank.json", "w") as f:
        json.dump(users, f)
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{user.name}'s Balance",
                          color=discord.Color.blurple())
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.add_field(name="Wallet", value=wallet_amt)
    embed.add_field(name="Bank", value=bank_amt)

    await ctx.send(embed=embed)


@slash.command(name="servers",
  description="check how many servers Bully Bot is in!",
)
async def servers(ctx):
  embed = discord.Embed(title=f"{client.user.name} is in ``{len(client.guilds)}`` servers", description=f"random server {client.user.name} is in")
  #print(client.guilds)
  embed.add_field(name=f"``{random.choice(client.guilds).name}``", value=f"``{random.choice(client.guilds).member_count}`` members")
#    for server in client.guilds:
#        embed.add_field(name=server.name, value="** **", inline=True)
  await ctx.send(embed=embed)


@slash.command(
    name="ping",
    description="show bot's ping",
)
async def ping(ctx):
    try:
        await ctx.send(f"Ping is: {round(client.latency * 1000)} ms")
    except:
        await ctx.send('error please try again')


@slash.command(name="userinfo",
               description="get info on a user",
               
               options=[
                   Option(name="member",
                          description="member to get info on",
                          required=True,
                          type=6)
               ])
async def userinfo(ctx, member: discord.Member):
    created_at = member.created_at.strftime("%b %d, %Y")
    embed = discord.Embed(title="User Info", decsription="")
    embed.add_field(name="Account Creation", value=created_at)
    embed.add_field(name="Server nickname",
                    value=member.display_name,
                    inline=True)
    embed.add_field(name=f"{ctx.guild} Join Date",
                    value=member.joined_at.strftime("%B %d %Y"),
                    inline=True)
    # .split makes the two parts of username (username and numbers) into a parts of a list e.g. bob#1111 into ['bob','1111'] then the zero accesses "bob"
    embed.set_author(name=str(member).split('#')[0],
                     icon_url=member.avatar_url)
    embed.add_field(name=f"Requested by", value=ctx.author, inline=False)
    await ctx.send(embed=embed)


@slash.command(name="worker",
               description="buys the worker role (1000 coins)",
               )
async def worker(ctx):
    user = ctx.author
    users = await get_bal()
    if users[str(ctx.author.id)]["wallet"] < 1000:
        await ctx.send(
            "Error! you do not have enough coins in your wallet to buy this role!"
        )
    else:
        users[str(user.id)]["wallet"] -= 1000
        with open("bank.json", "w") as f:
            json.dump(users, f)
        role = discord.utils.get(ctx.guild.roles, name="worker")
        await ctx.author.add_roles(role, reason="purchased worker role")
        await ctx.send(
            "1000 Coins have Been deducted from your Wallet and the role of Worker has been added!",
            ephemeral=False)


@slash.command(name="bid",
               description="bid on the curent item",
               guild_id=test_guilds,
               options=[
                   Option(name="amount",
                          description="amount to bid",
                          required=True,
                          type=Type.INTEGER)
               ])
async def bid(ctx, amount):
    users = await get_bal()
    user = ctx.author

    wallet_amt = users[str(user.id)]["wallet"]

    if amount > wallet_amt:
        await ctx.send(
            "You do not have enough coins in your wallet to do that!")
    else:
        bid_channel = client.get_channel(937780384664535111)
        await bid_channel.send(f"{ctx.author.mention} bid {amount} coins")
        await ctx.send(f"You have bid {amount} coins!")

"""
@slash.command(
  name="announce",
  description="send a announcement to all server Bully Bot is in",
  guild_ids=test_guilds,
  options=[
    Option(
      name="message",
      description="your message to send",
      required=True,
      type=Type.STRING
    )
  ]
)
async def announce(ctx, message):
  for guild in client.guilds:
    for channel in guild.channels:
      if "general" in str(channel):
        try:
          await channel.send(message)
          await ctx.send(f"sent message to {guild} in {channel}")
        except Exception:
          continue
      else:
        pass

"""
@slash.command(name="embed",
               description="send custom embed",
               
               options=[
                   Option(name="title",
                          description="title of embed",
                          required=True,
                          type=Type.STRING),
                   Option(name="description",
                          description="description of title",
                          required=True,
                          type=Type.STRING),
                   Option(name="field1",
                          description="field1 value",
                          required=True,
                          type=Type.STRING),
                   Option(name="name1",
                          description="title of field1",
                          required=True,
                          type=Type.STRING)
               ])
async def embed(ctx, title, description, field1, name1):
    embed = discord.Embed(title=title,
                          description=description,
                          color=discord.Color.blurple())
    embed.add_field(name=name1, value=field1)
    await ctx.send(embed=embed)


@slash.command(
    name="image",
    description="search google images",
    
    options=[
        Option(name="search",
               description="what you want to get",
               required=True,
               type=Type.STRING),
        Option(name="censored",
               description=
               "wether to censor image or not (doesnt censor by default)",
               type=5,
               required=False)
    ])
async def image(ctx, search, censored=False):
    if censored == False:
        num = random.randint(0, 0)
        resource = build("customsearch", "v1", developerKey=api).cse()
        result = resource.list(q=search,
                               cx="3f73517c636fcb9c3",
                               searchType="image").execute()
        url = result["items"][num]["link"]
        embed = discord.Embed(
            title=f"{ctx.author.name} searched for:  {search}")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    else:
        num = random.randint(0, 0)
        resource = build("customsearch", "v1", developerKey=api).cse()
        result = resource.list(q=search,
                               cx="3f73517c636fcb9c3",
                               searchType="image").execute()
        url = result["items"][num]["link"]
        await ctx.send(f"||{url}||")


@slash.command(name="kick",
               description="kick user from server",
               
               options=[
                   Option(name="user",
                          description="user to kick",
                          required=True,
                          type=6),
                   Option(name="reason",
                          description="reason for kick",
                          type=Type.STRING,
                          required=True),
                   Option(name="time",
                          description="time length user cannot join back for",
                          required=False,
                          type=Type.STRING)
               ])
async def kick(ctx, user, reason, time):
    if ctx.author.id == 399385792897744918:

        embed = discord.Embed(
            title=f"{user.name} has been kicked from this guild for {time}")
        embed.add_field(name=f"Reason: ", value=reason)
        embed.set_image(url=user.avatar_url)
        await user.send(
            f"You have been kicked from {ctx.author.guild} for {reason}. You cannt join back for {time} or else you may be banned."
        )
        await user.kick(reason=reason)
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            "Error! you do not have required permissions to preform this function!",
            emphemeral=True)

@slash.command(
  name="pride",
  description="happy pride!",
  guild_ids=test_guilds
)
async def pride(ctx):
  embed = discord.Embed(title=f"{random.choice(rights)} rights are human rights! ❤️ 🧡 💛 💚 💙 💜 🖤", )
  embed.set_image(url="flag.png")

  await ctx.send(embed = embed)
@slash.command(
    name="ruble",
    description="check the worth of the russian ruble",
)
async def ruble(ctx):
    resp = requests.get(url=rub_check)
    data = resp.json()
    embed = discord.Embed(title="Worth of Russian Ruble")
    embed.add_field(
        name="``",
        value=f"One Russian Ruble is woth `{data['RUB_USD']}` US Dollars")
    embed.set_footer(text="Stand with Ukraine 💙💛")
    await ctx.send(embed=embed)

@slash.command(
  name="top_story",
  description="get the top news story",
  guild_ids=test_guilds
)
async def top_story(ctx):
  data = get_story()
  embed = discord.Embed(title=data['title'], description=f"[{data['description']}]({data['url']})")
  
  try:
    embed.add_field(name=data['publishedAt'], value=data['content'].split('[')[0])
  except:
    embed.add_field(name=data['publishedAt'], value=data['content'])

  
  embed.set_thumbnail(url=data['image'])

  embed.set_author(name=data['source']['name'], url=data['source']['url'])

  await ctx.send(embed = embed)
  

@slash.command(
  name="track",
  description="track a package",
  guild_ids=test_guilds,
  options=[
    Option(
      name="number",
      description="tracking number",
      required=True,
      type=Type.STRING
    )
  ]
)
async def track(ctx,number):
  response = requests.get(url = "https://api.ship24.com/public/v1/tracking/search", params = {
    "trackingNumber": number
  }, headers = {
    "Authorization": f"Bearer {track_api}"
  })

  await ctx.send(response)


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == client.user:
        return
        if message.author.id == 159985870458322944:
            await message.channel.send(
                f'stfu {message.author.name}. i hate you')

    if "piss" in user_message.lower():
        await message.channel.send(random.choice(piss))

    if any(word in user_message.lower() for word in sheesh):
        await message.channel.send(
            f"sheeesh {message.author.mention} get into it :cold_face:")

    if "community" in user_message.lower():
        await message.channel.send(
            "i belong to two Facebook communities about my car")

    if "fuck you" in user_message.lower():
        await message.channel.send(f"bet {message.author.mention}")

    if "light mode" in user_message.lower():
        await message.channel.send("light mode sucks")

    if any(word in user_message.lower() for word in (rude)):
        await message.channel.send(
            f"{random.choice(rudelist)} {message.author.mention}")

    if "shut up" in user_message.lower():
        await message.channel.send(
            f"stfu {message.author.mention}. no one cares :neutral_face:")

    if "stfu" in user_message.lower():
        await message.channel.send(f"make me bitch {message.author.mention}")


#intro message
@client.event
async def on_guild_join(guild, ctx):
    new_servers = client.get_channel(884239840101687347)
    await new_servers.send(
        f"Someone invited me to a server! lets go!!! (server number: {str(len(client.guilds))}) Server: {guild.name}"
    )
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Thanks for invitng me!! <3 If you wanna hang out with cool people, or even suggest commands for me, you can join the bully bot support and community server (link in my bio). you can also follow my updates channel on the server for news about updates, new features, (and lots of boring stuff discord makes me do)'
            )
            await channel.send("\nhttps://top.gg/bot/838887977345613864")
        break


keep_alive()
client.run(TOKEN)
