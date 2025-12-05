# 🖥️ Système de Monitoring IT Portable - Secure Mon Ordi

> Système intelligent de **détection, analyse et recommandation** de pannes informatiques avec Intelligence Artificielle Avancée

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

## 📋 Description

**Secure Mon Ordi** est un système de monitoring IT portable et intelligent qui détecte automatiquement **plus de 30 types d'anomalies** système, analyse leurs causes racines et génère des recommandations adaptées à votre système d'exploitation.

### ✨ Fonctionnalités Principales

- ✅ **Détection automatique** de 30+ types d'anomalies (CPU, mémoire, disque, réseau, processus, sécurité)
- 🧠 **Analyse de cause racine** par Intelligence Artificielle
- 💡 **Recommandations intelligentes** avec commandes adaptées à votre OS
- 📊 **Dashboard visuel** en temps réel
- 📈 **Historique et statistiques** des métriques système
- 🔄 **Monitoring continu** avec alertes automatiques
- 📁 **Export de rapports** (JSON, CSV, HTML)
- ⚙️ **Configuration flexible** via fichiers JSON
- 🌐 **Interface web** pour visualisation à distance

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

2. **Lancer le programme**

```bash
# Mode interactif (recommandé)
python main.py

# Ou en ligne de commande
python main.py --monitor advanced
```

## 📖 Utilisation

### Mode Interactif

```bash
python main.py
```

Le menu interactif vous permet d'accéder à toutes les fonctionnalités :
- 📊 Informations système
- 🔍 Analyse instantanée (basique ou avancée)
- 👁️ Détails des anomalies avec recommandations
- 📺 Dashboard visuel en temps réel
- 🔄 Monitoring continu
- 📁 Export de rapports
- ⚙️ Configuration

### Mode Ligne de Commande

```bash
# Monitoring continu (avancé - 30+ anomalies)
python main.py --monitor advanced

# Générer un rapport unique
python main.py --report advanced

# Exporter un rapport JSON
python main.py --export

# Aide
python main.py --help
```

## 🔍 Types d'Anomalies Détectées

Le système détecte automatiquement :

- **Performance** : CPU élevé, mémoire critique, fuites mémoire, IO disque, throttling CPU
- **Stockage** : Disque plein, espace insuffisant, erreurs disque
- **Réseau** : Erreurs réseau, paquets perdus, ports suspects, latence élevée
- **Processus** : Processus zombies, processus gourmands, processus suspects
- **Sécurité** : Ports suspects, processus privilégiés, tentatives de connexion
- **Système** : Uptime long, load average élevé, surcharge globale

## 📊 Exemple de Sortie

```
╔═══════════════════════════════════════════════════════╗
║     Système de Monitoring IT Portable - v2.0          ║
║          Intelligence Artificielle Avancée            ║
╚═══════════════════════════════════════════════════════╝

💚 SCORE DE SANTÉ: 85/100 - EXCELLENT

📊 MÉTRIQUES ACTUELLES:
  CPU:      45.2% (8 cœurs)
  Mémoire:  62.3% (12.5/20 GB)
  Disque:   78.1% (156/200 GB)
  Réseau:   2.34 MB/s ↑ | 1.12 MB/s ↓

⚠️  2 ANOMALIE(S) DÉTECTÉE(S)

🔴 ANOMALIE #1 [WARNING]
   Type: cpu_high
   CPU utilisation élevée à 85%

💡 RECOMMANDATIONS:
   1. [HIGH] Analyser le processus chrome.exe (PID: 1234)
   2. [MEDIUM] Vérifier les tâches planifiées
```

## 📁 Structure du Projet

```
Secure_Mon_Ordi/
├── core/              # Cœur du système (monitor, métriques, config)
├── detection/         # Détection d'anomalies (basique et avancée)
├── analysis/          # Analyse IA (cause racine, recommandations)
├── web/               # Interface web (dashboard serveur)
├── utils/             # Utilitaires (logger, export, visualisation)
├── config/            # Configuration (config.json)
├── data/              # Données (logs, rapports, historique)
├── Documentation/     # Documentation détaillée
└── main.py           # Point d'entrée principal
```

## ⚙️ Configuration

La configuration se trouve dans `config/config.json`. Vous pouvez modifier :

- **Seuils d'alerte** : CPU, mémoire, disque, réseau
- **Intervalle de monitoring** : Fréquence de collecte (par défaut 5s)
- **Dashboard web** : Port et paramètres
- **Notifications** : Email, webhooks
- **Export automatique** : Format et fréquence

Modifiez directement le fichier ou utilisez le menu interactif (option 12).

## 📚 Documentation Complète

Pour plus de détails, consultez la documentation dans le dossier `Documentation/` :

- **[README.md](Documentation/README.md)** - Guide complet d'installation et d'utilisation
- **[QUICK_START.md](Documentation/QUICK_START.md)** - Guide de démarrage rapide
- **[ARCHITECTURE.md](Documentation/ARCHITECTURE.md)** - Architecture du système
- **[VISUALISATION.md](Documentation/VISUALISATION.md)** - Guide du dashboard visuel

## 🛠️ Dépendances

Les principales dépendances sont listées dans `requirements.txt` :

- `psutil` - Collecte de métriques système
- Autres dépendances optionnelles pour le dashboard web

## 🔧 Dépannage

### Erreur: "Module 'psutil' not found"
```bash
pip install psutil
```

### Permission denied (Linux/macOS)
```bash
sudo python3 main.py
```

### Le dashboard web ne démarre pas
Vérifiez que le port 8080 est libre ou modifiez-le dans `config/config.json`.

## 👨‍💻 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Support

Pour toute question ou problème :
- 📖 Consultez la [documentation complète](Documentation/README.md)

---

**Développé avec ❤️ pour sécuriser et optimiser votre système**


