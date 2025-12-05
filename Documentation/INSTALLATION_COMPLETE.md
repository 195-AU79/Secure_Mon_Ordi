# 🚀 Guide d'Installation Complet - IT Monitor v2.0

## 📋 Vue d'ensemble

Ce guide vous accompagne pas à pas pour installer le système IT Monitor sur votre machine.

---

## ⚡ Installation Automatique (Recommandée)

### 1. Téléchargez le fichier `setup.py`

### 2. Exécutez le script d'installation

```bash
# Linux/macOS
python3 setup.py

# Windows
python setup.py
```

Le script va automatiquement :
- ✅ Vérifier Python
- ✅ Créer tous les dossiers nécessaires
- ✅ Installer les dépendances
- ✅ Créer les fichiers de configuration

### 3. Copiez les fichiers dans les bons dossiers

Après avoir exécuté `setup.py`, copiez chaque fichier Python dans son dossier :

```
COPIER VERS LA RACINE:
├── main.py

COPIER VERS core/:
├── core/monitor.py
├── core/metrics_collector.py
└── core/config_manager.py

COPIER VERS detection/:
├── detection/anomaly_detector.py
└── detection/advanced_detector.py (si créé)

COPIER VERS analysis/:
├── analysis/root_cause_analyzer.py
└── analysis/recommendation_engine.py

COPIER VERS utils/:
├── utils/logger.py
└── utils/export.py

COPIER VERS web/:
└── web/dashboard_server.py (si créé)
```

### 4. Lancez le programme

```bash
python main.py
# ou
python3 main.py
```

---

## 🛠️ Installation Manuelle

Si vous préférez tout installer manuellement :

### Étape 1 : Créer les dossiers

```bash
# Linux/macOS
mkdir -p ITMonitor/{core,detection,analysis,web,utils,data/{logs,reports,history},config,scripts,tests}
cd ITMonitor
touch core/__init__.py detection/__init__.py analysis/__init__.py web/__init__.py utils/__init__.py tests/__init__.py

# Windows (PowerShell)
New-Item -ItemType Directory -Path ITMonitor\core,ITMonitor\detection,ITMonitor\analysis,ITMonitor\web,ITMonitor\utils,ITMonitor\data\logs,ITMonitor\data\reports,ITMonitor\data\history,ITMonitor\config,ITMonitor\scripts,ITMonitor\tests
cd ITMonitor
New-Item -ItemType File -Path core\__init__.py,detection\__init__.py,analysis\__init__.py,web\__init__.py,utils\__init__.py,tests\__init__.py
```

### Étape 2 : Installer les dépendances

```bash
pip install psutil
# ou
pip3 install psutil
```

### Étape 3 : Créer requirements.txt

```bash
echo "psutil>=5.9.0" > requirements.txt
```

### Étape 4 : Créer config/config.json

Créez le fichier `config/config.json` avec ce contenu :

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
    "enable_logging": true,
    "log_file": "data/logs/monitor.log"
  },
  "web_dashboard": {
    "enabled": true,
    "port": 8080
  }
}
```

### Étape 5 : Copier tous les fichiers .py

Copiez chaque fichier Python que vous avez reçu dans le bon dossier selon la structure ci-dessus.

---

## 📝 Liste Complète des Fichiers Nécessaires

### ✅ Fichiers Essentiels (Minimum)

```
ITMonitor/
├── main.py                              ⭐ OBLIGATOIRE
├── requirements.txt                     ⭐ OBLIGATOIRE
├── config/config.json                   ⭐ OBLIGATOIRE
├── core/
│   ├── __init__.py                      ⭐ OBLIGATOIRE
│   ├── monitor.py                       ⭐ OBLIGATOIRE
│   ├── metrics_collector.py             ⭐ OBLIGATOIRE
│   └── config_manager.py                ⭐ OBLIGATOIRE
├── detection/
│   ├── __init__.py                      ⭐ OBLIGATOIRE
│   └── anomaly_detector.py              ⭐ OBLIGATOIRE
├── analysis/
│   ├── __init__.py                      ⭐ OBLIGATOIRE
│   ├── root_cause_analyzer.py           ⭐ OBLIGATOIRE
│   └── recommendation_engine.py         ⭐ OBLIGATOIRE
└── utils/
    ├── __init__.py                      ⭐ OBLIGATOIRE
    ├── logger.py                        ✨ Recommandé
    └── export.py                        ✨ Recommandé
```

### ✨ Fichiers Optionnels (Fonctionnalités Avancées)

```
├── detection/
│   └── advanced_detector.py             # Détection 30+ anomalies
├── web/
│   ├── __init__.py
│   └── dashboard_server.py              # Dashboard web
├── scripts/
│   ├── start.sh
│   └── start.bat
└── README.md                            # Documentation
```

---

## 🧪 Vérification de l'Installation

### Test Rapide

```bash
# Afficher l'aide
python main.py --help

# Vérifier que psutil est installé
python -c "import psutil; print('✅ psutil OK')"

# Générer un rapport de test
python main.py --report basic
```

### Checklist d'Installation

Vérifiez que vous avez bien :

- [ ] Python 3.7+ installé (`python --version`)
- [ ] psutil installé (`pip show psutil`)
- [ ] Structure de dossiers créée
- [ ] Tous les fichiers __init__.py présents
- [ ] main.py à la racine
- [ ] Fichier config/config.json créé
- [ ] Tous les modules .py dans les bons dossiers
- [ ] Le programme se lance sans erreur

---

## 🚨 Résolution de Problèmes Courants

### Erreur: "No module named 'core'"

**Cause:** Les fichiers ne sont pas dans les bons dossiers

**Solution:**
```bash
# Vérifiez que vous êtes dans le dossier ITMonitor
pwd  # Linux/macOS
cd   # Windows

# Vérifiez la structure
ls -R  # Linux/macOS
tree   # Windows avec tree installé
```

### Erreur: "No module named 'psutil'"

**Cause:** psutil n'est pas installé

**Solution:**
```bash
pip install psutil
# ou
pip3 install psutil
# ou avec sudo sur Linux
sudo pip3 install psutil
```

### Erreur: "Permission denied"

**Cause:** Droits insuffisants pour lire certaines métriques

**Solution:**
```bash
# Linux/macOS
sudo python3 main.py

# Windows
# Clic droit sur cmd.exe > Exécuter en tant qu'administrateur
python main.py
```

### Le programme se lance mais crashe

**Solution:**
```bash
# Lancez avec plus de détails d'erreur
python main.py 2>&1 | tee error.log

# Vérifiez les imports
python -c "from core.monitor import ITMonitor; print('✅ Imports OK')"
```

### Erreur: "Config file not found"

**Cause:** Le fichier config.json est absent

**Solution:**
```bash
# Créer le dossier config s'il n'existe pas
mkdir -p config

# Créer un fichier de config minimal
cat > config/config.json << 'EOF'
{
  "thresholds": {"cpu": 80, "memory": 85, "disk": 90},
  "monitoring": {"interval_seconds": 5}
}
EOF
```

---

## 📊 Premier Lancement

### Mode Interactif

```bash
python main.py
```

Vous verrez :

```
╔═══════════════════════════════════════════════════════╗
║     Système de Monitoring IT Portable - v2.0          ║
║          Intelligence Artificielle Avancée            ║
╚═══════════════════════════════════════════════════════╝

🔧 Initialisation du système...
✅ Système: Windows 10 AMD64
✅ Hostname: MON-PC

MENU PRINCIPAL
1.  📊 Informations système
2.  🔍 Analyse instantanée (basique)
3.  🔬 Analyse complète (avancée - 30+ anomalies)
...
```

### Testez l'Analyse Complète

1. Choisissez l'option **3** dans le menu
2. Le système va analyser votre machine
3. Vous verrez le score de santé et les anomalies détectées
4. Des recommandations seront générées automatiquement

---

## 🎯 Configuration Initiale Recommandée

### 1. Ajustez les Seuils selon Votre Machine

Éditez `config/config.json` :

```json
{
  "thresholds": {
    "cpu": 75,        // 👈 Baissez si vous voulez plus d'alertes
    "memory": 80,     // 👈 Ajustez selon votre RAM
    "disk": 85        // 👈 Ajustez selon votre espace disque
  }
}
```

### 2. Activez le Logging (Recommandé)

```json
{
  "monitoring": {
    "enable_logging": true,
    "log_file": "data/logs/monitor.log"
  }
}
```

### 3. Testez le Monitoring Continu

```bash
# Mode basique (plus rapide)
python main.py --monitor basic

# Mode avancé (détection complète)
python main.py --monitor advanced
```

Appuyez sur **Ctrl+C** pour arrêter.

---

## 🌟 Fonctionnalités à Découvrir

### 1. Analyse Avancée (30+ Anomalies)

```bash
python main.py --report advanced
```

Détecte :
- CPU (pics, throttling, déséquilibre)
- Mémoire (fuites, SWAP excessif)
- Disque (saturation, IO élevé)
- Réseau (erreurs, paquets perdus, ports suspects)
- Processus (zombies, gourmands)
- Sécurité (processus suspects)

### 2. Export de Rapports

```bash
python main.py --export
```

Crée un fichier JSON dans `data/reports/`

### 3. Dashboard Web (Optionnel)

Si vous avez le fichier `web/dashboard_server.py` :

```bash
python web/dashboard_server.py
```

Puis ouvrez `http://localhost:8080`

---

## 📚 Ressources Supplémentaires

- 📖 **README.md** : Documentation complète
- 🔧 **config/config.json** : Toutes les options de configuration
- 📝 **data/logs/** : Historique des analyses
- 📊 **data/reports/** : Rapports exportés

---

## ✅ Installation Réussie !

Si vous pouvez :
- ✅ Lancer `python main.py`
- ✅ Voir le menu principal
- ✅ Faire une analyse (option 2 ou 3)
- ✅ Voir un score de santé

**🎉 Félicitations ! Votre installation est complète.**

---

## 🆘 Besoin d'Aide ?

Si vous rencontrez des problèmes :

1. Relisez ce guide
2. Vérifiez la checklist d'installation
3. Consultez la section "Résolution de Problèmes"
4. Vérifiez que tous les fichiers sont aux bons emplacements

**Astuce:** Utilisez `tree` (Linux/macOS) ou `dir /s` (Windows) pour voir votre structure de dossiers.

---

Bon monitoring ! 🖥️✨