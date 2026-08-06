# Bug Report Completo — MTH Security v5.1

## CRITICAL BUGS (Corrigidos)

| # | Bug | Linha | Impacto | Status |
|---|-----|-------|---------|--------|
| 1 | /report duplicado no CMD_HANDLERS (handle_report vs handle_report_url) | ~6007 | Bug reporting morto | ✅ Fixado |
| 2 | /admin sem cache, sem progress, sem buttons | 3619-3629 | UX quebrada | ✅ Fixado |
| 3 | /panel progress total hardcoded=100 | 3928 | Progress bar imprecisa | ✅ Fixado |
| 4 | Thread-unsafe `checked` counter | 1411-1412 | Progress counts errados | ✅ Fixado |
| 5 | `admin1/` duplicado na lista | 1354+1359 | Code smell | ✅ Fixado |
| 6 | Trailing slashes em FILE paths | 1345-1390 | False negatives | ✅ Fixado |
| 7 | Paths admin overlap com /dirs | 1378-1392 | Duplicação | ✅ Fixado |
| 8 | root_content fetched mas nunca usado | 1406-1408 | Memória desperdiçada | ✅ Fixado |
| 10 | handle_batch não cria STOP_EVENTS | 5702 | /cancel não funciona em batch | ✅ Fixado |
| 11 | rescan /admin e /panel sem db_cache_set | 4705-4714 | Cache não populado | ✅ Fixado |
| 15 | Help text enganoso (25 paths vs 100+) | 3406-3407 | Usuários confusos | ✅ Fixado |
| 19 | Result format inconsistente | 1491-1494 | Visual pobre | ✅ Fixado |

## WARNINGS (Corrigidos)

| # | Bug | Linha | Impacto | Status |
|---|-----|-------|---------|--------|
| 9 | handle_stop owner-only vs /cancel public | 4644 | Inconsistência | ⚠️ Design choice |
| 12 | Scheduled task loop missing V5.1 cmds | 6363-6373 | Agendamento limitado | ⚠️ Conhecido |
| 13 | botpanel v5.0 strings | 4004+ | Stale version | ✅ Fixado |
| 14 | botpanel missing V5.1 command list | 4027-4050 | Incompleto | ⚠️ Conhecido |
| 17 | STOP_EVENTS cleanup inconsistency | 4831-4833 | Memory leak potencial | ✅ Fixado |
| 18 | handle_scanall/deep/quick sem cache | 5560-5659 | Cache não populado | ⚠️ Conhecido |
| 22 | /report mapping ambiguity | 6007+6050 | Bug reporting morto | ✅ Fixado |
| 24 | Missing total calc in rescan /panel | 4711 | Progress impreciso | ✅ Fixado |

## NOTAS ADICIONAIS

- Todas as v5.0 strings atualizadas para v5.1
- Tool_admin_finder agora tem 120+ paths (de 80+)
- Todos os resultados agora usam formato consistente com emojis
- /admin e /panel agora ambos têm: cache, progress, inline buttons, STOP_EVENTS
