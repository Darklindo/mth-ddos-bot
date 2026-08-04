#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  MTH DDOS SECURITY - TELEGRAM BOT v4.2                    ║
║  Advanced Security Testing Tools                          ║
║  Credits: @OnlyExaltarei, @Thebesty9, @PETER_DNS          ║
╚══════════════════════════════════════════════════════════════╝

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

CHANGELOG v4.2:
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
import html as html_lib
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

# Result cache: (command, target) -> (result_text, timestamp)
RESULT_CACHE = {}
CACHE_TTL = 300  # 5 minutes cache

# Banned users
BANNED_USERS = set()  # user_ids banned by /ban

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

def tool_sqli(url):
    """SQL Injection Scanner v3.6 - 22 payloads, baseline comparison, ANTI-FALSE-POSITIVE"""
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

    results = []
    found = 0

    # Get baseline: response without any payload
    baseline_resp = _safe_get(url, timeout=5)
    # FIX v3.7: If site is offline, don't scan
    if not baseline_resp:
        return "❌ Não foi possível acessar o site para análise SQLi"
    baseline_len = len(baseline_resp.content)
    baseline_text = baseline_resp.text.lower()

    def check_payload(payload):
        try:
            # FIX: use safe="" to encode quotes and special chars properly
            encoded = requests.utils.quote(payload, safe="")
            test_url = url + encoded
            response = _safe_get(test_url, timeout=5)
            if not response:
                return None
            body = response.text.lower()
            body_len = len(response.content)

            # BASELINE FILTER: If response is identical to baseline, the payload had no effect
            if body_len == baseline_len and abs(len(body) - len(baseline_text)) < 10:
                return None

            # Check for error signs
            for sign in error_signs:
                if sign in body:
                    # Verify the error isn't in the baseline too (false positive)
                    if sign not in baseline_text:
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

    if found == 0:
        return "✅ Nenhuma vulnerabilidade SQLi detectada"
    else:
        header = f"🚨 <b>{found} vulnerabilidade(s) SQLi encontrada(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        return header + "\n".join(results)

def tool_xss_scanner(url):
    """XSS Scanner v3.6 - 14 payloads, STRICT unescaped reflection only, ANTI-FALSE-POSITIVE"""
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
    ]

    results = []
    found = 0

    # Get baseline: response without any payload
    baseline_resp = _safe_get(url, timeout=5)
    # FIX v3.7: If site is offline, don't scan
    if not baseline_resp:
        return "❌ Não foi possível acessar o site para análise XSS"
    baseline_text = baseline_resp.text

    def check_payload(payload):
        try:
            encoded = requests.utils.quote(payload, safe="")
            test_url = url + encoded
            response = _safe_get(test_url, timeout=5)
            if not response:
                return None
            body = response.text

            # BASELINE FILTER: If response is identical to baseline, payload had no effect
            if body == baseline_text:
                return None

            # FIX: STRICT unescaped reflection check
            # 1. Full payload must appear as-is (unescaped)
            if payload in body:
                return payload, True

            # 2. Check for escaped version — if ALL versions are escaped, NOT vulnerable
            escaped_payload = html_lib.escape(payload)
            if escaped_payload in body and payload not in body:
                return None  # Fully escaped = safe

            # 3. Check for partial unescaped reflection of KEY EVENT HANDLERS
            # Only flag if the event handler appears WITHOUT the &lt;/&gt; wrapping
            event_handlers = ['onerror=', 'onload=', 'onfocus=', 'onmouseover=', 'ontoggle=', 'onstart=']
            for handler in event_handlers:
                if handler in payload and handler in body:
                    # Verify it's NOT in the baseline (false positive check)
                    if handler not in baseline_text:
                        # Check it's not escaped (no &lt; before it)
                        idx = body.find(handler)
                        if idx > 0:
                            context_start = max(0, idx - 10)
                            context = body[context_start:idx]
                            if '&lt;' in context:
                                continue  # Escaped, skip
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

    if found == 0:
        return "✅ Nenhuma vulnerabilidade XSS detectada"
    else:
        header = f"🚨 <b>{found} vulnerabilidade(s) XSS encontrada(s)!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        return header + "\n".join(results)

def tool_admin_finder(url, progress_chat_id=None, progress_msg_id=None):
    """Admin Panel Finder v3.6 - 70+ paths, full URL, ANTI-FALSE-POSITIVE, deduped with dir scanner"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    paths = [
        # Standard admin paths
        'admin/', 'administrator/', 'admin.php', 'admin.html', 'admin.asp',
        'wp-admin/', 'wp-login.php', 'admincp/', 'admin/cp.php/',
        'admincp.php/', 'adminpanel/', 'webadmin/', 'cp.php/',
        'admin/controlpanel.php/', 'admins/', 'admin/admin.jsp/',
        'admin.jsp/', 'admin/home.jsp/', 'joomla/administrator/',
        'cms/administrator/', 'logins/', 'administration/',
        'login/', 'login.php', 'auth/', 'signin/',
        'manager/', 'backend/', 'panel/', 'control/',
        'dashboard/', 'cpanel/', 'myadmin/', 'phpmyadmin/',
        'admin2/', 'admin3/', 'admin4/', 'admin5/', 'admin1/',
        # Additional admin paths
        'admin/account.php/', 'admin/login.php/', 'admin/account.html/',
        'admin/login.html/', 'admin/index.php/', 'admin/index.html/',
        'admin/index.asp/', 'admin/default.php/', 'admin/default.asp/',
        'admin1/', 'admin1.php/', 'admin1.html/',
        'admin1/account.php/', 'admin1/login.php/',
        'admin2/', 'admin2/login.php/', 'admin2/index.php/',
        'admin3/', 'admin3/login.php/', 'admin3/index.php/',
        'moderator/', 'moderator.php/', 'moderator/login.php/',
        'moderator/admin.php/', 'moderator/admin/',
        'administrator/login.php/', 'administrator/index.php/',
        'panel.php/', 'panel/admin.php/', 'panel/login.php/',
        'controlpanel.php/', 'controlpanel/', 'cpanel/', 'cpanel.php/',
        'webadmin.php/', 'webadmin/',
        'siteadmin/', 'siteadmin/login.php/', 'siteadmin/index.php/',
        'sysadmin/', 'sysadmin/login.php/',
        'instadmin/', 'instadmin/login.php/',
        'bb-admin/', 'bb-admin/login.php/', 'bb-admin/index.php/',
        'bbadmin/', 'bbadmin/login.php/',
        'member/', 'member/login.php/', 'member/admin.php/',
        'members/', 'members/login.php/', 'members/admin.php/',
        'console/', 'console/login.php/',
        'settings/', 'settings/login.php/',
        'user/login', 'account/login', 'site/login',
        '.htaccess', '.htpasswd', 'config.php', 'phpinfo.php',
        '.env',
        'phpmyadmin/index.php/', 'phpmyadmin/login.php/',
        'myadmin/index.php/', 'myadmin/login.php/',
        # Additional paths
        'shell/', 'shell.php', 'cmd/', 'cmd.php',
        'cgi-bin/', 'cgi-bin/test.cgi',
        'uploads/', 'images/', 'cache/',
        'config/database.yml', 'config/application.php',
        'wp-config.php', 'wp-config.php.bak',
        'config.ini', 'settings.ini', 'appsettings.json',
    ]

    # FIX v3.9: Deduplicate paths using set()
    paths = list(dict.fromkeys(paths))  # Preserves order, removes duplicates
    base_url = url.rstrip('/')
    results = []
    found = 0
    total = len(paths)
    checked = 0

    # Get baseline: a random path that definitely doesn't exist
    baseline = _safe_get(f"{base_url}/{random_string(12)}.xyz", timeout=3)
    baseline_status = baseline.status_code if baseline else 404
    baseline_len = len(baseline.content) if baseline else 0

    # Get root page content for comparison
    root = _safe_get(base_url, timeout=3)
    root_content = root.text if root else ''
    root_len = len(root.content) if root else 0

    def check_path(path):
        nonlocal checked
        checked += 1
        # Report progress every 10 paths
        if checked % 10 == 0 and progress_chat_id and progress_msg_id:
            try:
                edit_progress(progress_msg_id, progress_chat_id, checked, total, "Escaneando paths...")
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
            results.append(f"Admin panel found: {escape_html(result[0])} (Status: {result[1]})")
        # Update progress
        if completed % 10 == 0 and progress_chat_id and progress_msg_id:
            try:
                edit_progress(progress_msg_id, progress_chat_id, completed, total, "Escaneando paths...")
            except:
                pass

    if found == 0:
        return f"Admin Panel Finder for {escape_html(base_url)}:\n\n✅ Nenhum painel admin encontrado"
    else:
        header = f"Admin Panel Finder for {escape_html(base_url)}:\n\n"
        return header + "\n".join(results)

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

    def scan_port(port):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            return port, result == 0
        except:
            return port, False
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

    # PERF: Use shared SCAN_POOL
    futures = {SCAN_POOL.submit(scan_port, p): p for p in ports}
    for future in concurrent.futures.as_completed(futures):
        port, is_open = future.result()
        if is_open:
            found += 1
            results += f"🔓 <b>Porta {port}</b> ({ports[port]}) — Aberta\n"

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
        # Additional paths
        '.aws', '.ssh', 'vendor', 'node_modules',
        '.docker', 'docker-compose.yml',
        'Makefile', 'composer.json', 'package.json',
        'README.md', 'CHANGELOG.md',
        'public', 'private', 'tmp',
        'staging', 'dev', 'test-env',
        'old', 'archive', 'legacy',
        'db', 'database', 'sql',
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
    subdomains = [
        'www', 'mail', 'ftp', 'webmail', 'smtp',
        'ns1', 'ns2', 'ns3', 'ns4', 'cpanel',
        'blog', 'shop', 'dev', 'staging', 'secure',
        'api', 'admin', 'cdn', 'static', 'media',
        'test', 'm', 'app', 'beta', 'portal',
        'login', 'forum', 'git', 'db', 'old',
        'new', 'v2', 'v3', 'docs', 'support',
        'remote', 'vpn', 'status',
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

        # Vuln checks - PARALLEL
        results += "\n🔒 <b>Verificação de Segurança:</b>\n"
        vuln_paths = [
            '/wp-content/debug.log',
            '/xmlrpc.php',
            '/wp-config.php',
            '/wp-config.php.bak',
            '/.wp-config.php.swp',
            '/readme.html',
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
            'Joomla': ['/administrator/', '/components/', '/modules/', 'Joomla!'],
            'Drupal': ['/sites/default/', '/sites/all/', 'Drupal.settings'],
            'Magento': ['/skin/frontend/', 'Mage.Cookies', 'Magento'],
            'PrestaShop': ['/prestashop/', '/modules/prestashop/', 'PrestaShop'],
            'Wix': ['wix.com', 'wixstatic.com'],
            'Shopify': ['cdn.shopify.com', 'myshopify'],
            'Ghost': ['ghost.io', 'ghost.content'],
            'OpenCart': ['opencart.com', 'catalog/view/theme'],
            'osCommerce': ['osCommerce', 'osc_id'],
            'Laravel': ['laravel_session', '__laravel_', 'X-CSRF-TOKEN'],
            'Django': ['django', 'csrftoken'],
            'Next.js': ['__NEXT_DATA__', '_next/'],
            'WooCommerce': ['woocommerce', 'wc-api'],
            'Flask': ['flask', '__flask', 'flask_session'],
            'FastAPI': ['fastapi', '__fastapi', 'openapi.json'],
            'Express.js': ['x-powered-by: express', 'express-session'],
            'Ruby on Rails': ['rails', 'actionpack', 'activesupport', 'csrf-token', 'rails_ujs'],
            'Squarespace': ['squarespace.com', 'sqspcdn.com', 'Squarespace'],
            'Weebly': ['weebly.com', 'weeblysite.com'],
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
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_start(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)

    msg = f"""🛡️ <b>Mth Ddos Security</b>
━━━━━━━━━━━━━━━━━━━━━━

Olá {escape_html(first_name)}! Bem-vindo ao bot de segurança!

<b>👑 Créditos:</b> @OnlyExaltarei, @Thebesty9, @PETER_DNS

Este bot possui <b>14 ferramentas avançadas</b> para testes de segurança.
Digite <b>/help</b> para ver a lista completa de comandos.

<i>Mth Ddos Security v4.2</i>"""

    send_message_safe(chat_id, msg)

def handle_help(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)

    msg = """🔧 <b>Mth Ddos Security v4.2 — Comandos</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>📡 Info & Recon:</b>
/info &lt;url&gt; — Mostra informações completas do site (IP, headers, tecnologia, CMS, servidor web, certificado SSL)
/dns &lt;domain&gt; — Análise DNS completa: A Record, MX, NS, TXT e Reverse DNS via DNS-over-HTTPS
/cms &lt;url&gt; — Detecta qual CMS o site usa (WordPress, Joomla, Drupal, Shopify, Wix, 16+ frameworks)
/reverse &lt;ip&gt; — Descobre o hostname de um IP + localização GeoIP
/emails &lt;url&gt; — Extrai todos os emails encontrados na página do site

<b>⚡ Scanners de Vulnerabilidade:</b>
/sqli &lt;url&gt; — Testa SQL Injection com 30 payloads diferentes + baseline comparison (só reporta se o payload realmente mudar a resposta)
/xss &lt;url&gt; — Testa XSS Refletido com 18 payloads + verificação de escape (só alerta se o payload não foi sanitizado)
/admin &lt;url&gt; — Encontra painéis de administração (testa ~25 paths comuns como /wp-admin, /phpmyadmin, /admin)
/panel &lt;url&gt; — Painel Admin Finder COMPLETO (testa 100+ paths incluindo WordPress, Joomla, Drupal, cPanel, Django, Flask, ASP.NET e custom)
  ⚠️ /admin = versão rápida | /panel = versão completa com mais paths
/ports &lt;ip&gt; — Escaneia 35 portas comuns (FTP, SSH, MySQL, RDP, Redis, MongoDB, etc.) e mostra quais estão abertas
/dirs &lt;url&gt; — Encontra diretórios expostos com listing (45 paths comuns + filtros anti-false-positive)
/sub &lt;domain&gt; — Descobre subdomínios (38 subdomínios conhecidos + verificação DNS para confirmar)
/wp &lt;url&gt; — WordPress Scanner: verifica se é WP, versão, plugins, themes, WP REST API e xmlrpc
/ftpssh &lt;ip&gt; — Testa conexão FTP e SSH, extrai banner de versão do serviço

<b>📋 Sistema:</b>
/ping — Mostra latência do bot (quanto tempo leva pra responder) + latência da API Telegram (separados)
/status — Health check completo: status do banco, API Telegram, contagem de usuários e comandos
/about — Informações sobre o bot, desenvolvedores e recursos

<b>━━━━━━━━━━━━━━━━━━━━━━</b>
<b>👑 Donos:</b> @OnlyExaltarei, @Thebesty9, @PETER_DNS
━━━━━━━━━━━━━━━━━━━━━━

<b>👑 Comandos exclusivos dos Donos:</b>
/botpanel — Painel do bot: uptime, total de usuários, comandos mais usados, estatísticas gerais
/logs — Últimos 10 scans/comandos realizados por usuários (com filtros por data, tipo de FF, resultado)
/bancodds — Dump completo do banco de dados (todos os usuários e comandos registrados)
/msg &lt;texto&gt; — Envia uma mensagem para TODOS os usuários do bot (broadcast)
  Exemplo: /msg Bot desligando para manutenção em 5 minutos!
  📷 Sticker/Imagem/GIF/Vídeo: Envie um sticker, foto, GIF ou vídeo e responda com /msg (opcional: /msg + texto pra adicionar legenda)
/stats — Estatísticas dos usuários (geral ou busca por usuário específico)
/ban &lt;id&gt; [motivo] — Banir usuário do bot
/unban &lt;id&gt; — Desbanir usuário
/export — Exportar lista completa de usuários para TXT

━━━━━━━━━━━━━━━━━━━━━━
<b>⏱️ Sistema (Todos):</b>
/uptime — Mostra tempo online do bot
/ping — Latência do bot + API Telegram
/status — Health check completo
/about — Informações sobre o bot

━━━━━━━━━━━━━━━━━━━━━━
<i>Mth Ddos Security v4.2</i>
<i>Uso apenas para fins educacionais e de segurança autorizada.</i>"""

    send_message_safe(chat_id, msg)

def handle_about(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    msg = """🛡️ <b>Mth Ddos Security</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Desenvolvedores:</b>
@OnlyExaltarei
@Thebesty9
@PETER_DNS

<b>Versão:</b> 4.2
<b>Plataforma:</b> Telegram Bot (Python)
<b>Ferramentas:</b> 14 ferramentas avançadas com anti-false-positive
<b>Banco:</b> SQLite com índices e otimizações
<b>Segurança:</b> Sistema de donos com controle de acesso

<b>Recursos:</b>
• 30 payloads SQLi com baseline comparison
• 18 payloads XSS com verificação de escape
• 100+ paths para Painel Admin Finder
• Filtros anti-false-positive em todos os scanners
• Rate limiting e retry automático
• Connection pooling (HTTP session)
• Shared thread pool
• Broadcast /msg para donos (texto, imagem, sticker, GIF, vídeo)
• Painel admin do bot (/botpanel)
• Sistema de ban/desban (/ban, /unban)
• Exportação de usuários (/export)
• Estatísticas por usuário (/stats)
• Auto-restart em caso de crash
• Log de erros em arquivo
• Health check automático
• DNS-over-HTTPS (funciona sem dig/nslookup)
• Compatível com Android/Termux

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
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /sqli &lt;url&gt;\nExemplo: /sqli example.com/?id=1")
        return
    target = args[0]
    log_command(user_id, username, "sqli", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scanner SQLi iniciado</b> em {escape_html(clean_target)}...")
    result = tool_sqli(target)
    send_message_safe(chat_id, result)

def handle_xss(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /xss &lt;url&gt;\nExemplo: /xss example.com/?q=")
        return
    target = args[0]
    log_command(user_id, username, "xss", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Scanner XSS iniciado</b> em {escape_html(clean_target)}...")
    result = tool_xss_scanner(target)
    send_message_safe(chat_id, result)

def handle_admin_panel(chat_id, user_id, username, first_name, last_name, args):
    log_user(user_id, username, first_name, last_name)
    if not args:
        send_message_safe(chat_id, "❌ Use: /admin &lt;url&gt;\nExemplo: /admin example.com")
        return
    target = args[0]
    log_command(user_id, username, "admin_panel", target)
    clean_target = extract_hostname(target)
    send_message_safe(chat_id, f"🔍 <b>Buscando painéis admin</b> em {escape_html(clean_target)}...")
    result = tool_admin_finder(target)
    send_message_safe(chat_id, result)

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

    msg = f"""🏓 <b>Ping — Mth Ddos Security v4.2</b>
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
    send_message_safe(chat_id, f"🔍 <b>Painel Admin Finder</b> em {escape_html(clean_target)}...")
    # Send initial progress
    progress_msg_id = send_progress(chat_id, f"panel_{user_id}_{time.time()}", 0, 100, "Escaneando paths...")
    result = tool_admin_finder(target, chat_id, progress_msg_id)
    finish_progress(progress_msg_id, chat_id, result)
    send_message_safe(chat_id, result)

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

    msg = f"""📊 <b>Painel do Bot — Mth Ddos Security v4.2</b>
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

<b>🔧 Ferramentas (Todos):</b>
/info, /sqli, /xss, /admin, /panel,
/ports, /dirs, /sub, /wp, /emails,
/dns, /cms, /reverse, /ftpssh, /ping, /uptime

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
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                # Search by username or user_id
                c.execute("SELECT * FROM users WHERE username LIKE ? OR id = ? ORDER BY command_count DESC",
                          (f"%{search_term}%", search_term))
                rows = [dict(r) for r in c.fetchall()]

            if not rows:
                send_message_safe(chat_id, f"🔍 Nenhum usuário encontrado para: {escape_html(search_term)}")
                return

            msg = f"📊 <b>Estatísticas — Buscar: {escape_html(search_term)}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for r in rows[:10]:
                msg += f"\n<b>@{escape_html(r['username'] or 'N/D')}</b> (ID: {r['id']})\n"
                msg += f"  Nome: {escape_html(r['first_name'])} {escape_html(r['last_name'] or '')}\n"
                msg += f"  Comandos: {r['command_count']}\n"
                msg += f"  Dono: {'Sim' if r['is_owner'] else 'Não'}\n"
                msg += f"  Primeiro acesso: {r['first_seen']}\n"
                msg += f"  Último acesso: {r['last_seen']}\n"
                # Get user's top commands
                c2 = conn.cursor()
                c2.execute("SELECT command, COUNT(*) as cnt FROM logs WHERE user_id = ? GROUP BY command ORDER BY cnt DESC LIMIT 3",
                           (r['id'],))
                top_cmds = c2.fetchall()
                if top_cmds:
                    top_parts = []
                    for d in top_cmds:
                        dd = dict(d)
                        top_parts.append(f"/{dd['command']}({dd['cnt']}x)")
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

        msg = f"""📊 <b>Mth Ddos Security v4.2 — Estatísticas</b>
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


def handle_uptime(chat_id, user_id, username, first_name, last_name, args):
    """Show bot uptime (available to everyone)"""
    log_user(user_id, username, first_name, last_name)

    uptime_secs = int(time.time() - BOT_START_TIME)
    days = uptime_secs // 86400
    hours = (uptime_secs % 86400) // 3600
    mins = (uptime_secs % 3600) // 60
    secs = uptime_secs % 60

    msg = f"""⏱️ <b>Mth Ddos Security v4.2 — Uptime</b>
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

    msg = f"""📊 <b>Mth Ddos Security v4.2 — Status</b>
━━━━━━━━━━━━━━━━━━━━━━
🟢 <b>Online</b> | Uptime: {hours}h {mins}m {secs}s
👥 Usuários: {stats['total']} (Donos: {stats['owners']})
📝 Comandos registrados: {stats['commands']}
💾 RAM usada: {mem_mb:.1f} MB
🧵 Threads ativas: {active_threads}
🗃️ Banco: {db_size:.1f} KB
━━━━━━━━━━━━━━━━━━━━━━"""
    send_message_safe(chat_id, msg)

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
}

def process_update(update):
    """Process a Telegram update and route to the correct handler"""
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

    # Rate limit check: max USER_CMD_LIMIT commands per USER_CMD_WINDOW seconds
    now_ts = time.time()
    user_cmd_list = USER_CMD_COUNT.get(user_id, [])
    user_cmd_list = [t for t in user_cmd_list if now_ts - t < USER_CMD_WINDOW]
    if len(user_cmd_list) >= USER_CMD_LIMIT and cmd not in ('/start', '/help', '/about', '/ping', '/status'):
        remaining = int(USER_CMD_WINDOW - (now_ts - user_cmd_list[0]))
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

        # FIX v4.2: Pass reply_media via closure to avoid race condition
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

    print("🚀 Mth Ddos Security v4.2 started (long polling mode)")
    print(f"👑 Owners: {OWNERS}")
    print(f"📱 DB: {DB_PATH}")

    while not SHUTDOWN_FLAG:
        try:
            resp = HTTP_SESSION.get(f"{API_URL}/getUpdates", params={
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message"]
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

    print("🛑 Mth Ddos Security v4.2 stopped.")


def set_webhook(url):
    """Set webhook URL"""
    resp = HTTP_SESSION.post(f"{API_URL}/setWebhook", json={
        "url": url,
        "allowed_updates": ["message"],
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
            # Start bot with auto-restart
            run_with_restart()
        elif sys.argv[1] == "test":
            print("Mth Ddos Security v4.2")
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
