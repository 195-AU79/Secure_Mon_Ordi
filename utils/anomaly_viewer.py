#!/usr/bin/env python3
"""
utils/anomaly_viewer.py
Visualisation détaillée des anomalies détectées
"""

import os
from datetime import datetime


class AnomalyViewer:
    """Visualiseur d'anomalies avec affichage détaillé"""
    
    def __init__(self):
        """Initialise le visualiseur"""
        self.colors_enabled = True
        self.width = 70
    
    def _get_severity_icon(self, severity):
        """Retourne l'icône selon la sévérité"""
        icons = {
            'critical': '🔴',
            'warning': '🟡',
            'info': '🔵',
            'error': '🔴'
        }
        return icons.get(severity.lower(), '⚪')
    
    def _clear_screen(self):
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_complete_report(self, report):
        """Affiche un rapport complet"""
        print("\n" + "="*self.width)
        print("📋 RAPPORT D'ANALYSE SYSTÈME".center(self.width))
        print("="*self.width)
        
        # Informations générales
        timestamp = report.get('timestamp', 'N/A')
        print(f"\n⏰ Généré le: {timestamp}")
        
        # Score de santé
        health_score = report.get('health_score', 0)
        if health_score >= 80:
            score_emoji = "💚"
            status = "EXCELLENT"
        elif health_score >= 60:
            score_emoji = "🟡"
            status = "MOYEN"
        else:
            score_emoji = "🔴"
            status = "CRITIQUE"
        
        print(f"\n{score_emoji} SCORE DE SANTÉ: {health_score}/100 - {status}")
        
        # Métriques
        print(f"\n{'='*self.width}")
        print("📊 MÉTRIQUES ACTUELLES")
        print("="*self.width)
        
        if 'metrics' in report:
            metrics = report['metrics']
            cpu = metrics.get('cpu', {})
            mem = metrics.get('memory', {})
            disk = metrics.get('disk', {})
            net = metrics.get('network', {})
            
            print(f"  CPU:     {cpu.get('percent', 0):>6.1f}% ({cpu.get('count_logical', 0)} cœurs)")
            print(f"  Mémoire: {mem.get('percent', 0):>6.1f}% ({mem.get('used_gb', 0):.1f}/{mem.get('total_gb', 0):.1f} GB)")
            print(f"  Disque:  {disk.get('percent', 0):>6.1f}% ({disk.get('used_gb', 0):.1f}/{disk.get('total_gb', 0):.1f} GB)")
            
            if net:
                sent = net.get('sent_mb_s', 0)
                recv = net.get('recv_mb_s', 0)
                print(f"  Réseau:  {sent:.2f} MB/s ↑ | {recv:.2f} MB/s ↓")
            
            if 'processes' in metrics:
                print(f"  Processus: {metrics['processes'].get('total', 0)}")
        
        # Anomalies
        anomalies = report.get('anomalies', [])
        if anomalies:
            print(f"\n{'='*self.width}")
            print(f"⚠️  {len(anomalies)} ANOMALIE(S) DÉTECTÉE(S)")
            print("="*self.width)
            
            # Trier par sévérité
            severity_order = {'critical': 0, 'warning': 1, 'info': 2, 'error': 0}
            sorted_anomalies = sorted(
                anomalies,
                key=lambda x: severity_order.get(x.get('severity', 'info'), 2)
            )
            
            for i, anomaly in enumerate(sorted_anomalies[:10], 1):  # Max 10 pour l'affichage
                severity = anomaly.get('severity', 'info')
                icon = self._get_severity_icon(severity)
                print(f"\n{icon} ANOMALIE #{i} [{severity.upper()}]")
                print(f"   Type: {anomaly.get('type', 'N/A')}")
                print(f"   {anomaly.get('message', 'N/A')}")
        else:
            print(f"\n{'='*self.width}")
            print("✅ AUCUNE ANOMALIE DÉTECTÉE")
            print("="*self.width)
            print("\nSystème en bon état ! 🎉")
        
        # Recommandations
        analyses = report.get('analyses', [])
        if analyses:
            print(f"\n{'='*self.width}")
            print("💡 RECOMMANDATIONS")
            print("="*self.width)
            
            for i, analysis in enumerate(analyses[:5], 1):  # Max 5 recommandations
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    root_cause = analysis.get('root_cause', 'N/A')
                    print(f"\n🔍 Analyse #{i}: {root_cause}")
                    for j, rec in enumerate(recommendations[:3], 1):  # Max 3 par analyse
                        priority = rec.get('priority', 'medium').upper()
                        action = rec.get('action', 'N/A')
                        print(f"   {j}. [{priority}] {action}")
        
        print("\n" + "="*self.width + "\n")
    
    def display_anomaly_list(self, anomalies):
        """Affiche la liste numérotée des anomalies"""
        if not anomalies:
            print("\n✅ Aucune anomalie détectée.")
            return
        
        print(f"\n{'='*self.width}")
        print(f"📋 LISTE DES ANOMALIES ({len(anomalies)}):")
        print("="*self.width)
        
        # Trier par sévérité
        severity_order = {'critical': 0, 'warning': 1, 'info': 2, 'error': 0}
        sorted_anomalies = sorted(
            anomalies,
            key=lambda x: severity_order.get(x.get('severity', 'info'), 2)
        )
        
        for i, anomaly in enumerate(sorted_anomalies, 1):
            severity = anomaly.get('severity', 'info')
            icon = self._get_severity_icon(severity)
            anomaly_type = anomaly.get('type', 'unknown')
            message = anomaly.get('message', 'N/A')
            
            # Tronquer le message si trop long
            if len(message) > 50:
                message = message[:47] + "..."
            
            print(f"\n{i}. {icon} [{severity.upper()}] {anomaly_type}")
            print(f"   {message}")
            print(f"   Valeur: {anomaly.get('value', 'N/A')}")
        
        print("="*self.width)
    
    def display_all_anomalies(self, anomalies):
        """Affiche toutes les anomalies en détail"""
        if not anomalies:
            print("\n✅ Aucune anomalie détectée.")
            return
        
        print(f"\n{'='*self.width}")
        print("👁️  TOUTES LES ANOMALIES EN DÉTAIL")
        print("="*self.width)
        
        # Trier par sévérité
        severity_order = {'critical': 0, 'warning': 1, 'info': 2, 'error': 0}
        sorted_anomalies = sorted(
            anomalies,
            key=lambda x: severity_order.get(x.get('severity', 'info'), 2)
        )
        
        for i, anomaly in enumerate(sorted_anomalies, 1):
            self.display_anomaly_with_analysis(anomaly, None, i)
            print("\n" + "-"*self.width + "\n")
    
    def display_anomaly_with_analysis(self, anomaly, analysis_data=None, index=None):
        """Affiche une anomalie avec son analyse"""
        if index:
            print(f"\n{'='*self.width}")
            print(f"ANOMALIE #{index}")
            print("="*self.width)
        else:
            print(f"\n{'='*self.width}")
            print("DÉTAILS DE L'ANOMALIE")
            print("="*self.width)
        
        severity = anomaly.get('severity', 'info')
        icon = self._get_severity_icon(severity)
        
        print(f"\n{icon} {severity.upper()}")
        print(f"\n📌 Type: {anomaly.get('type', 'N/A')}")
        print(f"📂 Catégorie: {anomaly.get('category', 'N/A')}")
        print(f"\n💬 {anomaly.get('message', 'N/A')}")
        
        # Valeurs
        print(f"\n📊 VALEURS:")
        value = anomaly.get('value', 'N/A')
        threshold = anomaly.get('threshold', 'N/A')
        
        print(f"   Valeur actuelle: {value}")
        print(f"   Seuil d'alerte:  {threshold}")
        
        if isinstance(value, (int, float)) and isinstance(threshold, (int, float)):
            diff = value - threshold
            if diff > 0:
                print(f"   Dépassement:     +{diff:.2f}")
        
        # Analyse de cause racine
        if analysis_data:
            print(f"\n{'='*self.width}")
            print("🔍 ANALYSE DE CAUSE RACINE")
            print("-"*self.width)
            
            if isinstance(analysis_data, str):
                print(f"\n💡 Cause identifiée:")
                print(f"   {analysis_data}")
            elif isinstance(analysis_data, dict):
                if 'cause' in analysis_data:
                    print(f"\n💡 Cause identifiée:")
                    print(f"   {analysis_data['cause']}")
                
                if 'components' in analysis_data:
                    print(f"\n⚙️  Composants affectés:")
                    for component in analysis_data['components']:
                        print(f"   • {component}")
                
                if 'factors' in analysis_data:
                    print(f"\n📈 Facteurs de sévérité:")
                    for factor in analysis_data['factors']:
                        print(f"   • {factor}")
        
        print("="*self.width)
    
    def display_recommendations(self, recommendations):
        """Affiche les recommandations"""
        if not recommendations:
            return
        
        print(f"\n{'='*self.width}")
        print("💡 RECOMMANDATIONS DE RÉSOLUTION")
        print("="*self.width)
        
        # Trier par priorité
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_recs = sorted(
            recommendations,
            key=lambda x: priority_order.get(x.get('priority', 'medium').lower(), 2)
        )
        
        for i, rec in enumerate(sorted_recs, 1):
            priority = rec.get('priority', 'medium').upper()
            action = rec.get('action', 'N/A')
            command = rec.get('command', '')
            impact = rec.get('impact', '')
            estimated_time = rec.get('estimated_time', '')
            warning = rec.get('warning', '')
            
            print(f"\n{i}. [{priority}] {action}")
            
            if command:
                print(f"   Commande: {command}")
            
            if impact:
                print(f"   Impact: {impact}")
            
            if estimated_time:
                print(f"   Temps estimé: {estimated_time}")
            
            if warning:
                print(f"   ⚠️  {warning}")
        
        print("="*self.width)
    
    def display_anomaly_summary(self, anomalies):
        """Affiche un résumé des anomalies"""
        if not anomalies:
            print("✅ Aucune anomalie")
            return
        
        # Compter par sévérité
        counts = {'critical': 0, 'warning': 0, 'info': 0, 'error': 0}
        for anomaly in anomalies:
            severity = anomaly.get('severity', 'info')
            if severity in counts:
                counts[severity] += 1
        
        summary_parts = []
        if counts['critical'] > 0:
            summary_parts.append(f"🔴 {counts['critical']} critique(s)")
        if counts['warning'] > 0:
            summary_parts.append(f"🟡 {counts['warning']} avertissement(s)")
        if counts['info'] > 0:
            summary_parts.append(f"🔵 {counts['info']} info(s)")
        
        if summary_parts:
            print(f"⚠️  {len(anomalies)} anomalie(s): {', '.join(summary_parts)}")
        else:
            print(f"⚠️  {len(anomalies)} anomalie(s) détectée(s)")

