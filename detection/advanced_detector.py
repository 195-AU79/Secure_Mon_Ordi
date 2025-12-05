#!/usr/bin/env python3
"""
detection/advanced_detector.py
Détection avancée d'anomalies système - 30+ types d'anomalies
"""

import psutil
import platform
from datetime import datetime


class AdvancedAnomalyDetector:
    """Détecteur d'anomalies avancé avec 30+ types de détections"""
    
    def __init__(self, thresholds=None):
        """
        Initialise le détecteur avancé
        
        Args:
            thresholds: Dictionnaire de seuils personnalisés
        """
        self.thresholds = thresholds if thresholds else self.get_default_thresholds()
        self.os_type = platform.system().lower()
    
    def get_default_thresholds(self):
        """Retourne les seuils par défaut"""
        return {
            'cpu': 80,
            'cpu_critical': 95,
            'cpu_spike': 90,
            'memory': 85,
            'memory_critical': 95,
            'memory_leak': 70,
            'disk': 90,
            'disk_critical': 95,
            'disk_io_high': 80,
            'swap': 50,
            'swap_critical': 80,
            'network_errors': 100,
            'network_latency': 100,
            'network_bandwidth': 80,
            'zombie_processes': 5,
            'process_count': 500,
            'process_cpu_high': 50,
            'process_memory_high': 30,
            'load_average': 2.0,
            'temperature': 80,
            'file_handles': 10000
        }
    
    def detect_all_anomalies(self, metrics):
        """
        Détecte toutes les anomalies avancées (30+ types)
        
        Args:
            metrics: Dictionnaire contenant toutes les métriques système
            
        Returns:
            Liste d'anomalies détectées
        """
        anomalies = []
        
        # Vérifier que les métriques sont valides
        if not metrics or not isinstance(metrics, dict):
            return anomalies
        
        # Performance (12 types)
        anomalies.extend(self._detect_cpu_anomalies(metrics))
        anomalies.extend(self._detect_memory_anomalies(metrics))
        anomalies.extend(self._detect_load_anomalies(metrics))
        anomalies.extend(self._detect_cpu_frequency_anomalies(metrics))
        
        # Stockage (5 types)
        anomalies.extend(self._detect_disk_anomalies(metrics))
        anomalies.extend(self._detect_disk_io_anomalies(metrics))
        anomalies.extend(self._detect_filesystem_anomalies(metrics))
        
        # Réseau (8 types)
        anomalies.extend(self._detect_network_anomalies(metrics))
        anomalies.extend(self._detect_network_bandwidth_anomalies(metrics))
        anomalies.extend(self._detect_network_connection_anomalies(metrics))
        
        # Processus (7 types)
        anomalies.extend(self._detect_process_anomalies(metrics))
        anomalies.extend(self._detect_process_performance_anomalies(metrics))
        anomalies.extend(self._detect_process_resource_anomalies(metrics))
        
        # Sécurité (3 types)
        anomalies.extend(self._detect_security_anomalies(metrics))
        
        # Système (5 types)
        anomalies.extend(self._detect_system_anomalies(metrics))
        anomalies.extend(self._detect_system_stability_anomalies(metrics))
        
        return anomalies
    
    def _detect_cpu_anomalies(self, metrics):
        """Détecte les anomalies CPU avancées"""
        anomalies = []
        
        if 'cpu' not in metrics or not isinstance(metrics['cpu'], dict):
            return anomalies
        
        cpu = metrics['cpu']
        cpu_percent = cpu.get('percent', 0)
        
        # CPU critique
        if cpu_percent >= self.thresholds['cpu_critical']:
            anomalies.append({
                'type': 'cpu_critical',
                'category': 'performance',
                'severity': 'critical',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu_critical'],
                'message': f"CPU critique à {cpu_percent:.1f}% - Système surchargé"
            })
        
        # CPU élevé
        elif cpu_percent >= self.thresholds['cpu']:
            anomalies.append({
                'type': 'cpu_high',
                'category': 'performance',
                'severity': 'warning',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu'],
                'message': f"Utilisation CPU élevée: {cpu_percent:.1f}%"
            })
        
        # Pic CPU soudain
        if cpu_percent >= self.thresholds['cpu_spike']:
            anomalies.append({
                'type': 'cpu_spike',
                'category': 'performance',
                'severity': 'warning',
                'value': cpu_percent,
                'threshold': self.thresholds['cpu_spike'],
                'message': f"Pic CPU détecté: {cpu_percent:.1f}% - Charge soudaine"
            })
        
        # Déséquilibre CPU (si multi-cœur)
        if 'per_cpu' in cpu and isinstance(cpu['per_cpu'], list) and len(cpu['per_cpu']) > 1:
            per_cpu = cpu['per_cpu']
            max_cpu = max(per_cpu)
            min_cpu = min(per_cpu)
            if max_cpu - min_cpu > 50:  # Déséquilibre > 50%
                anomalies.append({
                    'type': 'cpu_imbalance',
                    'category': 'performance',
                    'severity': 'info',
                    'value': max_cpu - min_cpu,
                    'threshold': 50,
                    'message': f"Déséquilibre CPU: {max_cpu:.1f}% max vs {min_cpu:.1f}% min"
                })
        
        # Fréquence CPU anormale
        if 'frequency' in cpu and cpu['frequency'].get('current', 0) > 0:
            freq = cpu['frequency']
            max_freq = freq.get('max', 0)
            current_freq = freq.get('current', 0)
            if max_freq > 0 and current_freq < max_freq * 0.5:
                anomalies.append({
                    'type': 'cpu_throttling',
                    'category': 'performance',
                    'severity': 'warning',
                    'value': current_freq,
                    'threshold': max_freq * 0.5,
                    'message': f"CPU throttling détecté: {current_freq:.0f} MHz (max: {max_freq:.0f} MHz)"
                })
        
        return anomalies
    
    def _detect_memory_anomalies(self, metrics):
        """Détecte les anomalies mémoire avancées"""
        anomalies = []
        
        if 'memory' not in metrics or not isinstance(metrics['memory'], dict):
            return anomalies
        
        mem = metrics['memory']
        mem_percent = mem.get('percent', 0)
        
        # Mémoire critique
        if mem_percent >= self.thresholds['memory_critical']:
            anomalies.append({
                'type': 'memory_critical',
                'category': 'performance',
                'severity': 'critical',
                'value': mem_percent,
                'threshold': self.thresholds['memory_critical'],
                'message': f"Mémoire critique à {mem_percent:.1f}% - Risque de crash"
            })
        
        # Mémoire élevée
        elif mem_percent >= self.thresholds['memory']:
            anomalies.append({
                'type': 'memory_high',
                'category': 'performance',
                'severity': 'warning',
                'value': mem_percent,
                'threshold': self.thresholds['memory'],
                'message': f"Utilisation mémoire élevée: {mem_percent:.1f}%"
            })
        
        # Fuite mémoire potentielle
        if mem_percent >= self.thresholds['memory_leak']:
            free_gb = mem.get('free_gb', 0)
            if free_gb < 1.0:  # Moins de 1 GB libre
                anomalies.append({
                    'type': 'memory_leak_suspected',
                    'category': 'performance',
                    'severity': 'warning',
                    'value': free_gb,
                    'threshold': 1.0,
                    'message': f"Fuite mémoire suspectée: seulement {free_gb:.2f} GB libre"
                })
        
        # SWAP
        if 'swap' in mem and isinstance(mem['swap'], dict):
            swap_percent = mem['swap'].get('percent', 0)
            
            if swap_percent >= self.thresholds['swap_critical']:
                anomalies.append({
                    'type': 'swap_critical',
                    'category': 'performance',
                    'severity': 'critical',
                    'value': swap_percent,
                    'threshold': self.thresholds['swap_critical'],
                    'message': f"SWAP critique: {swap_percent:.1f}% - Performances très dégradées"
                })
            elif swap_percent >= self.thresholds['swap']:
                anomalies.append({
                    'type': 'swap_high',
                    'category': 'performance',
                    'severity': 'warning',
                    'value': swap_percent,
                    'threshold': self.thresholds['swap'],
                    'message': f"Utilisation SWAP élevée: {swap_percent:.1f}%"
                })
        
        return anomalies
    
    def _detect_load_anomalies(self, metrics):
        """Détecte les anomalies de charge système"""
        anomalies = []
        
        try:
            if self.os_type != 'windows':
                import os
                load_avg = os.getloadavg()
                cpu_count = psutil.cpu_count()
                
                if load_avg[0] > cpu_count * self.thresholds['load_average']:
                    anomalies.append({
                        'type': 'load_average_high',
                        'category': 'performance',
                        'severity': 'warning',
                        'value': load_avg[0],
                        'threshold': cpu_count * self.thresholds['load_average'],
                        'message': f"Charge système élevée: {load_avg[0]:.2f} (CPU: {cpu_count})"
                    })
        except:
            pass  # Windows n'a pas de load average
        
        return anomalies
    
    def _detect_cpu_frequency_anomalies(self, metrics):
        """Détecte les anomalies de fréquence CPU"""
        anomalies = []
        
        if 'cpu' in metrics and 'frequency' in metrics['cpu']:
            freq = metrics['cpu']['frequency']
            if freq.get('current', 0) > 0 and freq.get('max', 0) > 0:
                if freq['current'] > freq['max'] * 1.1:  # 10% au-dessus du max
                    anomalies.append({
                        'type': 'cpu_overclock',
                        'category': 'performance',
                        'severity': 'info',
                        'value': freq['current'],
                        'threshold': freq['max'],
                        'message': f"CPU overclock détecté: {freq['current']:.0f} MHz"
                    })
        
        return anomalies
    
    def _detect_disk_anomalies(self, metrics):
        """Détecte les anomalies disque avancées"""
        anomalies = []
        
        if 'disk' not in metrics or not isinstance(metrics['disk'], dict):
            return anomalies
        
        disk = metrics['disk']
        disk_percent = disk.get('percent', 0)
        
        # Disque critique
        if disk_percent >= self.thresholds['disk_critical']:
            free_gb = disk.get('free_gb', 0)
            anomalies.append({
                'type': 'disk_critical',
                'category': 'storage',
                'severity': 'critical',
                'value': disk_percent,
                'threshold': self.thresholds['disk_critical'],
                'message': f"Disque critique: {disk_percent:.1f}% (reste {free_gb:.1f} GB)"
            })
        
        # Disque plein
        elif disk_percent >= self.thresholds['disk']:
            free_gb = disk.get('free_gb', 0)
            anomalies.append({
                'type': 'disk_full',
                'category': 'storage',
                'severity': 'warning',
                'value': disk_percent,
                'threshold': self.thresholds['disk'],
                'message': f"Disque presque plein: {disk_percent:.1f}% (reste {free_gb:.1f} GB)"
            })
        
        # Espace disque faible
        free_gb = disk.get('free_gb', 0)
        if free_gb < 5.0:  # Moins de 5 GB
            anomalies.append({
                'type': 'disk_space_low',
                'category': 'storage',
                'severity': 'warning',
                'value': free_gb,
                'threshold': 5.0,
                'message': f"Espace disque faible: {free_gb:.1f} GB restants"
            })
        
        return anomalies
    
    def _detect_disk_io_anomalies(self, metrics):
        """Détecte les anomalies d'I/O disque"""
        anomalies = []
        
        if 'disk' in metrics and 'io' in metrics['disk']:
            disk_io = metrics['disk']['io']
            read_percent = disk_io.get('read_percent', 0)
            write_percent = disk_io.get('write_percent', 0)
            
            if read_percent > self.thresholds['disk_io_high']:
                anomalies.append({
                    'type': 'disk_read_high',
                    'category': 'storage',
                    'severity': 'warning',
                    'value': read_percent,
                    'threshold': self.thresholds['disk_io_high'],
                    'message': f"Lecture disque intensive: {read_percent:.1f}%"
                })
            
            if write_percent > self.thresholds['disk_io_high']:
                anomalies.append({
                    'type': 'disk_write_high',
                    'category': 'storage',
                    'severity': 'warning',
                    'value': write_percent,
                    'threshold': self.thresholds['disk_io_high'],
                    'message': f"Écriture disque intensive: {write_percent:.1f}%"
                })
        
        return anomalies
    
    def _detect_filesystem_anomalies(self, metrics):
        """Détecte les anomalies de système de fichiers"""
        anomalies = []
        
        try:
            # Vérifier les handles de fichiers
            if hasattr(psutil, 'num_fds'):
                num_fds = psutil.Process().num_fds()
                if num_fds > self.thresholds.get('file_handles', 10000):
                    anomalies.append({
                        'type': 'file_handles_high',
                        'category': 'storage',
                        'severity': 'warning',
                        'value': num_fds,
                        'threshold': self.thresholds.get('file_handles', 10000),
                        'message': f"Nombre élevé de handles de fichiers: {num_fds}"
                    })
        except:
            pass
        
        return anomalies
    
    def _detect_network_anomalies(self, metrics):
        """Détecte les anomalies réseau avancées"""
        anomalies = []
        
        if 'network' not in metrics or not isinstance(metrics['network'], dict):
            return anomalies
        
        network = metrics['network']
        
        # Erreurs réseau
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
                'message': f"Erreurs réseau: {total_errors} erreurs (↓{errin} ↑{errout})"
            })
        
        # Paquets perdus
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
                'message': f"Paquets perdus: {total_dropped} paquets (↓{dropin} ↑{dropout})"
            })
        
        return anomalies
    
    def _detect_network_bandwidth_anomalies(self, metrics):
        """Détecte les anomalies de bande passante"""
        anomalies = []
        
        if 'network' in metrics:
            network = metrics['network']
            sent_mb_s = network.get('sent_mb_s', 0)
            recv_mb_s = network.get('recv_mb_s', 0)
            
            # Bande passante élevée
            if sent_mb_s > 100 or recv_mb_s > 100:  # > 100 MB/s
                anomalies.append({
                    'type': 'network_bandwidth_high',
                    'category': 'network',
                    'severity': 'info',
                    'value': max(sent_mb_s, recv_mb_s),
                    'threshold': 100,
                    'message': f"Bande passante élevée: ↓{recv_mb_s:.2f} MB/s ↑{sent_mb_s:.2f} MB/s"
                })
        
        return anomalies
    
    def _detect_network_connection_anomalies(self, metrics):
        """Détecte les anomalies de connexions réseau"""
        anomalies = []
        
        try:
            connections = psutil.net_connections(kind='inet')
            connection_count = len(connections)
            
            # Trop de connexions
            if connection_count > 1000:
                anomalies.append({
                    'type': 'network_connections_high',
                    'category': 'network',
                    'severity': 'warning',
                    'value': connection_count,
                    'threshold': 1000,
                    'message': f"Nombre élevé de connexions réseau: {connection_count}"
                })
            
            # Connexions TIME_WAIT
            time_wait = sum(1 for conn in connections if conn.status == 'TIME_WAIT')
            if time_wait > 500:
                anomalies.append({
                    'type': 'network_time_wait_high',
                    'category': 'network',
                    'severity': 'info',
                    'value': time_wait,
                    'threshold': 500,
                    'message': f"Nombre élevé de connexions TIME_WAIT: {time_wait}"
                })
        except:
            pass
        
        return anomalies
    
    def _detect_process_anomalies(self, metrics):
        """Détecte les anomalies de processus avancées"""
        anomalies = []
        
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
                'message': f"Processus zombies: {zombie_count} processus"
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
    
    def _detect_process_performance_anomalies(self, metrics):
        """Détecte les anomalies de performance des processus"""
        anomalies = []
        
        if 'processes' in metrics and 'top_cpu' in metrics['processes']:
            top_cpu = metrics['processes']['top_cpu']
            
            # Processus avec CPU très élevé
            for proc in top_cpu[:5]:  # Top 5
                cpu_percent = proc.get('cpu_percent', 0)
                if cpu_percent > self.thresholds['process_cpu_high']:
                    anomalies.append({
                        'type': 'process_cpu_high',
                        'category': 'processes',
                        'severity': 'warning',
                        'value': cpu_percent,
                        'threshold': self.thresholds['process_cpu_high'],
                        'message': f"Processus gourmand CPU: {proc.get('name', 'unknown')} ({cpu_percent:.1f}%)"
                    })
        
        return anomalies
    
    def _detect_process_resource_anomalies(self, metrics):
        """Détecte les anomalies de ressources des processus"""
        anomalies = []
        
        if 'processes' in metrics and 'top_memory' in metrics['processes']:
            top_memory = metrics['processes']['top_memory']
            
            # Processus avec mémoire très élevée
            for proc in top_memory[:5]:  # Top 5
                mem_percent = proc.get('memory_percent', 0)
                if mem_percent > self.thresholds['process_memory_high']:
                    anomalies.append({
                        'type': 'process_memory_high',
                        'category': 'processes',
                        'severity': 'warning',
                        'value': mem_percent,
                        'threshold': self.thresholds['process_memory_high'],
                        'message': f"Processus gourmand mémoire: {proc.get('name', 'unknown')} ({mem_percent:.1f}%)"
                    })
        
        return anomalies
    
    def _detect_security_anomalies(self, metrics):
        """Détecte les anomalies de sécurité"""
        anomalies = []
        
        try:
            # Vérifier les processus suspects
            processes = psutil.process_iter(['pid', 'name', 'username'])
            suspicious_names = ['crypto', 'miner', 'bitcoin', 'monero']
            
            for proc in processes:
                try:
                    name = proc.info['name'].lower()
                    if any(sus in name for sus in suspicious_names):
                        anomalies.append({
                            'type': 'suspicious_process',
                            'category': 'security',
                            'severity': 'warning',
                            'value': 1,
                            'threshold': 0,
                            'message': f"Processus suspect détecté: {proc.info['name']} (PID: {proc.info['pid']})"
                        })
                except:
                    continue
        except:
            pass
        
        return anomalies
    
    def _detect_system_anomalies(self, metrics):
        """Détecte les anomalies système"""
        anomalies = []
        
        # Uptime système
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            uptime_days = uptime_seconds / 86400
            
            if uptime_days > 365:  # Plus d'un an sans redémarrage
                anomalies.append({
                    'type': 'system_uptime_very_long',
                    'category': 'system',
                    'severity': 'info',
                    'value': uptime_days,
                    'threshold': 365,
                    'message': f"Système en fonctionnement depuis {uptime_days:.0f} jours - Redémarrage recommandé"
                })
        except:
            pass
        
        return anomalies
    
    def _detect_system_stability_anomalies(self, metrics):
        """Détecte les anomalies de stabilité système"""
        anomalies = []
        
        # Vérifier les statistiques CPU pour les interruptions
        if 'cpu' in metrics and 'stats' in metrics['cpu']:
            stats = metrics['cpu']['stats']
            interrupts = stats.get('interrupts', 0)
            
            if interrupts > 1000000:  # Plus d'un million d'interruptions
                anomalies.append({
                    'type': 'system_interrupts_high',
                    'category': 'system',
                    'severity': 'info',
                    'value': interrupts,
                    'threshold': 1000000,
                    'message': f"Nombre élevé d'interruptions système: {interrupts:,}"
                })
        
        return anomalies

