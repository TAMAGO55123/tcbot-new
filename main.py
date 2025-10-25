import discord
from discord.ext import commands, tasks
import re
import asyncio
from os import listdir, getenv
from dotenv import load_dotenv as dotenv
from typing import Union
from func.tools import SendEmbedModal, send_update_message
dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="tags!", intents=intents)

TOKEN = getenv("TOKEN")

async def main(bot:commands.Bot):
    @bot.event
    async def on_ready():
        print(f'{bot.user} としてログインしました^o^')
        try:
            synced = await bot.tree.sync()
            print(f'{len(synced)}個のコマンドを同期しました!')
        except Exception as e:
            print(f'コマンドの同期中にエラーが発生しました。: {e}')
        await send_update_message(bot)
    
    for cog in listdir("cogs"):
        if cog.endswith(".py"):
            await bot.load_extension(f"cogs.{cog[:-3]}")
    
    @bot.tree.context_menu(name="メッセージを再送信")
    async def message_re_send(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            await message.channel.send(content=message.content, embeds=message.embeds)
            await interaction.response.send_message(content="sended.",ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

    @bot.tree.context_menu(name="メッセージを埋め込みに変換")
    async def message_send_embed(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            modal = SendEmbedModal(channel=message.channel, message=message.content)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
    @bot.tree.context_menu(name="埋め込みをメッセージに変換")
    async def embed_send_message(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            a = ""
            for i in message.embeds:
                a = a + i.description
            await message.channel.send(content=a)
            await interaction.response.send_message("sended.", ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
    @bot.tree.context_menu(name="手動認証(管理者)")
    async def manual_verify(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            role = message.guild.get_role(1345231376026304653)
            await message.author.add_roles(role)
            await message.author.send(f"手動にて認証が完了いたしました。\n実行者: {interaction.user.name}")
            await interaction.response.send_message(f"ロール:{role.name} 付与完了。")
            await message.add_reaction("✅")
        else:
            await interaction.response.send_message("このコマンドは管理者のみ実行できます。",ephemeral=True)
    
    @bot.event
    async def on_message(message:discord.Message):
        if type(message.channel) != discord.DMChannel:
            if (message.channel.category.id == 1408781349631950856):
                if (message.author.id == 557628352828014614):
                        if ('Welcome' in message.content):
                            if ('Category: [Tag]' in message.content):
                                a:Union[re.Match,None] = re.search(r'```([\s\S]*?)```', message.embeds[1].description)
                                if a:
                                    b = a.group()[4:-3]
                                    if (b != ''):
                                        await message.channel.send(content=f"これは自動招待確認用メッセージです。\n{b}")
                                        try:
                                            c = await bot.fetch_invite(b)
                                            d = discord.Embed(
                                                title="情報",
                                                description=f"**Name**: `{c.guild.name}`,\n**ID**: `{c.guild.id}`",
                                                colour=discord.Colour.green()
                                            )
                                            await message.channel.send(embed=d)
                                        except (ValueError, discord.NotFound, discord.HTTPException) as e:
                                            await message.channel.send('招待が取得できませんでした。')
        await bot.process_commands(message)
    
    await bot.start(TOKEN)

try:
    discord.utils.setup_logging()
    asyncio.run(main(bot=bot))
except Exception as e:
    print(f'BOTの起動中にエラーが発生しました: {e}')