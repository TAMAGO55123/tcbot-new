from func.data import BOT_ADMIN
import discord
from discord.ext import commands
from datetime import datetime

def bot_ready_print(name:str):
    print(f"\033[32m| {name} ready! \033[0m")


# 管理者チェックの関数
def is_bot_admin(user_id:int) -> bool:
    return user_id in BOT_ADMIN

def color_code(code:str) -> int:
    if "#" in code:
        a = code.replace("#", "")
    else:
        a = code

    return int(f"0x{a}", 16)

class SendModal(discord.ui.Modal):
    def __init__(self, channel:discord.TextChannel, ifembed:bool,user:discord.Member):
        super().__init__(
            title="フォーム",
            timeout=None,
        )

        self.messages = discord.ui.TextInput(
            label="メッセージ",
            style=discord.TextStyle.paragraph,
            required=True,
        )
        self.add_item(self.messages)

        self.channel = channel
        self.ifembed = ifembed
        self.user = user

    async def on_submit(self, interaction:discord.Interaction):
        if self.ifembed:
            a = await self.channel.send(embed=discord.Embed(description=self.messages))
        else:
            a = await self.channel.send(content=self.messages)
        await interaction.response.send_message("sended.",ephemeral=True)

class SendEmbedModal(discord.ui.Modal):
    def __init__(self, channel:discord.TextChannel, message:str):
        super().__init__(
            title="フォーム",
            timeout=None,
        )

        self.messages = discord.ui.TextInput(
            label="Color Code",
            style=discord.TextStyle.short,
            max_length=6,
            required=False,
        )
        self.add_item(self.messages)

        self.channel = channel
        self.message = message

    async def on_submit(self, interaction:discord.Interaction):
        if self.messages.value:
            a = int(f"0x{self.messages.value}", 16)
        else:
            a = None
        await self.channel.send(embed=discord.Embed(description=self.message, color=a))
        await interaction.response.send_message("sended.",ephemeral=True)

async def send_update_message(bot:commands.Bot):
        update_id = 1408781350819069955
        update = await bot.fetch_channel(update_id)
        embed = discord.Embed(title='BOTが起動しました^o^',description="BOTが起動されました",color=0x0004ff,timestamp=datetime.now())
        await update.send(embed=embed)

admin_per = discord.Permissions()
admin_per.administrator=True