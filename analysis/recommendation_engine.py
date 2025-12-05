#!/usr/bin/env python3
"""
analysis/recommendation_engine.py
Génère des recommandations intelligentes basées sur les anomalies
"""

import platform


class RecommendationEngine:
    """Génère des recommandations de résolution d'anomalies"""
    
    def __init__(self):
        self.os_type = platform.system()
    
    def generate_recommendations(self, anomaly, root_cause, metrics):
        """
        Génère des recommandations basées sur l'anomalie et sa cause
        
        Args:
            anomaly: Anomalie détectée
            root_cause: Analyse de cause racine
            metrics: Métriques système
        
        Returns:
            list: Liste de recommandations priorisées
        """
        anomaly_type = anomaly.get('type')
        
        generators = {
            'cpu_high': self._recommend_cpu_high,
            'cpu_critical': self._recommend_cpu_critical,
            'memory_high': self._recommend_memory_high,
            'memory_critical': self._recommend_memory_critical,
            'memory_leak_suspected': self._recommend_memory_leak,
            'disk_full': self._recommend_disk_full,
            'disk_critical': self._recommend_disk_critical,
            'network_errors': self._recommend_network_errors,
            'zombie_processes': self._recommend_zombie_processes,
            'swap_high': self._recommend_swap_high
        }
        
        generator = generators.get(anomaly_type, self._recommend_generic)
        return generator(anomaly, root_cause, metrics)
    
    def _recommend_cpu_high(self, anomaly, root_cause, metrics):
        """Recommandations pour CPU élevé"""
        processes = metrics['processes']['top_cpu'][:3]
        recommendations = []
        
        if processes:
            top_proc = processes[0]
            kill_cmd = self._get_kill_command(top_proc['pid'])
            
            recommendations.append({
                'priority': 'high',
                'action': f"Analyser le processus {top_proc['name']}",
                'command': f"PID: {top_proc['pid']} | CPU: {top_proc.get('cpu_percent', 0):.1f}%",
                'impact': "Identification de la cause",
                'estimated_time': "2-5 minutes"
            })
            
            recommendations.append({
                'priority': 'medium',
                'action': f"Si le processus est non essentiel, l'arrêter",
                'command': kill_cmd,
                'impact': "Libération immédiate du CPU",
                'estimated_time': "Instantané",
                'warning': "Vérifier l'importance du processus avant de l'arrêter"
            })
        
        recommendations.append({
            'priority': 'medium',
            'action': "Vérifier les tâches planifiées actives",
            'command': self._get_task_list_command(),
            'impact': "Identification des tâches automatiques",
            'estimated_time': "3-5 minutes"
        })
        
        recommendations.append({
            'priority': 'low',
            'action': "Optimiser les applications au démarrage",
            'command': "Gestionnaire de tâches > Démarrage" if self.os_type == 'Windows' else "systemctl list-unit-files",
            'impact': "Amélioration long terme des performances",
            'estimated_time': "10-15 minutes"
        })
        
        return recommendations
    
    def _recommend_cpu_critical(self, anomaly, root_cause, metrics):
        """Recommandations pour CPU critique"""
        recs = self._recommend_cpu_high(anomaly, root_cause, metrics)
        
        # Ajouter une recommandation urgente en premier
        recs.insert(0, {
            'priority': 'urgent',
            'action': "ACTION IMMÉDIATE: Identifier et arrêter les processus critiques",
            'command': "Utiliser le gestionnaire de tâches",
            'impact': "Éviter le gel du système",
            'estimated_time': "Immédiat",
            'warning': "⚠️ Système à risque de gel"
        })
        
        return recs
    
    def _recommend_memory_high(self, anomaly, root_cause, metrics):
        """Recommandations pour mémoire élevée"""
        processes = metrics['processes']['top_memory'][:3]
        recommendations = []
        
        if processes:
            top_proc = processes[0]
            recommendations.append({
                'priority': 'urgent',
                'action': f"Fermer les applications non essentielles, notamment {top_proc['name']}",
                'command': f"RAM utilisée par {top_proc['name']}: {top_proc.get('memory_percent', 0):.1f}%",
                'impact': "Libération immédiate de RAM",
                'estimated_time': "Instantané"
            })
        
        recommendations.append({
            'priority': 'high',
            'action': "Redémarrer les applications gourmandes en mémoire",
            'command': "Clic droit > Redémarrer dans le gestionnaire de tâches",
            'impact': "Libération des fuites mémoire potentielles",
            'estimated_time': "1-2 minutes"
        })
        
        if metrics['memory']['swap']['percent'] > 20:
            recommendations.append({
                'priority': 'high',
                'action': "Réduire l'utilisation du SWAP",
                'command': "Fermer davantage d'applications",
                'impact': "Amélioration significative des performances",
                'estimated_time': "2-3 minutes"
            })
        
        recommendations.append({
            'priority': 'medium',
            'action': "Vider le cache système",
            'command': self._get_clear_cache_command(),
            'impact': "Libération de 500 MB à 2 GB",
            'estimated_time': "5 minutes"
        })
        
        recommendations.append({
            'priority': 'low',
            'action': "Envisager une augmentation de la RAM",
            'command': f"RAM totale actuelle: {metrics['memory']['total_gb']} GB",
            'impact': "Solution permanente",
            'estimated_time': "N/A"
        })
        
        return recommendations
    
    def _recommend_memory_critical(self, anomaly, root_cause, metrics):
        """Recommandations pour mémoire critique"""
        recs = self._recommend_memory_high(anomaly, root_cause, metrics)
        
        recs.insert(0, {
            'priority': 'urgent',
            'action': "⚠️ CRITIQUE: Sauvegarder votre travail immédiatement",
            'command': "Risque de crash système imminent",
            'impact': "Protection contre la perte de données",
            'estimated_time': "Immédiat",
            'warning': "🔴 Système à risque de crash"
        })
        
        return recs
    
    def _recommend_memory_leak(self, anomaly, root_cause, metrics):
        """Recommandations pour fuite mémoire"""
        processes = metrics['processes']['top_memory'][:2]
        
        recommendations = [{
            'priority': 'urgent',
            'action': "Redémarrer le processus suspect de fuite mémoire",
            'command': f"Processus: {processes[0]['name']}" if processes else "Identifier via monitoring",
            'impact': "Arrêt de la fuite mémoire",
            'estimated_time': "Instantané"
        }]
        
        recommendations.append({
            'priority': 'high',
            'action': "Surveiller l'évolution de la mémoire après redémarrage",
            'command': "Utiliser le monitoring continu pendant 30 minutes",
            'impact': "Confirmation de la résolution",
            'estimated_time': "30 minutes"
        })
        
        recommendations.append({
            'priority': 'medium',
            'action': "Vérifier les mises à jour de l'application",
            'command': "Le bug peut être corrigé dans une version récente",
            'impact': "Solution permanente",
            'estimated_time': "10-20 minutes"
        })
        
        return recommendations
    
    def _recommend_disk_full(self, anomaly, root_cause, metrics):
        """Recommandations pour disque plein"""
        recommendations = []
        
        recommendations.append({
            'priority': 'urgent',
            'action': "Nettoyer les fichiers temporaires",
            'command': self._get_disk_cleanup_command(),
            'impact': "Libération de 1-5 GB",
            'estimated_time': "5-10 minutes"
        })
        
        recommendations.append({
            'priority': 'urgent',
            'action': "Vider la corbeille",
            'command': self._get_empty_trash_command(),
            'impact': "Libération immédiate d'espace",
            'estimated_time': "1 minute"
        })
        
        recommendations.append({
            'priority': 'high',
            'action': "Identifier les fichiers volumineux",
            'command': self._get_find_large_files_command(),
            'impact': "Localisation des gros fichiers à supprimer",
            'estimated_time': "5-10 minutes"
        })
        
        recommendations.append({
            'priority': 'high',
            'action': "Supprimer les anciens logs système",
            'command': self._get_clean_logs_command(),
            'impact': "Libération de 500 MB à 5 GB",
            'estimated_time': "3-5 minutes"
        })
        
        recommendations.append({
            'priority': 'medium',
            'action': "Désinstaller les applications inutilisées",
            'command': "Panneau de configuration > Programmes" if self.os_type == 'Windows' else "apt list --installed",
            'impact': "Libération significative d'espace",
            'estimated_time': "15-30 minutes"
        })
        
        recommendations.append({
            'priority': 'low',
            'action': "Configurer un nettoyage automatique",
            'command': "Planifier une tâche de nettoyage hebdomadaire",
            'impact': "Prévention long terme",
            'estimated_time': "10 minutes"
        })
        
        return recommendations
    
    def _recommend_disk_critical(self, anomaly, root_cause, metrics):
        """Recommandations pour disque critique"""
        recs = self._recommend_disk_full(anomaly, root_cause, metrics)
        
        recs.insert(0, {
            'priority': 'urgent',
            'action': "🔴 CRITIQUE: Libérer de l'espace IMMÉDIATEMENT",
            'command': f"Espace libre: {metrics['disk']['free_gb']:.2f} GB",
            'impact': "Éviter le blocage du système",
            'estimated_time': "Immédiat",
            'warning': "⚠️ Risque de dysfonctionnement système"
        })
        
        return recs
    
    def _recommend_network_errors(self, anomaly, root_cause, metrics):
        """Recommandations pour erreurs réseau"""
        recommendations = []
        
        recommendations.append({
            'priority': 'high',
            'action': "Vérifier les câbles réseau",
            'command': "Contrôle visuel des connexions physiques",
            'impact': "Résolution si problème matériel",
            'estimated_time': "2-3 minutes"
        })
        
        recommendations.append({
            'priority': 'high',
            'action': "Redémarrer l'interface réseau",
            'command': self._get_network_restart_command(),
            'impact': "Réinitialisation de la connexion",
            'estimated_time': "1-2 minutes"
        })
        
        recommendations.append({
            'priority': 'medium',
            'action': "Vérifier la configuration réseau",
            'command': "ipconfig /all" if self.os_type == 'Windows' else "ip addr show",
            'impact': "Identification d'erreurs de configuration",
            'estimated_time': "5 minutes"
        })
        
        recommendations.append({
            'priority': 'low',
            'action': "Mettre à jour les pilotes réseau",
            'command': "Gestionnaire de périphériques > Cartes réseau",
            'impact': "Résolution de bugs connus",
            'estimated_time': "10-15 minutes"
        })
        
        return recommendations
    
    def _recommend_zombie_processes(self, anomaly, root_cause, metrics):
        """Recommandations pour processus zombies"""
        recommendations = []
        
        recommendations.append({
            'priority': 'medium',
            'action': "Identifier et redémarrer les processus parents",
            'command': "ps aux | grep 'Z'" if self.os_type != 'Windows' else "Gestionnaire de tâches",
            'impact': "Nettoyage des zombies",
            'estimated_time': "5 minutes"
        })
        
        recommendations.append({
            'priority': 'low',
            'action': "Si le problème persiste, redémarrer le système",
            'command': "shutdown /r" if self.os_type == 'Windows' else "sudo reboot",
            'impact': "Nettoyage complet",
            'estimated_time': "5-10 minutes"
        })
        
        return recommendations
    
    def _recommend_swap_high(self, anomaly, root_cause, metrics):
        """Recommandations pour SWAP élevé"""
        return [{
            'priority': 'urgent',
            'action': "Réduire l'utilisation mémoire pour limiter le SWAP",
            'command': "Fermer les applications non essentielles",
            'impact': "Amélioration significative des performances",
            'estimated_time': "2-3 minutes"
        }, {
            'priority': 'high',
            'action': "Redémarrer les applications majeures",
            'command': "Pour libérer la mémoire fragmentée",
            'impact': "Réduction de l'utilisation SWAP",
            'estimated_time': "3-5 minutes"
        }]
    
    def _recommend_generic(self, anomaly, root_cause, metrics):
        """Recommandations génériques"""
        return [{
            'priority': 'medium',
            'action': f"Analyser l'anomalie: {anomaly.get('message', 'Anomalie détectée')}",
            'command': "Consulter les logs système pour plus d'informations",
            'impact': "Compréhension du problème",
            'estimated_time': "5-10 minutes"
        }, {
            'priority': 'low',
            'action': "Surveiller l'évolution",
            'command': "Utiliser le monitoring continu",
            'impact': "Détection si le problème persiste",
            'estimated_time': "Ongoing"
        }]
    
    # ========== COMMANDES SPÉCIFIQUES OS ==========
    
    def _get_kill_command(self, pid):
        """Commande pour arrêter un processus"""
        if self.os_type == 'Windows':
            return f"taskkill /PID {pid} /F"
        else:
            return f"kill -9 {pid}"
    
    def _get_task_list_command(self):
        """Commande pour lister les tâches"""
        if self.os_type == 'Windows':
            return "schtasks /query"
        else:
            return "crontab -l && systemctl list-timers"
    
    def _get_clear_cache_command(self):
        """Commande pour vider le cache"""
        if self.os_type == 'Windows':
            return "Cleanmgr.exe"
        elif self.os_type == 'Darwin':  # macOS
            return "sudo purge"
        else:  # Linux
            return "sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
    
    def _get_disk_cleanup_command(self):
        """Commande de nettoyage disque"""
        if self.os_type == 'Windows':
            return "cleanmgr /sagerun:1"
        else:
            return "sudo apt-get clean && sudo apt-get autoremove"
    
    def _get_empty_trash_command(self):
        """Commande pour vider la corbeille"""
        if self.os_type == 'Windows':
            return "Clic droit sur Corbeille > Vider la corbeille"
        elif self.os_type == 'Darwin':
            return "rm -rf ~/.Trash/*"
        else:
            return "rm -rf ~/.local/share/Trash/*"
    
    def _get_find_large_files_command(self):
        """Commande pour trouver les gros fichiers"""
        if self.os_type == 'Windows':
            return "WinDirStat ou TreeSize Free"
        else:
            return "du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20"
    
    def _get_clean_logs_command(self):
        """Commande pour nettoyer les logs"""
        if self.os_type == 'Windows':
            return "Supprimer les fichiers dans C:\\Windows\\Logs"
        else:
            return "sudo find /var/log -name '*.log' -mtime +30 -delete"
    
    def _get_network_restart_command(self):
        """Commande pour redémarrer le réseau"""
        if self.os_type == 'Windows':
            return "ipconfig /release && ipconfig /renew"
        elif self.os_type == 'Darwin':
            return "sudo ifconfig en0 down && sudo ifconfig en0 up"
        else:
            return "sudo systemctl restart NetworkManager"