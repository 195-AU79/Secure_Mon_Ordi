#!/usr/bin/env python3
"""
utils/export.py
Export de rapports en différents formats
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path


class ReportExporter:
    """Export de rapports en différents formats"""
    
    def __init__(self, output_dir='data/reports'):
        """
        Initialise l'exporteur
        
        Args:
            output_dir: Répertoire de sortie pour les rapports
        """
        self.output_dir = output_dir
        
        # Créer le répertoire si nécessaire
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    
    def export(self, report, format='json', filename=None):
        """
        Exporte un rapport dans le format spécifié
        
        Args:
            report: Dictionnaire contenant le rapport
            format: Format d'export ('json', 'csv', 'html', 'pdf')
            filename: Nom du fichier (auto-généré si None)
            
        Returns:
            Chemin du fichier exporté
        """
        if not report:
            raise ValueError("Le rapport ne peut pas être vide")
        
        # Générer le nom de fichier si non fourni
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{timestamp}.{format}"
        
        # Ajouter le répertoire de sortie
        filepath = os.path.join(self.output_dir, filename)
        
        # Exporter selon le format
        if format.lower() == 'json':
            return self._export_json(report, filepath)
        elif format.lower() == 'csv':
            return self._export_csv(report, filepath)
        elif format.lower() == 'html':
            return self._export_html(report, filepath)
        elif format.lower() == 'pdf':
            return self._export_pdf(report, filepath)
        else:
            raise ValueError(f"Format non supporté: {format}. Formats disponibles: json, csv, html, pdf")
    
    def _export_json(self, report, filepath):
        """Exporte en JSON"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            return filepath
        except Exception as e:
            raise Exception(f"Erreur lors de l'export JSON: {e}")
    
    def _export_csv(self, report, filepath):
        """Exporte en CSV"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # En-tête principal
                writer.writerow(['Rapport de Monitoring IT'])
                writer.writerow(['Timestamp', report.get('timestamp', 'N/A')])
                writer.writerow(['Score de Santé', report.get('health_score', 0)])
                writer.writerow([])
                
                # Métriques
                writer.writerow(['MÉTRIQUES'])
                if 'metrics' in report:
                    metrics = report['metrics']
                    writer.writerow(['CPU (%)', metrics.get('cpu', {}).get('percent', 0)])
                    writer.writerow(['Mémoire (%)', metrics.get('memory', {}).get('percent', 0)])
                    writer.writerow(['Disque (%)', metrics.get('disk', {}).get('percent', 0)])
                writer.writerow([])
                
                # Anomalies
                writer.writerow(['ANOMALIES'])
                writer.writerow(['Type', 'Sévérité', 'Catégorie', 'Valeur', 'Seuil', 'Message'])
                
                anomalies = report.get('anomalies', [])
                if anomalies:
                    for anomaly in anomalies:
                        writer.writerow([
                            anomaly.get('type', 'N/A'),
                            anomaly.get('severity', 'N/A'),
                            anomaly.get('category', 'N/A'),
                            anomaly.get('value', 'N/A'),
                            anomaly.get('threshold', 'N/A'),
                            anomaly.get('message', 'N/A')
                        ])
                else:
                    writer.writerow(['Aucune anomalie détectée', '', '', '', '', ''])
                
            return filepath
        except Exception as e:
            raise Exception(f"Erreur lors de l'export CSV: {e}")
    
    def _export_html(self, report, filepath):
        """Exporte en HTML"""
        try:
            html_content = self._generate_html(report)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return filepath
        except Exception as e:
            raise Exception(f"Erreur lors de l'export HTML: {e}")
    
    def _generate_html(self, report):
        """Génère le contenu HTML"""
        timestamp = report.get('timestamp', 'N/A')
        health_score = report.get('health_score', 0)
        
        # Déterminer la couleur selon le score
        if health_score >= 80:
            score_color = '#28a745'  # Vert
            score_status = 'EXCELLENT'
        elif health_score >= 60:
            score_color = '#ffc107'  # Jaune
            score_status = 'MOYEN'
        else:
            score_color = '#dc3545'  # Rouge
            score_status = 'CRITIQUE'
        
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Monitoring IT</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: {score_color};
            text-align: center;
            margin: 20px 0;
        }}
        .status {{
            text-align: center;
            font-size: 24px;
            color: #666;
            margin-bottom: 30px;
        }}
        .section {{
            margin: 30px 0;
        }}
        .section h2 {{
            color: #007bff;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .critical {{
            color: #dc3545;
            font-weight: bold;
        }}
        .warning {{
            color: #ffc107;
            font-weight: bold;
        }}
        .info {{
            color: #17a2b8;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #007bff;
        }}
        .metric-label {{
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport de Monitoring IT</h1>
        <div class="score">{health_score}/100</div>
        <div class="status">Statut: {score_status}</div>
        <div class="section">
            <p><strong>Généré le:</strong> {timestamp}</p>
        </div>
        
        <div class="section">
            <h2>📈 Métriques Système</h2>
            <div class="metrics">
"""
        
        # Ajouter les métriques
        if 'metrics' in report:
            metrics = report['metrics']
            cpu = metrics.get('cpu', {})
            memory = metrics.get('memory', {})
            disk = metrics.get('disk', {})
            
            html += f"""
                <div class="metric-card">
                    <div class="metric-value">{cpu.get('percent', 0):.1f}%</div>
                    <div class="metric-label">CPU</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{memory.get('percent', 0):.1f}%</div>
                    <div class="metric-label">Mémoire</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{disk.get('percent', 0):.1f}%</div>
                    <div class="metric-label">Disque</div>
                </div>
"""
        
        html += """
            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ Anomalies Détectées</h2>
            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Sévérité</th>
                        <th>Catégorie</th>
                        <th>Valeur</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Ajouter les anomalies
        anomalies = report.get('anomalies', [])
        if anomalies:
            for anomaly in anomalies:
                severity = anomaly.get('severity', 'info')
                severity_class = severity
                html += f"""
                    <tr>
                        <td>{anomaly.get('type', 'N/A')}</td>
                        <td class="{severity_class}">{severity.upper()}</td>
                        <td>{anomaly.get('category', 'N/A')}</td>
                        <td>{anomaly.get('value', 'N/A')}</td>
                        <td>{anomaly.get('message', 'N/A')}</td>
                    </tr>
"""
        else:
            html += """
                    <tr>
                        <td colspan="5" style="text-align: center; color: #28a745;">
                            ✅ Aucune anomalie détectée - Système en bon état
                        </td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
"""
        
        # Ajouter les recommandations si présentes
        analyses = report.get('analyses', [])
        if analyses:
            html += """
        <div class="section">
            <h2>💡 Recommandations</h2>
"""
            for i, analysis in enumerate(analyses[:5], 1):  # Max 5 recommandations
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    html += f"""
            <h3>Recommandation #{i}</h3>
            <p><strong>Cause racine:</strong> {analysis.get('root_cause', 'N/A')}</p>
            <ul>
"""
                    for rec in recommendations[:3]:  # Max 3 par analyse
                        priority = rec.get('priority', 'medium')
                        html += f"""
                <li>
                    <strong>[{priority.upper()}]</strong> {rec.get('action', 'N/A')}
                    {f"<br><code>{rec.get('command', '')}</code>" if rec.get('command') else ''}
                </li>
"""
                    html += """
            </ul>
"""
            html += """
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        return html
    
    def _export_pdf(self, report, filepath):
        """Exporte en PDF (nécessite wkhtmltopdf ou une bibliothèque PDF)"""
        # Pour l'instant, on génère un HTML et on informe l'utilisateur
        # L'utilisateur peut convertir le HTML en PDF manuellement ou installer une bibliothèque
        
        html_filepath = filepath.replace('.pdf', '.html')
        self._export_html(report, html_filepath)
        
        print(f"⚠️  Export PDF non implémenté directement.")
        print(f"✅ Fichier HTML généré: {html_filepath}")
        print(f"💡 Vous pouvez convertir le HTML en PDF avec un outil comme wkhtmltopdf")
        print(f"   ou ouvrir le HTML dans un navigateur et utiliser 'Imprimer > Enregistrer en PDF'")
        
        return html_filepath

