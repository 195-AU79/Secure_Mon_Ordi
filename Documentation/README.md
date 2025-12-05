# 🖥️ Système de Monitoring IT Portable avec IA

## 📖 Description

Système intelligent de **détection, analyse et recommandation** de pannes informatiques.  
Compatible **Windows, Linux et macOS**, il détecte **plus de 30 types d'anomalies** et génère des recommandations automatiques.

### ✨ Fonctionnalités Principales

- ✅ **Détection automatique** de 30+ types d'anomalies
- 🧠 **Analyse de cause racine** par IA
- 💡 **Recommandations intelligentes** avec commandes adaptées à votre OS
- 📊 **Dashboard web** en temps réel
- 📈 **Historique et statistiques** des métriques
- 🔄 **Monitoring continu** avec alertes
- 📁 **Export de rapports** (JSON, CSV, HTML)
- ⚙️ **Configuration flexible** via fichiers JSON

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étape 1 : Télécharger le projet

```bash
# Cloner ou télécharger le projet
git clone https://github.com/votre-repo/ITMonitor.git
cd ITMonitor

# Ou créer la structure manuellement
mkdir ITMonitor
cd ITMonitor
```

### Étape 2 : Créer la structure des dossiers

```bash
# Linux/macOS
mkdir -p core detection analysis web utils data/{logs,reports,history} config scripts tests

# Windows (PowerShell)
New-Item -ItemType Directory -Path core,detection,analysis,web,utils,data\logs,data\reports,data\history,config,scripts,tests
```

### Étape 3 : Installer les dépendances

```bash
# Linux/macOS
pip3 install psutil

# Windows
pip install psutil
```

### Étape 4 : Lancer le programme

```bash
# Linux/macOS
python3 main.py

# Windows
python main.py
```

---

## 📁 Structure du Projet

```
ITMonitor/
│
├── 📁 core/                      # Cœur du système
│   ├── monitor.py                # Classe principale
│   ├── metrics_collector.py     # Collecte métriques
│   └── config_manager.py         # Gestion config
│
├── 📁 detection/                 # Détection d'anomalies
│   ├── anomaly_detector.py       # Détection basique
│   └── advanced_detector.py      # Détection avancée (30+ anomalies)
│
├── 📁 analysis/                  # Analyse intelligente
│   ├── root_cause_analyzer.py    # Analyse cause racine
│   └── recommendation_engine.py  # Recommandations IA
│
├── 📁 web/                       # Interface web
│   └── dashboard_server.py       # Serveur dashboard
│
├── 📁 utils/                     # Utilitaires
│   ├── logger.py                 # Système de logs
│   └── export.py                 # Export rapports
│
├── 📁 data/                      # Données
│   ├── logs/                     # Fichiers de logs
│   ├── reports/                  # Rapports générés
│   └── history/                  # Historique
│
├── 📁 config/                    # Configuration
│   └── config.json               # Config principale
│
├── main.py                       # Point d'entrée
└── requirements.txt              # Dépendances
```

---

## 🎯 Utilisation

### Mode Interactif (par défaut)

```bash
python main.py
```

Menu complet avec toutes les fonctionnalités disponibles.

### Mode Ligne de Commande

```bash
# Monitoring continu (basique)
python main.py --monitor basic

# Monitoring continu (avancé - 30+ anomalies)
python main.py --monitor advanced

# Générer un rapport unique
python main.py --report advanced

# Exporter un rapport JSON
python main.py --export

# Afficher l'aide
python main.py --help
```

---

## 🔍 Types d'Anomalies Détectées

### 🔥 Performance (12 types)
- CPU élevé / critique / pic soudain
- Mémoire élevée / critique / fuite mémoire
- Utilisation SWAP excessive
- IO disque élevé
- Déséquilibre CPU (charge inégale entre cœurs)
- Throttling CPU (surchauffe)
- Changements de contexte excessifs

### 💾 Stockage (5 types)
- Disque plein / critique
- Espace libre insuffisant
- Erreurs lecture/écriture disque
- Utilisation inodes élevée

### 🌐 Réseau (8 types)
- Erreurs réseau
- Paquets perdus
- Trop de connexions
- Ports suspects ouverts
- Bande passante élevée
- Latence réseau
- Interfaces réseau down

### ⚙️ Processus (7 types)
- Processus zombies
- Trop de processus
- Processus gourmand CPU
- Processus gourmand mémoire
- Ratio processus sleeping élevé
- Processus root/admin suspects

### 🔒 Sécurité (3 types)
- Ports suspects
- Trop de processus privilégiés
- Tentatives de connexion échouées

### 🖥️ Système (5 types)
- Uptime très long (besoin redémarrage)
- Load average élevé
- Surcharge système globale
- Température élevée (si détectable)

---

## 💡 Exemples de Recommandations IA

L'IA génère automatiquement des recommandations priorisées et adaptées à votre système :

### Exemple : CPU Élevé

```
🔴 ANOMALIE DÉTECTÉE: CPU critique à 94%

🔍 Cause Racine:
   3 processus consomment le plus de CPU
   Top processus: chrome.exe, firefox.exe, node.exe

💡 RECOMMANDATIONS:

   1. [URGENT] Analyser le processus chrome.exe
      Commande: PID: 1234 | CPU: 45.2%
      Impact: Identification de la cause
      Temps estimé: 2-5 minutes

   2. [HIGH] Si non essentiel, arrêter le processus
      Commande: taskkill /PID 1234 /F
      Impact: Libération immédiate du CPU
      ⚠️  Vérifier l'importance avant d'arrêter

   3. [MEDIUM] Vérifier les tâches planifiées
      Commande: schtasks /query
      Impact: Identification des tâches automatiques
```

### Exemple : Disque Plein

```
🔴 ANOMALIE DÉTECTÉE: Disque critique à 96%

🔍 Cause Racine:
   Espace libre: 2.3 GB
   C:\: 96% utilisé

💡 RECOMMANDATIONS:

   1. [URGENT] Nettoyer fichiers temporaires
      Commande: cleanmgr /sagerun:1
      Impact: Libération de 1-5 GB
      Temps estimé: 5-10 minutes

   2. [URGENT] Vider la corbeille
      Impact: Libération immédiate
      Temps estimé: 1 minute

   3. [HIGH] Identifier les gros fichiers
      Commande: WinDirStat ou TreeSize
      Impact: Localisation des fichiers volumineux
```

---

## ⚙️ Configuration

### Fichier `config/config.json`

```json
{
  "thresholds": {
    "cpu": 80,
    "memory": 85,
    "disk": 90
  },
  "monitoring": {
    "interval_seconds": 5,
    "history_size": 100,
    "enable_logging": true
  },
  "web_dashboard": {
    "enabled": true,
    "port": 8080
  }
}
```

### Modifier les seuils

```bash
# Via le menu interactif
python main.py
# Puis choisir option "10. Configuration"

# Ou modifier directement config/config.json
```

---

## 📊 Dashboard Web

### Lancement

```bash
python web/dashboard_server.py
```

Puis ouvrez votre navigateur : `http://localhost:8080`

### Fonctionnalités
- 📈 Visualisation en temps réel
- 🔄 Actualisation automatique (5s)
- 📊 Graphiques interactifs
- 💡 Recommandations en direct
- 📱 Interface responsive (mobile-friendly)

---

## 🧪 Tests

```bash
# Lancer les tests
python -m pytest tests/

# Test d'un module spécifique
python -m pytest tests/test_detection.py
```

---

## 📝 Export de Rapports

### Formats disponibles
- **JSON** : Données brutes complètes
- **CSV** : Pour Excel/LibreOffice
- **HTML** : Rapport formaté visualisable
- **PDF** : Rapport professionnel (nécessite wkhtmltopdf)

### Utilisation

```bash
# Via ligne de commande
python main.py --export

# Via le menu interactif
# Option "8. Exporter rapport"
```

Les rapports sont sauvegardés dans `data/reports/`

---

## 🔧 Commandes Utiles par OS

### Windows
```cmd
# Voir processus
tasklist

# Arrêter processus
taskkill /PID 1234 /F

# Nettoyer disque
cleanmgr

# Infos réseau
ipconfig /all
```

### Linux
```bash
# Voir processus
ps aux | grep <nom>

# Arrêter processus
kill -9 1234

# Nettoyer disque
sudo apt-get clean
sudo apt-get autoremove

# Infos réseau
ip addr show
```

### macOS
```bash
# Voir processus
ps aux | grep <nom>

# Arrêter processus
kill -9 1234

# Nettoyer cache
sudo purge

# Infos réseau
ifconfig
```

---

## 🚨 Dépannage

### Erreur: "Module 'psutil' not found"
```bash
pip install psutil
# ou
pip3 install psutil
```

### Erreur: "Permission denied"
```bash
# Linux/macOS
sudo python3 main.py

# Windows
# Exécuter en tant qu'administrateur
```

### Le dashboard web ne démarre pas
```bash
# Vérifier si le port 8080 est libre
netstat -an | grep 8080

# Changer le port dans config/config.json
```

---

## 📚 Documentation API

### Utilisation Programmatique

```python
from core.monitor import ITMonitor

# Créer une instance
monitor = ITMonitor()

# Collecter métriques
metrics = monitor.collect_metrics()

# Générer rapport
report = monitor.generate_report(detection_mode='advanced')

# Démarrer monitoring
def callback(report):
    print(f"Score: {report['health_score']}/100")
    
monitor.start_monitoring(interval=5, callback=callback)
```

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit vos changements (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour les détails.

---

## 👨‍💻 Auteur

Développé avec ❤️ par l'équipe IT Monitor

---

## 🌟 Support

- 📧 Email: support@itmonitor.com
- 🐛 Issues: [GitHub Issues](https://github.com/votre-repo/ITMonitor/issues)
- 📖 Documentation: [Wiki](https://github.com/votre-repo/ITMonitor/wiki)

---

## ✅ Checklist de Démarrage

- [ ] Python 3.7+ installé
- [ ] Dépendances installées (`pip install psutil`)
- [ ] Structure de dossiers créée
- [ ] Fichiers copiés aux bons emplacements
- [ ] Configuration vérifiée (`config/config.json`)
- [ ] Premier lancement réussi (`python main.py`)
- [ ] Test d'analyse complète (option 3)
- [ ] Dashboard web testé (optionnel)

**Vous êtes prêt ! 🎉**