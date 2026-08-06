# MTH Security v5.0 — TODO

## NEW SCANNERS (11 commands)
- [x] /ssl — Auditoria SSL/TLS completa
- [x] /headers — Security Headers (nota A-F)
- [x] /cors — Teste CORS misconfiguration
- [x] /robots — robots.txt analyzer
- [x] /sitemap — sitemap.xml analyzer
- [x] /tech — Tecnologia avançada (Wappalyzer-like)
- [x] /exposed — Arquivos sensíveis expostos (.env, .git, etc.)
- [x] /backup — Backups expostos
- [x] /api — Endpoints de API
- [x] /shell — Webshells comuns
- [x] /config — Arquivos de configuração expostos

## NEW INFO COMMANDS (5 commands)
- [x] /traceroute — Traceroute para IP
- [x] /whois — Whois completo do domínio
- [x] /ip — GeoIP avançado com ASN/ISP/proxy detection
- [x] /rate — Nota de segurança geral do site (0-100)
- [x] /compare — Comparar dois sites

## NEW UTILITY COMMANDS (4 commands)
- [x] /history — Histórico de scans de um site
- [x] /top — Top sites mais vulneráveis
- [x] /pdf — Relatório PDF do scan
- [x] /schedule — Agendar scan para depois

## IMPROVED EXISTING SCANNERS (7)
- [x] /sqli — Blind SQLi, time-based, boolean-based separados
- [x] /xss — DOM-based detection, polyglot payloads
- [x] /ports — Custom ports + melhor banner grabbing
- [x] /sub — 100+ subdomínios + permutation scan
- [x] /dirs — 150+ diretórios + wordlist mode
- [x] /wp — Vulnerabilidades em plugins/themes
- [x] /dns — DNSSEC, zone transfer, DMARC/SPF

## SYSTEM IMPROVEMENTS (5)
- [x] Queue system para scans simultâneos
- [x] Cache melhorado (já existe, otimizar)
- [x] Stealth mode (/stealth url cmd)
- [x] Export scan result (/exportscan id)
- [x] Notify quando site muda status

## OWNER IMPROVEMENTS (6)
- [x] /maintenance — Modo manutenção
- [x] /cooldown — Configurar rate limit
- [x] /vip add <id> — Usuário VIP
- [x] /log <comando> — Logs detalhados
- [x] /clearlogs — Limpar logs antigos
- [x] /broadcast schedule — Agendar broadcast

## REGISTRATION
- [x] Atualizar set_commands.py com todos os novos comandos
- [x] Atualizar /help e /about com novos comandos
- [x] Atualizar version para v5.0
## REVISÃO COMPLETA DE BUGS V5.0
- [x] Revisar imports, variáveis globais, DB init e helpers (linhas 1-700)
- [x] Revisar todas as tool functions (linhas 700-2970)
- [x] Revisar todos os handlers e CMD_HANDLERS (linhas 2970-5466)
- [x] Corrigir todos os bugs encontrados
- [x] Validar sintaxe, push no GitHub e entregar
## MELHORIAS NOS SCANNERS EXISTENTES
- [x] /sqli: WAF detection (Cloudflare, Sucuri, ModSecurity) + bypass suggestions
- [x] /sqli: GraphQL injection scan
- [x] /xss: Blind XSS com callback URL
- [x] /xss: Polyglot payloads multi-contexto
- [x] /ports: Service version detection (banner detalhado)
- [x] /ports: Range de portas customizado
- [x] /dirs: Modo brute-force com wordlist custom
- [x] /dirs: Rate limiting configurable
- [x] /sub: Certificate transparency logs (crt.sh)
- [x] /sub: DNSSEC validation
- [x] /wp: Themes vulneráveis com CVE
- [x] /dns: DKIM record check
- [x] /dns: Reverse PTR lookup
- [x] /cms: Detection de Joomla, Magento, Shopify, Ghost

## MELHORIAS NOS SCANNERS V5.0
- [x] /ssl: Certificate chain validation
- [x] /ssl: OCSP stapling check
- [x] /ssl: Certificate pinning check
- [x] /headers: Suggestions de headers faltantes
- [x] /headers: Grade visual com cores (A=verde, F=vermelho)
- [x] /tech: Server info detalhado (nginx version, apache modules)
- [x] /exposed: Mais padrões (.htaccess, .DS_Store, .svn, composer.json)
- [x] /api: GraphQL introspection detection
- [x] /api: OpenAPI/Swagger JSON parser

## NOVOS COMANDOS GERAIS
- [x] /scanall — Faz 6 scanners de uma vez
- [x] /deep — Scan profundo (6 scanners vulns)
- [x] /quick — Scan rápido (info + headers)
- [x] /diff <url> <scan_id> — Compara scan atual com anterior
- [x] /watch <url> — Monitora site continuamente
- [x] /report <url> — Relatório completo em texto
- [x] /ping <url> — Ping/latência do site
- [x] /http <url> — Redirect chains (HTTP→HTTPS)
- [x] /sslchain <url> — Cadeia de certificados SSL

## MELHORIAS DE USABILIDADE
- [x] Inline buttons em todos resultados (Rescan, PDF, Compartilhar)
- [x] Progress bar animada nos scans longos
- [x] Tempo estimado antes de começar
- [x] Cache inteligente (10 min TTL)
- [x] /cancel para parar scan em andamento
- [x] /batch url1.com url2.com /sqli — Scan em lote
## MULTILINGUAL SUPPORT (PT/EN/ES/VI/ID)
- [x] Adicionar suporte ao idioma vietnamita (vi) — 39 traduções
- [x] Adicionar suporte ao idioma indonésio (id) — 39 traduções
- [x] Atualizar /lang command com vi e id
- [x] Auto-detectar vi/id pelo language_code do Telegram
## DEEP BUG REVIEW (v5.2)
- [x] Fix: setlang mensagem de confirmação agora responde no idioma selecionado
- [x] Fix: show_main_menu — Full translation for all 5 languages
- [x] Fix: show_menu_vip — Full translation for all 5 languages
- [x] Fix: show_menu_owner — Full translation for all 5 languages
- [x] Fix: handle_lang — Responds in user's current language
- [x] Fix: Version consistency — All user-facing messages updated v5.1 → v5.2
- [x] Fix: IndentationError in _TRANSLATIONS dict
- [x] All 7 menus with get_user_lang verified
- [x] 90 tier functions, 75 handlers, 15 callbacks verified

## MULTILINGUAL SUPPORT (PT/EN/ES/VI/ID)
- [x] Adicionar suporte ao idioma vietnamita (vi) — 39 traduções
- [x] Adicionar suporte ao idioma indonésio (id) — 39 traduções
- [x] Atualizar /lang command com vi e id
- [x] Auto-detectar vi/id pelo language_code do Telegram
- [ ] Language detection system (username locale / Telegram user lang)
- [ ] Translation dictionary for all user-facing messages
- [ ] Replace hardcoded PT messages with translated versions
- [ ] Add /lang command for manual language selection
- [ ] Update /help and /about for all languages
## TIERED SCANNING SYSTEM (Normal/VIP/Owner)
- [x] Design tier system: Normal users get basic scanner, VIP sees 2 buttons (Normal/VIP), Owner sees 3 buttons (Normal/VIP/Owner)
- [x] Add VIP scanner upgrade: deeper analysis, more payloads, banner grabbing, subdomain enum, vuln path scan
- [x] Add Owner scanner upgrade: full WAF bypass, 0-day patterns, API fuzzing, config exposure, sensitive file scan
- [x] Add tier buttons to /sqli, /xss, /scanall, /deep (callback handlers for tier:prefix)
- [x] Add owner-exclusive commands: /forensic, /pentest, /osint
- [x] Update set_commands.py with new commands
- [x] Verify syntax, commit and push
## BUG FIXES
- [x] Fix broadcast giving too many failures
- [x] Fix bot not capturing username for all users (showing N/D)
- [x] Delete/edit the tier selection message after user picks a tier
## TIER BUTTONS FOR ALL SCANNERS
- [ ] Add tier buttons to /panel (admin finder)
- [ ] Add tier buttons to /admin
- [ ] Add tier buttons to /dirs (directory scanner)
- [ ] Add tier buttons to /sub (subdomain scanner)
- [ ] Add tier buttons to /wp (wordpress scanner)
- [ ] Add tier buttons to /ports
- [ ] Add tier buttons to /ssl
- [ ] Add tier buttons to /headers
- [ ] Add tier buttons to /exposed
- [ ] Add tier buttons to /backup
- [ ] Add tier buttons to /api
- [ ] Add tier buttons to /shell (webshell hunter)
- [ ] Add tier buttons to /config
- [ ] Add tier buttons to /cors
- [ ] Add tier buttons to /robots
- [ ] Add tier buttons to /sitemap
- [ ] Add tier buttons to /tech
- [ ] Add tier buttons to /ftpssh
- [ ] Add tier buttons to /cms
- [ ] Add tier buttons to /dns
- [ ] Add tier buttons to /info
- [ ] Add tier buttons to /quick
- [ ] Add tier buttons to /http
- [ ] Add tier buttons to /sslchain
- [ ] Add tier buttons to /emails
- [ ] Add tier buttons to /reverse
- [ ] Add tier buttons to /whois
- [ ] Add tier buttons to /rate
- [ ] Add tier buttons to /ip
- [ ] Add tier buttons to /compare
- [ ] Add tier callback handlers for all new scanner tiers
## INTERACTIVE MENU SYSTEM (V5.2 — Major UX Overhaul)
- [x] Create main menu with category pages (Vulnerabilidades, Recon, Auditoria, Arquivos)
- [x] Create VIP exclusive page with VIP-tier scanners
- [x] Create OWNER exclusive page with forensic/pentest/osint
- [x] Add target input flow (bot asks for URL after button click)
- [x] Add navigation callbacks (back button, page switching)
- [x] Add /start command that shows main menu
- [x] Add tier-gated buttons (Normal users don't see VIP/Owner pages)
- [x] Keep /commands working as fallback for power users
- [x] Update set_commands.py
- [x] Verify syntax, commit and push
## BROADCAST PROGRESS FIX
- [x] Broadcast should edit a single message instead of sending multiple progress messages
- [x] Fix progress spam in broadcast (10%, 20%, 30% etc sending new messages)

## MENU CLEANUP & REORGANIZE
- [x] Redesenhar show_main_menu — botões curtos, badge Owner/VIP, sem texto longo
- [x] Redesenhar show_menu_vulns — emojis curtos (⚡ SQLi, ⚡ XSS) sem descrições
- [x] Redesenhar show_menu_recon — botões curtos (🌐 Info, 📋 Whois)
- [x] Redesenhar show_menu_audit — botões curtos (🔒 SSL, 📋 Headers)
- [x] Redesenhar show_menu_files — botões curtos (🔑 Admin, 📁 Dirs)
- [x] Redesenhar show_menu_vip — botões curtos com badge ⭐ VIP
- [x] Redesenhar show_menu_owner — botões curtos com badge 👑 DONO
- [x] Simplificar handle_help — apenas DONO, /start e comandos essenciais

## v5.2 BUG REVIEW (LINE BY LINE)
- [x] Fix: handle_stats() missing args in menu:stats callback (already correct in v5.2)
- [x] Fix: 'args' not defined in callback_query section (flow correctly falls through)
- [x] Fix: Missing _run_info_normal/vip/owner functions (info scanner had no tier variants)
- [x] Full line-by-line bug review of entire file
- [x] All 30 _run_*_normal/vip/owner functions verified
- [x] set_commands.py updated with forensic/pentest/osint
## MENU NAVIGATION IMPROVEMENTS
- [x] Editar mensagem do menu ao navegar entre categorias (em vez de enviar nova)
- [x] Mostrar menu principal de volta após cada scan terminar
- [x] Salvar message_id do menu para poder editá-lo depois
- [x] edit_menu() function implemented
- [x] MENU_MSG_IDS dict for tracking
- [x] show_main_menu after tiered scanners (sqli, xss, scanall, deep)
- [x] show_main_menu after non-tiered scanners
- [x] show_main_menu after owner commands
- [x] show_main_menu after /batch and /quick
## BROADCAST AUTO-TRANSLATION (v5.2)
- [x] Add language_code column to users table
- [x] Store detected language_code when user interacts with bot
- [x] Implement auto-translate in handle_msg broadcast
- [x] Translate text broadcasts per-user language
- [x] Translate media captions per-user language
- [x] Fallback to PT if translation fails
## BUG REVIEW - COMPLETE CODE AUDIT (v5.2)
- [ ] Review imports, constants, config and DB schema (lines 1-400)
- [ ] Review utility functions, translation, rate limit, helpers (lines 400-1000)
- [ ] Review scan handlers (sqli, xss, ports, dirs, sub, wp, etc.) (lines 1000-5000)
- [ ] Review admin/broadcast handlers (msg, ban, export, etc.) (lines 5000-7000)
- [ ] Review monitor/schedule/owner handlers (lines 7000-9000)
- [ ] Review main loop, process_update and polling (lines 9000-10247)
- [ ] Consolidate all bugs and prepare fix list
- [ ] Fix all bugs found
- [ ] Verify syntax, tests and push to GitHub
