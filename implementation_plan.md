# Implementation Plan - All TODOs

## Current Architecture
- File: /home/ubuntu/mth-ddos-bot/Mth_Ddos_v50.py (~5665 lines)
- CMD_HANDLERS dict at line 5143-5207
- process_update at line 5209-5364
- long_polling at line 5367-5436
- Background threads: site_monitor_loop (5457), scheduled_task_loop (5502), health_check_loop (5588)
- __main__ at line 5634

## TODOs to Implement (all from todo.md)

### 1. MELHORIAS NOS SCANNERS EXISTENTES
- /sqli: WAF detection (Cloudflare, Sucuri, ModSecurity) + bypass suggestions
- /sqli: GraphQL injection scan
- /xss: Blind XSS with callback URL
- /xss: Polyglot payloads multi-context
- /ports: Service version detection (banner detalhado)
- /ports: Range de portas customizado
- /dirs: Modo brute-force com wordlist custom
- /dirs: Rate limiting configurable
- /sub: Certificate transparency logs (crt.sh)
- /sub: DNSSEC validation
- /wp: Themes vulneráveis com CVE
- /dns: DKIM record check
- /dns: Reverse PTR lookup
- /cms: Detection de Joomla, Magento, Shopify, Ghost (already partly done)

### 2. MELHORIAS NOS SCANNERS V5.0
- /ssl: Certificate chain validation
- /ssl: OCSP stapling check
- /ssl: Certificate pinning check
- /headers: Suggestions de headers faltantes
- /headers: Grade visual com cores (A=verde, F=vermelho)
- /tech: Server info detalhado (nginx version, apache modules)
- /exposed: Mais padrões (.htaccess, .DS_Store, .svn, composer.json) (already partly done)
- /api: GraphQL introspection detection
- /api: OpenAPI/Swagger JSON parser

### 3. NOVOS COMANDOS GERAIS
- /scanall <url> — Faz TODOS os scanners de uma vez
- /deep <url> — Scan profundo (todos + mais lento)
- /quick <url> — Scan rápido (headers, ssl, ports)
- /diff <url> <scan_id> — Compara scan atual com anterior
- /watch <url> — Monitora site continuamente (extends /notify)
- /report <url> — Relatório completo em texto
- /ping <url> — Ping/latência do site (when arg provided, site ping; no arg = bot ping)
- /http <url> — Redirect chains (HTTP→HTTPS)
- /sslchain <url> — Cadeia de certificados SSL

### 4. MELHORIAS DE USABILIDADE
- Inline buttons em todos resultados (Rescan, PDF, Compartilhar)
- Progress bar animada nos scans longos
- Tempo estimado antes de começar
- Cache inteligente (<1h reusa)
- /cancel para parar scan em andamento
- /batch url1.com url2.com /sqli — Scan em lote

## Implementation Strategy
1. Create a new Mth_Ddos_v51.py with ALL improvements
2. Add new tool functions for each improvement
3. Add new handlers
4. Update CMD_HANDLERS
5. Update help/about
6. Update set_commands.py
