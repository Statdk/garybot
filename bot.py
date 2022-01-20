import nextcord
from nextcord.ext import commands
import json
from datetime import datetime
import os


with open('./config.json') as f:
    CONFIG = json.load(f)
    f.close()
client = commands.Bot(command_prefix=CONFIG["prefix"])


# @client.command.has_permissions(manage_messages=True)
class admin():
    @client.command()
    async def shutdown(ctx):
        await ctx.send(f"Shutting down\n{datetime.now()}")
        exit()

    @client.command()
    async def ext_load(ctx, *, ext_name):
        try:
            client.load_extension(ext_name)
            await ctx.send(f"Loaded '{ext_name}'")
        except Exception as e:
            await ctx.send(f"Failed load of '{ext_name}':\n{e}")

    @client.command()
    async def ext_unload(ctx, *, ext_name):
        try:
            client.unload_extension(ext_name)
            await ctx.send(f"Unloaded '{ext_name}'")
        except Exception as e:
            await ctx.send(f"Failed unload of '{ext_name}':\n{e}")

    @client.command()
    async def ext_reload(ctx, *, ext_name):
        try:
            client.reload_extension(ext_name)
            await ctx.send(f"Reloaded '{ext_name}'")
        except Exception as e:
            await ctx.send(f"Failed reload of '{ext_name}':\n{e}")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.event
async def on_ready():
    print(
        f"Logged in as\n{client.user.name}\n{client.user.id}\n{datetime.now()}\n...")
    await client.get_channel(CONFIG["log_channel"]).send(f'Logged in as\n{client.user.name}\n{client.user.id}\n{datetime.now()}\n...')
    await client.change_presence(activity=nextcord.Activity(name="", type=4))

    tosend = "Loaded extensions:"
    for filename in os.listdir("./extensions/"):
        if filename.endswith(".py"):
            try:
                client.load_extension(filename)
                tosend += f"\n{filename}"
            except:
                continue
    await client.get_channel(CONFIG["log_channel"]).send(tosend)


client.run(CONFIG["token"])
