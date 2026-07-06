
# bot.py
import time
import random
import discord
class StaffButtons(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="✅ Accepter", style=discord.ButtonStyle.green)
    async def accept(self, button, interaction):
        try:
            await self.user.send(
                "🎉 Félicitations ! Ta candidature a été **acceptée**. Un membre du staff te contactera bientôt."
            )
        except:
            pass

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("✅ Candidature acceptée.", ephemeral=True)

    @discord.ui.button(label="❌ Refuser", style=discord.ButtonStyle.red)
    async def refuse(self, button, interaction):
        try:
            await self.user.send(
                "❌ Ta candidature a été **refusée**. Merci d'avoir postulé."
            )
        except:
            pass

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send("❌ Candidature refusée.", ephemeral=True)
import os
TOKEN = os.getenv("TOKEN")
STAFF_CHANNEL_ID = 1523723485686403212

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

last_reply = {}
replies = [
    "Steal a Brainrot est incroyable 😄",
    "Qui joue à Roblox ?",
    "Brainrot 🔥",
    "Bon chill à tous 😎",
]

questions = [
    "Quel est ton âge ?",
    "Quel est ton pseudo Roblox ?",
    "Pourquoi veux-tu être staff ?",
    "As-tu déjà été staff ?",
    "Combien d'heures peux-tu être actif par jour ?",
]

@bot.slash_command(description="Candidature staff")
async def staff(ctx):
    await ctx.respond("Regarde tes messages privés.", ephemeral=True)
    try:
        await ctx.author.send("📋 Début de la candidature.")
    except:
        return

    answers = []

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    for q in questions:
        await ctx.author.send(q)
        try:
            m = await bot.wait_for("message", check=check, timeout=300)
        except:
            await ctx.author.send("Temps écoulé.")
            return
        answers.append(m.content)

    ch = bot.get_channel(STAFF_CHANNEL_ID)

    emb = discord.Embed(title="Nouvelle candidature")
    emb.add_field(
        name="Membre",
        value=f"{ctx.author} ({ctx.author.id})",
        inline=False
    )

    for q, a in zip(questions, answers):
        emb.add_field(name=q, value=a, inline=False)

    await ch.send(embed=emb)
    await ctx.author.send("✅ Ta candidature a été envoyée.")
bot.run(TOKEN)
