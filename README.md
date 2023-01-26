# larm

## Introduction
Ce projet challenge 1 permet de faire deplacer un robot de maniere autonome dans um environnement clos grace a un LIDAR.
Le challenge 2 permet en plus du challenge 1 de récupérer la carte dans de l'environnement du robot. Il permet aussi de détecter une bouteille Nuka-Cola ou de Nuka-Cherry grâce à la caméra. Le challenge devrait permettre de localiser la bouteille dans son environnement. Cependant cette partie n'a pas pu etre realisee par manque de temps.

## Materiel utilise
Ce projet a ete realise sur le systeme d'exploitation linux et la version Ubuntu 20.04.5 LTS disponible ici : https://doc.ubuntu-fr.org/focal

Le developpement a ete realise sur ROS2 foxy : https://docs.ros.org/en/foxy/index.html

Le robot utilise est un kobuki turtlebot2 : http://kobuki.yujinrobot.com/

Le robot est equipe d'un hokuyo 2D lidar et d'une camera realsens RGBD d435i

## Comment faire fonctionner

1. Brancher le robot, le lidar ainsi que la camera pour les challenges 2 et 3
2. Cloner le repertoire groupe
3. Faire un ```colcon build```
4. Faire un ```source install/setup.sh```
5. Lancer la demonstration ```ros2 launch challenge1```

## Strategie challenge 1

## Strategie challenge 2

## Strategie challenge 3
 
## Pistes d'amelioration
Le projet reste incomplet avec plusieurs axes d'amelioration possibles.

- Realiser le challenge 3. Il n'a pas pu etre realise par manque de temps. Il consiste a estimer la distance des bouteilles reperees et de placer repere sur la carte.
- Ameliorer la detection des bouteilles de nuke cola, notamment pour eviter les faux positifs.
- Utiliser le teleop pour faire controler le robot en plus de son fonctionnement autonome.



## Credits
Projet realise par Maxence Cockedey et Oscar Letzgus

Pour toutes informations, contactez maxence.cockedey@etu.imt-nord-europe.fr
