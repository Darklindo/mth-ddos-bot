#!/bin/bash
# ============================================================
#  MTH Security v5.1 — Guia de Deploy / Atualização
# ============================================================
#  Uso:
#    chmod +x deploy.sh
#    ./deploy.sh
# ============================================================

set -e

echo "============================================"
echo "  MTH Security v5.1 — Deploy Script"
echo "============================================"

# 1. Sair do tmux sem matar o bot
echo ""
echo "[1/5] Saindo da sessão tmux (se existir)..."
tmux detach 2>/dev/null || true

# 2. Matar o bot antigo
echo "[2/5] Matando sessão tmux antiga..."
tmux kill-session -t mth 2>/dev/null || true
echo "  ✅ Sessão antiga encerrada."

# 3. Ir na pasta do bot e atualizar
echo "[3/5] Atualizando código..."
cd ~/mth-ddos-bot || { echo "ERRO: pasta ~/mth-ddos-bot não encontrada!"; exit 1; }
git pull origin master
echo "  ✅ Código atualizado."

# 4. Registrar os novos comandos no Telegram
echo "[4/5] Registrando comandos no Telegram..."
python3 set_commands.py
echo "  ✅ Comandos registrados."

# 5. Reiniciar o bot
echo "[5/5] Iniciando o bot..."
tmux new -d -s mth
tmux send-keys -t mth "cd ~/mth-ddos-bot && python3 Mth_Ddos_v50.py polling" C-m
echo "  ✅ Bot iniciado na sessão 'mth'."

echo ""
echo "============================================"
echo "  ✅ Deploy concluído com sucesso!"
echo "  Para ver o bot: tmux attach -t mth"
echo "============================================"
