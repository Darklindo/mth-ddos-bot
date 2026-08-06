#!/usr/bin/env python3
"""Translate common message patterns in Mth_Ddos_v50.py.
Wraps send_message_safe calls with a lang-aware t() function."""

import re

with open("Mth_Ddos_v50.py", "r") as f:
    content = f.read()

lines = content.split('\n')

# We'll process line by line, looking for send_message_safe calls
# and wrapping them with t(user_id, ...) where user_id is available.
# 
# Strategy: For the most critical messages (ban, maintenance, unknown cmd, rate limit)
# we already translated them inline. For the rest, we'll create a helper function
# that wraps send_message_safe to auto-translate based on user_id.
#
# Since send_message_safe doesn't have user_id, we'll create send_msg(msg, user_id, chat_id)
# that translates and calls send_message_safe.

# Actually, the better approach: just translate the most common patterns directly
# in the process_update and critical handlers. The "❌ Use:" patterns are 56 messages
# that follow a predictable format. We can handle them by adding a helper.

# Let's add a send_msg helper function that takes user_id for translation
# and replace send_message_safe with send_msg where user_id is available.

print("Script for batch translation - approach documented")
print(f"Total lines: {len(lines)}")
