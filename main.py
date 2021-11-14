import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import os

import random,time,asyncio
import datetime
bot = commands.Bot(command_prefix="uc_",activity=discord.Game("uc_help"))
bot.remove_command('help')
token = os.environ['DISCORD_BOT_TOKEN']
matti_data = {}




UC = {}

@bot.event
async def on_ready():
    print('Botを起動しました。')
    while True:
        global UC
        # 現在の時刻
        now = datetime.datetime.now()
        dt = now + datetime.timedelta(minutes=1,seconds=4)#.strftime('%H:%M')
        dt2 = str(dt)[11:]
        target = '.'
        idx = dt2.find(target)
        dt3 = dt2[:idx-3]

        dt_ = now - datetime.timedelta(seconds=35)#.strftime('%H:%M')
        dt_2 = str(dt_)[11:]
        target = '.'
        idx = dt_2.find(target)
        dt_3 = dt_2[:idx-3]

        print(dt3)
        #print(dt_3)
        print(UC.keys())


        if dt3 in UC:
            print("スタート")
            await uc_start(dt3)
        if dt_3 in UC:
            print("スタート2")
            await uc_leave(dt_3)
        #await client.send_message(channel, 'おはよう')
        await asyncio.sleep(2)

@bot.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return
    await bot.process_commands(message)

'''

@bot.command(aliases=["connect","come"]) #connectやsummonでも呼び出せる
async def join(ctx):
    """Botをボイスチャンネルに入室させます。"""
    voice_state = ctx.author.voice

    if (not voice_state) or (not voice_state.channel):
        await ctx.send("先にボイスチャンネルに入っている必要があります。")
        return

    channel = voice_state.channel

    await channel.connect()
    print("connected to:",channel.name)


@bot.command(aliases=["disconnect","bye"])
async def leave(ctx):
    """Botをボイスチャンネルから切断します。"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
        return

    await voice_client.disconnect()
    await ctx.send("ボイスチャンネルから切断しました。")

'''

@bot.command()
async def timer(ctx,time : str):
    """UC"""
    global UC
    #voice_client = ctx.message.guild.voice_client
    time_list=time.split(':')
    time_h = time_list[0]
    time_m = time_list[1]
    if time_h+":"+str(time_m) in UC:
        print("append")
        VC = UC[time_h+":"+time_m]
        VC.append(ctx)
        UC[time_h+":"+time_m] = VC
    if time_h+":"+time_m not in UC:
        print("追加")
        UC = {time_h+":"+time_m:[ctx]}
    await ctx.send(time_h+":"+time_m+"に設定しました。指定時間の3分前までにVCに参加していてください。")

@bot.command()
async def help(ctx):
    """コマンドの説明などを表示します"""
    embed = discord.Embed(title="UC timer Help",description="UC timerの使い方",color=discord.Colour.dark_green())
    #embed.add_field(name="uc_join",value="Botをボイスチャンネルに入室させます。(uc_connect,uc_comeでも使えます)")
    #embed.add_field(name="uc_leave",value="Botをボイスチャンネルから切断します。(uc_disconnect,uc_byeでも使えます)")
    embed.add_field(name="uc_timer",value="時間を設定します。(例: uc_timer 21:30)")
    embed.add_field(name="uc_timer の注意点",value="AM1時やAM9時などの一桁の時間の場合は01:00や09:00のように「0」を追加してください。")
    embed.add_field(name="使い方の流れ",value="タイマーセット後、指定時間になると参加者のいるVCに自動的に入り、再生されます。その後自動でVCから退出します。")
    embed.add_field(name="使い方の注意",value="指定時間の3分前までに参加されたVCが確認できない場合はキャンセルされます。")
    await ctx.send(embed=embed)

@bot.event
async def uc_leave(dt_3):
    global UC
    VC = UC[dt_3]
    for ctx in VC:
        await asyncio.create_task(uc_leave_vc(ctx))
    del UC[dt_3]
    print("uc_leave")

@bot.event
async def uc_leave_vc(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if not voice_client:
            #await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
            return

        await voice_client.disconnect()
    except:
        pass

@bot.event
async def uc_start(dt3):
    global UC
    VC = UC[dt3]
    for ctx in VC:
        await asyncio.create_task(uc_start_vc(ctx))

        #await ctx.send("ボイスチャンネルから切断しました。")

@bot.event
async def uc_start_vc(ctx):
    try:
        ffmpeg_audio_source = discord.FFmpegPCMAudio("UC.wav")
        voice_state = ctx.author.voice
        if (not voice_state) or (not voice_state.channel):
            #await ctx.send("ボイスチャンネルに入っているメンバーがいなかったためキャンセルされました")
            return

        channel = voice_state.channel
        await channel.connect()
        print("connected to:",channel.name)

        voice_client = ctx.message.guild.voice_client
        voice_client.play(ffmpeg_audio_source)
        print("UC")
    except:
        pass


bot.run(token)
