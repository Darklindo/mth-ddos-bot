# Bug Tracker — Mth_Ddos_v50.py Line-by-Line Audit

## CRITICAL BUGS

### BUG-001: show_main_menu uses undefined variable `b` (lines 4654-4658)
In `show_main_menu`, the function builds the menu text in variable `msg` but passes `b['title']`, `b['exclusive']`, `b['enter']` to `edit_menu()`. Variable `b` does not exist in this scope. Will cause NameError crash every time the main menu tries to show after a scan.

### BUG-002: edit_menu doesn't match current user's message_id (lines 1599-1629)
`edit_menu` iterates through ALL entries in `MENU_MSG_IDS` (which is `user_id -> message_id`) and edits the first one regardless of whether it matches the current `chat_id`. This means menu edits go to the wrong user when multiple users are active. Also, the fallback saves `MENU_MSG_IDS[chat_id]` (string key) but the loop checks `uid` (int key).

### BUG-003: handle_http calls _safe_get with unsupported keyword argument (line 8919)
`_safe_get` is defined as `_safe_get(url, timeout=5, headers=None)` but `handle_http` calls `_safe_get(url, timeout=10, allow_redirects=True)`. This will cause TypeError. `/http` command always crashes.

### BUG-004: DNS DMARC check queries wrong domain (line 2960)
DMARC detection does `dns_query_via_doh('TXT')` on the root domain, but DMARC records live at `_dmarc.<domain>`. Will never find DMARC records.

### BUG-005: DNS DKIM check is non-functional placeholder (lines 2972-2987)
DKIM detection also queries root TXT records. The selector loop at line 2983 calls `dns_query_via_doh('TXT')` without using the selector variable. Completely non-functional.

### BUG-006: SSL SAN extraction uses undefined variable `_` (line 3353)
`sans = [v for k, v in san if _ == 'DNS']` — variable `_` is undefined. Should be `k`. NameError swallowed by broad `except`.

### BUG-007: _run_ssl_normal and _run_ssl_owner call log_command with wrong args (lines 8384, 8398)
`log_command(user_id, '', 'ssl', '', target)` passes 5 args where `''` becomes `target` and `target` becomes `result_summary`. Target in log is always empty.

### BUG-008: site_monitor_loop + scheduled_task_loop NOT started in default polling mode (lines 10241-10246)
When running `python3 Mth_Ddos_v50.py` without arguments, only `health_check_loop` starts. `site_monitor_loop` and `scheduled_task_loop` only start with explicit `polling` argument. This means `/watch`, `/notify`, `/schedule` and scheduled broadcasts NEVER work in default mode.

### BUG-009: scheduled_task_loop passes None to handlers for aggregated commands (lines 10070-10074)
`'scanall': lambda t: handle_scanall(None, None, None, None, None, [t])` — passes None as chat_id, user_id, etc. Handlers will crash on `log_user(None, ...)` or `send_msg(None, ...)`.

### BUG-010: menu:cancel_target passes reply_markup as JSON string (line 9552)
`reply_markup` is `'{"inline_keyboard": ...}'` (string) instead of a Python dict. Telegram API returns 400 error. Cancel button in target input doesn't work.

### BUG-011: menu:lang uses send_message_with_buttons instead of edit_menu (lines 9444-9456)
When user clicks "Idioma", it sends a new message instead of editing the existing menu. Inconsistent with the edit_menu refactor.

### BUG-012: show_main_menu called without username/first_name after scans (lines 9580, 9588, 9596, 9604, 9674, 9678, 9682, 9736, 9744, 9771)
After each scan completes, `show_main_menu(chat_id, user_id)` is called without `username` and `first_name`. Greeting shows "Olá, User!" instead of actual name.

### BUG-013: site_monitor_loop ignores per-row watch_interval (lines 9996-10050)
Loop sleeps 60s and checks ALL monitors, ignoring the `watch_interval` column set by `/watch <url> <minutes>`. User sets 30min interval but bot checks every 60s.

### BUG-014: /notify off deletes /watch content monitors too (line 7500)
`DELETE FROM site_monitor WHERE user_id = ?` deletes ALL monitors including `/watch` content watches. Turning off status notifications wipes content watches.

### BUG-015: scheduled_task_loop always marks tasks as completed even on failure (lines 10157-10159)
Task status set to 'completed' regardless of whether execution succeeded or threw exception. No retry, no failure tracking.

### BUG-016: show_main_menu has duplicated message_id persistence block (lines 4659-4672)
The block that saves `MENU_MSG_IDS[user_id] = mid` appears twice identically. Redundant code.

### BUG-017: 76 handlers call log_user without language_code (various lines)
Only `handle_start` (line 4598) and `process_update` (line 9635) pass `language_code`. All other 76 handlers use default `'pt'`. The `process_update` call partially compensates, but DB writes from other paths are inconsistent.
