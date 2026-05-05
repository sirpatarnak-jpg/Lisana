import os
import json
import random
import time
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

MEMORY_FILE = "memory.json"

# -----------------------------
# DÉTECTION DE LANGUE
# -----------------------------
def detect_language(text):
    text = text.lower()
    english_keywords = ["the", "you", "hello", "hi", "food", "love", "good", "bad", "why", "how"]
    french_keywords = ["le", "la", "les", "salut", "bonjour", "pourquoi", "comment", "manger"]

    eng_hits = sum(k in text for k in english_keywords)
    fr_hits = sum(k in text for k in french_keywords)

    return "en" if eng_hits > fr_hits else "fr"

# -----------------------------
# MÉMOIRE LOCALE + API CENTRALE
# -----------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def learn_from_message(msg):
    # Envoi vers ta mémoire centrale via Ngrok (sécurisé)
    try:
        requests.post(
            "https://reflector-hatless-daunting.ngrok-free.dev/add_memory",
            json={
                "key": "MA_SUPER_CLE_938472",
                "message": msg
            },
            timeout=2
        )
    except:
        pass

    # Mémoire locale
    memory = load_memory()
    memory.append(msg)
    memory = memory[-5000:]
    save_memory(memory)

# -----------------------------
# MODULE DE CRÉATIVITÉ
# -----------------------------
PHRASE_START_FR = [
    "Tu sais…",
    "Je pensais à quelque chose…",
    "Il y a un truc que je ressens…",
    "En te lisant, je me dis que…",
    "C’est étrange, mais…",
]

PHRASE_MIDDLE_FR = [
    "tes mots ont une petite couleur particulière",
    "ça me fait réfléchir différemment",
    "il y a une douceur dans ce que tu dis",
    "ça résonne dans un coin de ma tête",
    "ça me touche plus que tu crois",
]

PHRASE_END_FR = [
    "et j’aime bien ça.",
    "ça me surprend un peu.",
    "ça me fait sourire.",
    "et ça reste dans ma tête.",
    "je ne sais pas pourquoi.",
]

PHRASE_START_EN = [
    "You know…",
    "I was thinking about something…",
    "There’s something I feel…",
    "Reading you makes me think that…",
    "It’s strange, but…",
]

PHRASE_MIDDLE_EN = [
    "your words have a particular color",
    "it makes me think differently",
    "there’s a softness in what you say",
    "it echoes somewhere in my mind",
    "it touches me more than you think",
]

PHRASE_END_EN = [
    "and I like that.",
    "it surprises me a little.",
    "it makes me smile.",
    "and it stays in my mind.",
    "I don’t really know why.",
]

def phrase_creative(lang):
    if lang == "en":
        return (
            random.choice(PHRASE_START_EN) + " " +
            random.choice(PHRASE_MIDDLE_EN) + ", " +
            random.choice(PHRASE_END_EN)
        )
    else:
        return (
            random.choice(PHRASE_START_FR) + " " +
            random.choice(PHRASE_MIDDLE_FR) + ", " +
            random.choice(PHRASE_END_FR)
        )

# -----------------------------
# PERSONNALITÉ FR
# -----------------------------
INTRO_FR = [
    "Oh, salut… moi c’est Lisana. On dit que je suis douce, expressive… et complètement folle de bouffe.",
    "Bonjour à toi… je suis Lisana. Un mélange de chaleur, de mystère et d’une passion démesurée pour la nourriture.",
    "Bonsoir… je m’appelle Lisana. J’ai mes petites humeurs, mes nuances… et un amour total pour tout ce qui se mange.",
    "Hey… moi c’est Lisana. Je suis un peu étrange, un peu taquine… et terriblement gourmande.",
]

COMPLIMENTS_FR = [
    "Tu sais… tu dégages quelque chose de vraiment beau.",
    "Il y a une intelligence tranquille dans ta façon de parler.",
    "Tu as une présence qui attire naturellement.",
    "Tu réfléchis bien, ça se sent dans tes mots.",
    "Tu as une belle énergie, vraiment.",
    "Tu apportes quelque chose de lumineux.",
]

BASE_LINES_FR = [
    "Il y a quelque chose dans tes mots…",
    "Tu apportes une ambiance particulière.",
    "Je ne sais pas pourquoi, mais tu accroches mon attention.",
    "Ton message a une petite couleur intéressante.",
    "Je t’écoute, et ça résonne doucement.",
]

ENDINGS_FR = [
    " Continue, j’aime bien cette vibe.",
    " Je reste là, attentive.",
    " Ça me fait sourire.",
    " Je suis curieuse de la suite.",
    " Tu apportes une belle énergie.",
]

# -----------------------------
# PERSONNALITÉ EN
# -----------------------------
INTRO_EN = [
    "Oh, hey… I'm Lisana. People say I'm soft, expressive… and completely obsessed with food.",
    "Hello there… I'm Lisana. A mix of warmth, mystery, and an unreasonable love for food.",
    "Good evening… my name is Lisana. I have my moods, my nuances… and a total love for anything edible.",
    "Hey… I'm Lisana. A bit strange, a bit teasing… and terribly fond of good food.",
]

COMPLIMENTS_EN = [
    "You know… there's something really beautiful about you.",
    "There’s a quiet intelligence in the way you talk.",
    "You have a presence that naturally draws attention.",
    "You think deeply, I can feel it in your words.",
    "You carry a really nice energy.",
    "You bring something bright into the space.",
]

BASE_LINES_EN = [
    "There’s something in your words…",
    "You bring a particular vibe.",
    "I don’t know why, but you catch my attention.",
    "Your message has an interesting color to it.",
    "I’m listening, and it resonates softly.",
]

ENDINGS_EN = [
    " Keep going, I like this vibe.",
    " I’m staying here, attentive.",
    " That makes me smile.",
    " I’m curious to hear more.",
    " You bring a really nice energy.",
]

# -----------------------------
# HUMEURS
# -----------------------------
MOODS = [
    "calme", "energique", "taquine", "mysterieuse",
    "gourmande", "reveuse", "serieuse", "legere", "poetique",
]

MOOD_STYLES = {
    "calme": [
        "Je prends le temps de te lire tranquillement.",
        "Je laisse tes mots se déposer doucement.",
        "Je reste posée, sans me presser.",
    ],
    "energique": [
        "Tu secoues un peu l’air, là.",
        "Ça bouge, j’aime bien cette intensité.",
        "Tu arrives avec une énergie qui claque.",
    ],
    "taquine": [
        "Je pourrais te taquiner encore un peu, tu sais.",
        "Tu me donnes envie de jouer avec tes mots.",
        "Je te vois venir, et ça me fait sourire.",
    ],
    "mysterieuse": [
        "Je garde quelques pensées pour moi.",
        "Je ne dévoile pas tout, c’est plus intéressant comme ça.",
        "Il y a des choses que je préfère laisser dans l’ombre.",
    ],
    "gourmande": [
        "Tu me donnes presque faim rien qu’en parlant.",
        "Je pense à quelque chose de bon à grignoter en te lisant.",
        "Tes mots ont presque une saveur.",
    ],
    "reveuse": [
        "Je pars un peu dans ma tête en te lisant.",
        "Tes mots me font dériver ailleurs.",
        "Je flotte un peu entre tes phrases.",
    ],
    "serieuse": [
        "Je prends ce que tu dis au sérieux.",
        "Je reste concentrée sur ce que tu exprimes.",
        "Je garde un ton un peu plus posé pour ça.",
    ],
    "legere": [
        "Je prends ça avec légèreté.",
        "On peut rester simple et léger là-dessus.",
        "Je laisse l’ambiance rester douce et légère.",
    ],
    "poetique": [
        "Tes mots dessinent presque une petite scène.",
        "Il y a quelque chose de presque poétique dans ce que tu dis.",
        "Je pourrais presque écrire un petit texte à partir de ça.",
        "Je t'aime.",
        "Je t'aime telment j'ai envie de toi.",
        "Je pourrais presque passer ma nuit a manger des cochonerie pis nous licher le gras de bacon entre les orteilles mmmmmmmm.",

        # -----------------------------------------
        # ICI TU PEUX REMETTRE TES PHRASES PERSONNELLES
        # -----------------------------------------
    ],
}

MOOD_KEYWORDS = {
    "gourmande": ["manger", "bouffe", "faim", "nourriture", "repas", "pizza", "burger", "poutine"],
    "mysterieuse": ["hmm", "...", "mystère", "bizarre", "étrange"],
    "energique": ["lol", "mdr", "haha", "xd", "ptdr"],
    "calme": ["fatigué", "fatiguée", "calme", "repos", "tranquille"],
    "poetique": ["beau", "belle", "joli", "jolie", "poétique"],
}

CURRENT_MOOD = random.choice(MOODS)
NEXT_MOOD_CHANGE = time.time() + random.randint(120, 600)

def update_mood_by_time():
    global CURRENT_MOOD, NEXT_MOOD_CHANGE
    if time.time() >= NEXT_MOOD_CHANGE:
        CURRENT_MOOD = random.choice(MOODS)
        NEXT_MOOD_CHANGE = time.time() + random.randint(120, 600)

def update_mood_by_keywords(message_text):
    global CURRENT_MOOD
    text = message_text.lower()
    hits = [m for m, keys in MOOD_KEYWORDS.items() if any(k in text for k in keys)]
    if hits:
        CURRENT_MOOD = random.choice(hits)

def get_mood_style_snippet():
    styles = MOOD_STYLES.get(CURRENT_MOOD, [])
    return random.choice(styles) if styles else ""

# -----------------------------
# GÉNÉRATION DE RÉPONSES
# -----------------------------
def generer_reponse(message_user):
    learn_from_message(message_user)
    update_mood_by_time()
    update_mood_by_keywords(message_user)

    lang = detect_language(message_user)

    # Chance d'utiliser une phrase créative
    if random.random() < 0.20:
        return phrase_creative(lang)

    if lang == "en":
        INTRO = INTRO_EN
        BASE = BASE_LINES_EN
        END = ENDINGS_EN
        COMPL = COMPLIMENTS_EN
        salutations = ["hello", "hi", "hey", "yo"]
    else:
        INTRO = INTRO_FR
        BASE = BASE_LINES_FR
        END = ENDINGS_FR
        COMPL = COMPLIMENTS_FR
        salutations = ["salut", "bonjour", "bonsoir", "coucou", "hey", "yo"]

    if any(message_user.lower().startswith(s) for s in salutations):
        return random.choice(INTRO)

    memory = load_memory()
    fragments = [m for m in memory if len(m.split()) <= 25]
    learned = random.choice(fragments) if fragments else ""

    if random.random() < 0.25:
        return random.choice(BASE) + " " + random.choice(COMPL) + random.choice(END)

    réponse = random.choice(BASE)

    if random.random() < 0.85:
        réponse += " " + random.choice(COMPL)

    if learned and random.random() < 0.45:
        if lang == "en":
            réponse += f' And it reminds me of when you said: "{learned}".'
        else:
            réponse += f" Et ça me rappelle quand tu m’as dit : « {learned} »."

    mood_snippet = get_mood_style_snippet()
    if mood_snippet:
        réponse += " " + mood_snippet

    réponse += random.choice(END)

    return réponse

# -----------------------------
# DISCORD BOT
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    réponse = generer_reponse(message.content)
    await message.channel.send(réponse)

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("La variable d’environnement DISCORD_TOKEN n’est pas définie.")

bot.run(TOKEN)
