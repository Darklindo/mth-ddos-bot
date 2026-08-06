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
- [ ] /sqli: WAF detection (Cloudflare, Sucuri, ModSecurity) + bypass suggestions
- [ ] /sqli: GraphQL injection scan
- [ ] /xss: Blind XSS com callback URL
- [ ] /xss: Polyglot payloads multi-contexto
- [ ] /ports: Service version detection (banner detalhado)
- [ ] /ports: Range de portas customizado
- [ ] /dirs: Modo brute-force com wordlist custom
- [ ] /dirs: Rate limiting configurable
- [ ] /sub: Certificate transparency logs (crt.sh)
- [ ] /sub: DNSSEC validation
- [ ] /wp: Themes vulneráveis com CVE
- [ ] /dns: DKIM record check
- [ ] /dns: Reverse PTR lookup
- [ ] /cms: Detection de Joomla, Magento, Shopify, Ghost

## MELHORIAS NOS SCANNERS V5.0
- [ ] /ssl: Certificate chain validation
- [ ] /ssl: OCSP stapling check
- [ ] /ssl: Certificate pinning check
- [ ] /headers: Suggestions de headers faltantes
- [ ] /headers: Grade visual com cores (A=verde, F=vermelho)
- [ ] /tech: Server info detalhado (nginx version, apache modules)
- [ ] /exposed: Mais padrões (.htaccess, .DS_Store, .svn, composer.json)
- [ ] /api: GraphQL introspection detection
- [ ] /api: OpenAPI/Swagger JSON parser

## NOVOS COMANDOS GERAIS
- [ ] /scan all — Faz TODOS os scanners de uma vez
- [ ] /deep — Scan profundo (todos + mais lento)
- [ ] /quick — Scan rápido (headers, ssl, ports)
- [ ] /diff <url> <scan_id> — Compara scan atual com anterior
- [ ] /watch <url> — Monitora site continuamente
- [ ] /report <url> — Relatório completo em texto
- [ ] /ping <url> — Ping/latência do site
- [ ] /http <url> — Redirect chains (HTTP→HTTPS)
- [ ] /sslchain <url> — Cadeia de certificados SSL

## MELHORIAS DE USABILIDADE
- [ ] Inline buttons em todos resultados (Rescan, PDF, Compartilhar)
- [ ] Progress bar animada nos scans longos
- [ ] Tempo estimado antes de começar
- [ ] Cache inteligente (<1h reusa)
- [ ] /cancel para parar scan em andamento
- [ ] /batch url1.com url2.com /sqli — Scan em lote
