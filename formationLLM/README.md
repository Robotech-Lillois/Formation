# Pour windows:

Vous installez winget sur le windows store

puis dans un terminal: winget install llama.cpp

# Pour linux:

curl -LsSf https://llama.app/install.sh | sh

# Commande pour installer le model

llama-server --hf-repo bartowski/Ling-3.0-tiny-GGUF:Q4_K_M -fa on

ou sur debian (quand c'est installé avec la commande, beaucoup plus de
controle si c'est installé avec un simple git clone):

llama serve --hf-repo bartowski/Ling-3.0-tiny-GGUF:Q4_K_M -fa on

# Quelques conseils:

Cette formation est pour les debutants. Vous pouvez gratter BEAUCOUP plus de
performances avec llama.cpp si vous manipulez bien les flags. RTFM.

Pour les systemes a très haute peformance (<32G VRAM):

Je recommande vLLM ou ninfer. llama.cpp est tres bien optimisé mais il
essaye de supporter trop de backends pour être la meilleure option.
