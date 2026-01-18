"""
Génération de rapports PDF
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from io import BytesIO
from utils.helpers import get_score_category, get_score_color
from utils.config import EXPORTS_DIR

class PDFReportGenerator:
    """Générateur de rapports PDF pour les analyses de CV"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés"""
        
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#667eea'),
            borderPadding=5,
            backColor=colors.HexColor('#f8f9fa')
        ))
        
        # Corps de texte
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Liste à puces
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=10
        ))
    
    def generate_candidate_report(self, analysis: dict, cv_name: str, job_title: str = "") -> BytesIO:
        """
        Génère un rapport PDF pour un candidat
        
        Args:
            analysis: Dictionnaire d'analyse du CV
            cv_name: Nom du CV
            job_title: Titre du poste (optionnel)
        
        Returns:
            BytesIO: Buffer contenant le PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # En-tête
        story.append(Paragraph("Rapport d'Analyse de CV", self.styles['CustomTitle']))
        story.append(Paragraph(f"Propulsé par CV AI Analyzer", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Informations générales
        info_data = [
            ['CV analysé:', cv_name],
            ['Date:', datetime.now().strftime("%d/%m/%Y à %H:%M")],
        ]
        
        if job_title:
            info_data.append(['Poste visé:', job_title])
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Score global
        score = analysis.get('score_global', 0)
        category = get_score_category(score)
        
        story.append(Paragraph("Score de Matching Global", self.styles['CustomSubtitle']))
        
        score_messages = {
            "excellent": "Excellent matching ! Le profil correspond parfaitement.",
            "bon": "Bon matching. Quelques ajustements mineurs possibles.",
            "moyen": "Matching moyen. Des améliorations sont recommandées.",
            "faible": "Matching faible. CV à retravailler significativement."
        }
        
        score_data = [
            ['Score', 'Évaluation', 'Commentaire'],
            [f"{score}/100", category.upper(), score_messages[category]]
        ]
        
        score_table = Table(score_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        story.append(score_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Scores détaillés
        story.append(Paragraph("Scores Détaillés par Section", self.styles['SectionTitle']))
        
        comp_tech = analysis.get('competences_techniques', {})
        experience = analysis.get('experience', {})
        formation = analysis.get('formation', {})
        
        detail_data = [
            ['Section', 'Score', 'Détails'],
            ['Compétences Techniques', f"{comp_tech.get('score', 0)}/100", 
             f"{len(comp_tech.get('presentes', []))} présentes, {len(comp_tech.get('manquantes', []))} manquantes"],
            ['Expérience', f"{experience.get('score', 0)}/100", 
             f"{experience.get('annees_experience', 0)} ans - {experience.get('pertinence', '')[:50]}..."],
            ['Formation', f"{formation.get('score', 0)}/100", 
             f"{formation.get('niveau', 'N/A')} - {formation.get('adequation', '')[:50]}..."],
        ]
        
        detail_table = Table(detail_data, colWidths=[2*inch, 1.2*inch, 2.8*inch])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        
        story.append(detail_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Compétences techniques
        story.append(Paragraph("Compétences Techniques", self.styles['SectionTitle']))
        
        presentes = comp_tech.get('presentes', [])
        manquantes = comp_tech.get('manquantes', [])
        
        if presentes:
            story.append(Paragraph("<b>✓ Compétences Présentes:</b>", self.styles['CustomBody']))
            for skill in presentes[:10]:  # Limiter à 10
                story.append(Paragraph(f"• {skill}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.1*inch))
        
        if manquantes:
            story.append(Paragraph("<b>✗ Compétences Manquantes:</b>", self.styles['CustomBody']))
            for skill in manquantes[:10]:  # Limiter à 10
                story.append(Paragraph(f"• {skill}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Soft Skills
        soft_skills = analysis.get('soft_skills', {})
        identifies = soft_skills.get('identifies', [])
        
        if identifies:
            story.append(Paragraph("Soft Skills Identifiées", self.styles['SectionTitle']))
            for skill in identifies[:8]:
                story.append(Paragraph(f"• {skill}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.2*inch))
        
        # Nouvelle page pour points forts et améliorations
        story.append(PageBreak())
        
        # Points forts
        points_forts = analysis.get('points_forts', [])
        if points_forts:
            story.append(Paragraph("💪 Points Forts", self.styles['SectionTitle']))
            for i, point in enumerate(points_forts, 1):
                story.append(Paragraph(f"{i}. {point}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.08*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Points d'amélioration
        points_amelioration = analysis.get('points_amelioration', [])
        if points_amelioration:
            story.append(Paragraph("🎯 Points d'Amélioration", self.styles['SectionTitle']))
            for i, point in enumerate(points_amelioration, 1):
                story.append(Paragraph(f"{i}. {point}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.08*inch))
            story.append(Spacer(1, 0.2*inch))
        
        # Synthèse
        synthese = analysis.get('synthese', '')
        if synthese:
            story.append(Paragraph("📝 Synthèse Globale", self.styles['SectionTitle']))
            story.append(Paragraph(synthese, self.styles['CustomBody']))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "Rapport généré par CV AI Analyzer | www.cv-ai-analyzer.com",
            self.styles['Normal']
        ))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    def generate_recruiter_report(self, ranking: dict, job_offer: str) -> BytesIO:
        """
        Génère un rapport PDF pour le mode recruteur
        
        Args:
            ranking: Dictionnaire de classement des candidats
            job_offer: Texte de l'offre d'emploi
        
        Returns:
            BytesIO: Buffer contenant le PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # En-tête
        story.append(Paragraph("Rapport de Classement des Candidats", self.styles['CustomTitle']))
        story.append(Paragraph(f"Mode Recruteur - CV AI Analyzer", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Informations générales
        info_data = [
            ['Date:', datetime.now().strftime("%d/%m/%Y à %H:%M")],
            ['Nombre de candidats:', str(len(ranking.get('classement', [])))],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2f6')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Synthèse globale
        synthese = ranking.get('synthese', '')
        if synthese:
            story.append(Paragraph("Synthèse Globale", self.styles['SectionTitle']))
            story.append(Paragraph(synthese, self.styles['CustomBody']))
            story.append(Spacer(1, 0.3*inch))
        
        # Classement
        story.append(Paragraph("Classement des Candidats", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.2*inch))
        
        candidates = ranking.get('classement', [])
        
        for i, candidate in enumerate(candidates, 1):
            # Carte candidat
            story.append(Paragraph(f"#{i} - {candidate.get('candidat', 'Candidat')}", 
                                 self.styles['SectionTitle']))
            
            # Score et recommandation
            score_data = [
                ['Score', 'Recommandation'],
                [f"{candidate.get('score', 0)}/100", candidate.get('recommandation', 'À évaluer')]
            ]
            
            score_table = Table(score_data, colWidths=[1.5*inch, 4.5*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(score_table)
            story.append(Spacer(1, 0.1*inch))
            
            # Points forts
            story.append(Paragraph("<b>Points Forts:</b>", self.styles['CustomBody']))
            for point in candidate.get('points_forts', []):
                story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.1*inch))
            
            # Réserves
            reserves = candidate.get('reserves', [])
            if reserves:
                story.append(Paragraph("<b>Réserves:</b>", self.styles['CustomBody']))
                for point in reserves:
                    story.append(Paragraph(f"• {point}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Séparateur entre candidats
            if i < len(candidates):
                story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "Rapport généré par CV AI Analyzer | Mode Recruteur",
            self.styles['Normal']
        ))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    def save_report(self, buffer: BytesIO, filename: str) -> str:
        """
        Sauvegarde le rapport PDF sur le disque
        
        Args:
            buffer: Buffer contenant le PDF
            filename: Nom du fichier (sans extension)
        
        Returns:
            str: Chemin du fichier sauvegardé
        """
        filepath = EXPORTS_DIR / f"{filename}.pdf"
        
        with open(filepath, 'wb') as f:
            f.write(buffer.getvalue())
        
        return str(filepath)