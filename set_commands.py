import requests
import json

TOKEN = "8534082821:AAGJWMhlW27eU0kjB4QHul6knrX8pGRIUjw"
API = f"https://api.telegram.org/bot{TOKEN}"

commands = [
    # Public
    {"command": "start", "description": "Iniciar o bot"},
    {"command": "help", "description": "Mostrar ajuda"},
    {"command": "about", "description": "Sobre o framework"},
    # Info & Recon
    {"command": "info", "description": "Info do site [url]"},
    {"command": "dns", "description": "Analise DNS [domain]"},
    {"command": "cms", "description": "Detectar CMS [url]"},
    {"command": "reverse", "description": "Reverse IP [ip]"},
    {"command": "emails", "description": "Extrair emails [url]"},
    # Vulnerability Scanners
    {"command": "sqli", "description": "Scanner SQLi [url] [verbose]"},
    {"command": "xss", "description": "Scanner XSS [url] [verbose]"},
    {"command": "admin", "description": "Painel admin [url]"},
    {"command": "panel", "description": "Painel Admin Finder [url]"},
    {"command": "ports", "description": "Scan de portas [ip]"},
    {"command": "dirs", "description": "Scan dirs [url]"},
    {"command": "sub", "description": "Scan subs [domain]"},
    {"command": "wp", "description": "WordPress scan [url]"},
    {"command": "ftpssh", "description": "Scan FTP/SSH [ip]"},
    # V5.0 Scanners
    {"command": "ssl", "description": "Auditoria SSL/TLS [url]"},
    {"command": "headers", "description": "Security Headers [url]"},
    {"command": "cors", "description": "Teste CORS [url]"},
    {"command": "robots", "description": "Robots.txt [url]"},
    {"command": "sitemap", "description": "Sitemap.xml [url]"},
    {"command": "tech", "description": "Detectar tecnologias [url]"},
    {"command": "exposed", "description": "Arquivos expostos [url]"},
    {"command": "backup", "description": "Backups expostos [url]"},
    {"command": "api", "description": "Descobrir APIs [url]"},
    {"command": "shell", "description": "Hunt webshells [url]"},
    {"command": "config", "description": "Configs expostas [url]"},
    # Extra Tools
    {"command": "traceroute", "description": "Traceroute [ip]"},
    {"command": "whois", "description": "Whois [domain]"},
    {"command": "ip", "description": "GeoIP avancado [ip]"},
    {"command": "rate", "description": "Nota de seguranca [url]"},
    {"command": "compare", "description": "Comparar 2 sites [url1] [url2]"},
    {"command": "history", "description": "Historico de scans [url]"},
    {"command": "pdf", "description": "Relatorio PDF [cmd] [url]"},
    {"command": "schedule", "description": "Agendar scan [min] [cmd] [url]"},
    {"command": "stealth", "description": "Scan stealth [cmd] [url]"},
    {"command": "notify", "description": "Notificar mudanca [url]"},
    # System
    {"command": "ping", "description": "Latencia e status do bot"},
    {"command": "uptime", "description": "Tempo online do bot"},
    {"command": "status", "description": "Health check completo"},
    {"command": "feedback", "description": "Enviar feedback/sugestoes"},
    {"command": "report", "description": "Reportar bug"},
    {"command": "rescan", "description": "Refazer scan [cmd] [url]"},
    {"command": "stop", "description": "Parar scan ativo"},
    # Owner
    {"command": "botpanel", "description": "Painel do bot (donos)"},
    {"command": "logs", "description": "Logs (donos)"},
    {"command": "stats", "description": "Estatisticas (donos)"},
    {"command": "ban", "description": "Banir usuario (donos)"},
    {"command": "unban", "description": "Desbanir (donos)"},
    {"command": "export", "description": "Exportar usuarios (donos)"},
    {"command": "bancodds", "description": "DB dump (donos)"},
    {"command": "msg", "description": "Broadcast pra todos (donos)"},
    {"command": "listdn", "description": "Lista comandos de dono (donos)"},
    {"command": "maintenance", "description": "Modo manutencao (donos)"},
    {"command": "cooldown", "description": "Rate limit (donos)"},
    {"command": "vip", "description": "Gerenciar VIP (donos)"},
    {"command": "log", "description": "Audit logs (donos)"},
    {"command": "clearlogs", "description": "Limpar logs (donos)"},
    {"command": "broadcast", "description": "Agendar broadcast (donos)"},
    {"command": "top", "description": "Top sites (donos)"},
]

resp = requests.post(f"{API}/setMyCommands", json={"commands": commands})
print(json.dumps(resp.json(), indent=2))
