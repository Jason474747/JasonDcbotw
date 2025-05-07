import nextcord
from nextcord.ext import commands
import random
import asyncio
from nextcord.ui import Button, View

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Giveaway Command mit Button
@bot.command()
async def giveaway(ctx, prize: str, duration: int, *additional_prizes):
    """Erstellt ein Giveaway mit mehreren Preisen und einem Teilnahme-Button."""

    if len(additional_prizes) > 0:
        prizes = [prize] + list(additional_prizes)
    else:
        prizes = [prize]

    # Erstelle das Embed für die Giveaway-Ankündigung
    embed = nextcord.Embed(
        title="🎉 **Giveaway!** 🎉",
        description=f"**Preise:**\n" + "\n".join([f"🎁 {prize}" for prize in prizes]) +
                    f"\n\n**Teilnehmen:** Klicke auf den Button unten, um teilzunehmen!\n\n**Dauer:** {duration} Sekunden",
        color=nextcord.Color.green()
    )
    embed.set_footer(text="Viel Glück! 🍀")

    # Erstelle einen Button
    button = Button(label="Teilnehmen 🎉", style=nextcord.ButtonStyle.green)

    # Callback-Funktion für Button-Klick
    async def button_callback(interaction):
        if interaction.user in users:
            await interaction.response.send_message("Du hast bereits teilgenommen!", ephemeral=True)
        else:
            users.append(interaction.user)
            await interaction.response.send_message(f"{interaction.user.mention} hat am Giveaway teilgenommen!", ephemeral=True)

    # Füge den Button hinzu
    button.callback = button_callback
    view = View()
    view.add_item(button)

    # Sende die Nachricht mit dem Button
    giveaway_message = await ctx.send(embed=embed, view=view)

    users = []  # Liste der Teilnehmer

    # Warte, bis das Giveaway endet
    await asyncio.sleep(duration)

    # Erstelle eine Nachricht, wenn das Giveaway beendet ist
    if len(users) == 0:
        await ctx.send("Leider hat niemand am Giveaway teilgenommen!")
    else:
        winners = []
        # Ziehe einen Gewinner für jeden Preis
        for prize in prizes:
            winner = random.choice(users)
            winners.append(f"🎁 **{prize}** geht an {winner.mention}! 🎉")
            users.remove(winner)  # Entferne den Gewinner, damit er nicht nochmal gewinnen kann

        # Sende die Benachrichtigung über die Gewinner
        await ctx.send("\n".join(winners))
        await ctx.send("Das Giveaway ist jetzt beendet! Herzlichen Glückwunsch an alle Gewinner! 🎉")

# Beispiel: giveaway Command
# !giveaway "Discord Nitro" 60 "VIP Rolle" "100€ Amazon Gutschein"
