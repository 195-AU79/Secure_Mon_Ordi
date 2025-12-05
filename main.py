#!/usr/bin/env python3
"""
main.py
Point d'entrée principal du système IT Monitor
"""

import sys
import os
import time

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.monitor import ITMonitor
from utils.anomaly_viewer import AnomalyViewer
try:
    from utils.visual_dashboard import VisualDashboard
    HAS_VISUAL_DASHBOARD = True
except ImportError:
    HAS_VISUAL_DASHBOARD = False


def print_banner():
    """Affiche la bannière du programme"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║     Système de Monitoring IT Portable - v2.0          ║
    ║          Intelligence Artificielle Avancée            ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def print_system_info(monitor):
    """Affiche les informations système"""
    print("\n" + "="*60)
    print("📊 INFORMATIONS SYSTÈME")
    print("="*60)
    info = monitor.get_system_info()
    for key, value in info.items():
        print(f"  {key.replace('_', ' ').title():20s}: {value}")
    print("="*60)


def interactive_menu(monitor):
    """Menu interactif principal"""
    viewer = AnomalyViewer()
    
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1.  📊 Informations système")
        print("2.  🔍 Analyse instantanée (basique)")
        print("3.  🔬 Analyse complète (avancée - 30+ anomalies)")
        print("4.  👁️  Voir détails des anomalies")
        print("5.  📺 Dashboard visuel en temps réel")
        print("6.  🔄 Monitoring continu (basique)")
        print("7.  🔄 Monitoring continu (avancé)")
        print("8.  🔥 Top 10 processus CPU")
        print("9.  💾 Top 10 processus Mémoire")
        print("10. 📁 Exporter rapport JSON")
        print("11. 📊 Statistiques d'historique")
        print("12. ⚙️  Configuration")
        print("13. ❌ Quitter")
        print("="*60)
        
        choice = input("\nVotre choix (1-13): ").strip()
        
        if choice == '1':
            print_system_info(monitor)
        
        elif choice == '2':
            print("\n🔍 ANALYSE BASIQUE EN COURS...")
            report = monitor.generate_report(detection_mode='basic')
            viewer.display_complete_report(report)
        
        elif choice == '3':
            print("\n🔬 ANALYSE AVANCÉE EN COURS...")
            print("⏳ Détection de 30+ types d'anomalies...\n")
            time.sleep(1)
            report = monitor.generate_report(detection_mode='advanced')
            viewer.display_complete_report(report)
        
        elif choice == '4':
            print("\n👁️  DÉTAILS DES ANOMALIES")
            print("Génération du rapport...")
            report = monitor.generate_report(detection_mode='advanced')
            anomalies = report.get('anomalies', [])
            
            if not anomalies:
                print("\n✅ Aucune anomalie détectée actuellement.")
                continue
            
            # Afficher la liste
            viewer.display_anomaly_list(anomalies)
            
            # Menu de sélection
            print("\nOptions:")
            print("  [1-{}] Voir détails d'une anomalie spécifique".format(len(anomalies)))
            print("  [A] Voir toutes les anomalies")
            print("  [R] Retour au menu")
            
            sub_choice = input("\nVotre choix: ").strip().upper()
            
            if sub_choice == 'A':
                viewer.display_all_anomalies(anomalies)
            elif sub_choice == 'R':
                continue
            elif sub_choice.isdigit() and 1 <= int(sub_choice) <= len(anomalies):
                idx = int(sub_choice) - 1
                anomaly = anomalies[idx]
                
                # Trouver l'analyse correspondante
                analyses = report.get('analyses', [])
                analysis_data = None
                recommendations = None
                
                for analysis in analyses:
                    if analysis.get('anomaly', {}).get('type') == anomaly.get('type'):
                        analysis_data = analysis.get('root_cause')
                        recommendations = analysis.get('recommendations')
                        break
                
                # Afficher
                viewer.display_anomaly_with_analysis(anomaly, analysis_data, int(sub_choice))
                if recommendations:
                    viewer.display_recommendations(recommendations)
            else:
                print("❌ Choix invalide")
        
        elif choice == '5':
            if not HAS_VISUAL_DASHBOARD:
                print("\n❌ Dashboard visuel non disponible")
                print("Copiez le fichier utils/visual_dashboard.py")
                continue
            
            print("\n📺 DASHBOARD VISUEL EN TEMPS RÉEL")
            print("Appuyez sur Ctrl+C pour arrêter...\n")
            time.sleep(2)
            
            try:
                dashboard = VisualDashboard()
                
                def dashboard_callback(report):
                    dashboard.display_realtime_dashboard(report)
                
                monitor.start_monitoring(detection_mode='advanced', callback=dashboard_callback)
                while monitor.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("\n\n✋ Dashboard arrêté.")
        
        elif choice == '6':
            print("\n🔄 MONITORING CONTINU BASIQUE ACTIVÉ")
            print("Intervalle: 5 secondes")
            print("Appuyez sur Ctrl+C pour arrêter...\n")
            try:
                def callback(report):
                    viewer.display_anomaly_summary(report.get('anomalies', []))
                
                monitor.start_monitoring(detection_mode='basic', callback=callback)
                while monitor.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("\n\n✋ Monitoring arrêté.")
        
        elif choice == '8':
            print("\n🔄 MONITORING CONTINU AVANCÉ ACTIVÉ")
            print("Intervalle: 5 secondes | Détection: 30+ anomalies")
            print("Appuyez sur Ctrl+C pour arrêter...\n")
            try:
                def callback(report):
                    os.system('clear' if os.name != 'nt' else 'cls')
                    print(f"⏰ {report['timestamp']}")
                    print(f"💚 Score: {report['health_score']}/100")
                    viewer.display_anomaly_summary(report.get('anomalies', []))
                
                monitor.start_monitoring(detection_mode='advanced', callback=callback)
                while monitor.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("\n\n✋ Monitoring arrêté.")
        
        elif choice == '7':
            metrics = monitor.collect_metrics()
            processes = metrics['processes']['top_cpu']
            print("\n🔥 TOP 10 PROCESSUS - CPU")
            print("-" * 60)
            print(f"{'PID':<10} {'Nom':<30} {'CPU %':<10}")
            print("-" * 60)
            for proc in processes:
                print(f"{proc['pid']:<10} {proc['name'][:28]:<30} {proc.get('cpu_percent', 0):<10.2f}")
        
        elif choice == '9':
            metrics = monitor.collect_metrics()
            processes = metrics['processes']['top_memory']
            print("\n💾 TOP 10 PROCESSUS - MÉMOIRE")
            print("-" * 60)
            print(f"{'PID':<10} {'Nom':<30} {'RAM %':<10}")
            print("-" * 60)
            for proc in processes:
                print(f"{proc['pid']:<10} {proc['name'][:28]:<30} {proc.get('memory_percent', 0):<10.2f}")
        
        elif choice == '10':
            print("\n📁 EXPORT DU RAPPORT...")
            filename = monitor.export_report(format='json')
            print(f"✅ Rapport exporté: {filename}")
        
        elif choice == '11':
            stats = monitor.get_statistics()
            print("\n📈 STATISTIQUES D'HISTORIQUE")
            print("="*60)
            for metric, data in stats.items():
                if data:
                    print(f"\n{metric.upper()}:")
                    print(f"  Actuel:  {data['current']:.1f}%")
                    print(f"  Moyen:   {data['average']:.1f}%")
                    print(f"  Min:     {data['min']:.1f}%")
                    print(f"  Max:     {data['max']:.1f}%")
        
        elif choice == '12':
            print("\n⚙️  CONFIGURATION")
            print("="*60)
            config = monitor.get_config()
            print(f"Seuils actuels:")
            thresholds = config.get('thresholds', {})
            for key, value in thresholds.items():
                print(f"  {key}: {value}")
            
            print("\n1. Modifier seuils")
            print("2. Retour")
            sub_choice = input("\nChoix: ").strip()
            
            if sub_choice == '1':
                print("\nEntrez les nouvelles valeurs (Entrée pour conserver):")
                for key in thresholds.keys():
                    new_val = input(f"{key} [{thresholds[key]}]: ").strip()
                    if new_val and new_val.isdigit():
                        monitor.update_config(f'thresholds.{key}', int(new_val))
                print("✅ Configuration mise à jour")
        
        elif choice == '13':
            print("\n👋 Au revoir!")
            if monitor.is_monitoring:
                monitor.stop_monitoring()
            break
        
        else:
            print("\n❌ Choix invalide")


def main():
    """Fonction principale"""
    print_banner()
    
    print("🔧 Initialisation du système...")
    
    try:
        # Créer l'instance du moniteur
        monitor = ITMonitor(config_file='config/config.json')
        
        print(f"✅ Système: {monitor.system_info['os']} {monitor.system_info['architecture']}")
        print(f"✅ Hostname: {monitor.system_info['hostname']}")
        
        # Vérifier les arguments de ligne de commande
        if len(sys.argv) > 1:
            viewer = AnomalyViewer()
            
            if sys.argv[1] == '--monitor':
                # Lancement direct en mode monitoring
                mode = sys.argv[2] if len(sys.argv) > 2 else 'basic'
                print(f"\n🔄 Lancement en mode monitoring {mode}")
                print("Appuyez sur Ctrl+C pour arrêter...\n")
                
                def callback(report):
                    viewer.display_complete_report(report)
                
                monitor.start_monitoring(detection_mode=mode, callback=callback)
                try:
                    while monitor.is_monitoring:
                        time.sleep(1)
                except KeyboardInterrupt:
                    monitor.stop_monitoring()
            
            elif sys.argv[1] == '--report':
                # Génération d'un rapport unique
                mode = sys.argv[2] if len(sys.argv) > 2 else 'basic'
                report = monitor.generate_report(detection_mode=mode)
                viewer.display_complete_report(report)
            
            elif sys.argv[1] == '--export':
                # Export direct
                filename = monitor.export_report()
                print(f"✅ Rapport exporté: {filename}")
            
            elif sys.argv[1] == '--help':
                print("\nUtilisation:")
                print("  python main.py                    # Mode interactif")
                print("  python main.py --monitor [mode]   # Monitoring continu (basic/advanced)")
                print("  python main.py --report [mode]    # Rapport unique")
                print("  python main.py --export           # Export rapport JSON")
                print("  python main.py --help             # Aide")
        else:
            # Mode interactif par défaut
            interactive_menu(monitor)
    
    except KeyboardInterrupt:
        print("\n\n✋ Programme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Programme terminé.")


if __name__ == "__main__":
    main()


def print_banner():
    """Affiche la bannière du programme"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║     Système de Monitoring IT Portable - v2.0          ║
    ║          Intelligence Artificielle Avancée            ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def print_system_info(monitor):
    """Affiche les informations système"""
    print("\n" + "="*60)
    print("📊 INFORMATIONS SYSTÈME")
    print("="*60)
    info = monitor.get_system_info()
    for key, value in info.items():
        print(f"  {key.replace('_', ' ').title():20s}: {value}")
    print("="*60)


def print_report(report):
    """Affiche un rapport formaté"""
    print("\n" + "="*60)
    print("📋 RAPPORT D'ANALYSE SYSTÈME")
    print("="*60)
    print(f"Généré le: {report['timestamp']}")
    
    # Score de santé
    score = report['health_score']
    if score >= 80:
        emoji = "💚"
        status = "EXCELLENT"
    elif score >= 60:
        emoji = "🟡"
        status = "MOYEN"
    else:
        emoji = "🔴"
        status = "CRITIQUE"
    
    print(f"\n{emoji} SCORE DE SANTÉ: {score}/100 - {status}")
    
    # Métriques
    print("\n📊 MÉTRIQUES ACTUELLES:")
    cpu = report['metrics']['cpu']
    mem = report['metrics']['memory']
    disk = report['metrics']['disk']
    net = report['metrics']['network']
    
    print(f"  CPU:     {cpu['percent']:>6.1f}% ({cpu['count_logical']} cœurs)")
    print(f"  Mémoire: {mem['percent']:>6.1f}% ({mem['used_gb']}/{mem['total_gb']} GB)")
    print(f"  Disque:  {disk['percent']:>6.1f}% ({disk['used_gb']}/{disk['total_gb']} GB)")
    print(f"  Réseau:  {net.get('sent_mb_s', 0):.2f} MB/s ↑ | {net.get('recv_mb_s', 0):.2f} MB/s ↓")
    print(f"  Processus: {report['metrics']['processes']['total']}")
    
    # Anomalies
    if report['anomalies']:
        print(f"\n{'='*60}")
        print(f"⚠️  {len(report['anomalies'])} ANOMALIE(S) DÉTECTÉE(S)")
        print("="*60)
        
        for i, anomaly in enumerate(report['anomalies'], 1):
            severity_icon = "🔴" if anomaly['severity'] == 'critical' else "🟡"
            print(f"\n{severity_icon} ANOMALIE #{i} [{anomaly['severity'].upper()}]")
            print(f"   Type: {anomaly['type']}")
            print(f"   {anomaly['message']}")
        
        # Recommandations
        if report['analyses']:
            print(f"\n{'='*60}")
            print("💡 RECOMMANDATIONS")
            print("="*60)
            
            for analysis in report['analyses'][:3]:  # Max 3
                if analysis.get('recommendations'):
                    print(f"\n🔍 {analysis['root_cause']}")
                    for i, rec in enumerate(analysis['recommendations'][:2], 1):
                        print(f"   {i}. [{rec['priority'].upper()}] {rec['action']}")
    else:
        print("\n✅ Aucune anomalie détectée. Système en bon état.")
    
    print("\n" + "="*60)


def interactive_menu(monitor):
    """Menu interactif principal"""
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1.  📊 Informations système")
        print("2.  🔍 Analyse instantanée (basique)")
        print("3.  🔬 Analyse complète (avancée - 30+ anomalies)")
        print("4.  🔄 Monitoring continu (basique)")
        print("5.  🔄 Monitoring continu (avancé)")
        print("6.  🔥 Top 10 processus CPU")
        print("7.  💾 Top 10 processus Mémoire")
        print("8.  📁 Exporter rapport JSON")
        print("9.  📊 Statistiques d'historique")
        print("10. ⚙️  Configuration")
        print("11. ❌ Quitter")
        print("="*60)
        
        choice = input("\nVotre choix (1-11): ").strip()
        
        if choice == '1':
            print_system_info(monitor)
        
        elif choice == '2':
            print("\n🔍 ANALYSE BASIQUE EN COURS...")
            report = monitor.generate_report(detection_mode='basic')
            print_report(report)
        
        elif choice == '3':
            print("\n🔬 ANALYSE AVANCÉE EN COURS...")
            print("⏳ Détection de 30+ types d'anomalies...\n")
            time.sleep(1)
            report = monitor.generate_report(detection_mode='advanced')
            print_report(report)
        
        elif choice == '4':
            print("\n🔄 MONITORING CONTINU BASIQUE ACTIVÉ")
            print("Intervalle: 5 secondes")
            print("Appuyez sur Ctrl+C pour arrêter...\n")
            try:
                monitor.start_monitoring(detection_mode='basic')
                while monitor.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("\n\n✋ Monitoring arrêté.")
        
        elif choice == '5':
            print("\n🔄 MONITORING CONTINU AVANCÉ ACTIVÉ")
            print("Intervalle: 5 secondes | Détection: 30+ anomalies")
            print("Appuyez sur Ctrl+C pour arrêter...\n")
            try:
                monitor.start_monitoring(detection_mode='advanced')
                while monitor.is_monitoring:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                print("\n\n✋ Monitoring arrêté.")
        
        elif choice == '6':
            metrics = monitor.collect_metrics()
            processes = metrics['processes']['top_cpu']
            print("\n🔥 TOP 10 PROCESSUS - CPU")
            print("-" * 60)
            print(f"{'PID':<10} {'Nom':<30} {'CPU %':<10}")
            print("-" * 60)
            for proc in processes:
                print(f"{proc['pid']:<10} {proc['name'][:28]:<30} {proc.get('cpu_percent', 0):<10.2f}")
        
        elif choice == '7':
            metrics = monitor.collect_metrics()
            processes = metrics['processes']['top_memory']
            print("\n💾 TOP 10 PROCESSUS - MÉMOIRE")
            print("-" * 60)
            print(f"{'PID':<10} {'Nom':<30} {'RAM %':<10}")
            print("-" * 60)
            for proc in processes:
                print(f"{proc['pid']:<10} {proc['name'][:28]:<30} {proc.get('memory_percent', 0):<10.2f}")
        
        elif choice == '8':
            print("\n📁 EXPORT DU RAPPORT...")
            filename = monitor.export_report(format='json')
            print(f"✅ Rapport exporté: {filename}")
        
        elif choice == '9':
            stats = monitor.get_statistics()
            print("\n📈 STATISTIQUES D'HISTORIQUE")
            print("="*60)
            for metric, data in stats.items():
                if data:
                    print(f"\n{metric.upper()}:")
                    print(f"  Actuel:  {data['current']:.1f}%")
                    print(f"  Moyen:   {data['average']:.1f}%")
                    print(f"  Min:     {data['min']:.1f}%")
                    print(f"  Max:     {data['max']:.1f}%")
        
        elif choice == '10':
            print("\n⚙️  CONFIGURATION")
            print("="*60)
            config = monitor.get_config()
            print(f"Seuils actuels:")
            thresholds = config.get('thresholds', {})
            for key, value in thresholds.items():
                print(f"  {key}: {value}")
            
            print("\n1. Modifier seuils")
            print("2. Retour")
            sub_choice = input("\nChoix: ").strip()
            
            if sub_choice == '1':
                print("\nEntrez les nouvelles valeurs (Entrée pour conserver):")
                for key in thresholds.keys():
                    new_val = input(f"{key} [{thresholds[key]}]: ").strip()
                    if new_val and new_val.isdigit():
                        monitor.update_config(f'thresholds.{key}', int(new_val))
                print("✅ Configuration mise à jour")
        
        elif choice == '11':
            print("\n👋 Au revoir!")
            if monitor.is_monitoring:
                monitor.stop_monitoring()
            break
        
        else:
            print("\n❌ Choix invalide")


def main():
    """Fonction principale"""
    print_banner()
    
    print("🔧 Initialisation du système...")
    
    try:
        # Créer l'instance du moniteur
        monitor = ITMonitor(config_file='config/config.json')
        
        print(f"✅ Système: {monitor.system_info['os']} {monitor.system_info['architecture']}")
        print(f"✅ Hostname: {monitor.system_info['hostname']}")
        
        # Vérifier les arguments de ligne de commande
        if len(sys.argv) > 1:
            if sys.argv[1] == '--monitor':
                # Lancement direct en mode monitoring
                mode = sys.argv[2] if len(sys.argv) > 2 else 'basic'
                print(f"\n🔄 Lancement en mode monitoring {mode}")
                print("Appuyez sur Ctrl+C pour arrêter...\n")
                monitor.start_monitoring(detection_mode=mode)
                try:
                    while monitor.is_monitoring:
                        time.sleep(1)
                except KeyboardInterrupt:
                    monitor.stop_monitoring()
            elif sys.argv[1] == '--report':
                # Génération d'un rapport unique
                mode = sys.argv[2] if len(sys.argv) > 2 else 'basic'
                report = monitor.generate_report(detection_mode=mode)
                print_report(report)
            elif sys.argv[1] == '--export':
                # Export direct
                filename = monitor.export_report()
                print(f"✅ Rapport exporté: {filename}")
            elif sys.argv[1] == '--help':
                print("\nUtilisation:")
                print("  python main.py                    # Mode interactif")
                print("  python main.py --monitor [mode]   # Monitoring continu (basic/advanced)")
                print("  python main.py --report [mode]    # Rapport unique")
                print("  python main.py --export           # Export rapport JSON")
                print("  python main.py --help             # Aide")
        else:
            # Mode interactif par défaut
            interactive_menu(monitor)
    
    except KeyboardInterrupt:
        print("\n\n✋ Programme interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔚 Programme terminé.")


if __name__ == "__main__":
    main()