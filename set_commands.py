import requests
import json

TOKEN = "8534082821:AAGJWMhlW27eU0kjB4QHul6knrX8pGRIUjw"
API = f"https://api.telegram.org/bot{TOKEN}"

commands = [
    # Public
    {"command": "start", "description": "Iniciar o bot"},
    {"command": "help", "description": "Mostrar ajuda completa"},
    {"command": "about", "description": "Sobre o bot e creditos"},
    # Info & Recon
    {"command": "info", "description": "Info completa do site [url]"},
    {"command": "dns", "description": "Analise DNS completa [domain]"},
    {"command": "cms", "description": "Detectar CMS (30+ CMS) [url]"},
    {"command": "reverse", "description": "Reverse IP + GeoIP [ip]"},
    {"command": "emails", "description": "Extrair emails do site [url]"},
    # Vulnerability Scanners
    {"command": "sqli", "description": "Scanner SQLi (30+ payloads) [url]"},
    {"command": "xss", "description": "Scanner XSS (18+ payloads) [url]"},
    {"command": "admin", "description": "Admin Finder (100+ paths) [url]"},
    {"command": "panel", "description": "Painel Admin Finder (100+ paths) [url]"},
    {"command": "ports", "description": "Scan portas (35+ common) [ip]"},
    {"command": "dirs", "description": "Scan diretorios (80+ paths) [url]"},
    {"command": "sub", "description": "Subdominios (100+ subs) [domain]"},
    {"command": "wp", "description": "WordPress Scanner completo [url]"},
    {"command": "ftpssh", "description": "Scan FTP/SSH banner [ip]"},
    # V5.0 Scanners
    {"command": "ssl", "description": "Auditoria SSL/TLS completa [url]"},
    {"command": "headers", "description": "Security Headers [url]"},
    {"command": "cors", "description": "Teste CORS misconfig [url]"},
    {"command": "robots", "description": "Robots.txt analise [url]"},
    {"command": "sitemap", "description": "Sitemap.xml analise [url]"},
    {"command": "tech", "description": "Detectar tecnologias [url]"},
    {"command": "exposed", "description": "Arquivos expostos [url]"},
    {"command": "backup", "description": "Backups expostos [url]"},
    {"command": "api", "description": "Descobrir APIs endpoints [url]"},
    {"command": "shell", "description": "Hunt webshells [url]"},
    {"command": "config", "description": "Configs expostas [url]"},
    # V5.1 New Scanners
    {"command": "quick", "description": "Quick scan (info+headers) [url]"},
    {"command": "scanall", "description": "Scan completo 6 ferramentas [url]"},
    {"command": "deep", "description": "Deep scan vulns (6 scanners) [url]"},
    {"command": "http", "description": "Analise HTTP response [url]"},
    {"command": "sslchain", "description": "Cadeia SSL completa [url]"},
    # Tools
    {"command": "batch", "description": "Scan multiplos targets [cmd urls]"},
    {"command": "watch", "description": "Monitorar mudancas [url]"},
    {"command": "cancel", "description": "Cancelar scan ativo"},
    {"command": "rate", "description": "Nota de seguranca [url]"},
    {"command": "compare", "description": "Comparar 2 sites [url1 url2]"},
    {"command": "history", "description": "Historico de scans [url]"},
    {"command": "ip", "description": "Info do IP + GeoIP [ip]"},
    {"command": "traceroute", "description": "Traceroute [ip]"},
    {"command": "whois", "description": "Whois lookup [domain]"},
    {"command": "report", "description": "Relatorio completo [url]"},
    {"command": "pdf", "description": "Exportar relatorio TXT [cmd] [url]"},
    {"command": "schedule", "description": "Agendar scan [min] [cmd] [url]"},
    {"command": "stealth", "description": "Scan stealth lento [cmd] [url]"},
    {"command": "notify", "description": "Notificar mudanca status [url]"},
    # System
    {"command": "ping", "description": "Latencia do bot"},
    {"command": "uptime", "description": "Tempo online do bot"},
    {"command": "status", "description": "Health check do bot"},
    {"command": "feedback", "description": "Enviar feedback"},
    {"command": "bugreport", "description": "Reportar bug"},
    {"command": "lang", "description": "Change language (pt/en/es)"},
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
    {"command": "listdn", "description": "Lista comandos dono (donos)"},
    {"command": "maintenance", "description": "Modo manutencao (donos)"},
    {"command": "cooldown", "description": "Rate limit user (donos)"},
    {"command": "vip", "description": "Gerenciar VIP (donos)"},
    {"command": "viplist", "description": "Listar todos os VIPs (donos)"},
    {"command": "log", "description": "Audit logs (donos)"},
    {"command": "clearlogs", "description": "Limpar logs (donos)"},
    {"command": "broadcast", "description": "Agendar broadcast (donos)"},
    {"command": "top", "description": "Top sites (donos)"},
    # Owner-exclusive scanners
    {"command": "forensic", "description": "Forensic analysis (donos)"},
    {"command": "pentest", "description": "Pentest automation (donos)"},
    {"command": "osint", "description": "OSINT intelligence (donos)"},
]

resp = requests.post(f"{API}/setMyCommands", json={"commands": commands})
print(json.dumps(resp.json(), indent=2))
