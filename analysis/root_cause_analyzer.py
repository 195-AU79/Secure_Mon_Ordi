#!/usr/bin/env python3
"""
analysis/root_cause_analyzer.py
Analyse de la cause racine des anomalies
"""

import psutil


class RootCauseAnalyzer:
    """Analyse les causes racines des anomalies détectées"""
    
    def analyze(self, anomaly, metrics):
        """
        Analyse une anomalie et identifie sa cause racine
        
        Args:
            anomaly: Dictionnaire contenant l'anomalie détectée
            metrics: Métriques système complètes
        
        Returns:
            dict: Analyse de la cause racine
        """
        anomaly_type = anomaly.get('type')
        
        analyzers = {
            'cpu_high': self._analyze_cpu_high,
            'cpu_critical': self._analyze_cpu_high,
            'cpu_spike': self._analyze_cpu_spike,
            'memory_high': self._analyze_memory_high,
            'memory_critical': self._analyze_memory_high,
            'memory_leak_suspected': self._analyze_memory_leak,
            'disk_full': self._analyze_disk_full,
            'disk_critical': self._analyze_disk_full,
            'network_errors': self._analyze_network_errors,
            'zombie_processes': self._analyze_zombie_processes,
            'process_cpu_hog': self._analyze_process_hog,
            'process_memory_hog': self._analyze_process_hog
        }
        
        analyzer = analyzers.get(anomaly_type, self._analyze_generic)
        return analyzer(anomaly, metrics)
    
    def _analyze_cpu_high(self, anomaly, metrics):
        """Analyse CPU élevé"""
        processes = metrics['processes']['top_cpu'][:5]
        
        return {
            'type': 'cpu_high',
            'cause': f"{len(processes)} processus consomment le plus de CPU",
            'details': f"Top processus: {', '.join([p['name'] for p in processes[:3]])}",
            'affected_components': [
                f"{p['name']} (PID {p['pid']}, {p.get('cpu_percent', 0):.1f}%)" 
                for p in processes
            ],
            'severity_factors': [
                f"CPU global: {anomaly['value']:.1f}%",
                f"Seuil dépassé de {anomaly['value'] - anomaly['threshold']:.1f}%"
            ],
            'timeline': [
                "Augmentation progressive de la charge CPU",
                "Processus identifiés comme responsables",
                "Impact sur les performances système"
            ]
        }
    
    def _analyze_cpu_spike(self, anomaly, metrics):
        """Analyse pic CPU soudain"""
        processes = metrics['processes']['top_cpu'][:3]
        
        return {
            'type': 'cpu_spike',
            'cause': "Pic CPU soudain détecté",
            'details': "Processus récemment lancé ou tâche planifiée",
            'affected_components': [p['name'] for p in processes],
            'severity_factors': [
                f"Variation brusque: {anomaly['value']:.1f}%",
                "Comportement anormal détecté"
            ],
            'timeline': [
                "État CPU normal",
                "Pic soudain d'utilisation",
                "Processus suspect identifié"
            ]
        }
    
    def _analyze_memory_high(self, anomaly, metrics):
        """Analyse mémoire élevée"""
        processes = metrics['processes']['top_memory'][:5]
        swap_used = metrics['memory']['swap']['percent']
        
        causes = []
        if swap_used > 20:
            causes.append("Utilisation du SWAP indiquant RAM insuffisante")
        if len(processes) > 0 and processes[0].get('memory_percent', 0) > 30:
            causes.append(f"Processus {processes[0]['name']} consomme {processes[0]['memory_percent']:.1f}% de RAM")
        
        return {
            'type': 'memory_high',
            'cause': " | ".join(causes) if causes else "Consommation mémoire excessive",
            'details': f"RAM disponible: {metrics['memory']['available_gb']:.2f} GB",
            'affected_components': [
                f"{p['name']} (PID {p['pid']}, {p.get('memory_percent', 0):.1f}%)" 
                for p in processes
            ],
            'severity_factors': [
                f"RAM utilisée: {anomaly['value']:.1f}%",
                f"SWAP utilisé: {swap_used:.1f}%",
                f"Mémoire disponible: {metrics['memory']['available_gb']:.2f} GB"
            ],
            'timeline': [
                "Augmentation progressive de l'utilisation RAM",
                "Début d'utilisation du SWAP" if swap_used > 0 else "RAM proche de la saturation",
                "Performances dégradées"
            ]
        }
    
    def _analyze_memory_leak(self, anomaly, metrics):
        """Analyse fuite mémoire potentielle"""
        processes = metrics['processes']['top_memory'][:3]
        
        return {
            'type': 'memory_leak',
            'cause': "Fuite mémoire suspectée - augmentation constante",
            'details': "Processus ne libérant pas la mémoire allouée",
            'affected_components': [p['name'] for p in processes],
            'severity_factors': [
                "Tendance d'augmentation constante détectée",
                f"RAM actuelle: {anomaly['value']:.1f}%"
            ],
            'timeline': [
                "Utilisation mémoire initiale normale",
                "Augmentation continue sur plusieurs cycles",
                "Fuite mémoire probable identifiée"
            ]
        }
    
    def _analyze_disk_full(self, anomaly, metrics):
        """Analyse disque plein"""
        disk_info = metrics['disk']
        
        causes = []
        causes.append(f"Espace libre: {disk_info['free_gb']:.2f} GB")
        
        # Identifier les partitions problématiques
        if disk_info.get('partitions'):
            for mount, info in disk_info['partitions'].items():
                if info['percent'] > 85:
                    causes.append(f"{mount}: {info['percent']:.1f}% utilisé")
        
        return {
            'type': 'disk_full',
            'cause': "Espace disque insuffisant",
            'details': " | ".join(causes),
            'affected_components': [
                "Système de fichiers",
                "Applications nécessitant de l'espace",
                "Fichiers temporaires et logs"
            ],
            'severity_factors': [
                f"Disque utilisé: {anomaly['value']:.1f}%",
                f"Espace libre: {disk_info['free_gb']:.2f} GB",
                "Risque de dysfonctionnement système"
            ],
            'timeline': [
                "Accumulation progressive de données",
                "Seuil d'alerte dépassé",
                "Risque imminent de saturation"
            ]
        }
    
    def _analyze_network_errors(self, anomaly, metrics):
        """Analyse erreurs réseau"""
        net = metrics['network']
        
        return {
            'type': 'network_errors',
            'cause': "Erreurs de transmission réseau détectées",
            'details': f"Erreurs entrée: {net['errin']}, Erreurs sortie: {net['errout']}",
            'affected_components': [
                "Interfaces réseau",
                "Connexions actives",
                "Applications réseau"
            ],
            'severity_factors': [
                f"Total erreurs: {anomaly['value']}",
                f"Paquets perdus: {net.get('dropin', 0) + net.get('dropout', 0)}"
            ],
            'timeline': [
                "Connexions réseau fonctionnelles",
                "Apparition d'erreurs de transmission",
                "Dégradation de la qualité réseau"
            ]
        }
    
    def _analyze_zombie_processes(self, anomaly, metrics):
        """Analyse processus zombies"""
        return {
            'type': 'zombie_processes',
            'cause': "Processus zombies non nettoyés",
            'details': f"{anomaly['value']} processus zombies détectés",
            'affected_components': [
                "Gestion des processus système",
                "Processus parents défaillants"
            ],
            'severity_factors': [
                f"Nombre de zombies: {anomaly['value']}",
                "Impact sur la stabilité système"
            ],
            'timeline': [
                "Terminaison de processus enfants",
                "Processus parent ne récupère pas le statut",
                "Accumulation de processus zombies"
            ]
        }
    
    def _analyze_process_hog(self, anomaly, metrics):
        """Analyse processus gourmand"""
        return {
            'type': 'process_hog',
            'cause': f"Processus consommant excessivement des ressources",
            'details': anomaly.get('message', ''),
            'affected_components': ["Performances système globales"],
            'severity_factors': [
                f"Valeur: {anomaly['value']:.1f}%",
                "Impact significatif sur les autres processus"
            ],
            'timeline': [
                "Lancement ou activation du processus",
                "Consommation excessive de ressources",
                "Dégradation des performances"
            ]
        }
    
    def _analyze_generic(self, anomaly, metrics):
        """Analyse générique pour anomalies non spécifiques"""
        return {
            'type': anomaly.get('type', 'unknown'),
            'cause': anomaly.get('message', 'Anomalie détectée'),
            'details': f"Valeur: {anomaly.get('value', 'N/A')}",
            'affected_components': ["Système"],
            'severity_factors': [
                f"Sévérité: {anomaly.get('severity', 'unknown')}",
                f"Catégorie: {anomaly.get('category', 'unknown')}"
            ],
            'timeline': [
                "Détection de l'anomalie",
                "Analyse en cours"
            ]
        }