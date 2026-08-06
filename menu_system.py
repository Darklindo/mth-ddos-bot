#!/usr/bin/env python3
"""
Script to add the interactive menu system to Mth_Ddos_v50.py
Adds:
- Main menu with category pages
- VIP exclusive page
- Owner exclusive page
- Target input flow (user clicks button -> bot asks for target -> runs scan)
- Navigation callbacks
"""

import re

# Read the file
with open('Mth_Ddos_v50.py', 'r') as f:
    content = f.read()

lines = content.split('\n')

# ============================================================
# STEP 1: Add PENDING_TARGETS state dict after USER_LANG
# ============================================================

insert_after_line = None
for i, line in enumerate(lines):
    if 'USER_LANG: dict = {}' in line:
        insert_after_line = i
        break

if insert_after_line is None:
    print("ERROR: Could not find USER_LANG dict")
    exit(1)

pending_targets_code = """
# ═══════════════════════════════════════════════════════════════
#  MENU SYSTEM — Target input state
# ═══════════════════════════════════════════════════════════════
# PENDING_TARGETS[user_id] = {'cmd': 'sqli', 'tier': 'normal', 'page': 'vulns'}
# When user clicks a scanner button, we store what they want to run
# Then when they send a URL, we execute it
PENDING_TARGETS: dict = {}  # user_id -> {cmd, tier}"""

lines.insert(insert_after_line + 1, pending_targets_code)

# ============================================================
# STEP 2: Rewrite handle_start to show the main menu
# ============================================================

# Find handle_start
start_line = None
for i, line in enumerate(lines):
    if 'def handle_start(' in line:
        start_line = i
        break

# Find the end of handle_start (next def at same indent level)
start_end = None
for i in range(start_line + 1, len(lines)):
    if lines[i].startswith('def ') or lines[i].startswith('class '):
        start_end = i
        break

if start_line and start_end:
    new_handle_start = '''def handle_start(chat_id, user_id, username, first_name, last_name, args=None):
    log_user(user_id, username, first_name, last_name)
    show_main_menu(chat_id, user_id, username, first_name)

'''
    # Replace the old handle_start
    lines[start_line:start_end] = new_handle_start.split('\n')

print(f"Rewrote handle_start (lines {start_line}-{start_end})")

# ============================================================
# STEP 3: Add the menu system functions before handle_help
# ============================================================

help_line = None
for i, line in enumerate(lines):
    if 'def handle_help(' in line and i > 4000:
        help_line = i
        break

if help_line is None:
    print("ERROR: Could not find handle_help")
    exit(1)

menu_functions = '''
# ═══════════════════════════════════════════════════════════════
#  INTERACTIVE MENU SYSTEM v5.2
# ═══════════════════════════════════════════════════════════════

def show_main_menu(chat_id, user_id, username='', first_name=''):
    """Show the main menu with category buttons"""
    owner = is_owner(user_id)
    vip = is_vip(user_id)
    display_name = first_name or username or 'User'
    
    msg = f"🛡️ <b>MTH Security v5.2</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
    msg += f"👋 Olá, <b>{escape_html(display_name)}</b>!\\n\\n"
    msg += "Selecione uma categoria para começar:\\n\\n"
    
    buttons = [
        [{"text": "🎯 Explorar Vulnerabilidades", "callback_data": "menu:vulns"},
         {"text": "🔍 Reconhecimento", "callback_data": "menu:recon"}],
        [{"text": "🛡️ Auditoria de Segurança", "callback_data": "menu:audit"},
         {"text": "📂 Arquivos & Diretórios", "callback_data": "menu:files"}],
    ]
    
    if vip or owner:
        buttons.append([{"text": "⭐ Ferramentas VIP", "callback_data": "menu:vip"}])
    
    if owner:
        buttons.append([{"text": "👑 Ferramentas DONO", "callback_data": "menu:owner"}])
    
    buttons.append([
        {"text": "📊 /stats", "callback_data": "menu:stats"},
        {"text": "🔧 /help", "callback_data": "cmd:help"},
        {"text": "ℹ️ /about", "callback_data": "cmd:about"}
    ])
    buttons.append([{"text": "🌐 Idioma", "callback_data": "menu:lang"}])
    
    send_message_with_buttons(chat_id, msg, buttons)

def show_menu_vulns(chat_id, user_id):
    """Show Vulnerability Exploration page"""
    buttons = [
        [{"text": "SQLi Scanner", "callback_data": "target:sqli:normal"},
         {"text": "XSS Scanner", "callback_data": "target:xss:normal"}],
        [{"text": "Admin Panel Finder", "callback_data": "target:admin:normal"},
         {"text": "Port Scanner", "callback_data": "target:ports:normal"}],
        [{"text": "Directory Scanner", "callback_data": "target:dirs:normal"},
         {"text": "Subdomain Scanner", "callback_data": "target:sub:normal"}],
        [{"text": "WordPress Scanner", "callback_data": "target:wp:normal"},
         {"text": "FTP/SSH Scanner", "callback_data": "target:ftpssh:normal"}],
        [{"text": "Email Scraper", "callback_data": "target:emails:normal"},
         {"text": "CMS Detector", "callback_data": "target:cms:normal"}],
        [{"text": "Reverse IP Lookup", "callback_data": "target:reverse:normal"},
         {"text": "DNS Tools", "callback_data": "target:dns:normal"}],
        [{"text": "🔄 ScanAll (6 scanners)", "callback_data": "target:scanall:normal"},
         {"text": "💀 Deep Scan (vulns)", "callback_data": "target:deep:normal"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    send_message_with_buttons(chat_id, 
        "🎯 <b>Explorar Vulnerabilidades</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "Selecione uma ferramenta. Você precisará inserir o alvo (URL, domínio ou IP) na próxima mensagem.\\n",
        buttons)

def show_menu_recon(chat_id, user_id):
    """Show Reconnaissance page"""
    buttons = [
        [{"text": "Website Information", "callback_data": "target:info:normal"},
         {"text": "Whois Lookup", "callback_data": "target:whois:normal"}],
        [{"text": "GeoIP Analysis", "callback_data": "target:ip:normal"},
         {"text": "Traceroute", "callback_data": "target:traceroute:normal"}],
        [{"text": "DNS Tools", "callback_data": "target:dns:normal"},
         {"text": "Subdomain Scanner", "callback_data": "target:sub:normal"}],
        [{"text": "Tech Detection", "callback_data": "target:tech:normal"},
         {"text": "CMS Detector", "callback_data": "target:cms:normal"}],
        [{"text": "Reverse IP Lookup", "callback_data": "target:reverse:normal"},
         {"text": "Email Scraper", "callback_data": "target:emails:normal"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    send_message_with_buttons(chat_id,
        "🔍 <b>Reconhecimento</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "Ferramentas de reconhecimento e informação sobre o alvo.\\n\\n"
        "Selecione uma ferramenta para começar.\\n",
        buttons)

def show_menu_audit(chat_id, user_id):
    """Show Security Audit page"""
    buttons = [
        [{"text": "SSL Audit", "callback_data": "target:ssl:normal"},
         {"text": "SSL Chain", "callback_data": "target:sslchain:normal"}],
        [{"text": "Headers Analysis", "callback_data": "target:headers:normal"},
         {"text": "HTTP Analysis", "callback_data": "target:http:normal"}],
        [{"text": "CORS Test", "callback_data": "target:cors:normal"},
         {"text": "Security Rating", "callback_data": "target:rate:normal"}],
        [{"text": "Robots.txt", "callback_data": "target:robots:normal"},
         {"text": "Sitemap Analysis", "callback_data": "target:sitemap:normal"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    send_message_with_buttons(chat_id,
        "🛡️ <b>Auditoria de Segurança</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "Ferramentas de auditoria e análise de segurança.\\n\\n"
        "Selecione uma ferramenta para começar.\\n",
        buttons)

def show_menu_files(chat_id, user_id):
    """Show Files & Directories page"""
    buttons = [
        [{"text": "Admin Panel Finder", "callback_data": "target:admin:normal"},
         {"text": "Directory Scanner", "callback_data": "target:dirs:normal"}],
        [{"text": "Port Scanner", "callback_data": "target:ports:normal"},
         {"text": "FTP/SSH Scanner", "callback_data": "target:ftpssh:normal"}],
        [{"text": "Exposed Files", "callback_data": "target:exposed:normal"},
         {"text": "Backup Finder", "callback_data": "target:backup:normal"}],
        [{"text": "Config Scanner", "callback_data": "target:config:normal"},
         {"text": "Webshell Hunter", "callback_data": "target:shell:normal"}],
        [{"text": "API Discovery", "callback_data": "target:api:normal"},
         {"text": "WordPress Scanner", "callback_data": "target:wp:normal"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    send_message_with_buttons(chat_id,
        "📂 <b>Arquivos & Diretórios</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "Ferramentas para buscar arquivos expostos, diretórios e configurações.\\n\\n"
        "Selecione uma ferramenta para começar.\\n",
        buttons)

def show_menu_vip(chat_id, user_id):
    """Show VIP exclusive page"""
    owner = is_owner(user_id)
    if not is_vip(user_id) and not owner:
        send_msg(user_id, chat_id, "❌ Esta seção é exclusiva para membros VIP.")
        return
    
    buttons = [
        [{"text": "⭐ SQLi VIP (WAF Bypass)", "callback_data": "target:sqli:vip"},
         {"text": "⭐ XSS VIP (Deep DOM)", "callback_data": "target:xss:vip"}],
        [{"text": "⭐ ScanAll VIP", "callback_data": "target:scanall:vip"},
         {"text": "⭐ Deep Scan VIP", "callback_data": "target:deep:vip"}],
        [{"text": "⭐ Port VIP (1000+ ports)", "callback_data": "target:ports:vip"},
         {"text": "⭐ Headers VIP", "callback_data": "target:headers:vip"}],
        [{"text": "⭐ DNS VIP (All Records)", "callback_data": "target:dns:vip"},
         {"text": "⭐ Tech VIP (WAF/CDN)", "callback_data": "target:tech:vip"}],
        [{"text": "⭐ Admin VIP (200+ paths)", "callback_data": "target:admin:vip"},
         {"text": "⭐ API VIP (GraphQL)", "callback_data": "target:api:vip"}],
        [{"text": "⭐ CORS VIP (Multi-origin)", "callback_data": "target:cors:vip"},
         {"text": "⭐ Exposed VIP (Sensitive)", "callback_data": "target:exposed:vip"}],
        [{"text": "⭐ Backup VIP", "callback_data": "target:backup:vip"},
         {"text": "⭐ Config VIP", "callback_data": "target:config:vip"}],
        [{"text": "⭐ Webshell VIP", "callback_data": "target:shell:vip"},
         {"text": "⭐ Robots VIP", "callback_data": "target:robots:vip"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    
    badge = "👑 OWNER + ⭐ VIP" if owner else "⭐ VIP"
    send_message_with_buttons(chat_id,
        f"⭐ <b>Ferramentas VIP</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        f"<b>Acesso:</b> {badge}\\n\\n"
        f"Scanners VIP possuem 3x mais payloads, WAF bypass, análise profunda e detecção avançada.\\n\\n"
        f"Selecione uma ferramenta VIP para começar.\\n",
        buttons)

def show_menu_owner(chat_id, user_id):
    """Show Owner exclusive page"""
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Esta seção é exclusiva para DONOS.")
        return
    
    buttons = [
        [{"text": "👑 Forensic Analysis", "callback_data": "cmd:forensic"},
         {"text": "👑 Pentest Automation", "callback_data": "cmd:pentest"}],
        [{"text": "👑 OSINT Intelligence", "callback_data": "cmd:osint"},
         {"text": "👑 SQLi Owner (0-day)", "callback_data": "target:sqli:owner"}],
        [{"text": "👑 XSS Owner (Blind+DOM)", "callback_data": "target:xss:owner"},
         {"text": "👑 ScanAll Owner", "callback_data": "target:scanall:owner"}],
        [{"text": "👑 Deep Owner", "callback_data": "target:deep:owner"},
         {"text": "👑 Port Owner (Vuln)", "callback_data": "target:ports:owner"}],
        [{"text": "👑 SSL Owner (Protocols)", "callback_data": "target:ssl:owner"},
         {"text": "👑 Headers Owner (CORS)", "callback_data": "target:headers:owner"}],
        [{"text": "👑 DNS Owner (Brute)", "callback_data": "target:dns:owner"},
         {"text": "👑 Tech Owner (CVE)", "callback_data": "target:tech:owner"}],
        [{"text": "👑 API Owner (Fuzzing)", "callback_data": "target:api:owner"},
         {"text": "👑 Config Owner (Creds)", "callback_data": "target:config:owner"}],
        [{"text": "👑 Exposed Owner (Git)", "callback_data": "target:exposed:owner"},
         {"text": "👑 Shell Owner (Encoded)", "callback_data": "target:shell:owner"}],
        [{"text": "🔙 Voltar ao Menu", "callback_data": "menu:back"}],
    ]
    
    send_message_with_buttons(chat_id,
        "👑 <b>Ferramentas DONO</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
        "<b>Acesso Exclusivo:</b> Apenas Donos\\n\\n"
        "Os scanners Owner incluem 0-day patterns, blind extraction, full WAF bypass, "
        "análise forense, pentest automation e OSINT intelligence.\\n\\n"
        "Selecione uma ferramenta para começar.\\n",
        buttons)

'''

lines[help_line:help_line] = menu_functions.split('\n')

# Re-find indices after insertion
print(f"Added menu functions before handle_help")

# ============================================================
# STEP 4: Add callback handlers for menu navigation
# ============================================================

# Find the tier: callback handler to insert menu callbacks before it
tier_callback_line = None
for i, line in enumerate(lines):
    if "if cb_data.startswith('tier:')" in line:
        tier_callback_line = i
        break

if tier_callback_line is None:
    print("ERROR: Could not find tier: callback")
    exit(1)

menu_callbacks = '''        # ═══════════════════════════════════════════════════════════
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
            handle_stats(chat_id, user_id, username, first_name, last_name)
            return
        
        if cb_data == 'menu:lang':
            buttons = [
                [{"text": "🇧🇷 Português", "callback_data": "setlang:pt"},
                 {"text": "🇺🇸 English", "callback_data": "setlang:en"},
                 {"text": "🇪🇸 Español", "callback_data": "setlang:es"}],
                [{"text": "🔙 Voltar", "callback_data": "menu:back"}],
            ]
            send_message_with_buttons(chat_id, 
                "🌐 <b>Selecione seu idioma</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n",
                buttons)
            return
        
        # Owner-exclusive command callbacks
        if cb_data == 'cmd:forensic':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_forensic(chat_id, user_id, username, first_name, last_name, args if args else [])
            return
        
        if cb_data == 'cmd:pentest':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_pentest(chat_id, user_id, username, first_name, last_name, args if args else [])
            return
        
        if cb_data == 'cmd:osint':
            if not is_owner(user_id):
                send_msg(user_id, chat_id, "❌ Este comando é exclusivo para DONOS.")
                return
            handle_osint(chat_id, user_id, username, first_name, last_name, args if args else [])
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
                }
                cmd_name = cmd_display.get(scan_cmd, scan_cmd)
                tier_badge = "⭐ VIP" if tier == 'vip' else "👑 OWNER" if tier == 'owner' else ""
                if tier_badge:
                    tier_badge = f" ({tier_badge})"
                
                buttons = [[{"text": "❌ Cancelar", "callback_data": "menu:cancel_target"}]]
                send_message_with_buttons(chat_id,
                    f"📋 <b>Insira o alvo</b>{tier_badge}\\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
                    f"Ferramenta: <b>{cmd_name}</b>\\n\\n"
                    f"Envie a URL, domínio ou IP do alvo.\\n"
                    f"<i>Exemplo: example.com, https://site.com, 192.168.1.1</i>\\n\\n"
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
                    "text": "❌ <b>Scan cancelado.</b>\\n━━━━━━━━━━━━━━━━━━━━━━\\n\\n"
                            "Volte ao menu principal para selecionar outra ferramenta.",
                    "parse_mode": "HTML",
                    "reply_markup": '{"inline_keyboard": [[{"text": "🔙 Menu Principal", "callback_data": "menu:back"}]]}'
                }, timeout=5)
            except:
                pass
            return
        
'''

lines[tier_callback_line:tier_callback_line] = menu_callbacks.split('\n')

print("Added menu callbacks before tier handler")

# ============================================================
# STEP 5: Add target input handling in message processing
# ============================================================

# Find the message processing section where cmd = parts[0]
target_input_line = None
for i, line in enumerate(lines):
    if "cmd = raw_cmd.split('@')[0]" in line:
        target_input_line = i
        break

if target_input_line is None:
    print("ERROR: Could not find cmd processing line")
    exit(1)

# Insert target input check BEFORE the cmd = line
target_input_code = '''    # ═══════════════════════════════════════════════════════════
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
                          'admin', 'ports', 'whois', 'rate',
                          'headers', 'dns', 'robots', 'tech',
                          'cms', 'exposed', 'backup', 'api',
                          'shell', 'config', 'cors', 'http', 'sslchain', 'ssl']
        
        if scan_cmd in TIERED_SCANNERS:
            fn_name = f"_run_{scan_cmd}_{tier}"
            fn = globals().get(fn_name)
            if fn:
                fn(chat_id, user_id, target)
                return
            else:
                # Fallback to normal
                fn_name = f"_run_{scan_cmd}_normal"
                fn = globals().get(fn_name)
                if fn:
                    fn(chat_id, user_id, target)
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
            return
    
'''

lines[target_input_line:target_input_line] = target_input_code.split('\n')

print("Added target input handling in message processing")

# Write the modified content back
with open('Mth_Ddos_v50.py', 'w') as f:
    f.write('\n'.join(lines))

print("\n✅ Menu system added successfully!")
print(f"Total lines: {len(lines)}")
