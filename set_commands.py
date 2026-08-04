import requests
import json

TOKEN = "8534082821:AAGJWMhlW27eU0kjB4QHul6knrX8pGRIUjw"
API = f"https://api.telegram.org/bot{TOKEN}"

commands = [
    {"command": "start", "description": "Iniciar o bot"},
    {"command": "help", "description": "Mostrar ajuda"},
    {"command": "about", "description": "Sobre o framework"},
    {"command": "info", "description": "Info do site [url]"},
    {"command": "sqli", "description": "Scanner SQLi [url]"},
    {"command": "xss", "description": "Scanner XSS [url]"},
    {"command": "admin", "description": "Painel admin [url]"},
    {"command": "panel", "description": "Painel Admin Finder [url]"},
    {"command": "ports", "description": "Scan de portas [ip]"},
    {"command": "dirs", "description": "Scan dirs [url]"},
    {"command": "sub", "description": "Scan subs [domain]"},
    {"command": "wp", "description": "WordPress scan [url]"},
    {"command": "emails", "description": "Extrair emails [url]"},
    {"command": "dns", "description": "Analise DNS [domain]"},
    {"command": "cms", "description": "Detectar CMS [url]"},
    {"command": "reverse", "description": "Reverse IP [ip]"},
    {"command": "ftpssh", "description": "Scan FTP/SSH [ip]"},
    {"command": "ping", "description": "Latência e status do bot"},
    {"command": "status", "description": "Health check completo"},
    {"command": "botpanel", "description": "Painel do bot (donos)"},
    {"command": "logs", "description": "Logs (donos)"},
    {"command": "bancodds", "description": "DB dump (donos)"},
    {"command": "msg", "description": "Broadcast pra todos (donos)"},
]

resp = requests.post(f"{API}/setMyCommands", json={"commands": commands})
print(json.dumps(resp.json(), indent=2))
