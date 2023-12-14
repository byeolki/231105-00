from setting import *

async def setup(bot: commands.Bot):
    await bot.add_cog(User_Manage(bot))

class User_Manage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @app_commands.command(name = "프로필", description = "[ 관리자 전용 ] 해당 채널에 프로필 입력 메세지를 생성합니다.")
    @app_commands.default_permissions(administrator=True)
    async def create_profile_command_(self, inter: Interaction):
        title = "<a:I_08:1169117865065070623>버튼을 클릭하고 프로필을 작성해 주세요<a:I_09:1169117870144364594>"
        description = f"""
<:I_00:1169064194591707136>{'<:I_01:1169064197502545941>'*12}<:I_02:1169064192863633419>
<:E_00:1119151498199322715><:E_00:1119151498199322715><:E_00:1119151498199322715><:E_00:1119151498199322715><a:F_01:1169067331008352347><:E_00:1119151498199322715><:I_12:1160631106475917342><:I_13:1160630420178731039><:I_14:1160630421961318511><:E_00:1119151498199322715><a:F_01:1169067331008352347>

> 서버에서 활동하시려면
<:E_00:1119151498199322715>아래 프로필을 작성해 주세요！

<:D_02:1119153793846743093>입력하지 않아도 괜찮아요

> 프로필을 작성해주시면 서버가 활성화 돼요！

> <:H_02:928331929575620638> 역할이 없으면 안보이는 채널이 많아요 <:H_03:928331938643726447>
<:E_00:1119151498199322715>프로필을 작성하고 역할을 받아 가세요！

<:I_00:1169064194591707136>{'<:I_01:1169064197502545941>'*12}<:I_02:1169064192863633419>
"""
        embed = Embed(title=title, description=description, color=0xffd5dc)
        button = Button(style=ButtonStyle.grey, label='시작하기', custom_id='cmc 0')
        view = View(timeout=None); view.add_item(button)
        message = await inter.channel.send(embed=embed, view=view)
        await inter.response.send_message(f'메세지를 성공적으로 생성했어요! https://ptb.discord.com/channels/{inter.guild_id}/{inter.channel_id}/{message.id}', ephemeral=True)

    @app_commands.command(name = "인증", description = "[ 관리자 전용 ] 해당 채널에 인증 메세지를 생성합니다.")
    @app_commands.default_permissions(administrator=True)
    async def create_cerfication_command_(self, inter: Interaction):
        title = "<a:I_08:1169117865065070623>버튼을 클릭하고 인증을 진행해 주세요<a:I_09:1169117870144364594>"
        description = f"""
<:I_00:1169064194591707136>{'<:I_01:1169064197502545941>'*12}<:I_02:1169064192863633419>
<:E_00:1119151498199322715><:E_00:1119151498199322715><:E_00:1119151498199322715><:E_00:1119151498199322715><a:F_01:1169067331008352347><:E_00:1119151498199322715><:I_12:1160631106475917342><:I_13:1160630420178731039><:I_14:1160630421961318511><:E_00:1119151498199322715><a:F_01:1169067331008352347>

> 서버전용 역할인<a:I_10:1169117883062833172>멤버<a:I_11:1169117887852728366> 역할을 받으시려면
<:E_00:1119151498199322715>아래 인증을 시작해 주세요！ 

<:D_02:1119153793846743093>입력하지 않아도 괜찮아요

> 인증 전용 역할인<a:I_10:1169117883062833172>멤버<a:I_11:1169117887852728366> 역할을 받으시면
<:E_00:1119151498199322715>다른 유저들과 차별화 된 기능을 사용할 수 있어요！

> <:H_02:928331929575620638> 서버의 모든 기능을 활성화 시킬 수 있어요 <:H_03:928331938643726447>
<:E_00:1119151498199322715>인증을 완료하고 모든 기능을 활성화 시키세요！

<:I_00:1169064194591707136>{'<:I_01:1169064197502545941>'*12}<:I_02:1169064192863633419>
"""
        embed = Embed(title=title, description=description, color=0xffd5dc)
        button = Button(style=ButtonStyle.grey, label='인증하기', custom_id='cmc 1')
        view = View(timeout=None); view.add_item(button)
        message = await inter.channel.send(embed=embed, view=view)
        await inter.response.send_message(f'메세지를 성공적으로 생성했어요! https://ptb.discord.com/channels/{inter.guild_id}/{inter.channel_id}/{message.id}', ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, inter: Interaction):
        if str(inter.type) == "InteractionType.component":
            try: command, data = list(inter.data.values())[0].split()
            except: return
            if command == 'cmc':
                if data == '0':
                    await inter.response.send_modal(Write_Profile(self.bot))
                elif data == '1':
                    await inter.response.send_modal(Write_Game(self.bot))

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        await member.add_roles(member.guild.get_role(901837523897167922))

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.attachments and message.channel == 1171018003761070081:
            t = '\n'
            await message.delete()
            await message.guild.owner.send(f'{message.author.mention}\n{t.join([atc.url for atc in message.attachments])}')

class Write_Profile(discord.ui.Modal):
    gender = discord.ui.TextInput(label='성별', placeholder='성별을 입력해주세요!', required=False)
    name = discord.ui.TextInput(label='닉네임', placeholder='서버에서 사용할 닉네임을 입력해주세요!', required=False, max_length=32)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(title='정보를 입력해주세요!', timeout=None, custom_id='WP')

    async def on_submit(self, inter: Interaction) -> None:
        gender = self.gender.value
        name = self.name.value
        woman = ['여', '여자', '여성', '녀', 'girl']
        man = ['남', '남자', '남성', 'boy']
        answer = []
        if gender in woman: await inter.user.add_roles(inter.guild.get_role(770945042596626474)); answer.append('역할 지급')
        elif gender in man: await inter.user.add_roles(inter.guild.get_role(770945093141397516)); answer.append('역할 지급')
        elif gender: return await inter.response.send_message(f'"남자"와 "여자"중에 입력하여주세요!', ephemeral=True)
        if name: await inter.user.edit(nick=name); answer.append('닉네임 변경')
        await inter.response.send_message(f'{"과 ".join(answer)}{"이" if answer else ""} 완료되었어요!', ephemeral=True)

class Write_Game(discord.ui.Modal):
    game = discord.ui.TextInput(label='게임', placeholder='주로 하시는 게임을 입력해 주세요!')
    name = discord.ui.TextInput(label='닉네임', placeholder='하고 계시는 게임의 닉네임을 입력해 주세요!', max_length=32)
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__(title='정보를 입력해주세요!', timeout=None, custom_id='WG')

    async def on_submit(self, inter: Interaction) -> None:
        game = self.game.value
        name = self.name.value
        await inter.user.remove_roles(inter.guild.get_role(901837523897167922))
        await inter.user.add_roles((inter.guild.get_role(1170243813739077642)))
        await inter.response.send_message('완료되었어요!', ephemeral=True)
        await inter.guild.owner.send(f'{inter.user.mention}\n게임: {game}\n닉네임: {name}')