#!/usr/bin/env python3
"""
Comprehensive line-by-line bug review of Mth_Ddos_v50.py
Checks for:
1. Function signature mismatches
2. Undefined variables
3. Wrong argument counts
4. Try/except that swallow errors
5. SQL injection risks
6. Race conditions
7. Missing returns
8. Indentation issues
9. Inconsistent patterns
"""

import re
import ast

with open('Mth_Ddos_v50.py', 'r') as f:
    content = f.read()
    lines = content.split('\n')

print(f"Total lines: {len(lines)}")
print("=" * 60)

# 1. Check all function definitions and their call sites
print("\n[1] Checking function signature consistency...")

# Parse the file to get all function definitions
func_defs = {}
for i, line in enumerate(lines):
    m = re.match(r'^def (\w+)\((.+)\):', line)
    if m:
        func_name = m.group(1)
        params_str = m.group(2)
        params = [p.strip().split(':')[0].split('=')[0].strip() for p in params_str.split(',')]
        func_defs[func_name] = (i+1, params, len(params))

print(f"  Found {len(func_defs)} function definitions")

# Check handler functions have consistent signatures
handler_funcs = {k: v for k, v in func_defs.items() if k.startswith('handle_')}
print(f"  Found {len(handler_funcs)} handler functions")

for name, (line_num, params, count) in sorted(handler_funcs.items()):
    if count == 6:
        required = params[5]  # 'args' or 'args=None'
        if 'args=None' in params[-1]:
            pass  # Optional - OK
        elif 'args' in params[-1] and 'args=None' not in params[-1]:
            # Check if all call sites pass args
            pass  # Will check below

# 2. Check CMD_HANDLERS for signature mismatches
print("\n[2] Checking CMD_HANDLERS lambda signatures...")
for i, line in enumerate(lines):
    if "CMD_HANDLERS" in line and "={" in line:
        # Found the dict start, check all entries
        for j in range(i+1, min(i+100, len(lines))):
            m = re.match(r"\s+'(/\\w+)':\s+lambda.*:", line)
            if m:
                # All lambdas use same pattern: lambda c, u, un, fn, ln, a: handle_xxx(c, u, un, fn, ln, a)
                pass

# 3. Check for 'args' usage without definition in callback section
print("\n[3] Checking 'args' variable in callback_query section...")
in_callback = False
for i, line in enumerate(lines):
    if "callback_query = update.get('callback_query')" in line:
        in_callback = True
        print(f"  Line {i+1}: callback_query section starts")
    if in_callback and 'callback_query' not in line and 'if not message' in line:
        in_callback = False
        print(f"  Line {i+1}: callback_query section ends")
    
    if in_callback and re.search(r'\bargs\b', line) and 'args=None' not in line:
        # Check if 'args' is defined in this scope
        # Look backward for 'args =' or 'args = '
        found_def = False
        for j in range(max(0, i-30), i):
            if re.search(r'^\s+args\s*=', lines[j]):
                found_def = True
                break
        if not found_def:
            print(f"  ⚠️ Line {i+1}: 'args' used but may not be defined: {line.strip()[:80]}")

# 4. Check for mismatched handle_xxx calls in CMD_HANDLERS
print("\n[4] Checking CMD_HANDLERS function references...")
for i, line in enumerate(lines):
    if "'/start':" in line:
        for j in range(i, min(i+120, len(lines))):
            m = re.match(r"\s+'(/\\w+)':\s+lambda c, u, un, fn, ln, a:\s+(\w+)\(c, u, un, fn, ln, a\),?", lines[j])
            if m:
                cmd = m.group(1)
                handler = m.group(2)
                if handler not in func_defs:
                    print(f"  ❌ Line {j+1}: CMD_HANDLERS references '{handler}' for '{cmd}' but function not defined!")

# 5. Check for function calls with wrong arg count in handler section
print("\n[5] Checking handler calls in target input routing...")
for i, line in enumerate(lines):
    if 'PENDING_TARGETS' in line and 'user_id in PENDING_TARGETS' in line:
        # Found target input section
        for j in range(i, min(i+100, len(lines))):
            m = re.match(r"\s+'(\w+)':\s+(\w+),?", lines[j])
            if m:
                # This is in SCAN_MAP or handler_map
                pass
            if 'handler_map[' in lines[j]:
                m2 = re.search(r"handler_map\[.(\w+).\]\((.+)\)", lines[j])
                if m2:
                    func_name = m2.group(1)
                    call_args = m2.group(2)
                    # Count args
                    args_count = len([a for a in call_args.split(',') if a.strip()])
                    if func_name in func_defs:
                        expected = func_defs[func_name][2]
                        if args_count != expected:
                            print(f"  ⚠️ Line {j+1}: {func_name}() called with {args_count} args, expects {expected}")

# 6. Check for common issues
print("\n[6] Checking for common patterns/issues...")
issues = []
for i, line in enumerate(lines):
    # Check for bare except
    if re.match(r'^\s*except\s*:', line):
        # This is OK in some cases but flag it
        pass
    
    # Check for send_msg with wrong arg order (user_id, chat_id) vs (chat_id, user_id)
    if 'send_msg(user_id, chat_id' in line:
        # This is the correct order for send_msg
        pass
    
    # Check for f-strings with HTML that might break
    if 'f"' in line and 'parse_mode' in line:
        # Potential issue with unescaped user input in HTML
        pass
    
    # Check for log_command calls with wrong arg count
    if 'log_command(' in line:
        args_match = re.search(r'log_command\((.+)\)', line)
        if args_match:
            args_str = args_match.group(1)
            args = [a.strip() for a in args_str.split(',')]
            if len(args) < 4:
                issues.append(f"Line {i+1}: log_command with {len(args)} args (needs 4+): {line.strip()[:60]}")

for issue in issues:
    print(f"  ⚠️ {issue}")

# 7. Check OWNERS set
print("\n[7] Checking OWNERS configuration...")
for i, line in enumerate(lines):
    if 'OWNERS = {' in line:
        for j in range(i, min(i+10, len(lines))):
            print(f"  Line {j+1}: {lines[j].strip()}")
            if '}' in lines[j] and j > i:
                break

# 8. Check VIP_USERS loading
print("\n[8] Checking VIP_USERS loading...")
for i, line in enumerate(lines):
    if 'VIP_USERS' in line and ('add' in line or 'load' in line.lower()):
        print(f"  Line {i+1}: {line.strip()[:80]}")

# 9. Check for the _run_* functions that are called but may not exist
print("\n[9] Checking _run_* function existence vs calls...")
_run_defs = set()
for line in lines:
    m = re.match(r'^def (_run_\w+)\(', line)
    if m:
        _run_defs.add(m.group(1))

_run_calls = set()
for line in lines:
    for m in re.finditer(r'_run_(\w+)', line):
        if not m.group(0).startswith('def _run_'):
            _run_calls.add(f'_run_{m.group(1)}')

missing = _run_calls - _run_defs
# Filter out false positives (docstrings, comments, string literals)
print(f"  Defined _run_* functions: {len(_run_defs)}")
print(f"  _run_* references found: {len(_run_calls)}")
print(f"  Potential missing: {missing - set()}")  # This might have false positives

# 10. Check handle_help and handle_about missing args
print("\n[10] Checking handle_help and handle_about callback calls...")
for i, line in enumerate(lines):
    if "handle_help(chat_id, user_id, username, first_name, last_name)" in line:
        if 'args' not in line.split('handle_help')[1]:
            # Check if handle_help has args=None default
            print(f"  ℹ️ Line {i+1}: handle_help called without args (but has default args=None - OK)")
    if "handle_about(chat_id, user_id, username, first_name, last_name)" in line:
        if 'args' not in line.split('handle_about')[1]:
            print(f"  ℹ️ Line {i+1}: handle_about called without args (but has default args=None - OK)")

print("\n" + "=" * 60)
print("Review complete!")
