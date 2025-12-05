#!/usr/bin/env python3
"""
Gestionnaire de Configuration pour IT Monitor
Charge et sauvegarde les paramètres depuis config.json
"""

import json
import os
from pathlib import Path

class ConfigManager:
    DEFAULT_CONFIG = {
        "system_name": "IT Monitor Portable",
        "version": "1.0.0",
        "thresholds": {
            "cpu": {"warning": 80, "critical": 95},
            "memory": {"warning": 85, "critical": 95},
            "disk": {"warning": 85, "critical": 95},
            "network_latency": {"warning": 150, "critical": 300}
        },
        "monitoring": {
            "interval_seconds": 5,
            "history_size": 100,
            "auto_start": False,
            "enable_logging": True,
            "log_file": "monitor.log"
        },
        "web_dashboard": {
            "enabled": True,
            "port": 8080,
            "host": "0.0.0.0",
            "auto_refresh_seconds": 5
        },
        "notifications": {
            "enabled": False,
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender": "",
                "recipients": [],
                "password": ""
            }
        },
        "ui": {
            "language": "fr",
            "theme": "dark"
        }
    }
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ Configuration chargée depuis {self.config_file}")
                return config
            except Exception as e:
                print(f"⚠️  Erreur lors du chargement de la config: {e}")
                print("📋 Utilisation de la configuration par défaut")
                return self.DEFAULT_CONFIG.copy()
        else:
            print(f"📝 Création d'un nouveau fichier de configuration")
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """Sauvegarde la configuration dans le fichier JSON"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuration sauvegardée dans {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def get(self, key_path, default=None):
        """
        Récupère une valeur de configuration
        Ex: get('thresholds.cpu.warning') retourne 80
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """
        Définit une valeur de configuration
        Ex: set('thresholds.cpu.warning', 75)
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        return self.save_config()
    
    def get_thresholds(self):
        """Retourne tous les seuils d'alerte"""
        return self.get('thresholds', {})
    
    def update_threshold(self, resource, level, value):
        """
        Met à jour un seuil spécifique
        Ex: update_threshold('cpu', 'warning', 75)
        """
        key_path = f'thresholds.{resource}.{level}'
        return self.set(key_path, value)
    
    def get_monitoring_interval(self):
        """Retourne l'intervalle de monitoring en secondes"""
        return self.get('monitoring.interval_seconds', 5)
    
    def get_web_config(self):
        """Retourne la configuration du dashboard web"""
        return self.get('web_dashboard', {})
    
    def is_notifications_enabled(self):
        """Vérifie si les notifications sont activées"""
        return self.get('notifications.enabled', False)
    
    def reset_to_defaults(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save_config()


# Exemple d'utilisation
if __name__ == "__main__":
    print("Test du gestionnaire de configuration\n")
    
    # Créer une instance
    config = ConfigManager()
    
    # Lire des valeurs
    print(f"Seuil CPU warning: {config.get('thresholds.cpu.warning')}%")
    print(f"Port web dashboard: {config.get('web_dashboard.port')}")
    print(f"Intervalle monitoring: {config.get_monitoring_interval()}s")
    
    # Modifier une valeur
    print("\nModification du seuil CPU à 75%...")
    config.update_threshold('cpu', 'warning', 75)
    
    # Vérifier le changement
    print(f"Nouveau seuil CPU: {config.get('thresholds.cpu.warning')}%")
    
    # Afficher tous les seuils
    print("\nTous les seuils:")
    for resource, levels in config.get_thresholds().items():
        print(f"  {resource}: {levels}")