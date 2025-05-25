import discord
from discord.ext import commands
from discord import app_commands
import random
import csv
import os

TOKEN = os.environ['discordkey']
QUESTIONS_FILE = 'questions.csv'
OKRUHY_FILE = 'okruhy.txt'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def nacti_otazky():
    otazky = []
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) >= 2:
                    okruh = row[0].strip()
                    text = row[1].strip()
                    if okruh and text:
                        otazky.append((okruh, text))
    except Exception as e:
        print(f"Chyba při načítání CSV: {e}")
    return otazky

def nacti_okruhy():
    try:
        with open(OKRUHY_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Chyba při načítání okruhů: {e}")
        return []

# === Slash příkazy ===

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Přihlášen jako {bot.user}')


@bot.tree.command(name='otazka', description='Vrátí náhodnou otázku ze všech okruhů.')
async def nahodna_otazka(interaction: discord.Interaction):
    otazky = nacti_otazky()
    if not otazky:
        await interaction.response.send_message("Nebyly nalezeny žádné otázky.")
        return
    okruh, text = random.choice(otazky)
    await interaction.response.send_message(f"Okruh {okruh}: {text}")


@bot.tree.command(name='otazka_z_okruhu', description='Vrátí náhodnou otázku z daného okruhu.')
@app_commands.describe(cislo='Číslo okruhu')
async def otazka_z_okruhu(interaction: discord.Interaction, cislo: int):
    otazky = nacti_otazky()
    vybrane = [text for okruh, text in otazky if okruh == str(cislo)]
    if not vybrane:
        await interaction.response.send_message(f"Nebyly nalezeny otázky pro okruh {cislo}.")
        return
    await interaction.response.send_message(f"Okruh {vybrane}: {random.choice(vybrane)}")


@bot.tree.command(name='okruh', description='Vrátí náhodný okruh.')
async def nahodny_okruh(interaction: discord.Interaction):
    okruhy = nacti_okruhy()
    if not okruhy:
        await interaction.response.send_message("Soubor s okruhy je prázdný nebo chybí.")
        return
    index = random.randint(0, len(okruhy) - 1)
    await interaction.response.send_message(f"Okruh {index + 1}: {okruhy[index]}")

@bot.tree.command(name='herbert_otazka', description='Poprosí Herberta o vygenerování náhodné otázky metodou HSCJ.')
async def otazka_irl(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("Tento příkaz lze použít pouze na serveru.")
        return

    tazatel = guild.get_member(485549873060642817)

    if not tazatel:
        await interaction.response.send_message("Herbert se ztratil :(")
        return

    await interaction.response.send_message(f":bum: {tazatel.mention} CumJar otázku prosím :zabickasdricko: ")

bot.run(TOKEN)
