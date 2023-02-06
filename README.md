## Préparer les onglets
Ctrl+click sur les liens suivants :

- https://www.msys2.org/ ;
- https://www.eclipse.org/downloads/ ;
- https://git-scm.com/download/win ;
- https://github.com/coreybutler/nvm-windows/releases ;
- https://code.visualstudio.com/download.

---
Télécharger les outils
-
- Créer un dossier `ilog` le plus haut possible dans l'arborescence des fichiers, idéalement `D:\ilog` ;
- Créer un dossier `ilog/downloads` ;
- Sur le bureau, créer un raccourci `ilog` vers le dossier `ilog`.

### Télécharger MSys2
On utilise cet environnement pour les outils de build en langage C.

Depuis https://www.msys2.org/ :
- télécharger l'installeur ;
- sauvegarder en `ilog\downloads` ;
- c'est tout pout l'instant.

### Télécharger Eclipse
Pour installer eclipse, on va télécharger l'installeur qui présente l'avantage de prendre aussi en charge l'installation éventuelle d'un JDK (Java Developer Kit).

Depuis https://www.eclipse.org/downloads/ :
- télécharger l'installeur ;
- sauvegarder dans `ilog\downloads`.

### Télécharger git
Depuis https://git-scm.com/download/win :
- cliquer `64-bit Git for Windows Setup` ;

### Télécharger Node Version Manager
Depuis https://github.com/coreybutler/nvm-windows/releases
- cliquer `nvm-setup.exe`.

### Télécharger VSCode
Depuis https://code.visualstudio.com/download ;

Dans `Windows` > `System Installer` : 
- télécharger `x64`.
 
---
Installer les outils
-
- Créer un dossier `D:\Programs` ;

### Installer MSys2
L'installation va avoir lieu dans `C:\msys64`.

- depuis `https://www.msys2.org/`, suivre les instructions 2. à 4. ;
- fermer le terminal `ucrt64` ;
- dans le dossier `ilog`, créer un raccourci mingw64 vers `C:\msys64\mingw64.exe` ;
- utiliser ce raccourci.

> - L'interprète de commandes de `MinGW64` se lance dans `mintty`. On va y utiliser **pacman** pour installer les outils de build en langage C.
> 
> - Quand *pacman* un paquet est installé, les paquets nécessaires au paquet installé (ses dépendances) sont aussi installés.
> 
> - **pacman** gère aussi des groupes de paquets ;
> 
> - pour en savoir plus sur les paquets, paquets de base et groupes de paquets, consulter l'[index des paquets](https://packages.msys2.org/queue).

- Commencer par mettre à jour les paquets existants :
```sh
pacman -Syu
```

- Installer ensuite les groupes de paquets suivants :
```sh
pacman -S base-devel
pacman -S mingw-w64-x86_64-toolchain
```

Concernant, la toolchain, le nombre de paquets étant assez important, on peut retirer les paquets relatifs à `ada`, `fortran` et `objectiveC`.

- indiquer les paquets suivants : `1-3 7 9-19`

>Les informations relatives à MSys2 sont issues de :
> - https://www.msys2.org/ ;
> - [*Configuration de MSys2 pour utilisation avec eclipse*](https://www.devdungeon.com/content/how-setup-gcc-msys2-eclipse-windows-c-development).

Modifier la variable d'environnement `Path` de Windows :
>
> Pour que les outils `gcc` et `make` soient accessibles aussi dans les CLI de Windows et dans eclipse, il est nécessaire que les dossiers `c:\msys64\usr\bin` et `c:\msys64\mingw64\bin` soient listés dans la variable d'environnement `Path` de Windows.
>

- `Win+R` (la touche Windows et R en même temps) ;

> La boîte de dialogue `Exécuter` apparaît...

- Entrer `SystemPropertiesAdvanced.exe` ;
- bouton `Variables d'environnement...`.

Ajouter ces 2 entrées à la variable `Path` :
- cliquer la ligne de la variable `Path` (*de l'utilisateur* c'est suffisant) ;
- bouton `Modifier` ;
- bouton `Nouveau` (pour ajouter une entrée) ;
- entrer la valeur `c:\msys64\usr\bin` ;
- bouton `Nouveau` ;
- entrer `c:\msys64\mingw64\bin` ;
- bouton `OK` (mais ce n'est pas fini).

### Ajouter des variables d'environnement

> Les variables `MSYS_HOME` et `MINGW_HOME` sont nécessaires pour faire connaître MSys2 et MinGW64 à eclipse :
- Bouton `Nouvelle...` pour ajouter une variable d'environnement ;
- la nommer `MSYS_HOME` ;
- lui donner la valeur `C:\msys64` ;
- bouton `OK`.

Idem pour la variable `MINGW_HOME` ;
- lui donner la valeur `C:\msys64\mingw64`.
- bouton `OK`.

Finir :
- Bouton `OK` ;
- Bouton `OK`.

Tester en lançant un CLI :
- `Win+R` `cmd` ;

Tester avec les commandes suivantes :
```cmd
echo %MSYS_HOME%
echo %MINGW_HOME%
gcc --version
make --version
exit
```

Installer Eclipse
---
- Créer d'abord le dossier du workspace eclipse `ilog\wse` ; il y en aura un autre pour VSCode.

>On va installer eclipse **pour le développement Java**.

- Exécuter l'installeur eclipse et se laisser guider ;
- choisir `Eclipse IDE for Java Developers` ;
- on peut laisser le choix de JDK proposé ;
- changer le dossier d'installation pour `D:\Programs`.

> Le dossier d'installation d'`eclipse` sera `D:\Programs\eclipse`

- Lancer l'installation ;
- lancer l'exécution du `eclipse` installé (`D:\Programs\eclipse\eclipse.exe`) ;
- changer le dossier du `w`ork`s`pace `e`clipse pour `ilog\wse` ;
- cocher la case pour que ce soit le dossier par défaut ;

Dans le dossier `ilog` :
- créer un raccourci `Eclipse` vers `D:\Programs\eclipse\eclipse.exe`.

Installer le CDT (C Development Tools)
-
Depuis le eclipse installé, on va maintenant installer les *plugins du CDT* (C/C++ Development Tools).

- Menu `Help` / `Eclipse Marketplace...` ;
- dans la zone de saisie de Find, taper `CDT` ;
- cliquer `Go` ou valider par `Entrée` ;
- choisir `Eclipse C/C++ IDE CDT` en cliquant le bouton `install` ;
- cliquer le bouton `Install More` pour revenir à l'étape précédente ;
- noter le Install Pending

De la même façon, chercher et planifier l'installation de :
- `eclox` (plugin pour le documenteur `doxygen`);
- cliquer `Install Now` pour passer à l'étape suivante ;

> laisser eclipse résoudre les dépendances...

- `Confirm`.
- `accept`er les licences d'utilisation.
- `Finish`.

>Noter en bas à droite la progression de l'installation.

- accepter l'installation de `eclox` sans certificat en cliquant `Trust` ;
- `Restart Now`.

> Eclipse redémarre. Le CDT est installé.

Installer git
-

- Exécuter l'installeur de git ;
- `Next` pour accepter la licence ;
- `Next` pour accepter le dossier d'installation proposé ;
- ajouter une icône sur le bureau ;
- ajouter un profil `bash` au terminal Windows ;
- `Next` ;
- `Next` pour accepter le nom de dossier `Git` proposé ;
- notepad
- openSSH bundled with Git ;
- openSSL library ;
- co windows ci unix ;
- main as default branch name ;
- bash and 3rd party softwares ;
- minTTy ;
- fast-forward.

Installer NVM
-






