# 🏗️ Architecture du Système IT Monitor

## 📐 Vue d'Ensemble

Le système IT Monitor est une application Python modulaire et extensible conçue pour détecter, analyser et recommander des solutions aux pannes informatiques sur n'importe quelle machine.

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Utilisateur                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │   Menu CLI  │  │ Dashboard Web│  │  API REST (futur)  │ │
│  └──────┬──────┘  └──────┬───────┘  └─────────┬──────────┘ │
└─────────┼────────────────┼───────────────────┼─────────────┘
          │                │                   │
          └────────────────┼───────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    ITMonitor (Core)                          │
│  • Orchestration générale                                    │
│  • Gestion du cycle de vie                                   │
│  • Coordination des modules                                  │
└────┬─────────┬──────────┬────────────┬───────────┬──────────┘
     │         │          │            │           │
     ▼         ▼          ▼            ▼           ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌─────────┐ ┌────────────┐
│Metrics  │ │Anomaly │ │Root    │ │Recomm.  │ │Config      │
│Collector│ │Detector│ │Cause   │ │Engine   │ │Manager     │
└─────────┘ └────────┘ └────────┘ └─────────┘ └────────────┘
     │         │          │            │           │
     └─────────┴──────────┴────────────┴───────────┘
                         │
                    ┌────▼────┐
                    │ psutil  │ (Bibliothèque système)
                    └─────────┘
```

---

## 🧩 Modules Principaux

### 1. **core/** - Cœur du Système

#### `monitor.py` - Classe Principale
```python
class ITMonitor:
    """
    Orchestrateur principal du système.
    Coordonne tous les modules et gère le cycle de vie.
    """
    
    Responsabilités:
    - Initialisation des composants
    - Collecte périodique des métriques
    - Détection et analyse des anomalies
    - Génération de rapports
    - Gestion du monitoring continu
```

**Flux d'exécution:**
```
Initialisation
    ↓
Configuration chargée
    ↓
Collecte métriques → Détection anomalies → Analyse cause → Recommandations
    ↓                      ↓                    ↓              ↓
Historique            Si anomalie         Root Cause      Solutions
                      détectée            Analysis        priorisées
```

#### `metrics_collector.py` - Collecteur de Métriques
```python
class MetricsCollector:
    """
    Collecte toutes les métriques système via psutil.
    Interface unique pour l'accès aux données système.
    """
    
    Métriques collectées:
    - CPU: utilisation, fréquence, statistiques, par cœur
    - Mémoire: RAM, SWAP, buffers, cache
    - Disque: utilisation, IO, partitions
    - Réseau: bande passante, erreurs, connexions
    - Processus: liste, statuts, top CPU/RAM
    - Système: uptime, load average, utilisateurs
```

#### `config_manager.py` - Gestionnaire de Configuration
```python
class ConfigManager:
    """
    Gestion de la configuration via fichiers JSON.
    Permet modification dynamique des paramètres.
    """
    
    Configuration gérée:
    - Seuils d'alerte personnalisables
    - Intervalles de monitoring
    - Options de logging
    - Paramètres dashboard
```

---

### 2. **detection/** - Détection d'Anomalies

#### `anomaly_detector.py` - Détection Basique
```python
class AnomalyDetector:
    """
    Détection basique basée sur des seuils simples.
    Performance: Très rapide (~100ms)
    """
    
    Anomalies détectées (6 types):
    - CPU élevé
    - Mémoire élevée
    - SWAP élevé
    - Disque plein
    - Erreurs réseau
    - Processus zombies
```

**Algorithme:**
```
Pour chaque métrique:
    Si valeur > seuil_warning:
        Créer anomalie (severity: warning)
    Si valeur > seuil_critical:
        Créer anomalie (severity: critical)
```

#### `advanced_detector.py` - Détection Avancée
```python
class AdvancedAnomalyDetector:
    """
    Détection avancée avec analyse temporelle.
    Performance: Rapide (~300ms)
    """
    
    Anomalies détectées (30+ types):
    • Performance: 12 types
    • Stockage: 5 types  
    • Réseau: 8 types
    • Processus: 7 types
    • Sécurité: 3 types
    • Système: 5 types
```

**Techniques utilisées:**
```
1. Seuils statiques
2. Analyse de tendances (historique)
3. Détection de pics soudains
4. Corrélation multi-métriques
5. Détection de patterns anormaux
```

---

### 3. **analysis/** - Analyse Intelligente

#### `root_cause_analyzer.py` - Analyse de Cause Racine
```python
class RootCauseAnalyzer:
    """
    Identifie la cause racine d'une anomalie.
    Utilise l'analyse contextuelle des métriques.
    """
    
    Méthodologie:
    1. Identifier le type d'anomalie
    2. Collecter le contexte (processus, métriques)
    3. Corréler les informations
    4. Déterminer la cause probable
    5. Construire la chronologie
```

**Exemple d'analyse:**
```
Anomalie: CPU élevé (92%)
    ↓
Contexte: 3 processus >20% CPU
    ↓
Corrélation: chrome.exe (45%), node.exe (30%)
    ↓
Cause racine: "Applications gourmandes multiples"
    ↓
Composants affectés: [chrome.exe, node.exe, system]
    ↓
Chronologie: [Lancement normal → Charge accrue → Saturation]
```

#### `recommendation_engine.py` - Moteur de Recommandations
```python
class RecommendationEngine:
    """
    Génère des recommandations intelligentes et priorisées.
    Adapte les commandes au système d'exploitation.
    """
    
    Stratégie:
    - Analyse anomalie + cause racine
    - Génération de solutions multi-niveaux
    - Priorisation (urgent/high/medium/low)
    - Adaptation OS (Windows/Linux/macOS)
    - Estimation temps et impact
```

**Structure des recommandations:**
```python
{
    'priority': 'urgent|high|medium|low',
    'action': 'Description de l'action',
    'command': 'Commande système spécifique',
    'impact': 'Impact attendu',
    'estimated_time': 'Temps estimé',
    'warning': 'Avertissements éventuels'
}
```

---

### 4. **utils/** - Utilitaires

#### `logger.py` - Système de Logs
```python
class SystemLogger:
    """
    Logging structuré des événements système.
    """
    
    Logs enregistrés:
    - Rapports de monitoring
    - Anomalies détectées
    - Actions effectuées
    - Erreurs système
```

#### `export.py` - Export de Rapports
```python
class ReportExporter:
    """
    Export multi-format des rapports.
    """
    
    Formats supportés:
    - JSON: Données complètes
    - CSV: Pour analyse Excel
    - HTML: Visualisation web
    - PDF: Rapport professionnel (optionnel)
```

---

## 🔄 Flux de Données

### Cycle de Monitoring Continu

```
┌─────────────────────────────────────────────────────┐
│ 1. Collecte Métriques (MetricsCollector)           │
│    • CPU, RAM, Disk, Network, Processes            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 2. Stockage Historique (deque)                     │
│    • Maintien des 100 dernières valeurs            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 3. Détection Anomalies                             │
│    • AnomalyDetector (basique) OU                  │
│    • AdvancedAnomalyDetector (avancé)              │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
         Anomalies détectées?
                 │
        ┌────────┴────────┐
        │ NON             │ OUI
        ▼                 ▼
┌──────────────┐  ┌────────────────────────────────┐
│ 4a. Rapport  │  │ 4b. Analyse Cause Racine       │
│     Normal   │  │     (RootCauseAnalyzer)        │
└──────────────┘  └────────────┬───────────────────┘
                               │
                               ▼
                  ┌─────────────────────────────────┐
                  │ 5. Génération Recommandations   │
                  │    (RecommendationEngine)       │
                  └────────────┬────────────────────┘
                               │
                               ▼
                  ┌─────────────────────────────────┐
                  │ 6. Rapport Complet avec         │
                  │    Analyses + Recommandations   │
                  └────────────┬────────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
        ▼                                             ▼
┌──────────────┐                            ┌─────────────────┐
│ 7a. Logging  │                            │ 7b. Affichage   │
│  (Logger)    │                            │     Utilisateur │
└──────────────┘                            └─────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│ 8. Attendre intervalle (5s par défaut)              │
└────────────────┬─────────────────────────────────────┘
                 │
                 └─────► Retour à l'étape 1
```

---

## 🧠 Intelligence Artificielle

### Algorithmes Utilisés

#### 1. **Détection d'Anomalies par Seuils Adaptatifs**
```python
# Seuils dynamiques basés sur l'historique
if len(history) >= 10:
    mean = statistics.mean(history)
    std = statistics.stdev(history)
    
    # Anomalie si > moyenne + 2 écarts-types
    if current_value > mean + (2 * std):
        detect_anomaly()
```

#### 2. **Analyse de Tendances**
```python
# Détection de croissance constante (fuite mémoire)
if all(history[i] < history[i+1] for i in range(len(history)-1)):
    detect_memory_leak()
```

#### 3. **Corrélation Multi-Métriques**
```python
# Surcharge système si CPU + RAM + SWAP élevés
if cpu > 80 and memory > 80 and swap > 20:
    severity = 'critical'
    type = 'system_overload'
```

#### 4. **Classification par Règles**
```python
# Système expert basé sur des règles
if anomaly_type == 'cpu_high':
    if top_process_cpu > 80:
        cause = 'single_process_hog'
    elif num_processes > 500:
        cause = 'too_many_processes'
    else:
        cause = 'system_load'
```

#### 5. **Moteur de Recommandations Contextuel**
```python
# Adaptation des solutions au contexte
recommendations = []

if os_type == 'Windows':
    command = 'taskkill /PID {pid} /F'
elif os_type == 'Linux':
    command = 'kill -9 {pid}'
else:  # macOS
    command = 'kill -9 {pid}'

recommendations.append({
    'priority': calculate_priority(severity, impact),
    'action': generate_action(anomaly_type),
    'command': command.format(pid=target_pid)
})
```

---

## 📊 Métriques et Performance

### Performance du Système

| Module                  | Temps d'exécution | Fréquence    |
|-------------------------|-------------------|--------------|
| MetricsCollector        | ~50-100ms         | Chaque cycle |
| AnomalyDetector (basic) | ~10-20ms          | Chaque cycle |
| AdvancedDetector        | ~100-300ms        | Chaque cycle |
| RootCauseAnalyzer       | ~5-10ms           | Si anomalie  |
| RecommendationEngine    | ~5-10ms           | Si anomalie  |
| **TOTAL (basique)**     | **~70ms**         | Chaque 5s    |
| **TOTAL (avancé)**      | **~120ms**        | Chaque 5s    |

### Utilisation Ressources du Monitor

- **CPU**: 0.5-2% en monitoring continu
- **RAM**: 30-50 MB
- **Disque**: ~1-5 MB pour logs/heure

---

## 🔌 Points d'Extension

Le système est conçu pour être facilement extensible :

### 1. Ajouter un Nouveau Détecteur

```python
# detection/ml_detector.py
from sklearn.ensemble import IsolationForest

class MLAnomalyDetector:
    """Détection par Machine Learning"""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
    
    def train(self, historical_data):
        self.model.fit(historical_data)
    
    def detect(self, current_metrics):
        prediction = self.model.predict([current_metrics])
        return prediction == -1  # -1 = anomalie
```

### 2. Ajouter un Système de Notification

```python
# utils/notification.py
class NotificationManager:
    """Envoi de notifications email/Slack/Discord"""
    
    def send_alert(self, anomaly, severity):
        if severity == 'critical':
            self.send_email(anomaly)
            self.send_slack(anomaly)
```

### 3. Ajouter une Base de Données

```python
# utils/database.py
import sqlite3

class MetricsDatabase:
    """Stockage long terme dans SQLite"""
    
    def store_metrics(self, metrics):
        self.conn.execute(
            "INSERT INTO metrics VALUES (?, ?, ?)",
            (timestamp, cpu, memory)
        )
```

### 4. Ajouter une API REST

```python
# web/api.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/status')
def get_status():
    report = monitor.generate_report()
    return jsonify(report)

@app.route('/api/metrics')
def get_metrics():
    metrics = monitor.collect_metrics()
    return jsonify(metrics)
```

---

## 🔒 Sécurité

### Permissions Requises

**Linux/macOS:**
- Lecture `/proc/*` : Métriques processus
- Lecture `/sys/*` : Métriques système
- Certaines métriques nécessitent `sudo`

**Windows:**
- Droits utilisateur standard suffisent
- Administrateur recommandé pour métriques complètes

### Données Sensibles

Le système ne collecte **AUCUNE** donnée sensible :
- ✅ Métriques système (CPU, RAM, etc.)
- ✅ Noms de processus
- ✅ Utilisation ressources
- ❌ Pas de contenu de mémoire
- ❌ Pas de données personnelles
- ❌ Pas de mots de passe

---

## 🌐 Compatibilité OS

### Support Multi-Plateforme

| Fonctionnalité          | Windows | Linux | macOS |
|-------------------------|---------|-------|-------|
| Métriques CPU           | ✅      | ✅    | ✅    |
| Métriques RAM           | ✅      | ✅    | ✅    |
| Métriques Disque        | ✅      | ✅    | ✅    |
| Métriques Réseau        | ✅      | ✅    | ✅    |
| Processus               | ✅      | ✅    | ✅    |
| Load Average            | ❌      | ✅    | ✅    |
| IO Disque détaillé      | ✅      | ✅    | ✅    |
| Température CPU         | ⚠️      | ⚠️    | ⚠️    |

⚠️ = Dépend du matériel et des capteurs

### Commandes Adaptées par OS

Le système génère automatiquement les commandes appropriées :

**Arrêter un processus:**
- Windows: `taskkill /PID 1234 /F`
- Linux: `kill -9 1234`
- macOS: `kill -9 1234`

**Nettoyer disque:**
- Windows: `cleanmgr`
- Linux: `sudo apt-get clean`
- macOS: `sudo rm -rf ~/.Trash/*`

---

## 📈 Évolutions Futures

### Version 3.0 (Roadmap)

1. **Machine Learning Avancé**
   - Prédiction de pannes avant qu'elles surviennent
   - Apprentissage du comportement normal du système
   - Détection d'anomalies par réseaux de neurones

2. **Monitoring Distribué**
   - Agent/Server architecture
   - Monitoring de plusieurs machines
   - Dashboard centralisé

3. **Intégration Cloud**
   - Export vers AWS CloudWatch
   - Intégration Prometheus/Grafana
   - Alertes PagerDuty/OpsGenie

4. **Auto-Résolution**
   - Exécution automatique de commandes (avec validation)
   - Redémarrage automatique de services
   - Nettoyage automatique planifié

5. **Analyse Prédictive**
   - "Dans 2h, vous manquerez d'espace disque"
   - "Fuite mémoire détectée, crash probable dans 30 min"

---

## 🔧 Guide du Développeur

### Ajouter une Nouvelle Métrique

```python
# 1. Dans metrics_collector.py
def collect_custom_metrics(self):
    return {
        'my_metric': get_my_metric_value()
    }

# 2. Intégrer dans collect_all_metrics()
def collect_all_metrics(self):
    return {
        # ... autres métriques
        'custom': self.collect_custom_metrics()
    }
```

### Ajouter un Nouveau Type d'Anomalie

```python
# 1. Dans advanced_detector.py
def detect_my_anomaly(self, metrics):
    anomalies = []
    
    if metrics['custom']['my_metric'] > threshold:
        anomalies.append({
            'type': 'my_anomaly',
            'category': 'custom',
            'severity': 'warning',
            'message': 'Ma nouvelle anomalie détectée'
        })
    
    return anomalies

# 2. Appeler dans detect_all_anomalies()
anomalies.extend(self.detect_my_anomaly(metrics))
```

### Ajouter une Recommandation Personnalisée

```python
# Dans recommendation_engine.py
def _recommend_my_anomaly(self, anomaly, root_cause, metrics):
    return [{
        'priority': 'high',
        'action': 'Ma solution personnalisée',
        'command': 'ma_commande --fix',
        'impact': 'Résolution du problème',
        'estimated_time': '5 minutes'
    }]

# Enregistrer dans le dictionnaire generators
generators = {
    'my_anomaly': self._recommend_my_anomaly,
    # ...
}
```

---

## 📚 Dépendances

### Bibliothèque Principale

**psutil** (v5.9.0+)
- Collecte de métriques système multi-plateforme
- Interface Python pour /proc, /sys, WMI, etc.
- Licence BSD

### Dépendances Optionnelles

```python
# Pour ML avancé (futur)
scikit-learn>=1.0.0
tensorflow>=2.0.0

# Pour dashboard web
flask>=2.0.0

# Pour export PDF
wkhtmltopdf
pdfkit

# Pour notifications
requests>=2.28.0  # Webhooks
smtplib           # Email (stdlib)
```

---

## 🎓 Glossaire

**Anomalie**: Déviation par rapport au comportement normal du système

**Cause Racine**: La raison fondamentale d'un problème (vs symptôme)

**Métrique**: Mesure quantitative d'un aspect du système

**Seuil**: Valeur limite déclenchant une alerte

**Monitoring**: Surveillance continue du système

**SWAP**: Mémoire virtuelle sur disque (plus lente que RAM)

**Load Average**: Charge système moyenne (Linux/macOS)

**Processus Zombie**: Processus terminé mais non nettoyé

**Throttling**: Réduction automatique de la performance (surchauffe)

---

## 📞 Contact & Support

Pour toute question technique sur l'architecture :

- 📧 Architecture: architecture@itmonitor.com
- 🐛 Bugs: [GitHub Issues](https://github.com/votre-repo/issues)
- 💡 Suggestions: [GitHub Discussions](https://github.com/votre-repo/discussions)

---

Dernière mise à jour: 2025-01-10