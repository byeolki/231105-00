from setting import *
from vc_data.vc_data import VC_Data
from setup_data.setup_data import Setup_Data

async def setup(bot: commands.Bot):
    await bot.add_cog(VC(bot))
    await bot.add_cog(Music(bot))
    for guild in bot.guilds:
        setup_data = Setup_Data(guild)
        if setup_data.check_setup():
            ch_id, msg_id = setup_data.get_setup()
            ch = guild.get_channel(ch_id)
            msg = await ch.fetch_message(msg_id)
            embed = Embed(title='현재 재생중인 곡이 없어요!', description='해당 채팅방에 원하는 곡의 제목 또는 URL을 입력해주세요!', color=0xffbac7)
            embed.set_image(url=main_embed_image)
            await msg.edit(embed=embed, view=Music_Control(bot, True, guild))

global guilds
guilds = {}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 3",
    "options": "-vn -b:a 320k",
}
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "89.116.231.104",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

def search(query: str):
    result = VideosSearch(query, 1).result()['result'][0]
    return result['title'], 'https://www.youtube.com/watch?v='+result['id'], result['viewCount']['text'].split()[0], result['thumbnails'][-1]['url'], result['duration'], result['channel']['name']

def ydl_url(url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['url']
    return URL

def embed_generator(guild: Guild) -> Embed:
    embed = Embed(description=f'{Pink_music_emoji}**[{guilds[guild.id]["NowPlaying"]["title"]}]({guilds[guild.id]["NowPlaying"]["url"]})**', color=0xffbac7)
    embed.set_author(name=guilds[guild.id]['NowPlaying']['user'].display_name, icon_url=guilds[guild.id]['NowPlaying']['user'].display_avatar.url)
    embed.add_field(name='시간', value=f'`{guilds[guild.id]["NowPlaying"]["duration"]}`')
    embed.add_field(name='조회수', value=f'`{guilds[guild.id]["NowPlaying"]["view_count"]}`')
    embed.add_field(name='업로더', value=f'`{guilds[guild.id]["NowPlaying"]["uploader"]}`')
    embed.add_field(name='예약된 곡', value=f'`{len(guilds[guild.id]["Queue"])}`')
    embed.add_field(name='음성채널', value=f'<#{guilds[guild.id]["VoiceClient"].channel.id}>')
    embed.add_field(name='일시정지', value=f'{OO_emoji if guilds[guild.id]["VoiceClient"].is_paused() else XX_emoji}')
    embed.set_image(url=guilds[guild.id]['NowPlaying']['thumbnail'])
    return embed

def next_play(self, message: Message):
    time.sleep(3)
    if message.guild.id not in guilds:
        return
    if 'Skip' not in guilds[message.guild.id]:
        if guilds[message.guild.id]['Loop_Mode'] == 0:
            if not guilds[message.guild.id]['Queue']:
                self.bot.loop.create_task(guilds[message.guild.id]['VoiceClient'].disconnect())
            else:
                URL = ydl_url(guilds[message.guild.id]['Queue'][0]['url'])
                guilds[message.guild.id]['Previous_Queue'].append(guilds[message.guild.id]['NowPlaying'])
                guilds[message.guild.id]['NowPlaying'] = guilds[message.guild.id]['Queue'][0]
                guilds[message.guild.id]['Queue'] = guilds[message.guild.id]['Queue'][1:]
                guilds[message.guild.id]['VoiceClient'].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: next_play(self, message))
                async def edit(bot: commands.Bot, guild: Guild):
                    setup_data = Setup_Data(guild)
                    embed = embed_generator(guild)
                    channel_id, message_id = setup_data.get_setup()
                    channel = bot.get_channel(channel_id)
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed)
                self.bot.loop.create_task(edit(self.bot, message.guild))
        elif guilds[message.guild.id]['Loop_Mode'] == 1:
            URL = ydl_url(guilds[message.guild.id]['NowPlaying']['url'])
            guilds[message.guild.id]['VoiceClient'].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: next_play(self, message))
        if guilds[message.guild.id]['Loop_Mode'] == 2:
            if not guilds[message.guild.id]['Queue']:
                self.bot.loop.create_task(guilds[message.guild.id]['VoiceClient'].disconnect())
            else:
                URL = ydl_url(guilds[message.guild.id]['Queue'][0]['url'])
                guilds[message.guild.id]['NowPlaying'] = guilds[message.guild.id]['Queue'][0]
                guilds[message.guild.id]['Queue'] = guilds[message.guild.id]['Queue'][1:]
                guilds[message.guild.id]['Queue'].append(guilds[message.guild.id]['NowPlaying'])
                guilds[message.guild.id]['VoiceClient'].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: next_play(self, message))
                async def edit(bot: commands.Bot, guild: Guild):
                    setup_data = Setup_Data(guild)
                    embed = embed_generator(guild)
                    channel_id, message_id = setup_data.get_setup()
                    channel = bot.get_channel(channel_id)
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed)
                self.bot.loop.create_task(edit(self.bot, message.guild))
    else:
        del guilds[message.guild.id]['Skip']

class VC(commands.GroupCog, name='음성채널'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name = "지정", description = "[ 관리자 전용 ] 생성형 음성 채널을 생성합니다.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.rename(name='이름')
    @app_commands.describe(name='생성형 음성 채널의 이름을 입력해주세요.')
    async def create_vc_command_(self, inter: Interaction, name: str):
        vc_data = VC_Data()
        channel = await inter.guild.create_voice_channel(name=name, category=inter.channel.category)
        vc_data.create_vc(channel)
        await inter.response.send_message(embed=Embed(title='음성 채널이 지정되었어요!', description='채널 권한은 마음대로 변경하셔도 좋아요!', color=0xffbac7, timestamp=datetime.now(pytz.timezone('Asia/Seoul'))))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceClient, after: VoiceClient):
        vc_data = VC_Data()
        setup_data = Setup_Data(member.guild)
        if after.channel and after.channel.id in [int(ch) for ch, t in vc_data.get_vc().items()]:
            channel = await after.channel.guild.create_voice_channel(name=f'{member.display_name}님의 채널', category=after.channel.category)
            vc_data.add_vc(after.channel, channel)
            await member.move_to(channel)
        elif before.channel and vc_data.check_temp_vc(before.channel) and vc_data.del_vc(before.channel):
            await before.channel.delete()


class Music(commands.GroupCog, name='음악채널'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name = "지정", description = "[ 관리자 전용 ] 셋텁 음악 채널을 생성합니다.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.rename(name='이름')
    @app_commands.describe(name='셋텁 음악 채널의 이름을 입력해주세요.')
    async def create_setup_command_(self, inter: Interaction, name: str):
        setup_data = Setup_Data(inter.guild)
        if not setup_data.check_setup():
            channel = await inter.guild.create_text_channel(name=name, category=inter.channel.category)
            await inter.response.send_message(embed=Embed(title='셋텁 채널이 지정되었어요!', description='채널 권한은 마음대로 변경하셔도 좋아요!', color=0xffbac7, timestamp=datetime.now(pytz.timezone('Asia/Seoul'))))
            embed = Embed(title='현재 재생중인 곡이 없어요!', description='해당 채팅방에 원하는 곡의 제목 또는 URL을 입력해주세요!', color=0xffbac7)
            embed.set_image(url=main_embed_image)
            message = await channel.send(embed=embed, view=Music_Control(self.bot, True, inter.guild))
            setup_data.create_setup(channel, message)
        else: await inter.response.send_message(embed=Embed(title='현재 지정된 셋텁 채널이 있어요!', description='해당 셋텁 채널을 삭제하여 주세요!', color=0xffbac7, timestamp=datetime.now(pytz.timezone('Asia/Seoul'))))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        setup_data = Setup_Data(channel.guild)
        if setup_data.check_setup() and setup_data.get_setup()[0] == channel.id:
            setup_data.del_setup()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        setup_data = Setup_Data(message.guild)
        if setup_data.check_setup() and setup_data.get_setup()[0] == message.channel.id:
            await message.delete()
            try: t = message.author.voice.channel.id
            except: return await message.channel.send('음성 채널에 입장하여 주세요!', delete_after=5)
            try: guilds[message.guild.id] = {
                    'VoiceClient':await message.author.voice.channel.connect(self_deaf=True),
                    'NowPlaying':{},
                    'Queue':[],
                    'Previous_Queue':[],
                    'Loop_Mode':0
                }
            except: 
                try: pass
                except: return await message.channel.send('음성 채널에 입장하여 주세요!', delete_after=5)
            if t != guilds[message.guild.id]['VoiceClient'].channel.id:
                return await message.channel.send('봇과 동일한 음성 채널에 입장하여 주세요!', delete_after=5)
            try: title, url, view_count, thumbnail, duration, uploader =  search(message.content)
            except Exception as e: return await message.channel.send('검색에 실패하였어요! 다시 한번 입력해주세요!', delete_after=5)
            video_data = {'title':title, 'url':url, 'view_count':view_count, 'thumbnail':thumbnail, 'duration':duration, 'uploader':uploader, 'user':message.author}
            if not guilds[message.guild.id]['VoiceClient'].is_playing():
                guilds[message.guild.id]['NowPlaying'] = video_data
                embed = embed_generator(message.guild)
                URL = ydl_url(url)
                guilds[message.guild.id]['VoiceClient'].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: next_play(self, message))
                channel_id, message_id = setup_data.get_setup()
                channel = self.bot.get_channel(channel_id)
                msg = await channel.fetch_message(message_id)
                await msg.edit(embed=embed, view=Music_Control(self.bot, False, message.guild))
            else:
                guilds[message.guild.id]['Queue'].append(video_data)
                embed = Embed(description=f'{Pink_music_emoji}**[{video_data["title"]}]({video_data["url"]})**', color=0xffbac7)
                embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
                embed.set_footer(text=f'{len(guilds[message.guild.id]["Queue"])}개의 음악이 다 재생되면 실행돼요!')
                await message.channel.send(embed=embed, delete_after=10)
                channel_id, message_id = setup_data.get_setup()
                channel = self.bot.get_channel(channel_id)
                msg = await channel.fetch_message(message_id)
                await msg.edit(embed=embed_generator(message.guild))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceClient, after: VoiceClient):
        setup_data = Setup_Data(member.guild)
        if before.channel and not after.channel and member.id == self.bot.user.id:
            del guilds[member.guild.id]
            channel_id, message_id = setup_data.get_setup()
            channel = self.bot.get_channel(channel_id)
            msg = await channel.fetch_message(message_id)
            embed = Embed(title='현재 재생중인 곡이 없어요!', description='해당 채팅방에 원하는 곡의 제목 또는 URL을 입력해주세요!', color=0xffbac7)
            embed.set_image(url=main_embed_image)
            await msg.edit(embed=embed, view=Music_Control(self.bot, True, member.guild))
        elif before.channel and len(before.channel.members) == 1 and self.bot.user.id in [user.id for user in before.channel.members]:
            await guilds[member.guild.id]['VoiceClient'].disconnect()

class Music_Control(View):
    def __init__(self, bot: commands.Bot, disabled: bool, guild: Guild):
        self.bot = bot
        super().__init__(timeout=None)
        for child in self.children:
            child.disabled = disabled
        self.add_item(Loop_Mode(bot, guild, disabled))
    
    @button(style = discord.ButtonStyle.gray, emoji=playlist_show_emoji, custom_id='playlist_show')
    async def playlist_show(self, inter: Interaction, button: Button):
        description = []
        count = 1
        for music in guilds[inter.guild.id]['Queue'][:10]:
            description.append(f'1. **[{music["title"]}]({music["url"]})**')
            count += 1
        embed = Embed(title='재생목록을 불러왔어요!', description='\n'.join(description), color=0xffbac7)
        await inter.response.send_message(embed=embed, view=Queue_Control(self.bot), ephemeral=True)

    @button(style = discord.ButtonStyle.gray, emoji=previous_music_emoji, custom_id='previous_music')
    async def previous_music(self, inter: Interaction, button: Button):
        if guilds[inter.guild.id]['Previous_Queue']:
            await inter.response.defer()
            guilds[inter.guild.id]['Queue'].append(guilds[inter.guild.id]['NowPlaying'])
            guilds[inter.guild.id]['NowPlaying'] = guilds[inter.guild.id]['Previous_Queue'][-1]
            print(guilds[inter.guild.id]['NowPlaying']); print(guilds[inter.guild.id]['Queue']); print(guilds[inter.guild.id]['Previous_Queue'])
            URL = ydl_url(guilds[inter.guild.id]['NowPlaying']['url'])
            guilds[inter.guild.id]['Skip'] = True
            guilds[inter.guild.id]['VoiceClient'].stop()
            guilds[inter.guild.id]['VoiceClient'].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after = lambda e: next_play(self, inter.message))
            await inter.edit_original_response(embed=embed_generator(inter.guild))
        else: await inter.response.send_message(f'이전에 재생했던 음악이 없어요!', ephemeral=True)

    @button(style = discord.ButtonStyle.gray, emoji=pause_emoji, custom_id='play_pause')
    async def play_pause(self, inter: Interaction, button: Button):
        await inter.response.defer()
        guilds[inter.guild.id]['VoiceClient'].resume() if guilds[inter.guild.id]['VoiceClient'].is_paused() else guilds[inter.guild.id]['VoiceClient'].pause()
        button.emoji = resume_emoji if guilds[inter.guild.id]["VoiceClient"].is_paused() else pause_emoji
        await inter.edit_original_response(embed=embed_generator(inter.guild), view=self)

    @button(style = discord.ButtonStyle.gray, emoji=skip_music_emoji, custom_id='skip_music')
    async def skip_music(self, inter: Interaction, button: Button):
        if guilds[inter.guild.id]['Queue'] or guilds[inter.guild.id]['Loop_Mode'] != 0:
            await inter.response.defer()
            guilds[inter.guild.id]['VoiceClient'].stop()
            await inter.edit_original_response(embed=embed_generator(inter.guild))
        else: await inter.response.send_message('다음 음악이 존재하지 않아요!', ephemeral=True)

    @button(style = discord.ButtonStyle.red, emoji=stop_music_emoji, custom_id='stop_music')
    async def stop_music(self, inter: Interaction, button: Button):
        await inter.response.defer()
        await guilds[inter.guild.id]['VoiceClient'].disconnect()

class Queue_Control(View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=None)

    @button(style = discord.ButtonStyle.blurple, emoji=previous_arrow_emoji, custom_id='arrow 0')
    async def left_arrow(self, inter: Interaction, button: Button):
        number = int(button.custom_id.split()[-1])
        if number == 0:
            await inter.response.send_message('더 이상 불러올 재생목록이 없어요!', ephemeral=True)
        else:
            await inter.response.defer(ephemeral=True)
            description = []
            count = 1
            for music in guilds[inter.guild.id]['Queue'][(10*(number-1)):(10*(number))]:
                description.append(f'1. **[{music["title"]}]({music["url"]})**')
                count += 1
            embed = Embed(title='재생목록을 불러왔어요!', description='\n'.join(description), color=0xffbac7)
            button.custom_id = f'arrow {number-1}'
            self.delete_music.custom_id = f'delete_music {number}'
            self.right_arrow.custom_id = f'arrow {number+1}'
            await inter.edit_original_response(embed=embed, view=self)
    
    @button(style = discord.ButtonStyle.blurple, emoji=delete_music_emoji, custom_id='delete_music 1')
    async def delete_music(self, inter: Interaction, button: Button):
        number = int(button.custom_id.split()[-1])
        await inter.response.send_modal(Delete_Music(guilds[inter.guild.id]['Queue'][(10*(number-1)):(10*(number)+1)], number-1))

    @button(style = discord.ButtonStyle.blurple, emoji=next_arrow_emoji, custom_id='arrow 2')
    async def right_arrow(self, inter: Interaction, button: Button):
        number = int(button.custom_id.split()[-1])
        if 10*(number-1) >= len(guilds[inter.guild.id]['Queue']):
            await inter.response.send_message('더 이상 불러올 재생목록이 없어요!', ephemeral=True)
        else:
            await inter.response.defer(ephemeral=True)
            description = []
            count = 1
            for music in guilds[inter.guild.id]['Queue'][(10*(number-1)):(10*(number)+1)]:
                description.append(f'1. **[{music["title"]}]({music["url"]})**')
                count += 1
            embed = Embed(title='재생목록을 불러왔어요!', description='\n'.join(description), color=0xffbac7)
            button.custom_id = f'arrow {number+1}'
            self.delete_music.custom_id = f'delete_music {number}'
            self.left_arrow.custom_id = f'arrow {number-1}'
            await inter.edit_original_response(embed=embed, view=self)

class Delete_Music(discord.ui.Modal):
    index = discord.ui.TextInput(label='번호', placeholder='불러온 재생목록에서 지우고 싶은 음악의 번호를 입력하여주세요!')
    def __init__(self, temp_queue: list, number: int) -> None:
        self.queue = temp_queue
        self.number = number
        super().__init__(title='재생목록에서 음악 제거', timeout=None, custom_id='Delete_Music')

    async def on_submit(self, inter: Interaction) -> None:
        setup_data = Setup_Data(inter.guild)
        try: index = int(self.children[0].value) - 1
        except: return await inter.response.send_message('노래에 매겨진 숫자를 입력해주세요!', ephemeral=True)
        if index in [_ for _ in range(0, 10)]:
            await inter.response.defer(ephemeral=True)
            del self.queue[index]
            del guilds[inter.guild.id]['Queue'][self.number*10+index]
            description = []
            count = 1
            for music in self.queue:
                description.append(f'1. **[{music["title"]}]({music["url"]})**')
                count += 1
            embed = Embed(title='재생목록을 불러왔어요!', description='\n'.join(description), color=0xffbac7)
            await inter.edit_original_response(embed=embed) if self.queue else await inter.edit_original_response('재생목록에 음악이 없어요!', embed=None)
            await inter.followup.send('노래를 성공적으로 제거하였어요!', ephemeral=True)
            await inter.followup.edit_message(setup_data.get_setup()[1], embed=embed_generator(inter.guild))
        else: await inter.response.send_message('노래에 매겨진 숫자를 입력해주세요!', ephemeral=True)

class Loop_Mode(discord.ui.Select):
    def __init__(self, bot: discord.Client, guild: Guild, disabled: bool):
        self.bot = bot
        options = []
        if guild.id in guilds:
            if guilds[guild.id]['Loop_Mode'] != 0: options.append(SelectOption(label = '반복 해제', value = 0, description='반복 모드를 해제합니다'))
            if guilds[guild.id]['Loop_Mode'] != 1: options.append(SelectOption(label = '1곡 반복', value = 1, description='재생중인 음악을 계속 반복 재생합니다'))
            if guilds[guild.id]['Loop_Mode'] != 2: options.append(SelectOption(label = '재생목록 반복', value = 2, description='대기열에 있는 음악을 반복 재생합니다'))
            super().__init__(placeholder=f'현재 반복 모드: {"반복 안 함" if guilds[guild.id]["Loop_Mode"] == 0 else "1곡 반복" if guilds[guild.id]["Loop_Mode"] == 1 else "재생목록 반복"}',
                            min_values=1, max_values=1, options=options, disabled=disabled)
        else:
            options.append(SelectOption(label = '?', value = 0, description='?')) 
            super().__init__(placeholder=f'음악을 먼저 재생해주세요!', min_values=1, max_values=1, options=options, disabled=disabled)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        mode = int(self.values[0])
        if mode == 2 and not guilds[inter.guild.id]['Queue']: return await inter.followup.send('대기열에 음악이 없어요!', ephemeral=True)
        elif mode == 2: guilds[inter.guild.id]['PreviousQueue'] = []
        guilds[inter.guild.id]['Loop_Mode'] = mode
        await inter.edit_original_response(view=Music_Control(self.bot, False, inter.guild))
        await inter.followup.send(f'반복 모드를 {"반복 안 함" if guilds[inter.guild.id]["Loop_Mode"] == 0 else "1곡 반복" if guilds[inter.guild.id]["Loop_Mode"] == 1 else "재생목록 반복"}으로 변경했어요!', ephemeral=True)