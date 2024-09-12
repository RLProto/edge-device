#!/bin/bash

# Atualiza os pacotes e instala o Docker
sudo apt remove -y docker-ce*
echo "[INFO] Atualizando o sistema e instalando o Docker..."
sudo apt-get update
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adiciona o usuário atual ao grupo Docker
echo "[INFO] Adicionando o usuário ao grupo Docker..."
sudo usermod -aG docker $USER
dockerd-rootless-setuptool.sh install

# (Opcional) Instala o Docker Compose
echo "[INFO] Instalando Docker Compose..."
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
