# img/ — figures

- `logo.png` : (à copier depuis `~/polytech/robotech/Formation/Git/img/logo.png` si besoin — le template l'utilise dans le titre et le headline).
- Les 24 fichiers `*.jpg` proviennent de la leçon **« Attention in transformers, step-by-step »** (Deep Learning, Chapter 6) de 3Blue1Brown :
  https://www.3blue1brown.com/lessons/attention
  Licence du contenu 3Blue1Brown : **CC BY-NC-SA 4.0** (usage non commercial, avec attribution — à vérifier avant toute diffusion publique du support).
  Attribution à conserver dans le support : « Figures : 3Blue1Brown (Grant Sanderson), 3blue1brown.com/lessons/attention, CC BY-NC-SA ».

## Mapping rapide figure → usage (voir plan.md §4.2)
- `Embeddings.jpg` — tokens → vecteurs, directions = sens
- `MoleExample.jpg` / `TowerExample.jpg` — besoin de contexte (mole, Eiffel)
- `lastvector.jpg` — le dernier vecteur porte tout le contexte (« the murderer was… »)
- `SingleHead.jpg` `W_Q.jpg` `QueryKey.jpg` `Keys.jpg` `DotProduct.jpg` — schéma Q/K/V, scores
- `SoftMax.jpg` `Normalized.jpg` `Masking.jpg` — motif d'attention + masquage
- `ValueVector.jpg` `ValueQueryKey.jpg` `DeltaE.jpg` `added.jpg` — mise à jour E′ = E + ΔE
- `MultiHeaded.jpg` `Harry.jpg` — multi-têtes (96 têtes, GPT-3)
- `ManyBlocks.jpg` — blocs empilés (96 couches)
- `CountQueryKey.jpg` `ParameterCount2.jpg` `FinalCount.jpg` — compte de paramètres (≈58 Md d'attention ≈ 1/3 de GPT-3)
- `square.jpg` — motif d'attention en context² (coût du contexte)
