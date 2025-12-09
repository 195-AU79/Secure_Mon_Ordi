#!/usr/bin/env python3
"""
core/server_manager.py
Gestionnaire de serveurs pour le monitoring
"""

import socket
import subprocess
import platform
import time
from datetime import datetime
from typing import List, Dict, Optional


class ServerManager:
    """Gestionnaire de serveurs à surveiller"""
    
    def __init__(self, config_manager=None):
        """
        Initialise le gestionnaire de serveurs
        
        Args:
            config_manager: Instance de ConfigManager pour charger/sauvegarder les serveurs
        """
        self.config_manager = config_manager
        self.servers = self._load_servers()
    
    def _load_servers(self) -> List[Dict]:
        """Charge la liste des serveurs depuis la configuration"""
        if self.config_manager:
            servers = self.config_manager.get('servers', [])
            return servers if isinstance(servers, list) else []
        return []
    
    def _save_servers(self):
        """Sauvegarde la liste des serveurs dans la configuration"""
        if self.config_manager:
            self.config_manager.set('servers', self.servers)
            self.config_manager.save()
    
    def add_server(self, name: str, host: str, port: int = None, 
                   server_type: str = 'ping', description: str = '') -> bool:
        """
        Ajoute un serveur à surveiller
        
        Args:
            name: Nom du serveur
            host: Adresse IP ou hostname
            port: Port (optionnel, pour vérification de port)
            server_type: Type de vérification ('ping', 'port', 'http')
            description: Description du serveur
        
        Returns:
            True si ajouté avec succès
        """
        # Vérifier si le serveur existe déjà
        if any(s['name'] == name for s in self.servers):
            return False
        
        server = {
            'name': name,
            'host': host,
            'port': port,
            'type': server_type,
            'description': description,
            'added_at': datetime.now().isoformat()
        }
        
        self.servers.append(server)
        self._save_servers()
        return True
    
    def remove_server(self, name: str) -> bool:
        """
        Supprime un serveur
        
        Args:
            name: Nom du serveur à supprimer
        
        Returns:
            True si supprimé avec succès
        """
        initial_count = len(self.servers)
        self.servers = [s for s in self.servers if s['name'] != name]
        
        if len(self.servers) < initial_count:
            self._save_servers()
            return True
        return False
    
    def get_server(self, name: str) -> Optional[Dict]:
        """Récupère un serveur par son nom"""
        for server in self.servers:
            if server['name'] == name:
                return server
        return None
    
    def list_servers(self) -> List[Dict]:
        """Retourne la liste de tous les serveurs"""
        return self.servers.copy()
    
    def check_server_status(self, server: Dict) -> Dict:
        """
        Vérifie l'état d'un serveur
        
        Args:
            server: Dictionnaire contenant les informations du serveur
        
        Returns:
            Dictionnaire avec le statut et les métriques
        """
        host = server['host']
        port = server.get('port')
        server_type = server.get('type', 'ping')
        
        status = {
            'name': server['name'],
            'host': host,
            'status': 'unknown',
            'online': False,
            'response_time_ms': None,
            'last_check': datetime.now().isoformat(),
            'error': None
        }
        
        try:
            if server_type == 'ping':
                # Vérification par ping
                response_time = self._ping_host(host)
                if response_time is not None:
                    status['status'] = 'online'
                    status['online'] = True
                    status['response_time_ms'] = round(response_time, 2)
                else:
                    status['status'] = 'offline'
                    status['error'] = 'Ping échoué'
            
            elif server_type == 'port':
                # Vérification de port
                if port is None:
                    status['error'] = 'Port non spécifié'
                    status['status'] = 'error'
                else:
                    response_time = self._check_port(host, port)
                    if response_time is not None:
                        status['status'] = 'online'
                        status['online'] = True
                        status['response_time_ms'] = round(response_time, 2)
                    else:
                        status['status'] = 'offline'
                        status['error'] = f'Port {port} fermé ou inaccessible'
            
            elif server_type == 'http':
                # Vérification HTTP (basique)
                port = port or 80
                response_time = self._check_http(host, port)
                if response_time is not None:
                    status['status'] = 'online'
                    status['online'] = True
                    status['response_time_ms'] = round(response_time, 2)
                else:
                    status['status'] = 'offline'
                    status['error'] = 'HTTP non accessible'
        
        except Exception as e:
            status['status'] = 'error'
            status['error'] = str(e)
        
        return status
    
    def check_all_servers(self) -> List[Dict]:
        """Vérifie l'état de tous les serveurs"""
        results = []
        for server in self.servers:
            status = self.check_server_status(server)
            results.append(status)
        return results
    
    def _ping_host(self, host: str, timeout: int = 3) -> Optional[float]:
        """
        Ping un host et retourne le temps de réponse en ms
        
        Args:
            host: Adresse IP ou hostname
            timeout: Timeout en secondes
        
        Returns:
            Temps de réponse en millisecondes ou None si échec
        """
        try:
            # Utiliser socket pour une vérification rapide
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # Essayer de se connecter sur un port commun (80)
            result = sock.connect_ex((host, 80))
            sock.close()
            
            elapsed = (time.time() - start_time) * 1000
            
            if result == 0:
                return elapsed
            
            # Si la connexion échoue, essayer avec ping système
            return self._system_ping(host, timeout)
        
        except Exception:
            return self._system_ping(host, timeout)
    
    def _system_ping(self, host: str, timeout: int = 3) -> Optional[float]:
        """Utilise la commande ping du système"""
        try:
            is_windows = platform.system().lower() == 'windows'
            
            if is_windows:
                # Windows: ping -n 1 -w timeout_ms host
                cmd = ['ping', '-n', '1', '-w', str(timeout * 1000), host]
            else:
                # Linux/Mac: ping -c 1 -W timeout host
                cmd = ['ping', '-c', '1', '-W', str(timeout), host]
            
            start_time = time.time()
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout + 1
            )
            elapsed = (time.time() - start_time) * 1000
            
            if result.returncode == 0:
                return elapsed
            return None
        
        except Exception:
            return None
    
    def _check_port(self, host: str, port: int, timeout: int = 3) -> Optional[float]:
        """
        Vérifie si un port est ouvert
        
        Args:
            host: Adresse IP ou hostname
            port: Numéro de port
            timeout: Timeout en secondes
        
        Returns:
            Temps de réponse en millisecondes ou None si fermé
        """
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, port))
            elapsed = (time.time() - start_time) * 1000
            sock.close()
            
            if result == 0:
                return elapsed
            return None
        
        except Exception:
            return None
    
    def _check_http(self, host: str, port: int = 80, timeout: int = 3) -> Optional[float]:
        """
        Vérifie si un serveur HTTP répond
        
        Args:
            host: Adresse IP ou hostname
            port: Numéro de port
            timeout: Timeout en secondes
        
        Returns:
            Temps de réponse en millisecondes ou None si inaccessible
        """
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, port))
            elapsed = (time.time() - start_time) * 1000
            sock.close()
            
            if result == 0:
                return elapsed
            return None
        
        except Exception:
            return None

