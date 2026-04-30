# utils/plataformas.py
# MÓDULO FULL - Validador + Detector de Plataforma
# MarconeBOT

from urllib.parse import urlparse


# ==================================================
# CONFIG DAS PLATAFORMAS ACEITAS
# ==================================================

PLATAFORMAS = {
    "tiktok.com": {
        "nome": "TikTok",
        "emoji": "<:tiktok:1489042503817498745> ",
        "cor": 0xff0050,
        "icone": "https://cdn-icons-png.flaticon.com/512/3046/3046121.png"
    },

    "instagram.com": {
        "nome": "Instagram",
        "emoji": "<:INSTA:1498915902807085127>",
        "cor": 0xe1306c,
        "icone": "https://cdn-icons-png.flaticon.com/512/2111/2111463.png"
    },

    "youtube.com": {
        "nome": "YouTube",
        "emoji": "<:yt:1489042362834616511>",
        "cor": 0xff0000,
        "icone": "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
    },

    "youtu.be": {
        "nome": "YouTube",
        "emoji": "<:yt:1489042362834616511>",
        "cor": 0xff0000,
        "icone": "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"
    },

    "twitch.tv": {
        "nome": "Twitch",
        "emoji": "<:twittch:1489042382480478240> ",
        "cor": 0x9146ff,
        "icone": "https://cdn-icons-png.flaticon.com/512/5968/5968819.png"
    },

    "kick.com": {
        "nome": "Kick",
        "emoji": "<:kick:1489042452974407871> ",
        "cor": 0x53fc18,
        "icone": "https://seeklogo.com/images/K/kick-logo-7E72A4F2F7-seeklogo.com.png"
    },

    "facebook.com": {
        "nome": "Facebook Gaming",
        "emoji": "<:FacebookGaming:1498915393056804975> ",
        "cor": 0x1877f2,
        "icone": "https://cdn-icons-png.flaticon.com/512/733/733547.png"
    },

    "trovo.live": {
        "nome": "Trovo",
        "emoji": "<:TROVO:1498915372164845638>",
        "cor": 0x19ff6a,
        "icone": "https://play-lh.googleusercontent.com/Nm7E_xxx"
    }
}


# ==================================================
# DOMÍNIOS PROIBIDOS
# ==================================================

BLOQUEADOS = [
    "bit.ly",
    "tinyurl.com",
    "cutt.ly",
    "goo.gl",
    "grabify",
    "iplogger",
    "discord-free",
    "steamgift",
    "nitrofree"
]


# ==================================================
# LIMPA URL
# ==================================================

def limpar_url(link: str):
    link = link.strip().lower()

    if not link.startswith("http://") and not link.startswith("https://"):
        link = "https://" + link

    return link


# ==================================================
# PEGA DOMÍNIO
# ==================================================

def pegar_dominio(link: str):
    try:
        link = limpar_url(link)
        parsed = urlparse(link)
        dominio = parsed.netloc.replace("www.", "")
        return dominio
    except:
        return None


# ==================================================
# LINK BLOQUEADO?
# ==================================================

def link_bloqueado(link: str):
    dominio = pegar_dominio(link)

    if not dominio:
        return True

    for item in BLOQUEADOS:
        if item in dominio:
            return True

    return False


# ==================================================
# DETECTAR PLATAFORMA
# ==================================================

def detectar_plataforma(link: str):
    dominio = pegar_dominio(link)

    if not dominio:
        return None

    for site, dados in PLATAFORMAS.items():
        if site in dominio:
            return dados

    return None


# ==================================================
# LINK PERMITIDO?
# ==================================================

def link_permitido(link: str):
    if link_bloqueado(link):
        return False

    if detectar_plataforma(link):
        return True

    return False


# ==================================================
# TEXTO BONITO
# ==================================================

def nome_plataforma(link: str):
    dados = detectar_plataforma(link)

    if dados:
        return dados["nome"]

    return "Desconhecida"


# ==================================================
# EXEMPLO DE USO:
#
# from utils.plataformas import *
#
# if not link_permitido(link):
#     print("Link inválido")
#
# dados = detectar_plataforma(link)
#
# print(dados["nome"])
# print(dados["emoji"])
# print(dados["cor"])
# print(dados["icone"])
# ==================================================