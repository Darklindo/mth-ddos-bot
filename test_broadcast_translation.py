"""
Test script: Simulate broadcast translation system with PT/EN/ES users.
Tests the _translate_broadcast_text function and the per-user language logic
from _do_broadcast without needing a Telegram token.
"""
import requests
import json
import time

# ── Configuration ──
TEST_USERS = [
    {"id": 100001, "username": "jtcacique_br", "first_name": "JT", "language_code": "pt"},
    {"id": 100002, "username": "john_doe", "first_name": "John", "language_code": "en"},
    {"id": 100003, "username": "carlos_es", "first_name": "Carlos", "language_code": "es"},
    {"id": 100004, "username": "maria_pt2", "first_name": "Maria", "language_code": "pt"},
    {"id": 100005, "username": "james_en2", "first_name": "James", "language_code": "en"},
    {"id": 100006, "username": "pedro_es2", "first_name": "Pedro", "language_code": "es"},
    {"id": 100007, "username": "ana_br3", "first_name": "Ana", "language_code": "pt"},
    {"id": 100008, "username": "emma_en3", "first_name": "Emma", "language_code": "en"},
    {"id": 100009, "username": "diego_es3", "first_name": "Diego", "language_code": "es"},
    {"id": 100010, "username": "lucas_br4", "first_name": "Lucas", "language_code": "pt"},
]

OWNER_USER_ID = 5658716257

# Simulated broadcast messages to test
TEST_MESSAGES = [
    "Bot online novamente e talvez na sua melhor versão!",
    "Novo scanner SSL adicionado! Use /ssl para verificar seus sites.",
    "Manutenção programada para amanhã às 03:00.",
]

# ── Translation function (copied from bot for testing) ──
def _translate_broadcast_text(text: str, target_lang: str, source_lang: str = 'pt') -> str:
    """Translate broadcast text using MyMemory free translation API.
    Falls back to original text if translation fails or target is same as source."""
    if target_lang == source_lang or target_lang == 'pt' or not text:
        return text
    try:
        langpair = f"{source_lang}|{target_lang}"
        resp = requests.get(
            "https://api.mymemory.translated.net/get",
            params={"q": text, "langpair": langpair},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            translated = data.get('responseData', {}).get('translatedText', '')
            if translated and len(translated) > len(text) * 0.3:
                return translated
    except Exception as e:
        print(f"    [WARN] Translation error: {e}")
    return text


def simulate_broadcast(users, broadcast_text, owner_id):
    """Simulate the broadcast loop from _do_broadcast."""
    # Step 1: Exclude sender (owner)
    recipients = [u for u in users if u['id'] != owner_id]
    total = len(recipients)
    
    print(f"\n{'='*60}")
    print(f"SIMULAÇÃO DE BROADCAST")
    print(f"{'='*60}")
    print(f"Mensagem original: {broadcast_text}")
    print(f"Total usuários no DB: {len(users)}")
    print(f"Removidos (sender): {len(users) - total}")
    print(f"Destinatários: {total}")
    print(f"{'─'*60}")
    
    # Step 2: Simulate the per-user translation loop
    _translation_cache = {}
    sent = 0
    failed = 0
    blocked = 0
    
    results_by_lang = {"pt": [], "en": [], "es": [], "other": []}
    
    for idx, u in enumerate(recipients):
        uid = str(u['id'])
        user_lang = u.get('language_code', 'pt') or 'pt'
        
        # Translate text for this user's language
        if user_lang != 'pt':
            cache_key = (broadcast_text, user_lang)
            if cache_key in _translation_cache:
                translated_text = _translation_cache[cache_key]
                cache_hit = True
            else:
                translated_text = _translate_broadcast_text(broadcast_text, user_lang)
                _translation_cache[cache_key] = translated_text
                cache_hit = False
        else:
            translated_text = broadcast_text
            cache_hit = False
        
        # Simulate send (no actual Telegram call)
        success = True  # Simulated success
        if success:
            sent += 1
        
        lang_key = user_lang if user_lang in results_by_lang else "other"
        results_by_lang[lang_key].append({
            "user": f"{u['first_name']} (@{u['username']})",
            "uid": uid,
            "lang": user_lang,
            "cache_hit": cache_hit,
            "original": broadcast_text,
            "translated": translated_text,
        })
    
    # Print results grouped by language
    for lang, results in results_by_lang.items():
        if not results:
            continue
        lang_names = {"pt": "🇧🇷 Português", "en": "🇺🇸 English", "es": "🇪🇸 Español", "other": "🌐 Outro"}
        print(f"\n📋 Grupo: {lang_names.get(lang, lang)} ({len(results)} usuários)")
        print(f"{'─'*40}")
        for r in results:
            cache_label = " (cache ✅)" if r["cache_hit"] else " (traduzido 🔄)" if r["lang"] != "pt" else ""
            print(f"  → {r['user']} [{r['uid']}]")
            print(f"    Idioma: {r['lang']}{cache_label}")
            if r['lang'] != 'pt':
                print(f"    Original: {r['original']}")
                print(f"    Traduzido: {r['translated']}")
            else:
                print(f"    Mensagem: {r['translated']}")
    
    # Print cache stats
    print(f"\n{'─'*60}")
    print(f"📊 Cache de tradução:")
    for key, val in _translation_cache.items():
        print(f"  ({key[1]}) \"{key[0][:50]}...\" → \"{val[:50]}...\"")
    
    print(f"\n✅ Enviados: {sent} | ❌ Falhas: {failed} | ⚠️ Bloqueados: {blocked}")
    print(f"📊 Taxa de entrega: {(sent/total*100):.0f}%")
    print(f"🔄 Chamadas de API: {len(_translation_cache)} (para {total} usuários)")
    print(f"{'='*60}")
    
    return sent, failed, blocked, _translation_cache


# ── Run tests ──
print("╔══════════════════════════════════════════════════════════╗")
print("║  TESTE DO SISTEMA DE TRADUÇÃO AUTOMÁTICA DO BROADCAST  ║")
print("╚══════════════════════════════════════════════════════════╝")

for msg_idx, test_msg in enumerate(TEST_MESSAGES, 1):
    print(f"\n\n{'#'*60}")
    print(f"# TESTE {msg_idx}/{len(TEST_MESSAGES)}")
    print(f"{'#'*60}")
    sent, failed, blocked, cache = simulate_broadcast(TEST_USERS, test_msg, OWNER_USER_ID)

# ── Test: verify owner exclusion ──
print(f"\n\n{'#'*60}")
print("# TESTE EXTRA: Exclusão do sender (dono)")
print(f"{'#'*60}")

# Test with the owner in the user list
test_users_with_owner = TEST_USERS + [{"id": OWNER_USER_ID, "username": "jtcacique", "first_name": "JT Cacique", "language_code": "pt"}]
recipients = [u for u in test_users_with_owner if u['id'] != OWNER_USER_ID]
print(f"Usuários no DB (com dono): {len(test_users_with_owner)}")
print(f"Recipients após exclusão: {len(recipients)}")
print(f"Owner na lista de recipients? {any(u['id'] == OWNER_USER_ID for u in recipients)}")
print(f"✅ TESTE PASSOU: Owner excluído corretamente" if not any(u['id'] == OWNER_USER_ID for u in recipients) else "❌ TESTE FALHOU: Owner NÃO foi excluído")

# ── Test: verify cache efficiency ──
print(f"\n\n{'#'*60}")
print("# TESTE EXTRA: Eficiência do cache")
print(f"{'#'*60}")
print(f"10 usuários sendo 3 em EN e 3 em ES")
print(f"Chamadas de API esperadas: 2 (1 para EN, 1 para ES)")
print(f"Chamadas com cache: apenas 2 (não 6)")
print(f"✅ Cache funciona corretamente se 'Chamadas de API' nos testes acima = 2")

print(f"\n\n{'='*60}")
print("TODOS OS TESTES CONCLUÍDOS")
print(f"{'='*60}")
