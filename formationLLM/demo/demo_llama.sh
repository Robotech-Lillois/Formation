#!/usr/bin/env bash
# ============================================================================
# Démos de la formation « Des LLM aux agents locaux » (Robotech)
# Vérifié contre les sources au 2025-09-29 — relire plan.md §9 avant de jouer.
# ============================================================================
set -euo pipefail

# Petit CSV de démo pour la partie agent
mkdir -p ~/dsh-work && cd ~/dsh-work
printf 'name,qty\nwidget,3\nbolt,12\n' > parts.csv

# ----------------------------------------------------------------------------
# DEMO A — llama.cpp : chat local + serveur (API OpenAI-compatible + web UI)
# ----------------------------------------------------------------------------
# A1 : chat direct depuis Hugging Face (télécharge puis discute dans le terminal)
llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF

# A2 : serveur — API OpenAI-compatible ET interface web intégrée
#      --jinja : indispensable pour que les tool calls sortent au format OpenAI
llama-server -hf ggml-org/Qwen3.5-0.8B-GGUF \
  --host 127.0.0.1 --port 8080 -c 8192 --jinja

# A3 (pendant que le serveur tourne) : vérifier le modèle annoncé côté serveur
curl -s http://127.0.0.1:8080/v1/models | head -c 400; echo

# ----------------------------------------------------------------------------
# DEMO B — harnais d'agents : DeepSeek Harness branché sur le modèle local
# ----------------------------------------------------------------------------
# Préreq : Node >= 22.19 (ligne 22.x) ou >= 24 (Node 23 exclu) ; dsh en developer
# preview -> épingler la version testée en répétition.
#
# B1 : démarrer llama-server (voir A2, port 8080) avec -c 16384 pour les agents :
#   llama-server -hf ggml-org/Qwen3.5-0.8B-GGUF --host 127.0.0.1 --port 8080 -c 16384 --jinja
#
# B2 : démarrer l'interface web de dsh (UI sur http://127.0.0.1:3080)
npx @deepseek-ai/dsh web

# B3 : dans Settings -> Models -> "Add a custom model API", renseigner :
#   Provider ID : local
#   Base URL    : http://127.0.0.1:8080/v1
#   Protocol    : OpenAI Chat Completions (openai-completions)
#   Credential  : toute valeur non vide (le serveur local l'ignore), p.ex. "local"
#   Model id    : exactement ce qu'annonce GET /v1/models
#   contextWindow : <= au -c du serveur !! (sinon troncature silencieuse)
#
#   Équivalent YAML (profil web : $DSH_HOME/profiles/web/cordis.patch.yml ;
#   d'anciennes builds utilisaient ~/.dsh/settings.yaml — vérifier la version) :
#     voir dsh-provider-example.yaml dans ce dossier.
#
# B4 : tâche à lancer dans l'UI (démo de la boucle agent + coût du contexte) :
#   "Lis parts.csv et donne-moi la quantité totale."
#   Attendu : l'agent appelle l'outil de lecture de fichier puis répond 15.
#   Bonus : montrer dans les logs llama-server le prompt >10K tokens
#   (catalogue d'outils ~25 schémas renvoyés à chaque étape).
#
# PLANCULTE : si le modèle local est trop lent pour la boucle agent en direct,
# basculer la session sur l'API hébergée DeepSeek (même harnais, même démo).
