# Bug Audit Complete - MTH Security v5.1

## CRITICAL BUGS

### BUG 1: /report collision — duplicate key in CMD_HANDLERS
Line 6007: `'/report': handle_report` (bug report handler)
Line 6050: `'/report': handle_report_url` (URL report handler) — OVERWRITES the first one
Impact: /report can never reach handle_report (bug report). Users lose bug reporting.

### BUG 2: /admin has no cache, no progress, no inline buttons
Line 3628: handle_admin_panel calls tool_admin_finder(target) — no db_cache, no buttons
Lines 3619-3629: No db_cache_get/db_cache_set, no send_message_with_buttons

### BUG 3: /panel progress total hardcoded to 100
Line 3928: send_progress(chat_id, scan_id, 0, 100, ...) — total should be dynamic

### BUG 4: Thread-unsafe `checked` counter in tool_admin_finder
Line 1411-1412: `nonlocal checked; checked += 1` inside worker threads
Impact: Progress counts can be inaccurate under load

### BUG 5: Duplicate path `admin1/` in tool_admin_finder
Line 1354 and 1359 both have 'admin1/'

### BUG 6: Trailing slashes on FILE paths in admin finder
Lines 1345-1390: Paths like admin/account.php/, admin1.php/, panel.php/ etc.
Files should NOT have trailing slashes

### BUG 7: Overlap between /admin and /dirs paths
admin finder includes: .htaccess, .htpasswd, .env, config.php, phpinfo.php, uploads/, images/, cache/, cgi-bin/, shell/, shell.php, cmd/, cmd.php
These should only be in /dirs or /exposed

### BUG 8: root_content fetched but never used
Lines 1406-1408: root.text stored but root_content never used for content comparison

### BUG 9: handle_stop allows ANY user to stop scans
Line 4644: Only checks is_owner, but the /cancel command (line 5662) allows ANY user to cancel their own scan
Inconsistency: /stop is owner-only, /cancel is public

### BUG 10: handle_batch doesn't create STOP_EVENTS
Line 5702: `if user_id in STOP_EVENTS` — but handle_batch never creates one
Impact: /cancel can't cancel batch scans

### BUG 11: rescan /admin missing db_cache_set
Line 4707: handle_rescan for /admin doesn't call db_cache_set
Line 4712: handle_rescan for /panel also doesn't call db_cache_set

### BUG 12: Scheduled task loop missing V5.1 commands
Line 6363-6373: tool_map doesn't include scanall, deep, quick, http, sslchain, report, watch

### BUG 13: botpanel lists v5.0 instead of v5.1
Line 3964: "Painel do Bot — MTH Security v5.0" — stale version string

### BUG 14: botpanel tool list missing V5.1 commands
Lines 4027-4050: Doesn't list scanall, deep, quick, http, sslchain, batch, watch, cancel, report

### BUG 15: Help text says /admin is "~25 paths" and /panel is "100+ paths"
Lines 3406-3407: Misleading — both use the same tool_admin_finder with ~80 paths

### BUG 16: ACTIVE_THREADS.acquire timeout=30 too short
Line 6189: If all 50 slots are busy for 30s, user gets "Servidor ocupado" — could be extended

### BUG 17: STOP_EVENTS cleanup only in handle_rescan, not in handle_panel
Line 4831-4833: STOP_EVENTS[user_id] deleted after rescan, but handle_panel also creates one
Line 3927: scan_id created but STOP_EVENTS never set for /panel

### BUG 18: handle_scanall/handle_deep/handle_quick send results without cache
No db_cache_set calls in these aggregated handlers

### BUG 19: tool_admin_finder result format inconsistent
Lines 1491-1494: Returns plain "Admin panel found: ..." without emoji formatting
Other tools use 🔓/🚫/✅/⚠️ emojis

### BUG 20: handle_stop uses STOP_EVENTS but never creates them for direct scans
handle_stop (line 4653) checks STOP_EVENTS[target_user_id] but only /rescan and /batch create these events
Direct /admin, /panel, /sqli etc. never create STOP_EVENTS for the user

### BUG 21: set_commands.py doesn't include /bugreport
set_commands.py should have /bugreport as alias for /report (bug reporting)

### BUG 22: handle_report_url called from /report but /report also maps to handle_report
The second entry in CMD_HANDLERS wins (handle_report_url), so bug reporting is dead

### BUG 23: tool_admin_finder paths `admin1/` duplicate
Line 1354: 'admin1/' and line 1359: 'admin1/' — redundant

### BUG 24: Missing `total` calculation in handle_rescan for /panel
Line 4711: send_progress uses hardcoded 100, should match actual path count

### BUG 25: `db_cache_get` checks but /admin handler never populates cache
handle_admin_panel (line 3628) doesn't check cache before running

## USABILITY IMPROVEMENTS NEEDED

1. /admin should have progress bar like /panel
2. /admin should have inline rescan button
3. /admin should use DB cache
4. /panel should use dynamic progress total
5. Tool results should use consistent emoji formatting
6. Botpanel should show v5.1 version
7. Botpanel should list all V5.1 commands
8. Help text should accurately describe /admin vs /panel
