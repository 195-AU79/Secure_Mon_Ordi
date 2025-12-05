#!/usr/bin/env python3
"""
utils/visual_dashboard.py
Dashboard visuel en temps réel dans la console
"""

import os
import platform
import time


class VisualDashboard:
    """Dashboard visuel en temps réel"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.supports_unicode = self._supports_unicode()
    
    def _supports_unicode(self):
        """Vérifie si le terminal supporte Unicode"""
        try:
            '█'.encode(sys.stdout.encoding or 'utf-8')
            return True
        except:
            return False
    
    def clear_screen(self):
        """Efface l'écran"""
        os.system('clear' if self.os_type != 'Windows' else 'cls')
    
    def create_bar(self, value, max_value=100, width=30, style='block'):
        """
        Crée une barre de progression visuelle
        
        Args:
            value: Valeur actuelle
            max_value: Valeur maximale
            width: Largeur de la barre
            style: 'block', 'line', ou 'simple'
        """
        percentage = min(100, (value / max_value) * 100)
        filled = int((percentage / 100) * width)
        
        if style == 'block' and self.supports_unicode:
            bar = '█' * filled + '░' * (width - filled)
        elif style == 'line':
            bar = '▓' * filled + '░' * (width - filled)
        else:
            bar = '#' * filled + '-' * (width - filled)
        
        # Couleur selon le pourcentage
        if percentage >= 90:
            color = '\033[91m'  # Rouge
        elif percentage >= 80:
            color = '\033[93m'  # Jaune
        elif percentage >= 60:
            color = '\033[92m'  # Vert
        else:
            color = '\033[94m'  # Bleu
        
        reset = '\033[0m'
        
        return f"{color}[{bar}]{reset} {value:.1f}%"
    
    def create_gauge(self, value, label, threshold_warning=80, threshold_critical=90):
        """Crée une jauge visuelle avec label"""
        bar = self.create_bar(value)
        
        # Indicateur de statut
        if value >= threshold_critical:
            status = "🔴 CRITIQUE"
        elif value >= threshold_warning:
            status = "🟡 ATTENTION"
        else:
            status = "🟢 OK"
        
        return f"{label:12s} {bar} {status}"
    
    def display_mini_graph(self, history, height=5, width=30):
        """
        Affiche un mini graphique ASCII des dernières valeurs
        
        Args:
            history: Liste des valeurs historiques
            height: Hauteur du graphique
            width: Largeur du graphique
        """
        if not history or len(history) < 2:
            return "Données insuffisantes"
        
        # Prendre les dernières valeurs
        data = list(history)[-width:]
        
        # Normaliser les données
        max_val = max(data) if data else 100
        min_val = min(data) if data else 0
        range_val = max_val - min_val if max_val != min_val else 1
        
        # Créer le graphique
        graph_lines = []
        for y in range(height, 0, -1):
            line = ""
            threshold = min_val + (range_val * y / height)
            
            for value in data:
                if value >= threshold:
                    line += "█" if self.supports_unicode else "#"
                else:
                    line += " "
            
            # Ajouter l'échelle
            scale_value = min_val + (range_val * (y - 1) / (height - 1))
            graph_lines.append(f"{scale_value:5.1f}% |{line}|")
        
        # Ligne du bas
        graph_lines.append("      " + "─" * (len(data) + 2))
        
        return "\n".join(graph_lines)
    
    def display_realtime_dashboard(self, report):
        """Affiche un dashboard complet en temps réel"""
        self.clear_screen()
        
        # En-tête
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 15 + "DASHBOARD SYSTÈME EN TEMPS RÉEL" + " " * 21 + "║")
        print("╚" + "═" * 68 + "╝")
        
        # Timestamp
        print(f"\n⏰ {report['timestamp']}")
        
        # Score de santé (grand et visible)
        score = report.get('health_score', 0)
        if score >= 80:
            emoji = "💚"
            status = "EXCELLENT"
        elif score >= 60:
            emoji = "🟡"
            status = "MOYEN"
        else:
            emoji = "🔴"
            status = "CRITIQUE"
        
        print(f"\n{emoji}  SCORE DE SANTÉ: {score}/100 - {status}")
        print("─" * 70)
        
        # Métriques principales
        metrics = report.get('metrics', {})
        
        print("\n📊 RESSOURCES SYSTÈME:")
        print("─" * 70)
        
        if 'cpu' in metrics:
            cpu_val = metrics['cpu']['percent']
            print(self.create_gauge(cpu_val, "CPU", 80, 95))
        
        if 'memory' in metrics:
            mem_val = metrics['memory']['percent']
            print(self.create_gauge(mem_val, "Mémoire", 85, 95))
        
        if 'disk' in metrics:
            disk_val = metrics['disk']['percent']
            print(self.create_gauge(disk_val, "Disque", 85, 95))
        
        if 'memory' in metrics and 'swap' in metrics['memory']:
            swap_val = metrics['memory']['swap']['percent']
            print(self.create_gauge(swap_val, "SWAP", 50, 80))
        
        # Graphiques historiques
        if hasattr(report, '_history'):
            print("\n📈 TENDANCES (30 dernières secondes):")
            print("─" * 70)
            
            if report._history.get('cpu'):
                print("\nCPU:")
                print(self.display_mini_graph(report._history['cpu']))
            
            if report._history.get('memory'):
                print("\nMémoire:")
                print(self.display_mini_graph(report._history['memory']))
        
        # Informations réseau
        if 'network' in metrics:
            net = metrics['network']
            print("\n🌐 RÉSEAU:")
            print("─" * 70)
            sent = net.get('sent_mb_s', 0)
            recv = net.get('recv_mb_s', 0)
            print(f"  ↑ Upload:   {sent:>8.2f} MB/s")
            print(f"  ↓ Download: {recv:>8.2f} MB/s")
            print(f"  📦 Paquets perdus: {net.get('dropin', 0) + net.get('dropout', 0)}")
            print(f"  ⚠️  Erreurs: {net.get('errin', 0) + net.get('errout', 0)}")
        
        # Processus
        if 'processes' in metrics:
            proc = metrics['processes']
            print("\n⚙️  PROCESSUS:")
            print("─" * 70)
            print(f"  Total:   {proc.get('total', 0)}")
            print(f"  Running: {proc.get('running', 0)}")
            print(f"  Zombie:  {proc.get('zombie', 0)}")
            
            # Top 3 CPU
            if proc.get('top_cpu'):
                print("\n  🔥 Top CPU:")
                for p in proc['top_cpu'][:3]:
                    print(f"     • {p['name'][:25]:25s} {p.get('cpu_percent', 0):>5.1f}%")
        
        # Anomalies
        anomalies = report.get('anomalies', [])
        
        print("\n⚠️  ANOMALIES:")
        print("─" * 70)
        
        if not anomalies:
            print("  ✅ Aucune anomalie détectée")
        else:
            critical = sum(1 for a in anomalies if a.get('severity') == 'critical')
            warning = sum(1 for a in anomalies if a.get('severity') == 'warning')
            info = sum(1 for a in anomalies if a.get('severity') == 'info')
            
            if critical > 0:
                print(f"  🔴 Critique: {critical}")
            if warning > 0:
                print(f"  🟡 Attention: {warning}")
            if info > 0:
                print(f"  🔵 Info: {info}")
            
            print("\n  Dernières anomalies:")
            for anomaly in anomalies[:3]:
                icon = '🔴' if anomaly.get('severity') == 'critical' else '🟡'
                msg = anomaly.get('message', 'Anomalie détectée')[:50]
                print(f"     {icon} {msg}...")
        
        # Pied de page
        print("\n" + "─" * 70)
        print("Appuyez sur Ctrl+C pour arrêter le monitoring")
        print("═" * 70)
    
    def display_anomaly_card(self, anomaly, index=None):
        """Affiche une carte visuelle pour une anomalie"""
        severity = anomaly.get('severity', 'unknown')
        
        # Bordure selon sévérité
        if severity == 'critical':
            border_char = '█'
            color = '\033[91m'
        elif severity == 'warning':
            border_char = '▓'
            color = '\033[93m'
        else:
            border_char = '░'
            color = '\033[94m'
        
        reset = '\033[0m'
        
        # En-tête de carte
        header = f"{color}{border_char * 70}{reset}"
        
        print(f"\n{header}")
        
        if index:
            print(f"{color}║{reset} ANOMALIE #{index}" + " " * (57) + f"{color}║{reset}")
        else:
            print(f"{color}║{reset} ANOMALIE DÉTECTÉE" + " " * (50) + f"{color}║{reset}")
        
        print(f"{header}")
        
        # Contenu
        print(f"\n  Type:     {anomaly.get('type', 'unknown')}")
        print(f"  Sévérité: {severity.upper()}")
        print(f"  Message:  {anomaly.get('message', 'Pas de description')}")
        
        if 'value' in anomaly:
            value = anomaly['value']
            threshold = anomaly.get('threshold', 0)
            
            print(f"\n  Valeur:   {self.create_bar(value, 100, 40)}")
            print(f"  Seuil:    {threshold}%")
        
        print(f"\n{header}\n")
    
    def display_comparison_view(self, metrics_now, metrics_before):
        """Affiche une vue comparative entre deux moments"""
        print("\n" + "═" * 70)
        print("📊 COMPARAISON AVANT/MAINTENANT")
        print("═" * 70)
        
        print(f"\n{'Métrique':<15} {'Avant':>12} {'Maintenant':>12} {'Variation':>15}")
        print("─" * 70)
        
        # CPU
        cpu_now = metrics_now.get('cpu', {}).get('percent', 0)
        cpu_before = metrics_before.get('cpu', {}).get('percent', 0)
        diff_cpu = cpu_now - cpu_before
        arrow = "↑" if diff_cpu > 0 else "↓" if diff_cpu < 0 else "→"
        print(f"{'CPU':<15} {cpu_before:>11.1f}% {cpu_now:>11.1f}% {arrow} {abs(diff_cpu):>6.1f}%")
        
        # Mémoire
        mem_now = metrics_now.get('memory', {}).get('percent', 0)
        mem_before = metrics_before.get('memory', {}).get('percent', 0)
        diff_mem = mem_now - mem_before
        arrow = "↑" if diff_mem > 0 else "↓" if diff_mem < 0 else "→"
        print(f"{'Mémoire':<15} {mem_before:>11.1f}% {mem_now:>11.1f}% {arrow} {abs(diff_mem):>6.1f}%")
        
        # Disque
        disk_now = metrics_now.get('disk', {}).get('percent', 0)
        disk_before = metrics_before.get('disk', {}).get('percent', 0)
        diff_disk = disk_now - disk_before
        arrow = "↑" if diff_disk > 0 else "↓" if diff_disk < 0 else "→"
        print(f"{'Disque':<15} {disk_before:>11.1f}% {disk_now:>11.1f}% {arrow} {abs(diff_disk):>6.1f}%")
        
        print("═" * 70)
    
    def display_alert_banner(self, message, severity='warning'):
        """Affiche une bannière d'alerte"""
        if severity == 'critical':
            char = '█'
            color = '\033[91m'
            icon = '🚨'
        elif severity == 'warning':
            char = '▓'
            color = '\033[93m'
            icon = '⚠️ '
        else:
            char = '░'
            color = '\033[94m'
            icon = 'ℹ️ '
        
        reset = '\033[0m'
        
        banner = f"{color}{char * 70}{reset}"
        
        print(f"\n{banner}")
        print(f"{color}{icon}  {message.upper()}{reset}")
        print(f"{banner}\n")
    
    def display_summary_box(self, title, items, width=70):
        """Affiche une boîte de résumé"""
        print("\n┌" + "─" * (width - 2) + "┐")
        print(f"│ {title:^{width-4}} │")
        print("├" + "─" * (width - 2) + "┤")
        
        for item in items:
            print(f"│ {item:<{width-4}} │")
        
        print("└" + "─" * (width - 2) + "┘")
    
    def display_quick_actions(self, recommendations):
        """Affiche les actions rapides recommandées"""
        print("\n💡 ACTIONS RAPIDES RECOMMANDÉES:")
        print("═" * 70)
        
        if not recommendations:
            print("  Aucune action requise pour le moment")
            return
        
        urgent = [r for r in recommendations if r.get('priority') == 'urgent']
        high = [r for r in recommendations if r.get('priority') == 'high']
        
        actions = urgent + high
        
        for i, rec in enumerate(actions[:3], 1):
            priority = rec.get('priority', 'medium').upper()
            action = rec.get('action', 'Action recommandée')
            
            icon = '🚨' if priority == 'URGENT' else '⚠️ '
            
            print(f"\n  {i}. {icon} [{priority}]")
            print(f"     {action}")
            
            if rec.get('command'):
                print(f"     💻 Commande: {rec['command']}")


# Fonction utilitaire
def create_dashboard():
    """Crée une instance du dashboard"""
    return VisualDashboard()