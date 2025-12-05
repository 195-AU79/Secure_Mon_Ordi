# 👁️ Guide des Fonctionnalités de Visualisation

## 🎨 Nouvelles Fonctionnalités Visuelles

Votre système IT Monitor dispose maintenant de **3 modes de visualisation** pour voir clairement toutes les anomalies !

---

## 📊 Mode 1 : Vue Détaillée des Anomalies (Option 4)

### ✨ Ce que vous voyez :

```
📋 LISTE DES ANOMALIES (3):
======================================================================

1. 🔴 [CRITICAL] cpu_critical
   Utilisation CPU critique: 94.2%...
   Valeur: 94.2%

2. 🟡 [WARNING] memory_high
   Utilisation mémoire élevée: 87.3%...
   Valeur: 87.3%

3. 🔵 [INFO] many_sleeping_processes
   75% des processus en sommeil...
```

### 🎯 Actions disponibles :

- **Taper un numéro (1-3)** : Voir tous les détails de cette anomalie
- **Taper A** : Voir toutes les anomalies en détail
- **Taper R** : Retour au menu

### 📋 Détails d'une Anomalie Spécifique :

```
======================================================================
ANOMALIE #1
======================================================================

🔴 CRITICAL

📌 Type: cpu_critical
📂 Catégorie: performance

💬 Utilisation CPU critique: 94.2%

📊 VALEURS:
   Valeur actuelle: 94.2%
   Seuil d'alerte:  90%
   Dépassement:     +4.2%

🔍 ANALYSE DE CAUSE RACINE:
----------------------------------------------------------------------

💡 Cause identifiée:
   3 processus consomment le plus de CPU

📝 Détails:
   Top processus: chrome.exe, firefox.exe, node.exe

⚙️  Composants affectés:
   • chrome.exe (PID 1234, 45.2%)
   • firefox.exe (PID 5678, 30.1%)
   • node.exe (PID 9012, 19.3%)

📈 Facteurs de sévérité:
   • CPU global: 94.2%
   • Seuil dépassé de 4.2%

📅 Chronologie:
   1. Augmentation progressive de la charge CPU
   2. Processus identifiés comme responsables
   3. Impact sur les performances système

💡 RECOMMANDATIONS DE RÉSOLUTION:
======================================================================

🚨 URGENT
----------------------------------------------------------------------

1. Analyser le processus chrome.exe
   📋 Commande: PID: 1234 | CPU: 45.2%
   ✅ Impact: Identification de la cause
   ⏱️  Temps estimé: 2-5 minutes

⚠️  PRIORITÉ HAUTE
----------------------------------------------------------------------

2. Si non essentiel, arrêter le processus
   📋 Commande: taskkill /PID 1234 /F
   ✅ Impact: Libération immédiate du CPU
   ⏱️  Temps estimé: Instantané
   ⚠️  Vérifier l'importance du processus avant de l'arrêter

3. Vérifier les tâches planifiées actives
   📋 Commande: schtasks /query
   ✅ Impact: Identification des tâches automatiques
   ⏱️  Temps estimé: 3-5 minutes
```

---

## 📺 Mode 2 : Dashboard Visuel en Temps Réel (Option 5)

### 🎯 Interface Complète avec Barres de Progression

```
╔════════════════════════════════════════════════════════════════════╗
║               DASHBOARD SYSTÈME EN TEMPS RÉEL                      ║
╚════════════════════════════════════════════════════════════════════╝

⏰ 2025-01-10 15:30:45

💚  SCORE DE SANTÉ: 85/100 - EXCELLENT
──────────────────────────────────────────────────────────────────────

📊 RESSOURCES SYSTÈME:
──────────────────────────────────────────────────────────────────────
CPU          [████████████░░░░░░░░░░░░░░░░░░] 42.3% 🟢 OK
Mémoire      [███████████████████░░░░░░░░░░░] 65.7% 🟢 OK
Disque       [██████████████████████████░░░░] 88.2% 🟡 ATTENTION
SWAP         [███░░░░░░░░░░░░░░░░░░░░░░░░░░░] 12.5% 🟢 OK

📈 TENDANCES (30 dernières secondes):

CPU:
100.0% |█                             |
 75.0% |█  █                          |
 50.0% |█  █ █   █                    |
 25.0% |█  █ █ █ █  █                 |
  0.0% |█ ██ █ █ █ ██  █ █           |
       ──────────────────────────────

Mémoire:
100.0% |                              |
 75.0% |           █                  |
 50.0% |     █  █  █ █  █             |
 25.0% |  █  █  █  █ █  █  █          |
  0.0% | ██ ███ ████████████ ██       |
       ──────────────────────────────

🌐 RÉSEAU:
──────────────────────────────────────────────────────────────────────
  ↑ Upload:       1.25 MB/s
  ↓ Download:     8.43 MB/s
  📦 Paquets perdus: 0
  ⚠️  Erreurs: 0

⚙️  PROCESSUS:
──────────────────────────────────────────────────────────────────────
  Total:   267
  Running: 12
  Zombie:  0

  🔥 Top CPU:
     • chrome.exe                 15.2%
     • code.exe                   8.3%
     • python.exe                 5.1%

⚠️  ANOMALIES:
──────────────────────────────────────────────────────────────────────
  🟡 Attention: 1

  Dernières anomalies:
     🟡 Disque presque plein: 88.2%...

──────────────────────────────────────────────────────────────────────
Appuyez sur Ctrl+C pour arrêter le monitoring
══════════════════════════════════════════════════════════════════════
```

### ✨ Fonctionnalités du Dashboard :

- **Actualisation automatique** toutes les 5 secondes
- **Barres de progression colorées** :
  - 🔴 Rouge : Critique (>90%)
  - 🟡 Jaune : Attention (>80%)
  - 🟢 Vert : OK (>60%)
  - 🔵 Bleu : Excellent (<60%)

- **Mini-graphiques ASCII** montrant les tendances
- **Top 3 processus** les plus gourmands
- **Résumé des anomalies** en temps réel
- **Score de santé** mis à jour en direct

---

## 📋 Mode 3 : Rapport Complet (Options 2 & 3)

### 🎯 Rapport Détaillé avec Tout :

```
══════════════════════════════════════════════════════════════════════
📋 RAPPORT COMPLET D'ANALYSE SYSTÈME
══════════════════════════════════════════════════════════════════════

⏰ Généré le: 2025-01-10T15:30:45.123456

🖥️  Système: Windows AMD64
💻 Hostname: MON-PC

🟡 SCORE DE SANTÉ: 72/100 - MOYEN

📊 MÉTRIQUES ACTUELLES:
──────────────────────────────────────────────────────────────────────
  🔥 CPU:      65.3% (8 cœurs)
  🧠 Mémoire:  78.9% (12.6/16.0 GB)
  💾 Disque:   88.2% (441.0/500.0 GB)
  🌐 Réseau:   1.25 MB/s ↑ | 8.43 MB/s ↓
  ⚙️  Processus: 267

══════════════════════════════════════════════════════════════════════

⚠️  2 ANOMALIE(S) DÉTECTÉE(S)
══════════════════════════════════════════════════════════════════════

🟡 ATTENTION: 2

📋 DÉTAILS ET ANALYSES:

[Puis affichage détaillé de chaque anomalie avec analyse et recommandations]
```

---

## 🎨 Codes Couleurs

### Sévérité des Anomalies :

- 🔴 **CRITIQUE** : Action immédiate requise
- 🟡 **ATTENTION** : Surveiller et agir bientôt  
- 🔵 **INFO** : Informationnel, pas d'urgence

### État des Ressources :

- **Rouge** (>90%) : Saturé, risque élevé
- **Jaune** (80-90%) : Élevé, attention requise
- **Vert** (60-80%) : Normal, bon état
- **Bleu** (<60%) : Optimal, excellent

---

## 🚀 Guide d'Utilisation Rapide

### Pour Voir une Anomalie Spécifique :

1. Lancez le programme : `python main.py`
2. Choisissez option **4** (Voir détails des anomalies)
3. Le système affiche la liste numérotée
4. Tapez le numéro de l'anomalie à examiner
5. Voyez tous les détails + recommandations !

### Pour le Dashboard en Temps Réel :

1. Lancez le programme : `python main.py`
2. Choisissez option **5** (Dashboard visuel)
3. Observez les barres et graphiques en direct
4. Ctrl+C pour arrêter

### Pour une Analyse Ponctuelle :

1. Lancez le programme : `python main.py`
2. Choisissez option **3** (Analyse complète)
3. Attendez 1-2 secondes
4. Lisez le rapport détaillé

---

## 💡 Astuces de Visualisation

### 1. **Comparaison Avant/Après**

Faites une analyse, appliquez une recommandation, puis refaites une analyse :

```bash
# Analyse 1
python main.py --report advanced > avant.txt

# [Appliquez la recommandation]

# Analyse 2
python main.py --report advanced > apres.txt

# Comparez
diff avant.txt apres.txt
```

### 2. **Monitoring Continu avec Logs**

```bash
# Lance le dashboard et sauvegarde dans un fichier
python main.py --monitor advanced 2>&1 | tee monitoring.log
```

### 3. **Focus sur les Anomalies Critiques**

Dans l'option 4, les anomalies sont triées par sévérité :
- Les critiques apparaissent en premier 🔴
- Puis les avertissements 🟡
- Puis les infos 🔵

---

## 🔧 Personnalisation de l'Affichage

### Désactiver les Couleurs (si problème d'affichage)

Éditez `utils/anomaly_viewer.py` :

```python
def __init__(self):
    self.colors_enabled = False  # ← Mettez False
```

### Changer la Largeur des Barres

Éditez `utils/visual_dashboard.py` :

```python
def create_bar(self, value, max_value=100, width=40):  # ← Changez width
```

### Modifier la Hauteur des Graphiques

```python
def display_mini_graph(self, history, height=7):  # ← Changez height
```

---

## 📊 Exemples Concrets

### Exemple 1 : Détecter une Fuite Mémoire

```
1. Lancez option 5 (Dashboard)
2. Observez le graphique "Mémoire"
3. Si la ligne monte constamment : fuite mémoire !
4. Appuyez sur Ctrl+C
5. Choisissez option 4 pour voir les détails
6. Suivez les recommandations
```

### Exemple 2 : Identifier un Processus Gourmand

```
1. Option 3 (Analyse complète)
2. Regardez la section "⚠️  ANOMALIES"
3. Si "process_cpu_hog" détecté :
   - Le nom du processus est affiché
   - Le PID est indiqué
   - La commande pour l'arrêter est fournie
```

### Exemple 3 : Surveiller l'Espace Disque

```
1. Option 5 (Dashboard)
2. Regardez la barre "Disque"
3. Si elle devient jaune (>85%) ou rouge (>90%) :
   - Sortez du dashboard (Ctrl+C)
   - Option 4 pour voir les détails
   - Appliquez les recommandations de nettoyage
```

---

## 🎯 Quelle Vue Utiliser Quand ?

### 📺 **Dashboard Visuel (Option 5)**
**Quand ?** Monitoring quotidien, surveillance continue
**Avantage** : Vue d'ensemble rapide, tendances visuelles

### 👁️ **Détails Anomalies (Option 4)**
**Quand ?** Problème détecté, besoin d'analyse approfondie
**Avantage** : Détails complets, recommandations précises

### 📋 **Rapport Complet (Option 3)**
**Quand ?** Audit, documentation, export
**Avantage** : Toutes les informations en un seul rapport

---

## 🆘 Résolution de Problèmes d'Affichage

### Problème : Caractères bizarres (█ ░ ▓)

**Cause** : Encodage du terminal

**Solution** :
```bash
# Windows
chcp 65001

# Linux/macOS
export LANG=en_US.UTF-8
```

### Problème : Couleurs ne s'affichent pas

**Cause** : Terminal ne supporte pas les couleurs ANSI

**Solution** : Utilisez un terminal moderne :
- Windows : Windows Terminal (recommandé)
- Linux : gnome-terminal, konsole
- macOS : iTerm2, Terminal.app

### Problème : Dashboard clignote

**Cause** : Rafraîchissement trop rapide

**Solution** : Augmentez l'intervalle dans `config/config.json` :
```json
{
  "monitoring": {
    "interval_seconds": 10
  }
}
```

---

## 📚 Récapitulatif des Fichiers

### Fichiers de Visualisation :

```
utils/
├── anomaly_viewer.py        # Vue détaillée des anomalies
└── visual_dashboard.py      # Dashboard temps réel
```

### Pour Installer :

1. Copiez `anomaly_viewer.py` dans `utils/`
2. Copiez `visual_dashboard.py` dans `utils/`
3. Relancez `main.py`
4. Profitez des nouvelles vues ! 🎉

---

## ✨ Fonctionnalités Futures

En développement :

- 📸 **Captures d'écran** des anomalies
- 📧 **Alertes email** avec visualisations
- 📱 **Dashboard mobile** (HTML)
- 🎨 **Thèmes personnalisables**
- 📊 **Export PDF** avec graphiques

---

**Vous pouvez maintenant voir TOUTES vos anomalies de manière claire et détaillée ! 🎊**