#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  MTH DDOS Bot — Deploy automático para Fly.io (Termux)
#  Uso: bash fly_deploy.sh
# ═══════════════════════════════════════════════════════════════

set -e

echo "🚀 MTH DDOS Bot — Deploy Fly.io (Termux)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Atualizar Termux
echo ""
echo "📦 [1/6] Atualizando Termux..."
pkg update -y && pkg upgrade -y 2>/dev/null

# 2. Instalar dependências necessárias
echo ""
echo "📦 [2/6] Instalando dependências (git, curl, python, nano)..."
pkg install -y git curl python nano 2>/dev/null

# 3. Instalar flyctl
echo ""
echo "🛸 [3/6] Instalando flyctl..."
curl -L https://fly.io/install.sh | sh

# Adicionar flyctl ao PATH
export FLYCTL_INSTALL="/data/data/com.termux/files/home/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
echo "export FLYCTL_INSTALL=\"/data/data/com.termux/files/home/.fly\"" >> ~/.bashrc
echo "export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\"" >> ~/.bashrc

# 4. Login no Fly.io
echo ""
echo "🔑 [4/6] Fazendo login no Fly.io..."
echo "   Vai abrir o navegador. Faz login com sua conta Fly.io."
flyctl auth login

# 5. Clonar o repo e entrar na pasta
echo ""
echo "📂 [5/6] Clonando o bot..."
cd ~
if [ -d "mth-ddos-bot" ]; then
    echo "   Pasta já existe, atualizando..."
    cd mth-ddos-bot
    git pull origin master
else
    git clone https://github.com/Darklindo/mth-ddos-bot.git
    cd mth-ddos-bot
fi

# 6. Deploy
echo ""
echo "🚀 [6/6] Fazendo deploy no Fly.io..."
echo ""
echo "   Escolha a região: gru (São Paulo) ou ewr (Nova York)"
echo "   Dica: gru é mais rápido pro Brasil"
echo ""

# Criar ou atualizar o app
flyctl launch --no-deploy --name mth-ddos-bot --region gru --yes 2>/dev/null || true

# Deploy
flyctl deploy

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deploy concluído!"
echo ""
echo "📋 Comandos úteis:"
echo "   flyctl status          - Ver status do bot"
echo "   flyctl logs            - Ver logs em tempo real"
echo "   flyctl ssh console     - Acessar o servidor"
echo "   flyctl restart         - Reiniciar o bot"
echo "   flyctl doctor          - Diagnóstico"
echo ""
echo "📱 Para testar o bot, manda /start no Telegram!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
