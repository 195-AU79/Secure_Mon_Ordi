#!/usr/bin/env python3
"""
core/metrics_collector.py
Collecteur de métriques système multi-plateforme
"""

import psutil
import platform
import socket
from datetime import datetime


class MetricsCollector:
    """Collecte toutes les métriques système"""
    
    def __init__(self):
        self.last_network_io = None
        self.last_disk_io = None
        self.system_info = self._get_system_info()
    
    def _get_system_info(self):
        """Collecte les informations système statiques"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            ip_address = "unknown"
        
        return {
            'hostname': hostname,
            'ip': ip_address,
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
    
    def get_system_info(self):
        """Retourne les informations système"""
        return self.system_info
    
    def collect_cpu_metrics(self):
        """Collecte les métriques CPU"""
        cpu_freq = psutil.cpu_freq()
        cpu_stats = psutil.cpu_stats()
        cpu_times = psutil.cpu_times()
        
        return {
            'percent': psutil.cpu_percent(interval=1),
            'per_cpu': psutil.cpu_percent(interval=0.5, percpu=True),
            'count_logical': psutil.cpu_count(logical=True),
            'count_physical': psutil.cpu_count(logical=False),
            'frequency': {
                'current': cpu_freq.current if cpu_freq else 0,
                'min': cpu_freq.min if cpu_freq else 0,
                'max': cpu_freq.max if cpu_freq else 0
            },
            'stats': {
                'ctx_switches': cpu_stats.ctx_switches,
                'interrupts': cpu_stats.interrupts,
                'soft_interrupts': cpu_stats.soft_interrupts,
                'syscalls': cpu_stats.syscalls if hasattr(cpu_stats, 'syscalls') else 0
            },
            'times': {
                'user': cpu_times.user,
                'system': cpu_times.system,
                'idle': cpu_times.idle
            }
        }
    
    def collect_memory_metrics(self):
        """Collecte les métriques mémoire"""
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        
        return {
            'percent': virtual_mem.percent,
            'total_gb': round(virtual_mem.total / (1024**3), 2),
            'available_gb': round(virtual_mem.available / (1024**3), 2),
            'used_gb': round(virtual_mem.used / (1024**3), 2),
            'free_gb': round(virtual_mem.free / (1024**3), 2),
            'buffers_gb': round(getattr(virtual_mem, 'buffers', 0) / (1024**3), 2),
            'cached_gb': round(getattr(virtual_mem, 'cached', 0) / (1024**3), 2),
            'swap': {
                'percent': swap_mem.percent,
                'total_gb': round(swap_mem.total / (1024**3), 2),
                'used_gb': round(swap_mem.used / (1024**3), 2),
                'free_gb': round(swap_mem.free / (1024**3), 2)
            }
        }
    
    def collect_disk_metrics(self):
        """Collecte les métriques disque"""
        disks = {}
        
        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks[partition.mountpoint] = {
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'percent': usage.percent,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2)
                }
            except (PermissionError, OSError):
                continue
        
        # IO disque
        disk_io = psutil.disk_io_counters()
        io_metrics = {}
        if disk_io:
            io_metrics = {
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count,
                'read_bytes': disk_io.read_bytes,
                'write_bytes': disk_io.write_bytes,
                'read_time': disk_io.read_time,
                'write_time': disk_io.write_time
            }
            
            # Calcul des vitesses si on a l'historique
            if self.last_disk_io:
                time_delta = 1  # Approximation
                io_metrics['read_mb_s'] = round((disk_io.read_bytes - self.last_disk_io['read_bytes']) / (1024**2 * time_delta), 2)
                io_metrics['write_mb_s'] = round((disk_io.write_bytes - self.last_disk_io['write_bytes']) / (1024**2 * time_delta), 2)
            
            self.last_disk_io = io_metrics.copy()
        
        return {
            'partitions': disks,
            'io': io_metrics,
            # Métrique agrégée du disque principal
            'percent': list(disks.values())[0]['percent'] if disks else 0,
            'total_gb': sum(d['total_gb'] for d in disks.values()),
            'used_gb': sum(d['used_gb'] for d in disks.values()),
            'free_gb': sum(d['free_gb'] for d in disks.values())
        }
    
    def collect_network_metrics(self):
        """Collecte les métriques réseau"""
        net_io = psutil.net_io_counters()
        
        metrics = {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
        
        # Calcul des vitesses
        if self.last_network_io:
            time_delta = 1
            metrics['sent_mb_s'] = round((net_io.bytes_sent - self.last_network_io['bytes_sent']) / (1024**2 * time_delta), 2)
            metrics['recv_mb_s'] = round((net_io.bytes_recv - self.last_network_io['bytes_recv']) / (1024**2 * time_delta), 2)
        
        self.last_network_io = metrics.copy()
        
        # Interfaces réseau
        interfaces = {}
        try:
            net_if_stats = psutil.net_if_stats()
            for iface, stats in net_if_stats.items():
                interfaces[iface] = {
                    'is_up': stats.isup,
                    'speed_mbps': stats.speed,
                    'mtu': stats.mtu
                }
        except:
            pass
        
        # Connexions
        try:
            connections = psutil.net_connections(kind='inet')
            metrics['connections_count'] = len(connections)
            metrics['established'] = sum(1 for c in connections if c.status == 'ESTABLISHED')
            metrics['listening'] = sum(1 for c in connections if c.status == 'LISTEN')
        except:
            metrics['connections_count'] = 0
            metrics['established'] = 0
            metrics['listening'] = 0
        
        metrics['interfaces'] = interfaces
        
        return metrics
    
    def collect_process_metrics(self):
        """Collecte les métriques des processus"""
        processes = {
            'total': 0,
            'running': 0,
            'sleeping': 0,
            'zombie': 0,
            'stopped': 0,
            'top_cpu': [],
            'top_memory': []
        }
        
        all_processes = []
        status_count = {'running': 0, 'sleeping': 0, 'zombie': 0, 'stopped': 0}
        
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 
                                         'memory_percent', 'username', 'num_threads']):
            try:
                info = proc.info
                status = info['status']
                
                if status in status_count:
                    status_count[status] += 1
                
                all_processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        processes['total'] = len(all_processes)
        processes['running'] = status_count['running']
        processes['sleeping'] = status_count['sleeping']
        processes['zombie'] = status_count['zombie']
        processes['stopped'] = status_count['stopped']
        
        # Top 10 CPU
        processes['top_cpu'] = sorted(
            [p for p in all_processes if p.get('cpu_percent')],
            key=lambda x: x['cpu_percent'],
            reverse=True
        )[:10]
        
        # Top 10 Memory
        processes['top_memory'] = sorted(
            [p for p in all_processes if p.get('memory_percent')],
            key=lambda x: x['memory_percent'],
            reverse=True
        )[:10]
        
        return processes
    
    def collect_system_metrics(self):
        """Collecte les métriques système générales"""
        boot_time = psutil.boot_time()
        uptime_seconds = psutil.time.time() - boot_time
        
        metrics = {
            'boot_time': datetime.fromtimestamp(boot_time).isoformat(),
            'uptime_seconds': round(uptime_seconds),
            'uptime_hours': round(uptime_seconds / 3600, 2),
            'uptime_days': round(uptime_seconds / 86400, 2),
            'users_count': len(psutil.users())
        }
        
        # Load average (Linux/macOS)
        if hasattr(psutil, 'getloadavg'):
            try:
                load_avg = psutil.getloadavg()
                metrics['load_average'] = {
                    '1min': round(load_avg[0], 2),
                    '5min': round(load_avg[1], 2),
                    '15min': round(load_avg[2], 2)
                }
            except:
                pass
        
        return metrics
    
    def collect_all_metrics(self):
        """Collecte toutes les métriques en une fois"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.collect_cpu_metrics(),
            'memory': self.collect_memory_metrics(),
            'disk': self.collect_disk_metrics(),
            'network': self.collect_network_metrics(),
            'processes': self.collect_process_metrics(),
            'system': self.collect_system_metrics()
        }