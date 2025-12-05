#!/usr/bin/env python3
"""
utils/logger.py
Système de logging structuré pour le monitoring IT
"""

import os
import json
from datetime import datetime
from pathlib import Path


class SystemLogger:
    """Système de logging structuré pour les événements système"""
    
    def __init__(self, log_file='data/logs/monitor.log'):
        """
        Initialise le logger
        
        Args:
            log_file: Chemin vers le fichier de log
        """
        self.log_file = log_file
        
        # Créer le répertoire si nécessaire
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def _write_log(self, level, message, data=None):
        """
        Écrit une entrée de log
        
        Args:
            level: Niveau de log (INFO, WARNING, ERROR, etc.)
            message: Message de log
            data: Données supplémentaires (optionnel)
        """
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        
        if data:
            log_entry['data'] = data
        
        # Formater la ligne de log
        log_line = f"[{timestamp}] [{level}] {message}"
        if data:
            log_line += f" | Data: {json.dumps(data, default=str)}"
        log_line += "\n"
        
        # Écrire dans le fichier
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except Exception as e:
            # Si on ne peut pas écrire dans le fichier, afficher l'erreur
            print(f"⚠️  Erreur lors de l'écriture du log: {e}")
    
    def log_info(self, message, data=None):
        """Log un message d'information"""
        self._write_log('INFO', message, data)
    
    def log_warning(self, message, data=None):
        """Log un avertissement"""
        self._write_log('WARNING', message, data)
    
    def log_error(self, message, data=None):
        """Log une erreur"""
        self._write_log('ERROR', message, data)
    
    def log_report(self, report):
        """
        Log un rapport de monitoring
        
        Args:
            report: Dictionnaire contenant le rapport
        """
        if not report:
            return
        
        # Extraire les informations principales
        timestamp = report.get('timestamp', datetime.now().isoformat())
        health_score = report.get('health_score', 0)
        anomalies_count = len(report.get('anomalies', []))
        
        message = f"Rapport généré - Score: {health_score}/100, Anomalies: {anomalies_count}"
        
        # Données à logger
        log_data = {
            'health_score': health_score,
            'anomalies_count': anomalies_count,
            'timestamp': timestamp
        }
        
        # Ajouter un résumé des anomalies si présentes
        if anomalies_count > 0:
            anomalies_summary = []
            for anomaly in report.get('anomalies', [])[:5]:  # Max 5 pour ne pas surcharger
                anomalies_summary.append({
                    'type': anomaly.get('type'),
                    'severity': anomaly.get('severity'),
                    'message': anomaly.get('message', '')[:100]  # Limiter la longueur
                })
            log_data['anomalies_summary'] = anomalies_summary
        
        # Logger selon le niveau de santé
        if health_score >= 80:
            self.log_info(message, log_data)
        elif health_score >= 60:
            self.log_warning(message, log_data)
        else:
            self.log_error(message, log_data)
    
    def log_anomaly(self, anomaly):
        """
        Log une anomalie détectée
        
        Args:
            anomaly: Dictionnaire contenant l'anomalie
        """
        if not anomaly:
            return
        
        anomaly_type = anomaly.get('type', 'unknown')
        severity = anomaly.get('severity', 'info')
        message = f"Anomalie détectée: {anomaly_type} [{severity}]"
        
        log_data = {
            'type': anomaly_type,
            'severity': severity,
            'category': anomaly.get('category'),
            'value': anomaly.get('value'),
            'threshold': anomaly.get('threshold'),
            'message': anomaly.get('message')
        }
        
        if severity == 'critical':
            self.log_error(message, log_data)
        elif severity == 'warning':
            self.log_warning(message, log_data)
        else:
            self.log_info(message, log_data)
    
    def log_monitoring_start(self, mode='basic', interval=5):
        """Log le démarrage du monitoring"""
        message = f"Monitoring démarré - Mode: {mode}, Intervalle: {interval}s"
        self.log_info(message, {'mode': mode, 'interval': interval})
    
    def log_monitoring_stop(self):
        """Log l'arrêt du monitoring"""
        self.log_info("Monitoring arrêté")
    
    def log_config_change(self, key, old_value, new_value):
        """Log un changement de configuration"""
        message = f"Configuration modifiée: {key}"
        self.log_info(message, {
            'key': key,
            'old_value': old_value,
            'new_value': new_value
        })
    
    def get_log_file(self):
        """Retourne le chemin du fichier de log"""
        return self.log_file
    
    def clear_logs(self):
        """Efface le fichier de log"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write("")
                self.log_info("Logs effacés")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'effacement des logs: {e}")

