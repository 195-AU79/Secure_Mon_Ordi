#!/usr/bin/env python3
"""
core/monitor.py
Classe principale du système de monitoring
"""

import time
import threading
from datetime import datetime
from collections import deque

from core.metrics_collector import MetricsCollector
from core.config_manager import ConfigManager
from detection.anomaly_detector import AnomalyDetector
from detection.advanced_detector import AdvancedAnomalyDetector
from analysis.root_cause_analyzer import RootCauseAnalyzer
from analysis.recommendation_engine import RecommendationEngine
from utils.logger import SystemLogger
from utils.export import ReportExporter


class ITMonitor:
    """Classe principale du système de monitoring IT"""
    
    def __init__(self, config_file='config/config.json'):
        print("🔧 Initialisation du système IT Monitor...")
        
        # Chargement de la configuration
        self.config = ConfigManager(config_file)
        
        # Composants du système
        self.metrics_collector = MetricsCollector()
        self.anomaly_detector = AnomalyDetector(self.config.get_thresholds())
        self.advanced_detector = AdvancedAnomalyDetector(self.config.get_thresholds())
        self.root_cause_analyzer = RootCauseAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        
        # Utilitaires
        self.logger = SystemLogger(self.config.get('monitoring.log_file', 'data/logs/monitor.log'))
        self.exporter = ReportExporter()
        
        # État du système
        self.is_monitoring = False
        self.monitoring_thread = None
        self.system_info = self.metrics_collector.get_system_info()
        
        # Historique
        history_size = self.config.get('monitoring.history_size', 100)
        self.metrics_history = {
            'cpu': deque(maxlen=history_size),
            'memory': deque(maxlen=history_size),
            'disk': deque(maxlen=history_size),
            'network': deque(maxlen=history_size)
        }
        
        print("✅ Système initialisé avec succès")
    
    def collect_metrics(self):
        """Collecte toutes les métriques système"""
        metrics = self.metrics_collector.collect_all_metrics()
        
        # Mise à jour de l'historique
        self.metrics_history['cpu'].append(metrics['cpu']['percent'])
        self.metrics_history['memory'].append(metrics['memory']['percent'])
        self.metrics_history['disk'].append(metrics['disk']['percent'])
        
        return metrics
    
    def detect_anomalies(self, metrics, mode='basic'):
        """
        Détecte les anomalies
        mode: 'basic' ou 'advanced'
        """
        if mode == 'advanced':
            return self.advanced_detector.detect_all_anomalies(metrics)
        else:
            return self.anomaly_detector.detect_anomalies(metrics)
    
    def analyze_anomalies(self, anomalies, metrics):
        """Analyse les anomalies et génère des recommandations"""
        analyses = []
        
        for anomaly in anomalies:
            # Analyse de la cause racine
            root_cause = self.root_cause_analyzer.analyze(anomaly, metrics)
            
            # Génération des recommandations
            recommendations = self.recommendation_engine.generate_recommendations(
                anomaly, root_cause, metrics
            )
            
            analyses.append({
                'anomaly': anomaly,
                'root_cause': root_cause,
                'recommendations': recommendations
            })
        
        return analyses
    
    def generate_report(self, detection_mode='basic'):
        """Génère un rapport complet du système"""
        # Collecte des métriques
        metrics = self.collect_metrics()
        
        # Détection d'anomalies
        anomalies = self.detect_anomalies(metrics, mode=detection_mode)
        
        # Analyse si des anomalies sont détectées
        analyses = []
        if anomalies:
            analyses = self.analyze_anomalies(anomalies, metrics)
        
        # Calcul du score de santé
        health_score = self.calculate_health_score(metrics)
        
        # Construction du rapport
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.system_info,
            'metrics': metrics,
            'health_score': health_score,
            'anomalies': anomalies,
            'analyses': analyses,
            'statistics': self.get_statistics()
        }
        
        # Logging
        self.logger.log_report(report)
        
        return report
    
    def calculate_health_score(self, metrics):
        """Calcule un score de santé global (0-100)"""
        score = 100
        
        # Pénalités basées sur l'utilisation
        cpu_penalty = max(0, (metrics['cpu']['percent'] - 60) * 0.6)
        memory_penalty = max(0, (metrics['memory']['percent'] - 70) * 0.5)
        disk_penalty = max(0, (metrics['disk']['percent'] - 75) * 0.4)
        
        score -= (cpu_penalty + memory_penalty + disk_penalty)
        
        # Bonus si performances optimales
        if metrics['cpu']['percent'] < 40 and metrics['memory']['percent'] < 50:
            score = min(100, score + 5)
        
        return max(0, min(100, round(score)))
    
    def get_statistics(self):
        """Récupère les statistiques d'historique"""
        stats = {}
        
        for key, history in self.metrics_history.items():
            if history:
                stats[key] = {
                    'current': history[-1],
                    'average': sum(history) / len(history),
                    'min': min(history),
                    'max': max(history)
                }
        
        return stats
    
    def start_monitoring(self, interval=None, callback=None, detection_mode='basic'):
        """
        Démarre le monitoring en continu
        
        Args:
            interval: Intervalle en secondes (défaut depuis config)
            callback: Fonction à appeler avec chaque rapport
            detection_mode: 'basic' ou 'advanced'
        """
        if self.is_monitoring:
            print("⚠️  Le monitoring est déjà en cours")
            return
        
        if interval is None:
            interval = self.config.get('monitoring.interval_seconds', 5)
        
        self.is_monitoring = True
        
        def monitoring_loop():
            print(f"🔄 Monitoring démarré (intervalle: {interval}s, mode: {detection_mode})")
            while self.is_monitoring:
                try:
                    report = self.generate_report(detection_mode=detection_mode)
                    
                    if callback:
                        callback(report)
                    else:
                        # Affichage par défaut
                        self._default_display(report)
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"❌ Erreur dans le monitoring: {e}")
                    self.logger.log_error(str(e))
        
        self.monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        return self.monitoring_thread
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        if not self.is_monitoring:
            print("⚠️  Le monitoring n'est pas en cours")
            return
        
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        print("✋ Monitoring arrêté")
    
    def _default_display(self, report):
        """Affichage par défaut des rapports"""
        print(f"\n[{report['timestamp']}]")
        print(f"💚 Score de santé: {report['health_score']}/100")
        
        if report['anomalies']:
            print(f"⚠️  {len(report['anomalies'])} anomalie(s) détectée(s)")
            for anomaly in report['anomalies'][:3]:  # Max 3 pour ne pas encombrer
                print(f"   - {anomaly.get('message', anomaly.get('type'))}")
    
    def export_report(self, format='json', filename=None):
        """
        Exporte le rapport
        
        Args:
            format: 'json', 'csv', 'html', 'pdf'
            filename: Nom du fichier (auto-généré si None)
        """
        report = self.generate_report(detection_mode='advanced')
        return self.exporter.export(report, format=format, filename=filename)
    
    def get_system_info(self):
        """Retourne les informations système"""
        return self.system_info
    
    def get_config(self):
        """Retourne la configuration actuelle"""
        return self.config.config
    
    def update_config(self, key_path, value):
        """Met à jour une valeur de configuration"""
        return self.config.set(key_path, value)


# Fonction utilitaire pour créer une instance facilement
def create_monitor(config_file='config/config.json'):
    """Crée et retourne une instance du moniteur"""
    return ITMonitor(config_file)