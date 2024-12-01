from distutils.dist import DistributionMetadata
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from sunau import AUDIO_FILE_ENCODING_MULAW_8
from sys import _debugmallocstats
import datetime
from discord.ext import tasks, commands
import discord
import random
import requests
import prtpy
from numberpartitioning import karmarkar_karp
import re
import math
import asyncio
import sqlite3
from discord.ext import commands
from bs4 import BeautifulSoup
from faceit_data import FaceitData

faceit_data = FaceitData("")

player_details = faceit_data.player_details("")


TOKEN = ''
client = commands.Bot(command_prefix=',')
client.remove_command("help")
db = sqlite3.connect('main.db')
dbmatches = sqlite3.connect('matches.db')
cursor = db.cursor()
cursorm = dbmatches.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
        id integer PRIMARY KEY AUTOINCREMENT,
        faceit TEXT,
        userid TEXT,
        currentelo INTEGER,
        name TEXT
    )
''')
cursorm.execute('''
    CREATE TABLE IF NOT EXISTS matches(
        id integer PRIMARY KEY AUTOINCREMENT,
        playerOne TEXT,
        playerTwo TEXT,
        playerThree TEXT,
        playerFour TEXT,
        playerFive TEXT,
        playerSix TEXT,
        playerSeven TEXT,
        playerEight TEXT,
        playerNine TEXT,
        playerTen TEXT,
        map TEXT,
        score TEXT,
        ongoing INTEGER
    )
''')

def eloToImg(elo):
    if elo >= 2001:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/NQc-2ZDNlBD.png'
    elif elo >= 1851: 
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/sMJ-bF07xuy.png'
    elif elo >= 1701:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/VFK-P8FMPlG.png'
    elif elo >= 1551:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/cMb-XYBHhEq.png'
    elif elo >= 1401:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/KpO-rnFa22r.png'
    elif elo >= 1251:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/zo2-m8V2jma.png'
    elif elo >= 1101:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/jNh-0mTaj6D.png'
    elif elo >= 951:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/xW90vXd7'
    elif elo >= 801:
        return 'https://i.imgur.com/4a4marb.png'
    else:
        return 'https://bucketeer-4624e8f0-5976-4ecd-b68c-0f0cc0f8959a.s3.eu-west-1.amazonaws.com/8Pu-zW0YZQL.png'

def eloToHex(elo):
    if elo >= 2001:
        return 0xfd1f00
    elif elo >= 1701:
        return 0xff6309
    elif elo >= 1101:
        return 0xffc800
    elif elo >= 801:
        return 0x1ce400
    else:
        return 0xf7f7f7

def getElo(playerId):
    cursorz = db.cursor()
    myName = cursorz.execute("SELECT name FROM main WHERE userid = :authorid", {"authorid" : playerId}).fetchall()
    if len(myName) != 0:
        myName = str(myName[0][0])
        url = f'https://faceitstats.com/player/{myName}'
        result = requests.get(url)
        doc = BeautifulSoup(result.content, "html.parser")
        maindata = str(doc.findAll('meta')[-1]).split("/")
        return str(maindata[1].split(' ', 2)[1])
    else:
        return 'N/A'

def getEloDB(playerId):
    cursorz = db.cursor()
    myElo = cursorz.execute("SELECT currentelo FROM main WHERE userid = :authorid", {"authorid" : playerId}).fetchall()
    if len(myElo) != 0:
        return str(myElo[0][0])
    else:
        return 'N/A'

def retrieveIdFromPlayer(num, matchId):
    player = ""
    if num == 1:
        player = 'playerOne'
    elif num == 2:
        player = 'playerTwo'
    elif num == 3:
        player = 'playerThree'
    elif num == 4:
        player = 'playerFour'
    elif num == 5:
        player = 'playerFive'
    elif num == 6:
        player = 'playerSix'
    elif num == 7:
        player = 'playerSeven'
    elif num == 8:
        player = 'playerEight'
    elif num == 9:
        player = 'playerNine'
    else:
        player = 'playerTen'
    finalId = cursorm.execute(f"SELECT {player} FROM matches WHERE id = :mid", {"mid" : matchId}).fetchall()[0][0]
    # print("Final id is " + str(finalId) + " for player num " + str(num))
    return str(finalId)

def formatRetrieval(num, matchId):
    if retrieveIdFromPlayer(num, matchId) == 'None':
        return ''
    else:
        return f'<@{retrieveIdFromPlayer(num, matchId)}>'

def retrieveMapImg(map):
    if map == 'dust':
        return 'https://static.wikia.nocookie.net/cswikia/images/3/3f/Csgo_set_dust_2_new.png'
    elif map == 'ancient':
        return 'https://static.wikia.nocookie.net/cswikia/images/7/7c/Map_icon_de_ancient.png'
    elif map == 'train':
        return 'https://static.wikia.nocookie.net/cswikia/images/6/60/Set_train.png'
    elif map == 'mirage':
        return 'https://static.wikia.nocookie.net/cswikia/images/9/96/Set_mirage.png'
    elif map == 'vertigo':
        return 'https://static.wikia.nocookie.net/cswikia/images/4/46/Vertigo-logo-new.png'
    elif map == 'inferno':
        return 'https://static.wikia.nocookie.net/cswikia/images/9/99/Set_inferno_2.png'
    else:
        return 'https://static.wikia.nocookie.net/cswikia/images/e/ef/Set_nuke_2.png'
        
@tasks.loop(hours=24)
async def refreshData():
    channel = client.get_channel(998156498922373170)
    await channel.send("Refreshing every user's ELO in the database. This may take a moment...")
    cur2 = db.cursor()
    for row in cur2.execute('SELECT userid FROM main' ):
        cursor.execute('''UPDATE main SET currentelo = ? WHERE userid= ?''', (int(getElo(row[0])), row[0]))
    await channel.send("Successfully updated every user's ELO.")
    await channel.send("Clearing unfinished matches. This may take a moment...")
    cur2 = dbmatches.cursor()
    for row in cur2.execute('SELECT id, score, ongoing FROM matches' ):
        if str(row[1]) == 'None' and row[2] == 0:
            cursorm.execute('DELETE FROM matches WHERE id = :uniqueid', {"uniqueid" : int(row[0])})
    dbmatches.commit()
    await channel.send("Successfully cleared unfinished matches.")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    refreshData.start()

@client.command()
async def leaderboard(ctx):

    allowed_mentions = discord.AllowedMentions(users=False)

    data = cursor.execute("SELECT userid, currentelo FROM main ORDER BY currentelo DESC").fetchall()
    def namegenerator(page):
        page += 1
        st = ''
        for i in range((page*10)-9,(page*10)+1):
            if i-1 == len(data):
                break
            st = st + f'{i}: ' + '<@' + str(data[i-1][0]) + '>' + '\n'
        return st

    def elogenerator(page):
        page += 1
        st = ''
        for i in range((page*10)-9,(page*10)+1):
            if i-1 == len(data):
                break
            st = st + str(data[i-1][1]) + '\n'
        return st

    nameContents = ['']

    for i in range(0,math.ceil(len(nameContents) / 10.0)):
        nameContents.insert(i, namegenerator(i))
    pages =  math.ceil(len(nameContents) / 10.0)
    cur_page = 1
    statEmbed = discord.Embed(color=0x37729c)
    statEmbed.set_author(name = f"Page {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
    statEmbed.add_field(name="Profile", value=namegenerator(cur_page-1), inline=True)
    statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
    message = await ctx.send(embed=statEmbed, allowed_mentions = allowed_mentions)
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                statEmbed = discord.Embed(color=0x37729c)
                statEmbed.set_author(name = f"Page {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
                statEmbed.add_field(name="Profile", value=namegenerator(cur_page-1), inline=True)
                statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
                await message.edit(embed=statEmbed, allowed_mentions = allowed_mentions)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                statEmbed = discord.Embed(color=0x37729c)
                statEmbed.set_author(name = f"Page {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
                statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
                await message.edit(embed=statEmbed, allowed_mentions = allowed_mentions)
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break

@client.command()
async def last(ctx,num,name):
    data = faceit_data.search_players(f"{name}")
    if int(round(float(num))) > 25 or int(round(float(num))) < 5:
        await ctx.channel.send(f"`{num}` is not a valid number. Number of matches must be between `5` and `25` inclusive.")
    elif not data.get('items'):
        await ctx.channel.send(f"Could not find user `{name}`. ")
    elif data.get('items')[0].get('nickname').lower() != f'{name.lower()}':
        await ctx.channel.send(f"Could not find user `{name}`. Did you mean `{data.get('items')[0].get('nickname')}`?")
    else:   
        fulldata = faceit_data.player_id_details(f"{data.get('items')[0].get('player_id')}")
        pelo = fulldata.get('games').get('csgo').get('faceit_elo')

        historydata = faceit_data.player_matches(f"{data.get('items')[0].get('player_id')}", 'csgo', None , None , None , f'{num}')
        matches = []
        rounds = 0
        kills = 0
        deaths = 0
        kd = 0
        kr = 0
        win = 0
        for k in historydata.get('items'):
            if k.get('game_id') == 'csgo':
                matches.append(k.get('match_id'))
                continue
        for k in matches:
            found = 0
            matchdata = faceit_data.match_stats(k).get('rounds')
            rounds = rounds + int(matchdata[0].get('round_stats').get('Rounds'))
            for p in matchdata[0].get('teams')[0].get('players'):
                if p.get('player_id') == data.get('items')[0].get('player_id'):
                    kills = kills + int(p.get('player_stats').get('Kills'))
                    deaths = deaths + int(p.get('player_stats').get('Deaths'))
                    kd = kd + float(p.get('player_stats').get('K/D Ratio'))
                    kr = kr + float(p.get('player_stats').get('K/R Ratio'))
                    win = win + int(p.get('player_stats').get('Result'))
                    found = 1
                    break
            if found == 0:
               for p in matchdata[0].get('teams')[1].get('players'):
                    if p.get('player_id') == data.get('items')[0].get('player_id'):
                        kills = kills + int(p.get('player_stats').get('Kills'))
                        deaths = deaths + int(p.get('player_stats').get('Deaths'))
                        kd = kd + float(p.get('player_stats').get('K/D Ratio'))
                        kr = kr + float(p.get('player_stats').get('K/R Ratio'))
                        win = win + int(p.get('player_stats').get('Result'))
                        break
        ckd = round(kd/int(num), 2)
        ckr = round(kr/int(num), 2)
        tkd = round(kills/float(deaths), 2)
        tkr = round(kills/float(rounds), 2)
        print(win)
        wr = round((win/int(num))*100)

        lifeEmbed = discord.Embed(color=eloToHex(int(pelo)))
        lifeEmbed.set_thumbnail(url=f"{fulldata.get('avatar')}")
        lifeEmbed.set_author(name = f"{data.get('items')[0].get('nickname')}", icon_url=eloToImg(int(pelo)))
        lifeEmbed.add_field(name="Profiles", value= f'{fulldata.get("faceit_url")}'.replace("{lang}", "en")+ '\n' + 'https://steamcommunity.com/profiles/' + f'{fulldata.get("steam_id_64")}', inline=False)
        lifeEmbed.add_field(name="\u200B", value=f'**Last {num} Statistics**', inline=False)
        lifeEmbed.add_field(name="K/D", value=f'{ckd}', inline=True)
        lifeEmbed.add_field(name="K/R", value=f'{ckr}', inline=True)
        lifeEmbed.add_field(name="ELO", value=f'{pelo}', inline=True)
        lifeEmbed.add_field(name="True K/D", value=f'{tkd}', inline=True)
        lifeEmbed.add_field(name="True K/R", value=f'{tkr}', inline=True)
        lifeEmbed.add_field(name="Winrate", value=f'{wr}' + '%', inline=True)
        await ctx.channel.send(embed=lifeEmbed)

@last.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title="Retrieve last X match statistics",description="Retrieves last X matches and calculates statistics such as K/D, K/R, etc.")
        em.add_field(name = "**Syntax**", value = "`,last <number of matches> <player>`", inline=False)
        em.add_field(name = "**Notes**", value = "`<number of matches>` has to be between `5` and `25` inclusive. \n True statistics are calculated by using kills, deaths, etc. in the matches, whereas regular is an average of K/Ds in matches.", inline=False)
        await ctx.channel.send(embed=em) 

@client.command(aliases=['search', 'lookup', 'stats'])
async def find(ctx, name):
    data = faceit_data.search_players(f"{name}")
    if not data.get('items'):
        await ctx.channel.send(f"Could not find user `{name}`. ")
    elif data.get('items')[0].get('nickname').lower() != f'{name.lower()}':
        await ctx.channel.send(f"Could not find user `{name}`. Did you mean `{data.get('items')[0].get('nickname')}`?")
    else:
        fulldata = faceit_data.player_id_details(f"{data.get('items')[0].get('player_id')}")
        moredata = faceit_data.player_stats(f"{data.get('items')[0].get('player_id')}", 'csgo')
        rankingdata = faceit_data.player_ranking_of_game('csgo', f'{fulldata.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}")
        regiondata = faceit_data.player_ranking_of_game('csgo', f'{fulldata.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}", f'{fulldata.get("country")}')

        # print(rankingdata.items())
        # print(regiondata.items())
        # print(fulldata.items())
        # print(moredata.items())
        pelo = fulldata.get('games').get('csgo').get('faceit_elo')
        lifeEmbed = discord.Embed(color=eloToHex(int(pelo)))
        lifeEmbed.set_thumbnail(url=f"{fulldata.get('avatar')}")
        lifeEmbed.set_author(name = f"{data.get('items')[0].get('nickname')}", icon_url=eloToImg(int(pelo)))
        lifeEmbed.add_field(name="Profiles", value= f'{fulldata.get("faceit_url")}'.replace("{lang}", "en")+ '\n' + 'https://steamcommunity.com/profiles/' + f'{fulldata.get("steam_id_64")}', inline=False)
        lifeEmbed.add_field(name="\u200B", value='**Lifetime Statistics**', inline=False)
        lifeEmbed.add_field(name="ELO", value=f'{pelo}', inline=True)
        lifeEmbed.add_field(name="Winrate", value=f'{moredata.get("lifetime").get("Win Rate %")}' + '%', inline=True)
        lifeEmbed.add_field(name="K/D", value=f'{moredata.get("lifetime").get("Average K/D Ratio")}', inline=True)
        lifeEmbed.add_field(name="\u200B", value='**Ranking Statistics**', inline=False)
        lifeEmbed.add_field(name=f'{fulldata.get("games").get("csgo").get("region")}' + " Ranking", value=f'{rankingdata.get("position")}', inline=True)
        lifeEmbed.add_field(name=f':flag_{fulldata.get("country")}:'+" Ranking", value=f'{regiondata.get("position")}', inline=True)
        await ctx.channel.send(embed=lifeEmbed)

@find.error
async def missing_parameter(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        
        myName = cursor.execute("SELECT name FROM main WHERE userid = :authorid", {"authorid" : ctx.author.id}).fetchall()
        if len(myName) != 0:
            data = faceit_data.search_players(f"{myName[0][0]}")
            fulldata = faceit_data.player_id_details(f"{data.get('items')[0].get('player_id')}")
            moredata = faceit_data.player_stats(f"{data.get('items')[0].get('player_id')}", 'csgo')
            rankingdata = faceit_data.player_ranking_of_game('csgo', f'{fulldata.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}")
            regiondata = faceit_data.player_ranking_of_game('csgo', f'{fulldata.get("games").get("csgo").get("region")}', f"{data.get('items')[0].get('player_id')}", f'{fulldata.get("country")}')

            # print(rankingdata.items())
            # print(regiondata.items())
            # print(fulldata.items())
            # print(moredata.items())
            pelo = fulldata.get('games').get('csgo').get('faceit_elo')
            lifeEmbed = discord.Embed(color=eloToHex(int(pelo)))
            lifeEmbed.set_thumbnail(url=f"{fulldata.get('avatar')}")
            lifeEmbed.set_author(name = f"{data.get('items')[0].get('nickname')}", icon_url=eloToImg(int(pelo)))
            lifeEmbed.add_field(name="Profiles", value= f'{fulldata.get("faceit_url")}'.replace("{lang}", "en")+ '\n' + 'https://steamcommunity.com/profiles/' + f'{fulldata.get("steam_id_64")}', inline=False)
            lifeEmbed.add_field(name="\u200B", value='**Lifetime Statistics**', inline=False)
            lifeEmbed.add_field(name="ELO", value=f'{pelo}', inline=True)
            lifeEmbed.add_field(name="Winrate", value=f'{moredata.get("lifetime").get("Win Rate %")}' + '%', inline=True)
            lifeEmbed.add_field(name="K/D", value=f'{moredata.get("lifetime").get("Average K/D Ratio")}', inline=True)
            lifeEmbed.add_field(name="\u200B", value='**Ranking Statistics**', inline=False)
            lifeEmbed.add_field(name=f'{fulldata.get("games").get("csgo").get("region")}' + " Ranking", value=f'{rankingdata.get("position")}', inline=True)
            lifeEmbed.add_field(name=f':flag_{fulldata.get("country")}:'+" Ranking", value=f'{regiondata.get("position")}', inline=True)
            await ctx.channel.send(embed=lifeEmbed)
        else:
            await ctx.send("Your account is not linked to a FACEIT profile and you have not specified a user to search. If you wish to search yourself, either link your account and try again, or enter your name in the argument.")

@client.command()
async def myid(ctx):
    myid = cursor.execute("SELECT id FROM main WHERE userid = :authorid", {"authorid" : ctx.author.id}).fetchall()
    if len(myid) != 0:
        await ctx.send("Your unique id is " + str(myid[0][0]) + ".")
    else:
        await ctx.send("Your Discord account is not linked to a FACEIT profile.")

@client.command()
async def unlink(ctx):
    myid = cursor.execute("SELECT id FROM main WHERE userid = :authorid", {"authorid" : ctx.author.id}).fetchall()
    if len(myid) != 0:
        cursor.execute("DELETE FROM main WHERE userid = :uniqueid", {"uniqueid" : ctx.author.id})
        db.commit()
        await ctx.send("Successfully removed your profile data.")
    else:
        await ctx.send("Your Discord account is not linked to a FACEIT profile.")

@commands.has_permissions(administrator=True)
@client.command(aliases=['create', 'matchcreate'])
async def creatematch(ctx, map):
    validMap = False
    if map == 'dust' or map == 'ancient' or map == 'train' or map == 'mirage' or map == 'vertigo' or map == 'inferno' or map == 'nuke':
        validMap = True
    else:
        await ctx.channel.send('Invalid map. You must choose between `dust`, `train`, `mirage`, `vertigo`, `inferno`, or `nuke`.')
    if validMap:
        cursorm.execute("INSERT INTO matches (map, ongoing) VALUES (?, ?)", (map, 0))
        dbmatches.commit()
        matchId = cursorm.execute("SELECT id FROM matches ORDER BY id DESC LIMIT 1").fetchall()[0][0]
        matchEmbed = discord.Embed(title=f'Match {matchId}', color=0x37729c)
        matchEmbed.set_thumbnail(url=retrieveMapImg(map))
        matchEmbed.add_field(name="Team 1 Avg ELO", value='N/A', inline=True)
        matchEmbed.add_field(name="Team 2 Avg ELO", value='N/A', inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 1", value=
                                            "1: " + f'{formatRetrieval(1, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(2, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(3, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(4, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(5, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(1, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(2, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(3, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(4, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(5, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 2", value=
                                            "1: " + f'{formatRetrieval(6, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(7, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(8, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(9, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(10, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(6, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(7, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(8, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(9, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(10, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        await ctx.channel.send(embed=matchEmbed)


@client.command(aliases=['begin', 'matchbegin', 'startmatch', 'matchstart', 'start'])
async def beginmatch(ctx, matchId):

    def getAvgElo(teamNo, match):
        eloSum = 0
        playerSum = 0
        if teamNo == 1:
            if getEloDB(retrieveIdFromPlayer(1, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(1, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(2, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(2, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(3, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(3, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(4, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(4, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(5, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(5, match)))
                playerSum += 1
        else:
            if getEloDB(retrieveIdFromPlayer(6, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(6, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(7, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(7, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(8, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(8, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(9, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(9, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(10, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(10, match)))
                playerSum += 1
        if eloSum == 0:
            return 'N/A'
        else:
            return str(round(eloSum/playerSum))

    captOne = retrieveIdFromPlayer(1, matchId)
    captTwo = retrieveIdFromPlayer(6, matchId)

    statusm = cursorm.execute(f"SELECT ongoing FROM matches WHERE id = {matchId}").fetchall()
    if statusm[0][0] != 0:
        await ctx.channel.send("The match is either ongoing of finished.")
    elif str(ctx.author.id) == str(captOne) or str(ctx.author.id) == str(captTwo):
        cursorm.execute(f"UPDATE matches SET ongoing = 1 WHERE id = :mmid", {"mmid" : matchId})
        dbmatches.commit()

        messages_in_channel = await ctx.channel.history(limit=50).flatten()

        for message in messages_in_channel:
            x = message.embeds
            if x:
                if f'Match {matchId}' in x[0].title:  # if it has an embed
                    await message.delete()
                    break

        map = cursorm.execute("SELECT map FROM matches WHERE id = :trueId", {"trueId" : matchId}).fetchall()[0][0]
        matchEmbed = discord.Embed(title=f'ONGOING Match {matchId}', color=0xff0000)
        matchEmbed.set_thumbnail(url=retrieveMapImg(map))
        matchEmbed.add_field(name="Team 1 Avg ELO", value=getAvgElo(1, matchId), inline=True)
        matchEmbed.add_field(name="Team 2 Avg ELO", value=getAvgElo(2, matchId), inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 1", value=
                                            "1: " + f'{formatRetrieval(1, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(2, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(3, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(4, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(5, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(1, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(2, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(3, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(4, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(5, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 2", value=
                                            "1: " + f'{formatRetrieval(6, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(7, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(8, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(9, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(10, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(6, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(7, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(8, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(9, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(10, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        await ctx.channel.send(embed=matchEmbed)
    else:
        await ctx.channel.send("Only team captains (first player of both teams) can use this command.")

@beginmatch.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
        em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator or team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
        await ctx.channel.send(embed=em) 

@creatematch.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title="Create match",description="Creates a match with two teams. Creator is automatically in Team 1.")
        em.add_field(name = "**Syntax**", value = "`,creatematch <map>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Has alias commands named `create` and `matchcreate`.", inline=False)
        await ctx.channel.send(embed=em)

@client.command(aliases=['join', 'matchjoin'])
async def joinmatch(ctx, matchId, teamNo):

    def getAvgElo(teamNo, match):
        eloSum = 0
        playerSum = 0
        if teamNo == '1':
            if getEloDB(retrieveIdFromPlayer(1, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(1, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(2, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(2, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(3, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(3, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(4, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(4, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(5, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(5, match)))
                playerSum += 1
        else:
            if getEloDB(retrieveIdFromPlayer(1, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(6, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(2, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(7, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(3, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(8, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(4, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(9, match)))
                playerSum += 1
            if getEloDB(retrieveIdFromPlayer(5, match)) != 'N/A':
                eloSum += int(getEloDB(retrieveIdFromPlayer(10, match)))
                playerSum += 1
        if eloSum == 0:
            return 'N/A'
        else:
            return str(round(eloSum/playerSum))

    teamNo = str(teamNo)
    full = True
    spot = 0
    myid = cursorm.execute("SELECT id FROM matches WHERE id = :mid", {"mid" : matchId}).fetchall()
    inTeam = False
    if teamNo == '1' and len(myid) != 0:
        for i in range(1,6):
            if str(retrieveIdFromPlayer(i, matchId)) == 'None':
                full = False
                spot = i
                break
    if teamNo == '2' and len(myid) != 0:
        for i in range(6,11):
            if str(retrieveIdFromPlayer(i, matchId)) == 'None':
                full = False
                spot = i
                break

    for i in range(1,11):
        if len(myid) != 0 and str(retrieveIdFromPlayer(i, matchId)) == f'{ctx.author.id}':
            inTeam = True
            break
    if len(myid) == 0:
        await ctx.channel.send("Could not find the match ID.")
    elif not (teamNo == '1' or teamNo == '2'):
        await ctx.channel.send("Please enter a valid team number.")
    elif full:
        await ctx.channel.send("Team is full.")
    elif inTeam:
        await ctx.channel.send("You are already in a team.")
    else: 
        player = ""
        if spot == 1:
            player = 'playerOne'
        elif spot == 2:
            player = 'playerTwo'
        elif spot == 3:
            player = 'playerThree'
        elif spot == 4:
            player = 'playerFour'
        elif spot == 5:
            player = 'playerFive'
        elif spot == 6:
            player = 'playerSix'
        elif spot == 7:
            player = 'playerSeven'
        elif spot == 8:
            player = 'playerEight'
        elif spot == 9:
            player = 'playerNine'
        elif spot == 10:
            player = 'playerTen'

        cursorm.execute(f"UPDATE matches SET {player} = {ctx.author.id} WHERE id = :mmid", {"mmid" : matchId})
        dbmatches.commit()
        messages_in_channel = await ctx.channel.history(limit=50).flatten()

        for message in messages_in_channel:
            x = message.embeds
            if x:
                if f'Match {matchId}' in x[0].title:  # if it has an embed
                    await message.delete()
                    break
        map = cursorm.execute("SELECT map FROM matches WHERE id = :trueId", {"trueId" : matchId}).fetchall()[0][0]
        matchEmbed = discord.Embed(title=f'Match {matchId}', color=0x37729c)
        matchEmbed.set_thumbnail(url=retrieveMapImg(map))
        matchEmbed.add_field(name="Team 1 Avg ELO", value='N/A', inline=True)
        matchEmbed.add_field(name="Team 2 Avg ELO", value='N/A', inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 1", value=
                                            "1: " + f'{formatRetrieval(1, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(2, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(3, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(4, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(5, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(1, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(2, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(3, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(4, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(5, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 2", value=
                                            "1: " + f'{formatRetrieval(6, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(7, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(8, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(9, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(10, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(6, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(7, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(8, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(9, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(10, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        await ctx.channel.send(embed=matchEmbed)

@joinmatch.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title="Join match",description="Joins a match that was created using `,creatematch`")
        em.add_field(name = "**Syntax**", value = "`,joinmatch <match id> <team number>`", inline=False)
        await ctx.channel.send(embed=em)

@client.command()
async def refreshelo(ctx):
    myid = cursor.execute("SELECT id FROM main WHERE userid = :authorid", {"authorid" : ctx.author.id}).fetchall()
    if len(myid) != 0:
        cursor.execute(f"UPDATE main SET currentelo = {getElo(ctx.author.id)} WHERE userid = {ctx.author.id}")
        db.commit()
        await ctx.channel.send("Successfully updated your ELO.")
    else:
        await ctx.send("Your Discord account is not linked to a FACEIT profile.")

@client.command(aliases=['frefresh'])
@commands.has_permissions(administrator=True)
async def forcerefresh(ctx, uid):
    allowed_mentions = discord.AllowedMentions(users=False)
    myid = cursor.execute("SELECT userid FROM main WHERE id = :authorid", {"authorid" : uid}).fetchall()
    if len(myid) != 0:
        cursor.execute(f"UPDATE main SET currentelo = {getElo(myid[0][0])} WHERE userid = {myid[0][0]}")
        db.commit()
        await ctx.channel.send(f"Successfully updated the ELO of user <@{myid[0][0]}>.", allowed_mentions = allowed_mentions)
    else:
        await ctx.send(f"The ID `{uid}` is not linked to a profile.")

@forcerefresh.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Force Refresh",description="Forcefully refreshes a user's ELO.")
        em.add_field(name = "**Syntax**", value = "`,forcerefresh <id>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use.", inline=False)
        await ctx.channel.send(embed=em)

@client.command(aliases=['report', 'matchreport'])
async def reportmatch(ctx, matchId, scrm):
    score = cursorm.execute("SELECT ongoing FROM matches WHERE id = :mid", {"mid" : matchId}).fetchall()
    captOne = retrieveIdFromPlayer(1, matchId)
    captTwo = retrieveIdFromPlayer(6, matchId)

    if (score[0][0]) == 0:
        await ctx.channel.send("The match has not started yet.")
    elif score[0][0] == 2:
        await ctx.channel.send("The match has already finished.")
    elif (score[0][0]) == 1 and (str(ctx.author.id) == str(captOne) or str(ctx.author.id) == str(captTwo)):

        cursorm.execute(f'UPDATE matches SET score = (?) WHERE id = {matchId}', [str(scrm)])
        cursorm.execute(f'UPDATE matches SET ongoing = 2 WHERE id = {matchId}')
        dbmatches.commit()

        def getAvgElo(teamNo, match):
            eloSum = 0
            playerSum = 0
            if teamNo == 1:
                if getEloDB(retrieveIdFromPlayer(1, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(1, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(2, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(2, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(3, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(3, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(4, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(4, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(5, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(5, match)))
                    playerSum += 1
            else:
                if getEloDB(retrieveIdFromPlayer(6, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(6, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(7, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(7, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(8, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(8, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(9, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(9, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(10, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(10, match)))
                    playerSum += 1
            if eloSum == 0:
                return 'N/A'
            else:
                return str(round(eloSum/playerSum))

        messages_in_channel = await ctx.channel.history(limit=50).flatten()

        for message in messages_in_channel:
            x = message.embeds
            if x:
                if f'Match {matchId}' in x[0].title:  # if it has an embed
                    await message.delete()
                    break
        
        map = cursorm.execute("SELECT map FROM matches WHERE id = :trueId", {"trueId" : matchId}).fetchall()[0][0]
        matchEmbed = discord.Embed(title=f'FINISHED Match {matchId}', color=0x00ff00)
        matchEmbed.set_thumbnail(url=retrieveMapImg(map))
        matchEmbed.add_field(name="Team 1 Avg ELO", value=getAvgElo(1, matchId), inline=True)
        matchEmbed.add_field(name="Team 2 Avg ELO", value=getAvgElo(2, matchId), inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 1", value=
                                            "1: " + f'{formatRetrieval(1, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(2, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(3, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(4, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(5, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(1, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(2, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(3, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(4, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(5, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 2", value=
                                            "1: " + f'{formatRetrieval(6, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(7, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(8, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(9, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(10, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(6, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(7, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(8, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(9, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(10, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name ="Score", value=f'{scrm}', inline=False)
        await ctx.channel.send(embed=matchEmbed)
    else:
        await ctx.channel.send("Only team captains (first player of both teams) can use this command.")

@reportmatch.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Report a match score",description="Finishes an ongoing match with the reported score.")
        em.add_field(name = "**Syntax**", value = "`,report <match id> <score>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator to use. \n Has alias command named `report`.", inline=False)
        await ctx.channel.send(embed=em) 

@client.command(aliases=['freport'])
@commands.has_permissions(administrator=True)
async def forcereport(ctx, matchId, scrm):

    score = cursorm.execute("SELECT ongoing FROM matches WHERE id = :mid", {"mid" : matchId}).fetchall()
    if (score[0][0]) == 0:
        await ctx.channel.send("The match has not started yet.")
    elif (score[0][0]) == 1:

        cursorm.execute(f'UPDATE matches SET score = (?) WHERE id = {matchId}', [str(scrm)])
        cursorm.execute(f'UPDATE matches SET ongoing = 2 WHERE id = {matchId}')
        dbmatches.commit()

        def getAvgElo(teamNo, match):
            eloSum = 0
            playerSum = 0
            if teamNo == 1:
                if getEloDB(retrieveIdFromPlayer(1, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(1, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(2, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(2, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(3, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(3, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(4, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(4, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(5, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(5, match)))
                    playerSum += 1
            else:
                if getEloDB(retrieveIdFromPlayer(6, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(6, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(7, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(7, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(8, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(8, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(9, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(9, match)))
                    playerSum += 1
                if getEloDB(retrieveIdFromPlayer(10, match)) != 'N/A':
                    eloSum += int(getEloDB(retrieveIdFromPlayer(10, match)))
                    playerSum += 1
            if eloSum == 0:
                return 'N/A'
            else:
                return str(round(eloSum/playerSum))

        messages_in_channel = await ctx.channel.history(limit=50).flatten()

        for message in messages_in_channel:
            x = message.embeds
            if x:
                if f'Match {matchId}' in x[0].title:  # if it has an embed
                    await message.delete()
                    break
        
        map = cursorm.execute("SELECT map FROM matches WHERE id = :trueId", {"trueId" : matchId}).fetchall()[0][0]
        matchEmbed = discord.Embed(title=f'FINISHED Match {matchId}', color=0x00ff00)
        matchEmbed.set_thumbnail(url=retrieveMapImg(map))
        matchEmbed.add_field(name="Team 1 Avg ELO", value=getAvgElo(1, matchId), inline=True)
        matchEmbed.add_field(name="Team 2 Avg ELO", value=getAvgElo(2, matchId), inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 1", value=
                                            "1: " + f'{formatRetrieval(1, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(2, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(3, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(4, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(5, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(1, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(2, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(3, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(4, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(5, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name="Team 2", value=
                                            "1: " + f'{formatRetrieval(6, matchId)}' + "\n" +
                                            "2: " + f'{formatRetrieval(7, matchId)}' + "\n" +
                                            "3: " + f'{formatRetrieval(8, matchId)}' + "\n" +
                                            "4: " + f'{formatRetrieval(9, matchId)}' + "\n" +
                                            "5: " + f'{formatRetrieval(10, matchId)}'
                                            , inline=True)
        matchEmbed.add_field(name="ELO", value=
                                            f"{getEloDB(retrieveIdFromPlayer(6, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(7, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(8, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(9, matchId))}" + "\n" +
                                            f"{getEloDB(retrieveIdFromPlayer(10, matchId))}" 
                                            , inline=True)
        matchEmbed.add_field(name="\u200B", value='\u200B', inline=True)
        matchEmbed.add_field(name ="Score", value=f'{scrm}', inline=False)
        await ctx.channel.send(embed=matchEmbed)
    else:
        cursorm.execute(f'UPDATE matches SET score = (?) WHERE id = {matchId}', [str(scrm)])
        cursorm.execute(f'UPDATE matches SET ongoing = 2 WHERE id = {matchId}')
        dbmatches.commit()
        await ctx.channel.send(f"Successfully updated match with id `{matchId}`.")

@forcereport.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Force report a match score",description="Updates the score of an old match or forcefully ends an ongoing match with the reported score in the argument.")
        em.add_field(name = "**Syntax**", value = "`,forcereport <match id> <score>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator to use. \n Has alias command named `freport`.", inline=False)
        await ctx.channel.send(embed=em) 

@client.command()
@commands.has_permissions(administrator=True)
async def clearmatches(ctx):
    await ctx.channel.send("Clearing unfinished matches. This may take a moment...")
    cur2 = dbmatches.cursor()
    for row in cur2.execute('SELECT id, score FROM matches' ):
        if str(row[1]) == 'None' and row[2] == 0:
            cursorm.execute('DELETE FROM matches WHERE id = :uniqueid', {"uniqueid" : int(row[0])})
    dbmatches.commit()
    await ctx.channel.send("Successfully cleared unfinished matches.")

@client.command()
@commands.has_permissions(administrator=True)
async def balance(ctx, k, *args):

    allowed_mentions = discord.AllowedMentions(users=False)

    eloList = []
    userList = []
    sortedTeamList = []
    error = False

    def namegenerator(page):
        i = 1
        st = ''
        for pid in sortedTeamList[page]:
            tag = cursor.execute(f'SELECT userid FROM main WHERE id={pid}').fetchall()[0][0]
            st = st + f'{str(i)}: ' + '<@' + f'{str(tag)}' + '>' + '\n'
            i += 1
        return st

    def elogenerator(page):
        st = ''
        for elo in teams[page]:
            st = st + str(elo) + '\n'
        return st

    for arguments in args:
        rawElo = cursor.execute(f'SELECT currentelo FROM main WHERE id={arguments}').fetchall()
        if len(rawElo) == 0:
            await ctx.channel.send(f"Could not find the ID `{arguments}` in the database.")
            error = True
            break
        else:
            eloList.append(int(rawElo[0][0]))
            userList.append((int(rawElo[0][0]), int(arguments)))
    if not error:
        teams = karmarkar_karp(eloList, int(k)).partition
        for team in teams:
            userTeam = []
            for playerElo in team:
                found = False
                if found:
                    continue
                for tup in userList:
                    if found:
                        continue
                    if playerElo == tup[0]:
                        userTeam.append(tup[1])
                        userList.remove(tup)
                        found = True

            sortedTeamList.append(userTeam)
        
        pages =  len(teams)
        cur_page = 1
        statEmbed = discord.Embed(color=0x37729c)
        statEmbed.set_author(name = f"Team {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
        statEmbed.add_field(name="Profile", value=namegenerator(cur_page-1), inline=True)
        statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
        message = await ctx.send(embed=statEmbed, allowed_mentions = allowed_mentions)
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    statEmbed = discord.Embed(color=0x37729c)
                    statEmbed.set_author(name = f"Team {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
                    statEmbed.add_field(name="Profile", value=namegenerator(cur_page-1), inline=True)
                    statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
                    await message.edit(embed=statEmbed, allowed_mentions = allowed_mentions)
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    statEmbed = discord.Embed(color=0x37729c)
                    statEmbed.set_author(name = f"Team {cur_page}/{pages}", icon_url='https://i.imgur.com/tHQpKw4.png')
                    statEmbed.add_field(name="Profile", value=namegenerator(cur_page-1), inline=True)
                    statEmbed.add_field(name="ELO", value=elogenerator(cur_page-1), inline=True)
                    await message.edit(embed=statEmbed, allowed_mentions = allowed_mentions)
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

@balance.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Balance",description="Uses the Karmarkar-Karp algorithm to balance players into `k` teams as specified from the argument.")
        em.add_field(name = "**Syntax**", value = "`,balance <k> <id1> <id2> ...`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Minimum partitions of 2. Minimum 4 ids. \n It is highly recommended to set `k` as `ceil(Number of players/5)` or `floor(Number of players/5)` to obtain optimal results.", inline=False)
        await ctx.channel.send(embed=em) 

@client.command()
@commands.has_permissions(administrator=True)
async def searchid(ctx, arg):
    lowerArg = arg.lower()
    name = cursor.execute(f"SELECT id FROM main WHERE name  = :args", {"args" : lowerArg}).fetchall()
    cleanArg = arg.replace("<","")
    cleanArg = cleanArg.replace(">","")
    cleanArg = cleanArg.replace("@","")
    uid = cursor.execute(f"SELECT id FROM main WHERE userid  = :args", {"args" : cleanArg}).fetchall()
    if len(name) != 0:
        await ctx.channel.send(f'The ID associated with `{arg}` is `{name[0][0]}`.')
    elif len(uid) != 0:
        await ctx.channel.send(f'The ID associated with `{arg}` is `{uid[0][0]}`.')
    else:
        await ctx.channel.send(f'Could not find user associated with the argument `{arg}`')

@searchid.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Search ID",description="Finds the ID associated with the argument.")
        em.add_field(name = "**Syntax**", value = "`,searchid <arg>`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n The argument can be the associated `FACEIT nickname` or `@user`.", inline=False)
        await ctx.channel.send(embed=em) 
                
@client.command(aliases=['frefreshall'])
@commands.has_permissions(administrator=True)
async def forcerefreshall(ctx):
    await ctx.channel.send("Refreshing every user's ELO in the database. This may take a moment...")
    cur2 = db.cursor()
    for row in cur2.execute('SELECT userid FROM main' ):
        cursor.execute('''UPDATE main SET currentelo = ? WHERE userid= ?''', (int(getElo(row[0])), row[0]))
    await ctx.channel.send("Successfully updated every user's ELO.")

@forcerefreshall.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title="Force Refresh All",description="Forcefully refreshes every linked user's ELO.")
        em.add_field(name = "**Syntax**", value = "`,forcerefreshall`", inline=False)
        em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use.", inline=False)
        await ctx.channel.send(embed=em)

@client.command()
@commands.dm_only()
async def link(ctx, name):
    link = False
    myid = cursor.execute("SELECT id FROM main WHERE userid = :authorid", {"authorid" : ctx.author.id}).fetchall()
    if "https://www.faceit.com/en/players/" in name:
        name = name.split('https://www.faceit.com/en/players/',1)[1]
        link = True
    if not link:
        await ctx.channel.send("You must send a FACEIT profile link!")
        return
    faceiturl = cursor.execute("SELECT name FROM main WHERE name = :thename", {"thename" : name.lower()})
    url = f'https://faceitstats.com/player/{name}'
    result = requests.get(url)
    doc = BeautifulSoup(result.content, "html.parser")
    check = doc.find_all("div", class_="alert alert-danger")
    maindata = str(doc.findAll('meta')[-1]).split("/")
    elo = int(maindata[1].split(' ', 2)[1])
    if len(myid) != 0:
        await ctx.channel.send("Your Discord is already linked!")
    elif len(faceiturl.fetchall()) != 0:
        await ctx.channel.send("The FACEIT profile is already linked!")
    elif "Could not find user" in str(check):
        await ctx.channel.send(f"Could not find user `{name}`. ")
    else:
        truelink = f"https://www.faceit.com/en/players/{name}"
        await ctx.channel.send("Successfully linked your Discord with your FACEIT.")
        cursor.execute("INSERT INTO main (faceit, userid, name, currentelo) VALUES (?, ?, ?, ?)", (truelink, ctx.author.id, name.lower(), elo))
        db.commit()

@link.error
async def missing_param(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title="Link",description="Links your Discord account to the FACEIT profile that is provided as an argument.")
        em.add_field(name = "**Syntax**", value = "`,link <FACEIT Profile Link>`", inline=False)
        em.add_field(name = "**Notes**", value = "Works only if the command is sent as a DM to the BOT.", inline=False)
        await ctx.channel.send(embed=em)

@client.command()
@commands.has_permissions(administrator=True)
async def unlinkid(ctx, theid):
    cursor.execute("DELETE FROM main WHERE id = :uniqueid", {"uniqueid" : theid})
    db.commit()
    await ctx.channel.send(f"Successfully removed the user with the id {theid} if they exist")

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help page",description="It is highly suggested to link your Discord profile with your FACEIT profile to gain access to all features. Type `,help link` for information on how to link your profile. Furthermore, use `,help <command>` for extra information on a specific command. ")
    em.add_field(name = "Administrator", value = "`,unlinkid`" + "\n" + "`,searchid`" +"\n" + "`,swisscreate`" + "\n" + "`,forcereport`" + "\n" + "`,forcerefresh`" + '\n' + "`,forcerefreshall`" + '\n' + '`,balance`' + '\n' + '`,searchid`', inline=False)
    em.add_field(name = "User", value = "`,search`" + "\n" + "`,link`" +"\n" + "`,unlink`" + "\n" + "`,leaderboard`" + "\n" + "`,refreshelo`" + "\n" + "`,creatematch`" + "\n" + "`,joinmatch`" + "\n" + "`,startmatch`" + "\n" + '`,last`', inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def link(ctx):
    em = discord.Embed(title="Link",description="Links your Discord account to the FACEIT profile that is provided as an argument.")
    em.add_field(name = "**Syntax**", value = "`,link <FACEIT Profile Link>`", inline=False)
    em.add_field(name = "**Notes**", value = "Works only if the command is sent as a DM to the BOT.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def forcerefresh(ctx):
    em = discord.Embed(title="Force Refresh",description="Forcefully refreshes a user's ELO.")
    em.add_field(name = "**Syntax**", value = "`,forcerefresh <id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Has alias command named `frefresh`", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def forcerefreshall(ctx):
    em = discord.Embed(title="Force Refresh All",description="Forcefully refreshes every linked user's ELO.")
    em.add_field(name = "**Syntax**", value = "`,forcerefreshall`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Has alias command named `frefreshall`.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def myid(ctx):
    em = discord.Embed(title="My ID",description="Displays your personal ID assigned by the BOT after linking your FACEIT account.")
    em.add_field(name = "**Syntax**", value = "`,myid`", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def unlink(ctx):
    em = discord.Embed(title="Unlink",description="Unlinks your Discord account to the currently linked FACEIT profile if exists in the database.")
    em.add_field(name = "**Syntax**", value = "`,unlink`", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def unlinkid(ctx):
    em = discord.Embed(title="Unlink ID",description="Unlinks the FACEIT account that is associated with the ID given in the argument.")
    em.add_field(name = "**Syntax**", value = "`,unlinkid <id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def search(ctx):
    em = discord.Embed(title="Search",description="Displays FACEIT information about a specific user.")
    em.add_field(name = "**Syntax**", value = "`,search <name>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `lookup`, `find`, and `stats`. Displays the linked FACEIT account if no parameter is given.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def lookup(ctx):
    em = discord.Embed(title="Search",description="Displays FACEIT information about a specific user.")
    em.add_field(name = "**Syntax**", value = "`,search <name>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `lookup`, `find`, and `stats`. Displays the linked FACEIT account if no parameter is given.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def refreshelo(ctx):
    em = discord.Embed(title="Refresh ELO",description="Refreshes the ELO stored in the database using your live FACEIT information.")
    em.add_field(name = "**Syntax**", value = "`,refreshelo`", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def joinmatch(ctx):
    em = discord.Embed(title="Join match",description="Joins a match that was created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,joinmatch <match id> <team number>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `join` and `matchjoin`.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def join(ctx):
    em = discord.Embed(title="Join match",description="Joins a match that was created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,joinmatch <match id> <team number>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `join` and `matchjoin`.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def matchjoin(ctx):
    em = discord.Embed(title="Join match",description="Joins a match that was created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,joinmatch <match id> <team number>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `join` and `matchjoin`.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def creatematch(ctx):
    em = discord.Embed(title="Create match",description="Creates a match with two teams. Creator is automatically in Team 1.")
    em.add_field(name = "**Syntax**", value = "`,creatematch <map>", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Has alias commands named `create` and `matchcreate`.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def find(ctx):
    em = discord.Embed(title="Search",description="Displays FACEIT information about a specific user.")
    em.add_field(name = "**Syntax**", value = "`,search <name>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `lookup`, `find`, and `stats`. Displays the linked FACEIT account if no parameter is given.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def stats(ctx):
    em = discord.Embed(title="Search",description="Displays FACEIT information about a specific user.")
    em.add_field(name = "**Syntax**", value = "`,search <name>`", inline=False)
    em.add_field(name = "**Notes**", value = "Has alias commands named `lookup`, `find`, and `stats`. Displays the linked FACEIT account if no parameter is given.", inline=False)
    await ctx.channel.send(embed=em)

@help.command()
async def balance(ctx):
    em = discord.Embed(title="Balance",description="Uses the Karmarkar-Karp algorithm to balance players into `k` teams as specified from the argument.")
    em.add_field(name = "**Syntax**", value = "`,balance <k> <id1> <id2> ...`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n Minimum partitions of 2. Minimum 4 ids. \n It is highly recommended to set `k` as `ceil(Number of players/5)` and let the incomplete team members be subs for optimal results. \n Currently, this command can be optimised if it was to use a balanced multi-way partitioning algorithm. Unfortunately, my ability to implement such an algorithm falls short. http://www.mysmu.edu/faculty/kyriakos/IJCAI11.pdf", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def searchid(ctx):
    em = discord.Embed(title="Search ID",description="Finds the database ID associated with the argument.")
    em.add_field(name = "**Syntax**", value = "`,searchid <arg>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use. \n The argument can be the associated `FACEIT nickname` or `@user`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def startmatch(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def start(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def matchstart(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 
    
@help.command()
async def begin(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def beginmatch(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires team captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def matchbegin(ctx):
    em = discord.Embed(title="Start Match",description="Starts a match created using `,creatematch`")
    em.add_field(name = "**Syntax**", value = "`,startmatch <match id>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires eam captain permissions to use. \n Has alias commands named `start`, `matchstart`, `begin`,`beginmatch` and `matchbegin`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def clearmatches(ctx):
    em = discord.Embed(title="Clear Matches",description="Clears created matches that were created using `,creatematch` and deletes them if score is not reported.")
    em.add_field(name = "**Syntax**", value = "`,clearmatch`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator permissions to use", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def forcereport(ctx):
    em = discord.Embed(title="Force report a match score",description="Updates or forcefully ends an ongoing match with the reported score in the argument.")
    em.add_field(name = "**Syntax**", value = "`,forcereport <match id> <score>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator to use. \n Has alias command named `freport`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def reportmatch(ctx):
    em = discord.Embed(title="Report a match score",description="Finishes an ongoing match with the reported score.")
    em.add_field(name = "**Syntax**", value = "`,report <match id> <score>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator to use. \n Has alias command named `report`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def report(ctx):
    em = discord.Embed(title="Report a match score",description="Finishes an ongoing match with the reported score.")
    em.add_field(name = "**Syntax**", value = "`,report <match id> <score>`", inline=False)
    em.add_field(name = "**Notes**", value = "Requires Administrator to use. \n Has alias command named `report`.", inline=False)
    await ctx.channel.send(embed=em) 

@help.command()
async def last(ctx):
    em = discord.Embed(title="Retrieve last X match statistics",description="Retrieves last X matches and calculates statistics such as K/D, K/R, etc.")
    em.add_field(name = "**Syntax**", value = "`,last <number of matches> <player>`", inline=False)
    em.add_field(name = "**Notes**", value = "`<number of matches>` has to be between `5` and `25` inclusive. \n True statistics are calculated by using kills, deaths, etc. in the matches, whereas regular is an average of K/Ds in matches.", inline=False)
    await ctx.channel.send(embed=em) 
client.run(TOKEN)
