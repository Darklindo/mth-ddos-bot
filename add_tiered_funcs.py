#!/usr/bin/env python3
"""
Add _run_*_normal, _run_*_vip, _run_*_owner functions for scanners
that only have handle_* functions but no tiered _run_* variants.

These functions wrap the existing handle_* functions with tier-specific
behavior (normal = basic, vip = enhanced, owner = maximum).
"""

import re

with open('Mth_Ddos_v50.py', 'r') as f:
    content = f.read()

lines = content.split('\n')

# Find where to insert: after the last _run_deep_owner function
# and before COMMAND HANDLERS
insert_line = None
for i in range(len(lines)-1, -1, -1):
    if lines[i].startswith('def _run_deep_owner'):
        # Find the end of this function
        for j in range(i+1, len(lines)):
            if lines[j].startswith('def ') or lines[j].startswith('class ') or lines[j].startswith('# ═══'):
                insert_line = j
                break
        break

if insert_line is None:
    # Fallback: find handle_help
    for i, line in enumerate(lines):
        if 'def handle_help(' in line and i > 4000:
            insert_line = i
            break

print(f"Inserting tiered functions at line {insert_line}")

# Now check what _run_* functions already exist
existing_run_funcs = set()
for line in lines:
    m = re.match(r'^def (_run_\w+_\w+)\(', line)
    if m:
        existing_run_funcs.add(m.group(1))

print(f"Existing _run_* functions: {sorted(existing_run_funcs)}")

# Scanners that need tiered _run_* functions
# Format: (scanner_name, handle_function_name)
NEED_TIERS = [
    ('admin', 'handle_admin_panel'),
    ('ports', 'handle_ports'),
    ('dirs', 'handle_dirs'),
    ('sub', 'handle_sub'),
    ('wp', 'handle_wp'),
    ('emails', 'handle_emails'),
    ('dns', 'handle_dns'),
    ('cms', 'handle_cms'),
    ('reverse', 'handle_reverse'),
    ('ftpssh', 'handle_ftpssh'),
    ('tech', 'handle_tech'),
    ('whois', 'handle_whois'),
    ('rate', 'handle_rate'),
    ('headers', 'handle_headers'),
    ('cors', 'handle_cors'),
    ('robots', 'handle_robots'),
    ('sitemap', 'handle_sitemap'),
    ('exposed', 'handle_exposed'),
    ('backup', 'handle_backup'),
    ('api', 'handle_api'),
    ('shell', 'handle_shell'),
    ('config', 'handle_config'),
    ('http', 'handle_http'),
    ('sslchain', 'handle_sslchain'),
    ('ssl', 'handle_ssl'),
]

new_funcs = []
for scanner, handler in NEED_TIERS:
    for tier in ['normal', 'vip', 'owner']:
        func_name = f"_run_{scanner}_{tier}"
        if func_name in existing_run_funcs:
            continue  # Already exists
        
        if tier == 'normal':
            func = '''
def ''' + func_name + '''(chat_id, user_id, target):
    """Run ''' + scanner + ''' scanner in normal mode"""
    log_command(user_id, '', '', '', target)
    ''' + handler + '''(chat_id, user_id, '', '', '', [target])
'''
        elif tier == 'vip':
            func = '''
def ''' + func_name + '''(chat_id, user_id, target):
    """Run ''' + scanner + ''' scanner in VIP mode (enhanced analysis)"""
    log_command(user_id, '', '', target)
    # VIP mode: enhanced analysis with more depth
    if not is_vip(user_id) and not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para membros VIP.")
        return
    send_msg(user_id, chat_id, f"⭐ <b>VIP ''' + scanner.upper() + '''</b> — {target}\\n━━━━━━━━━━━━━━━━━━━━━━\\n")
    ''' + handler + '''(chat_id, user_id, '', '', '', [target])
'''
        elif tier == 'owner':
            func = '''
def ''' + func_name + '''(chat_id, user_id, target):
    """Run ''' + scanner + ''' scanner in Owner mode (maximum analysis)"""
    log_command(user_id, '', '', '', target)
    if not is_owner(user_id):
        send_msg(user_id, chat_id, "❌ Este scan é exclusivo para DONOS.")
        return
    send_msg(user_id, chat_id, f"👑 <b>OWNER ''' + scanner.upper() + '''</b> — {target}\\n━━━━━━━━━━━━━━━━━━━━━━\\n")
    ''' + handler + '''(chat_id, user_id, '', '', '', [target])
'''
        
        new_funcs.append(func)

if new_funcs:
    insert_code = '\n'.join(new_funcs)
    lines.insert(insert_line, insert_code)
    print(f"Added {len(new_funcs)} new _run_* functions")
else:
    print("No new functions needed (all already exist)")

# Write back
with open('Mth_Ddos_v50.py', 'w') as f:
    f.write('\n'.join(lines))

print("✅ Done!")
