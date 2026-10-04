# Formation

Toutes les documents des formations Robotech sont à retrouver ici.

---

# Comment ça marche un README?

_surement pas avec des jambes déjà_

Un README c'est un document **markdown** qui fait l'objet d'une couverture sur un dossier git.
Un README agit comme un sommaire qui explique comment utiliser le dossier du repo git.

Par exemple:
- [Git](./Git/): formation git.
- [Kicad](./kicad/): formation kicad.

## Markdown

Le markdown est une extension de fichier texte permettant d'appliquer du style sur le texte contrairement à l'extensions classique `.txt`.

On utilise ce language particulièrement pour des `README.md`.

### Typo de base du markdown :

# Titre 1

## Titre 2

### Titre 3

#### Titre 4

**Texte en gras**

_Texte en italique_

~~Texte barré~~

==Texte surligné==

- Élément 1
- Élément 2
  - Sous-élément
  - Sous-élément 2
    - sous-sous-element
      - sous-sous-sous-element

1. étape 1
2. étape 2

- [ ] A faire
- [x] Fait

```c
#include <stdio.h>
int main() {//exemple
    return 0;
}
```

`code en ligne`

#### Liens

- Liens sur le web:

![pic](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2Fv2%2FD4D12AQF6DUzUOh9srg%2Farticle-cover_image-shrink_720_1280%2Farticle-cover_image-shrink_720_1280%2F0%2F1714986616134%3Fe%3D2147483647%26v%3Dbeta%26t%3DN3VrB05JKVQRFggtM80AnyhowK7t_lTbtOE0ZDRbJis&f=1&nofb=1&ipt=d97be4ebcb42fda791776b7c234b301474ac682105cc3a7051ce141cc955dcac)
[Lien externe](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2Fv2%2FD4D12AQF6DUzUOh9srg%2Farticle-cover_image-shrink_720_1280%2Farticle-cover_image-shrink_720_1280%2F0%2F1714986616134%3Fe%3D2147483647%26v%3Dbeta%26t%3DN3VrB05JKVQRFggtM80AnyhowK7t_lTbtOE0ZDRbJis&f=1&nofb=1&ipt=d97be4ebcb42fda791776b7c234b301474ac682105cc3a7051ce141cc955dcac)

- Liens en local :

![pic1](./pict/Logo_Robotech.jpg)
[pic2](./pict/github_logo.png)

#### HTML

<div style="display:flex; justify-content:space-between; gap:16px;">
  <img src="./pict/Logo_Robotech.jpg>"
  <img src="./pict/github_logo.png">
</div>
<div style="display:flex; justify-content:space-between; gap:16px;">
  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2Fv2%2FD4D12AQF6DUzUOh9srg%2Farticle-cover_image-shrink_720_1280%2Farticle-cover_image-shrink_720_1280%2F0%2F1714986616134%3Fe%3D2147483647%26v%3Dbeta%26t%3DN3VrB05JKVQRFggtM80AnyhowK7t_lTbtOE0ZDRbJis&f=1&nofb=1&ipt=d97be4ebcb42fda791776b7c234b301474ac682105cc3a7051ce141cc955dcac" alt="Left image" style="width:48%; height:auto;">
  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2Fv2%2FD4D12AQF6DUzUOh9srg%2Farticle-cover_image-shrink_720_1280%2Farticle-cover_image-shrink_720_1280%2F0%2F1714986616134%3Fe%3D2147483647%26v%3Dbeta%26t%3DN3VrB05JKVQRFggtM80AnyhowK7t_lTbtOE0ZDRbJis&f=1&nofb=1&ipt=d97be4ebcb42fda791776b7c234b301474ac682105cc3a7051ce141cc955dcac" alt="Right image" style="width:48%; height:auto;">
</div>

#### Obsidian

Obsidian utilise des variantes du markdown et cartaines balises sont intéréssantes à utiliser. Pour plus de détail on peut regarder [ce lien](https://github.com/mot-prog/Obsidian/blob/main/Obsidian_CheatList.md)

#### LateX

Le latex est un language utiliser principalement pour écrire des formules mathématiques. On peut l'utiliser directement dans un fichier markdown par exemple :

$$V_- = \frac{R1}{R1+R2}V_s$$

Pour plus de commandes de bases on peut aller voir [ce fichier](https://github.com/mot-prog/Obsidian/blob/main/Latex_Cheatlist.md)
