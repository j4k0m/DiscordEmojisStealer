import json, discord, glob

CONFIG = json.load(open("config.json", "r"))
PREFIX = CONFIG["prefix"]
TOKEN = CONFIG["token"]

non_anim = "https://cdn.discordapp.com/emojis/{}.png?v=1"
anim = "https://cdn.discordapp.com/emojis/{}.gif?v=1"

class Client(discord.Client):
    async def on_message(self, message):
        if message.content.lower() == PREFIX + "load":
            EMOJIS_OBJECT = message.guild.emojis
            if len(EMOJIS_OBJECT) > 1:
                table = {}
                for i in EMOJIS_OBJECT:
                    table[i.id] = {"name": i.name, "link": non_anim.format(i.id) if i.animated == False else anim.format(i.id)}
                with open(f"emojis/{message.guild.id}.json", "w") as save_file:
                    json.dump(table, save_file)
                    save_file.close()
                await message.reply(f"{len(message.guild.emojis)} Emojis loaded! Now you can use them in any server.")
            else:
                await message.reply("No emojis to load.")
                
        elif message.content.startswith(PREFIX + "emoji"):
            if len(message.content.split(" ")) > 1:
                emoji_exist = None
                emoji_link = ""
                emoji_name = message.content.split(" ")[1]
                for i in glob.glob("emojis/*.json"):
                    data = json.load(open(i, "r"))
                    for d in data:
                        if data[d]["name"] == emoji_name:
                            emoji_exist = True
                            emoji_link = data[d]["link"]
                            break
                if emoji_exist:
                    emoji_exist = None
                    await message.channel.send(emoji_link)
                    await message.delete()
                    emoji_link = ""
                else:
                    await message.reply("Can't find the emoji.")
            else:
                await message.reply("Set emoji name.")


client = Client()
client.run(TOKEN, bot=False)