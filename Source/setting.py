import discord, json, os, datetime, pytz, youtubesearchpython, yt_dlp, time
from datetime import datetime
from discord import app_commands, Interaction, Embed, ButtonStyle, Member, Message, VoiceClient, VoiceChannel, Guild, TextChannel, FFmpegPCMAudio, SelectOption
from discord.abc import GuildChannel
from discord.ext import commands
from discord.ui import Button, View, button
from discord.utils import get
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

bot_name = '231105-00' #디렉터리명
prefix = 'Prefix' #접두사
vc_json_path = rf'/root/BYEOLKI/{bot_name}/vc_data/vc.json' #vc.json 경로
setup_json_path = fr'/root/BYEOLKI/{bot_name}/setup_data/setup.json' #setup.json 경로
TOKEN = 'Token' #토큰

Pink_music_emoji = 'Pink_music_emoji ' 
delete_music_emoji = 'delete_music_emoji ' 
previous_arrow_emoji = 'previous_arrow '
next_arrow_emoji = 'next_arrow '
resume_emoji = 'resume ' 
pause_emoji = 'pause ' 
playlist_add_emoji = 'playlist_add ' 
playlist_show_emoji = 'playlist_show ' 
previous_music_emoji = 'previous_music ' 
skip_music_emoji = 'skip_music ' 
stop_music_emoji = 'stop_music '
XX_emoji = 'XX ' 
OO_emoji = 'OO '
main_embed_image = 'main_embed_image'