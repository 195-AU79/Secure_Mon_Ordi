#!/usr/bin/env python3
"""
detection/anomaly_detector.py
Détection basique d'anomalies système - CODE CORRIGÉ
"""


class AnomalyDetector:
    """Détecteur d'anomalies basique avec seuils configurables"""
    
    def __init__(self, thresholds=None):
        """
        Initialise le détecteur
        
        Args:
            thresholds: Dictionnaire de seuils personnalisés
        """
        self.thresholds = thresholds if thresholds else self.get_default_thresholds()
    
    def get_default_thresholds(self):
        """Retourne les seuils par défaut"""
        return {
            'cpu': 80,
            'cpu_critical': 95,
            'memory': 85,
            'memory_critical': 95,
            'disk': 90,
            'disk_critical': 95,
            'swap': 50,
            'swap_critical': 80,
            'network_errors': 100,
            'zombie_processes': 5,
            'process_count': 500
        }
    
    def detect_anomalies(self, metrics):
        """
        Détecte toutes les anomalies basiques dans les métriques
        
        Args:
            metrics: Dictionnaire contenant toutes les métriques système
            
        Returns:
            Liste d'anomalies détectées
        """
        anomalies = []
        
        # Vérifier que les métriques sont valides
        if not metrics or not isinstance(metrics, dict):
            return anomalies
        
        # Détection CPU
        anomalies.extend(self._detect_cpu_anomalies(metrics))
        
        # Détection Mémoire
        anomalies.extend(self._detect_memory_anomalies(metrics))
        
        # Détection Disque
        anomalies.extend(self._detect_disk_anomalies(metrics))
        
        # Détection Réseau
        anomalies.extend(self._detect_network_anomalies(metrics))
        
        # Détection Processus
        anomalies.extend(self._detect_process_anomalies(metrics))
        
        return anomalies
    
    def _detect_cpu_anomalies(self, metrics):
        """Détecte les anomalies CPU"""
        anomalies = []
        
        # Vérifier que les données CPU existent
        if 'cpu' not in metrics or not isinstance(metrics['cpu'], dict):
            return anomalies
        
        cpu_percent = metrics['cpu'].get('percent', 0)
        
        # CPU critique (>95%)
        if cpu_percent >= self.thresholds['cpu_critical']:
            anomalies.append({
                'type': 'cpu_critical',
                'category': 'performance',
                'severity': 'critical',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu_critical'],
                'message': f"CPU critique à {cpu_percent:.1f}% - Action immédiate requise"
            })
        # CPU élevé (>80%)
        elif cpu_percent >= self.thresholds['cpu']:
            anomalies.append({
                'type': 'cpu_high',
                'category': 'performance',
                'severity': 'warning',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu'],
                'message': f"Utilisation CPU élevée: {cpu_percent:.1f}%"
            })
        
        return anomalies
    
    def _detect_memory_anomalies(self, metrics):
        """Détecte les anomalies mémoire"""
        anomalies = []
        
        # Vérifier que les données mémoire existent
        if 'memory' not in metrics or not isinstance(metrics['memory'], dict):
            return anomalies
        
        mem_percent = metrics['memory'].get('percent', 0)
        
        # Mémoire critique (>95%)
        if mem_percent >= self.thresholds['memory_critical']:
            anomalies.append({
                'type': 'memory_critical',
                'category': 'performance',
                'severity': 'critical',
                'value': mem_percent,
                'threshold': self.thresholds['memory_critical'],
                'message': f"Mémoire critique à {mem_percent:.1f}% - Risque de crash système"
            })
        # Mémoire élevée (>85%)
        elif mem_percent >= self.thresholds['memory']:
            anomalies.append({
                'type': 'memory_high',
                'category': 'performance',
                'severity': 'warning',
                'value': mem_percent,
                'threshold': self.thresholds['memory'],
                'message': f"Utilisation mémoire élevée: {mem_percent:.1f}%"
            })
        
        # Vérifier SWAP si disponible
        if 'swap' in metrics['memory'] and isinstance(metrics['memory']['swap'], dict):
            swap_percent = metrics['memory']['swap'].get('percent', 0)
            
            # SWAP critique (>80%)
            if swap_percent >= self.thresholds['swap_critical']:
                anomalies.append({
                    'type': 'swap_critical',
                    'category': 'performance',
                    'severity': 'critical',
                    'value': swap_percent,
                    'threshold': self.thresholds['swap_critical'],
                    'message': f"Utilisation SWAP critique: {swap_percent:.1f}% - Performances très dégradées"
                })
            # SWAP élevé (>50%)
            elif swap_percent >= self.thresholds['swap']:
                anomalies.append({
                    'type': 'swap_high',
                    'category': 'performance',
                    'severity': 'warning',
                    'value': swap_percent,
                    'threshold': self.thresholds['swap'],
                    'message': f"Utilisation SWAP élevée: {swap_percent:.1f}% - Performances dégradées"
                })
        
        return anomalies
    
    def _detect_disk_anomalies(self, metrics):
        """Détecte les anomalies disque"""
        anomalies = []
        
        # Vérifier que les données disque existent
        if 'disk' not in metrics or not isinstance(metrics['disk'], dict):
            return anomalies
        
        disk_percent = metrics['disk'].get('percent', 0)
        
        # Disque critique (>95%)
        if disk_percent >= self.thresholds['disk_critical']:
            free_gb = metrics['disk'].get('free_gb', 0)
            anomalies.append({
                'type': 'disk_critical',
                'category': 'storage',
                'severity': 'critical',
                'value': disk_percent,
                'threshold': self.thresholds['disk_critical'],
                'message': f"Disque critique à {disk_percent:.1f}% (reste {free_gb:.1f} GB) - Risque de blocage"
            })
        # Disque plein (>90%)
        elif disk_percent >= self.thresholds['disk']:
            free_gb = metrics['disk'].get('free_gb', 0)
            anomalies.append({
                'type': 'disk_full',
                'category': 'storage',
                'severity': 'warning',
                'value': disk_percent,
                'threshold': self.thresholds['disk'],
                'message': f"Disque presque plein: {disk_percent:.1f}% (reste {free_gb:.1f} GB)"
            })
        
        return anomalies
    
    def _detect_network_anomalies(self, metrics):
        """Détecte les anomalies réseau"""
        anomalies = []
        
        # Vérifier que les données réseau existent
        if 'network' not in metrics or not isinstance(metrics['network'], dict):
            return anomalies
        
        network = metrics['network']
        
        # Calculer le total des erreurs
        errin = network.get('errin', 0)
        errout = network.get('errout', 0)
        total_errors = errin + errout
        
        if total_errors > self.thresholds['network_errors']:
            anomalies.append({
                'type': 'network_errors',
                'category': 'network',
                'severity': 'warning',
                'value': total_errors,
                'threshold': self.thresholds['network_errors'],
                'message': f"Erreurs réseau détectées: {total_errors} erreurs (↓{errin} ↑{errout})"
            })
        
        # Vérifier les paquets perdus
        dropin = network.get('dropin', 0)
        dropout = network.get('dropout', 0)
        total_dropped = dropin + dropout
        
        if total_dropped > 100:
            anomalies.append({
                'type': 'network_packet_loss',
                'category': 'network',
                'severity': 'warning',
                'value': total_dropped,
                'threshold': 100,
                'message': f"Paquets réseau perdus: {total_dropped} paquets (↓{dropin} ↑{dropout})"
            })
        
        return anomalies
    
    def _detect_process_anomalies(self, metrics):
        """Détecte les anomalies de processus"""
        anomalies = []
        
        # Vérifier que les données processus existent
        if 'processes' not in metrics or not isinstance(metrics['processes'], dict):
            return anomalies
        
        processes = metrics['processes']
        
        # Processus zombies
        zombie_count = processes.get('zombie', 0)
        if zombie_count >= self.thresholds['zombie_processes']:
            anomalies.append({
                'type': 'zombie_processes',
                'category': 'stability',
                'severity': 'warning',
                'value': zombie_count,
                'threshold': self.thresholds['zombie_processes'],
                'message': f"Processus zombies détectés: {zombie_count} processus"
            })
        
        # Trop de processus
        total_processes = processes.get('total', 0)
        if total_processes > self.thresholds['process_count']:
            anomalies.append({
                'type': 'too_many_processes',
                'category': 'performance',
                'severity': 'info',
                'value': total_processes,
                'threshold': self.thresholds['process_count'],
                'message': f"Nombre élevé de processus: {total_processes}"
            })
        
        return anomalies
    
    def get_anomaly_summary(self, anomalies):
        """
        Génère un résumé des anomalies
        
        Args:
            anomalies: Liste des anomalies détectées
            
        Returns:
            Dictionnaire avec statistiques
        """
        if not anomalies:
            return {
                'total': 0,
                'critical': 0,
                'warning': 0,
                'info': 0,
                'categories': {}
            }
        
        summary = {
            'total': len(anomalies),
            'critical': 0,
            'warning': 0,
            'info': 0,
            'categories': {}
        }
        
        for anomaly in anomalies:
            # Compter par sévérité
            severity = anomaly.get('severity', 'info')
            if severity in summary:
                summary[severity] += 1
            
            # Compter par catégorie
            category = anomaly.get('category', 'unknown')
            if category not in summary['categories']:
                summary['categories'][category] = 0
            summary['categories'][category] += 1
        
        return summary


# Fonction utilitaire pour créer une instance
def create_detector(thresholds=None):
    """
    Crée et retourne une instance du détecteur
    
    Args:
        thresholds: Seuils personnalisés (optionnel)
        
    Returns:
        Instance de AnomalyDetector
    """
    return AnomalyDetector(thresholds)