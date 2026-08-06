# Bug Audit - Mth Ddos v5.1

## BUGS FOUND SO FAR (Lines 1-1500)

### BUG 1: tool_admin_finder paths with trailing slashes on non-directory paths
Lines 1345-1390: Many paths like `admin/account.php/`, `admin1.php/`, `panel.php/`, `cpanel.php/` have trailing slashes appended to FILE paths (not directories). 
A path like `admin/account.php/` is not the same as `admin/account.php` - the server may return different results.
Affected paths: `admin/cp.php/`, `admincp.php/`, `cp.php/`, `admin/controlpanel.php/`, `admin/admin.jsp/`, `admin.jsp/`, `admin/home.jsp/`, `admin/account.php/`, `admin/login.php/`, `admin/account.html/`, `admin/login.html/`, `admin/index.php/`, `admin/index.html/`, `admin/index.asp/`, `admin/default.php/`, `admin/default.asp/`, `admin1.php/`, `admin1.html/`, `admin1/account.php/`, `admin1/login.php/`, `admin2/login.php/`, `admin2/index.php/`, `admin3/login.php/`, `admin3/index.php/`, `moderator.php/`, `moderator/login.php/`, `moderator/admin.php/`, `administrator/login.php/`, `administrator/index.php/`, `panel.php/`, `panel/admin.php/`, `panel/login.php/`, `controlpanel.php/`, `cpanel.php/`, `webadmin.php/`, `siteadmin/login.php/`, `siteadmin/index.php/`, `sysadmin/login.php/`, `instadmin/login.php/`, `bb-admin/login.php/`, `bb-admin/index.php/`, `bbadmin/login.php/`, `member/login.php/`, `member/admin.php/`, `members/login.php/`, `members/admin.php/`, `console/login.php/`, `settings/login.php/`, `phpmyadmin/index.php/`, `phpmyadmin/login.php/`, `myadmin/index.php/`, `myadmin/login.php/`

### BUG 2: tool_admin_finder called without progress args from /admin handler
Line 3628: `handle_admin_panel` calls `tool_admin_finder(target)` without progress_chat_id/progress_msg_id.
But `/panel` (line 3929) calls it WITH progress args. This means /admin has no progress indicator and no inline buttons.

### BUG 3: /admin handler has no cache, no inline buttons, no DB cache
Line 3628: Unlike /sqli, /xss which have db_cache_get/db_cache_set and send_message_with_buttons, /admin just does send_message_safe.

### BUG 4: Tool paths overlap with /dirs scanner
The admin finder includes paths that should be in /dirs: `.htaccess`, `.htpasswd`, `.env`, `config.php`, `phpinfo.php`, `uploads/`, `images/`, `cache/`, `cgi-bin/`, `shell/`, `shell.php`, `cmd/`, `cmd.php`, `config/database.yml`, `config/application.php`, `config.ini`, `settings.ini`, `appsettings.json`. These overlap with the exposed files scanner and directory scanner.

### BUG 5: dedup list has `admin1/` twice
Line 1354 has `'admin1/'` and line 1359 has `'admin1/'` again. The `dict.fromkeys()` dedup handles this but it's a code smell.

### BUG 6: `root_content` fetched but never used for content comparison
Lines 1406-1408: `root.text` is fetched but `root_content` variable is never used - only `root_len` is used. The content itself could be used for smarter dedup.

### BUG 7: Thread safety issue with `checked` counter
Line 1411-1412: `checked` is modified with `nonlocal` inside worker threads. This is NOT thread-safe in Python. The `+=` operation is not atomic. Should use a Lock.

### BUG 8: `completed` counter in main thread vs `checked` in worker threads
Lines 1476-1488: Both `completed` (main thread) and `checked` (worker threads) try to track progress. This is redundant and `checked` is unreliable due to thread safety.

### BUG 9: progress_msg_id hardcoded total=100 in /panel
Line 3928: `send_progress(chat_id, scan_id, 0, 100, ...)` — the total is hardcoded to 100, but the actual path count varies. Should use `len(paths)` or pass it as parameter.

### BUG 10: /admin and /panel are functionally duplicate commands
Both call `tool_admin_finder`. `/admin` is a subset (no progress). This is confusing for users.

### BUG 11: `db_cache_set` never called for /admin or /panel
Neither handler stores results in DB cache, so results are never reused.

### BUG 12: Missing inline buttons for /admin and /panel
No rescan buttons added to results.
