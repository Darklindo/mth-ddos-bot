import ast

with open('Mth_Ddos_v50.py', 'r') as f:
    source = f.read()
    tree = ast.parse(source)

# 1. Top-level duplicate function names
top_level = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        if node.name in top_level:
            print(f"DUPLICATE top-level: {node.name} at {top_level[node.name]} and {node.lineno}")
        else:
            top_level[node.name] = node.lineno

print(f"\nTotal top-level functions: {len(top_level)}")

# 2. Find all nested functions named _clean_html, _get_whois_text, _clean, check_payload
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name in ('_clean_html', '_get_whois_text', '_clean', 'check_payload'):
        # Find parent function
        pass

# 3. Check for functions that are never called
# Get all function definitions and all function calls
func_defs = set()
func_calls = set()

class FuncDefVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defs = set()
        self.calls = set()
        
    def visit_FunctionDef(self, node):
        self.defs.add(node.name)
        self.generic_visit(node)
        
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        self.generic_visit(node)

visitor = FuncDefVisitor()
visitor.visit(tree)

# Functions defined but never called (excluding special ones)
special = {'main', 'handle_msg', '__init__', '__repr__', '__str__', '__eq__', '__hash__',
           'run_handler', 'scan_port', 'check_payload', 'check_dir', 'check_path', 'check_sub',
           'grab_banner', 'is_vip', 'is_owner', 'is_banned', 'get_user_lang', 'extract_hostname',
           'escape_html', 'send_msg', 'send_message_safe', 'log_user', 'log_command', 'log_error',
           'log_owner_command', '_safe_get', '_safe_post', 'audit_log', 'get_user_rate_limit',
           '_rate_limit_wait', 'handle_lang', 'show_main_menu', '_run_sqli_normal', 
           '_run_xss_normal', '_run_admin_normal', '_run_ports_normal', '_run_dirs_normal',
           '_run_sub_normal', '_run_wp_normal', '_run_dns_normal', '_run_cms_normal',
           '_run_reverse_normal', '_run_ftpssh_normal', '_run_info_normal', '_run_emails_normal',
           '_run_ssl_normal', '_run_headers_normal', '_run_cors_normal', '_run_robots_normal',
           '_run_sitemap_normal', '_run_tech_normal', '_run_exposed_normal', '_run_backup_normal',
           '_run_api_normal', '_run_shell_normal', '_run_config_normal', '_run_scanall',
           '_run_deep', '_run_quick', '_run_http', '_run_sslchain', 'handle_dashboard',
           'handle_portmon', 'handle_cooldown', 'handle_stats', 'handle_share', 'handle_rescan',
           'handle_feedback', 'handle_watch', 'handle_whois', 'handle_traceroute',
           'handle_history', 'handle_score', 'handle_dashboard', 'send_feedback_poll',
           'record_scan_history', 'send_share_result', 'record_badge', 'check_badges',
           'get_badge_def', '_clean_html', '_get_whois_text', '_clean', '_log_encrypted',
           'send_document', 'send_message_with_buttons', 'process_update', 'run_with_restart',
           'health_check_loop', 'backup_loop', 'check_updates', 'site_monitor_loop',
           'scheduled_task_loop', '_clean_html', '_get_whois_text'}

unused = func_defs - func_calls - special
# Filter out private helpers that might be called via strings
print(f"\nPotentially unused functions (may be called via strings):")
for fn in sorted(unused):
    if not fn.startswith('__'):
        # Check if it's in CMD_HANDLERS or other dict values
        print(f"  - {fn}")

# 4. Check for bare except: pass patterns in critical paths
class ExceptVisitor(ast.NodeVisitor):
    def __init__(self):
        self.bare_pass = []
        
    def visit_ExceptHandler(self, node):
        if node.body and len(node.body) == 1:
            if isinstance(node.body[0], ast.Pass):
                self.bare_pass.append(node.lineno)
        self.generic_visit(node)

except_visitor = ExceptVisitor()
except_visitor.visit(tree)
print(f"\nBare except: pass locations ({len(except_visitor.bare_pass)} total):")
for ln in except_visitor.bare_pass[:20]:
    print(f"  Line {ln}")
if len(except_visitor.bare_pass) > 20:
    print(f"  ... and {len(except_visitor.bare_pass) - 20} more")

# 5. Check for global variables modified without global keyword
# (This is hard to check via AST alone, but we can look for obvious cases)

# 6. Check for mutable default arguments
class MutableDefaultVisitor(ast.NodeVisitor):
    def __init__(self):
        self.mutable_defaults = []
        
    def visit_FunctionDef(self, node):
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.mutable_defaults.append(f"{node.name}:{node.lineno}")
        self.generic_visit(node)

mvisitor = MutableDefaultVisitor()
mvisitor.visit(tree)
print(f"\nMutable default arguments ({len(mvisitor.mutable_defaults)}):")
for item in mvisitor.mutable_defaults[:10]:
    print(f"  - {item}")

print("\n=== ANALYSIS COMPLETE ===")
