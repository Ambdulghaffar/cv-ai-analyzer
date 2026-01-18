"""
Interface Mode Recruteur
"""
import streamlit as st
from src.pdf_processor import PDFProcessor
from src.ai_analyzer import CVAnalyzer
from utils.helpers import get_score_color

def render_recruiter_mode():
    """Interface principale du mode recruteur"""
    
    st.title("👔 Mode Recruteur")
    st.markdown("Comparez plusieurs CVs par rapport à une offre d'emploi et obtenez un classement automatique.")
    
    st.markdown("---")
    
    # Vérifier la clé API
    if 'groq_api_key' not in st.session_state or not st.session_state.groq_api_key:
        st.error("⚠️ Veuillez configurer votre clé API Groq dans la barre latérale")
        return
    
    # Offre d'emploi
    st.markdown("### 💼 Offre d'Emploi")
    job_offer = st.text_area(
        "Collez l'offre d'emploi",
        height=200,
        placeholder="Poste, missions, compétences requises..."
    )
    
    st.markdown("---")
    
    # Upload multiple CVs
    st.markdown("### 📄 CVs des Candidats")
    uploaded_cvs = st.file_uploader(
        "Uploadez plusieurs CVs (PDF)",
        type=['pdf'],
        accept_multiple_files=True,
        help="Sélectionnez plusieurs fichiers PDF"
    )
    
    if uploaded_cvs:
        st.success(f"✅ {len(uploaded_cvs)} CV(s) chargé(s)")
        
        # Afficher la liste
        with st.expander("📋 Liste des CVs"):
            for i, cv in enumerate(uploaded_cvs, 1):
                st.markdown(f"{i}. {cv.name}")
    
    st.markdown("---")
    
    # Bouton d'analyse
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analyze_button = st.button(
            "🔍 Analyser et Classer les Candidats",
            use_container_width=True,
            type="primary",
            disabled=not (uploaded_cvs and job_offer and len(uploaded_cvs) > 0)
        )
    
    if analyze_button:
        with st.spinner(f"🤖 Analyse de {len(uploaded_cvs)} CV(s) en cours..."):
            try:
                # Extraire tous les CVs
                cvs_data = []
                
                for cv_file in uploaded_cvs:
                    cv_text = PDFProcessor.extract_text(cv_file)
                    
                    if cv_text and len(cv_text) > 50:
                        cvs_data.append({
                            'name': cv_file.name,
                            'text': cv_text
                        })
                    else:
                        st.warning(f"⚠️ {cv_file.name} semble vide ou illisible")
                
                if not cvs_data:
                    st.error("❌ Aucun CV valide à analyser")
                    return
                
                # Analyser avec l'IA
                analyzer = CVAnalyzer(api_key=st.session_state.groq_api_key)
                ranking = analyzer.analyze_multiple_cvs(cvs_data, job_offer)
                
                # Sauvegarder
                st.session_state.recruiter_ranking = ranking
                st.session_state.recruiter_job_offer = job_offer
                
                st.success("✅ Analyse terminée !")
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
                return
    
    # Affichage des résultats
    if 'recruiter_ranking' in st.session_state:
        ranking = st.session_state.recruiter_ranking
        
        st.markdown("---")
        st.markdown("## 🏆 Classement des Candidats")
        
        # Synthèse globale
        if 'synthese' in ranking:
            st.info(f"**📊 Synthèse:** {ranking['synthese']}")
        
        st.markdown("---")
        
        # Afficher chaque candidat
        candidates = ranking.get('classement', [])
        
        for i, candidate in enumerate(candidates, 1):
            score = candidate.get('score', 0)
            color = get_score_color(score)
            recommandation = candidate.get('recommandation', 'À évaluer')
            
            # Icône selon la recommandation
            if "Recommandé" in recommandation:
                icon = "🌟"
                bg_color = "#e8f5e9"
            elif "considérer" in recommandation.lower():
                icon = "👍"
                bg_color = "#fff9c4"
            else:
                icon = "⚠️"
                bg_color = "#ffebee"
            
            # Carte candidat
            with st.container():
                st.markdown(f"""
                <div style="
                    background-color: {bg_color};
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid {color};
                    margin: 15px 0;
                ">
                    <h3 style="margin: 0 0 10px 0;">
                        {icon} #{i} - {candidate.get('candidat', 'Candidat')}
                    </h3>
                    <p style="margin: 5px 0;">
                        <strong>Score:</strong> <span style="color: {color}; font-size: 1.5em; font-weight: bold;">{score}/100</span>
                    </p>
                    <p style="margin: 5px 0;">
                        <strong>Recommandation:</strong> {recommandation}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Points forts et réserves
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**💪 Points Forts:**")
                    for point in candidate.get('points_forts', []):
                        st.markdown(f"- ✓ {point}")
                
                with col2:
                    st.markdown("**⚠️ Réserves:**")
                    reserves = candidate.get('reserves', [])
                    if reserves:
                        for point in reserves:
                            st.markdown(f"- ⚠️ {point}")
                    else:
                        st.markdown("*Aucune réserve majeure*")
                
                st.markdown("---")
        
        # Options d'export
        st.markdown("---")
        st.markdown("## 📥 Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Exporter en Texte", use_container_width=True):
                # Générer le rapport texte
                report = f"RAPPORT D'ANALYSE - CLASSEMENT DES CANDIDATS\n"
                report += f"=" * 60 + "\n\n"
                report += f"Offre d'emploi:\n{st.session_state.recruiter_job_offer}\n\n"
                report += f"Date: {st.session_state.get('timestamp', 'N/A')}\n\n"
                report += f"=" * 60 + "\n\n"
                
                for i, candidate in enumerate(candidates, 1):
                    report += f"#{i} - {candidate.get('candidat', 'Candidat')}\n"
                    report += f"Score: {candidate.get('score', 0)}/100\n"
                    report += f"Recommandation: {candidate.get('recommandation', '')}\n\n"
                    
                    report += "Points forts:\n"
                    for point in candidate.get('points_forts', []):
                        report += f"  - {point}\n"
                    
                    report += "\nRéserves:\n"
                    for point in candidate.get('reserves', []):
                        report += f"  - {point}\n"
                    
                    report += "\n" + "-" * 60 + "\n\n"
                
                st.download_button(
                    "💾 Télécharger le rapport",
                    report,
                    file_name="classement_candidats.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            st.info("📊 Export PDF à venir dans une prochaine version")
    
    else:
        # Instructions
        st.info("""
        ### 📖 Comment utiliser le Mode Recruteur:
        
        1. **Collez l'offre d'emploi** complète dans la zone de texte
        2. **Uploadez plusieurs CVs** (format PDF) de vos candidats
        3. **Cliquez sur Analyser** et attendez quelques secondes
        4. **Consultez le classement** automatique avec scores et recommandations
        5. **Exportez le rapport** pour archivage ou partage
        
        💡 **Astuce:** Plus l'offre d'emploi est détaillée, plus l'analyse sera précise !
        """)