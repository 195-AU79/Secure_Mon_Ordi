#!/usr/bin/env python3
"""
setup.py
Script d'installation automatique du système IT Monitor
"""

import os
import sys
import subprocess
import platform


def print_banner():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     Installation Automatique - IT Monitor v2.0        ║
    ╚═══════════════════════════════════════════════════════╝
    """)


def check_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ requis. Version actuelle: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} détecté")
    return True


def create_directory_structure():
    """Crée la structure de dossiers"""
    print("\n📁 Création de la structure des dossiers...")
    
    directories = [
        'core',
        'detection',
        'analysis',
        'web',
        'web/static',
        'utils',
        'data/logs',
        'data/reports',
        'data/history',
        'config',
        'scripts',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✓ {directory}/")
    
    # Créer les fichiers __init__.py
    init_dirs = ['core', 'detection', 'analysis', 'web', 'utils', 'tests']
    for directory in init_dirs:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""{directory} package"""\n')
    
    print("✅ Structure créée avec succès")


def install_dependencies():
    """Installe les dépendances Python"""
    print("\n📦 Installation des dépendances...")
    
    try:
        # Vérifier si pip est disponible
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      check=True, capture_output=True)
        
        # Installer psutil
        print("   Installation de psutil...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'],
                      check=True)
        
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation des dépendances")
        print("   Essayez manuellement: pip install psutil")
        return False


def create_config_file():
    """Crée le fichier de configuration par défaut"""
    print("\n⚙️  Création du fichier de configuration...")
    
    config_content = """{
  "system_name": "IT Monitor Portable",
  "version": "2.0.0",
  
  "thresholds": {
    "cpu": 80,
    "memory": 85,
    "disk": 90,
    "swap": 50,
    "network_errors": 100,
    "zombie_processes": 5
  },
  
  "monitoring": {
    "interval_seconds": 5,
    "history_size": 100,
    "auto_start": false,
    "enable_logging": true,
    "log_file": "data/logs/monitor.log"
  },
  
  "web_dashboard": {
    "enabled": true,
    "port": 8080,
    "host": "0.0.0.0",
    "auto_refresh_seconds": 5
  },
  
  "notifications": {
    "enabled": false
  },
  
  "ui": {
    "language": "fr",
    "theme": "dark"
  }
}
"""
    
    config_path = 'config/config.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ Configuration créée: {config_path}")


def create_requirements_file():
    """Crée le fichier requirements.txt"""
    print("\n📝 Création du fichier requirements.txt...")
    
    with open('requirements.txt', 'w') as f:
        f.write('psutil>=5.9.0\n')
    
    print("✅ requirements.txt créé")


def create_gitignore():
    """Crée le fichier .gitignore"""
    print("\n🔒 Création du fichier .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Données
data/logs/*.log
data/reports/*.json
data/reports/*.csv
data/reports/*.html
data/history/*

# Config personnalisée (optionnel)
# config/config.json

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore créé")


def verify_installation():
    """Vérifie que l'installation est complète"""
    print("\n🔍 Vérification de l'installation...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'config/config.json'
    ]
    
    required_dirs = [
        'core',
        'detection',
        'analysis',
        'utils',
        'data'
    ]
    
    all_ok = True
    
    # Vérifier les fichiers
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - MANQUANT")
            all_ok = False
    
    # Vérifier les dossiers
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"   ✓ {directory}/")
        else:
            print(f"   ✗ {directory}/ - MANQUANT")
            all_ok = False
    
    return all_ok


def display_next_steps():
    """Affiche les prochaines étapes"""
    os_type = platform.system()
    python_cmd = "python" if os_type == "Windows" else "python3"
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║              Installation Terminée ! 🎉                ║
    ╚═══════════════════════════════════════════════════════╝
    
    📋 PROCHAINES ÉTAPES:
    
    1. Copiez tous les fichiers Python (.py) dans les dossiers correspondants:
       
       • main.py                        → Racine du projet
       • core/monitor.py                → Dossier core/
       • core/metrics_collector.py      → Dossier core/
       • core/config_manager.py         → Dossier core/
       • detection/anomaly_detector.py  → Dossier detection/
       • analysis/root_cause_analyzer.py    → Dossier analysis/
       • analysis/recommendation_engine.py  → Dossier analysis/
       • utils/logger.py                → Dossier utils/
       • utils/export.py                → Dossier utils/
    
    2. Lancez le programme:
    """)
    
    print(f"       {python_cmd} main.py")
    
    print("""
    3. Testez une analyse complète (option 3 du menu)
    
    4. Consultez le README.md pour plus d'informations
    
    ╔═══════════════════════════════════════════════════════╗
    ║              Commandes Rapides                         ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    print(f"    # Lancer en mode interactif")
    print(f"    {python_cmd} main.py")
    print()
    print(f"    # Monitoring continu avancé")
    print(f"    {python_cmd} main.py --monitor advanced")
    print()
    print(f"    # Générer un rapport")
    print(f"    {python_cmd} main.py --report advanced")
    print()
    print(f"    # Voir l'aide")
    print(f"    {python_cmd} main.py --help")
    print()


def main():
    """Fonction principale d'installation"""
    print_banner()
    
    # Vérification Python
    if not check_python_version():
        sys.exit(1)
    
    # Créer la structure
    create_directory_structure()
    
    # Installer les dépendances
    if not install_dependencies():
        print("\n⚠️  Installation partielle. Installez manuellement les dépendances.")
    
    # Créer les fichiers de configuration
    create_config_file()
    create_requirements_file()
    create_gitignore()
    
    # Vérification finale
    print()
    if verify_installation():
        print("\n✅ Installation complète et vérifiée")
    else:
        print("\n⚠️  Installation incomplète - vérifiez les fichiers manquants")
    
    # Afficher les prochaines étapes
    display_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Installation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'installation: {e}")
        import traceback
        traceback.print_exc()