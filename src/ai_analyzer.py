"""
Logique d'analyse IA avec Groq
"""
import json
from groq import Groq
from typing import Dict, Optional
from src.prompt_templates import (
    SYSTEM_PROMPT,
    ANALYSIS_PROMPT,
    COVER_LETTER_PROMPT,
    SUGGESTIONS_PROMPT,
    RECRUITER_ANALYSIS_PROMPT
)

class CVAnalyzer:
    """Analyseur de CV avec IA"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        Initialise l'analyseur avec une clé API
        
        Args:
            api_key: Clé API Groq (OBLIGATOIRE)
            model: Modèle à utiliser
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("❌ Clé API Groq obligatoire. Entrez votre clé dans la barre latérale.")
        
        if not api_key.startswith("gsk_"):
            raise ValueError("❌ Clé API invalide. Elle doit commencer par 'gsk_'")
        
        try:
            self.client = Groq(api_key=api_key)
            self.model = model
            
            # Test de connexion rapide
            self._test_connection()
            
        except Exception as e:
            raise ValueError(f"❌ Erreur de connexion à Groq: {str(e)}")
    
    def _test_connection(self):
        """Teste la connexion avec un appel minimal"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                temperature=0
            )
            # Si on arrive ici, la clé est valide
        except Exception as e:
            raise ValueError(f"❌ Clé API invalide ou problème de connexion: {str(e)}")
    
    def _call_groq(self, prompt: str, system_prompt: str = SYSTEM_PROMPT, 
                   temperature: float = 0.3, 
                   max_tokens: int = 4000) -> str:
        """
        Appel générique à l'API Groq
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Erreur API Groq: {str(e)}")
    
    def analyze_cv_matching(self, cv_text: str, job_offer: str) -> Dict:
        """
        Analyse principale: matching CV vs offre d'emploi
        
        Returns:
            Dict contenant l'analyse complète
        """
        prompt = ANALYSIS_PROMPT.format(
            cv_text=cv_text,
            job_offer=job_offer
        )
        
        response = self._call_groq(prompt, temperature=0.3)
        
        # Extraire le JSON de la réponse
        try:
            # Chercher le JSON dans la réponse
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                analysis = json.loads(json_str)
                return analysis
            else:
                raise ValueError("Aucun JSON trouvé dans la réponse")
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur parsing JSON: {str(e)}\nRéponse: {response}")
    
    def generate_cover_letter(self, cv_text: str, job_offer: str, 
                             analysis: Dict) -> str:
        """
        Génère une lettre de motivation personnalisée
        """
        prompt = COVER_LETTER_PROMPT.format(
            cv_text=cv_text,
            job_offer=job_offer,
            score=analysis.get('score_global', 0),
            strengths=", ".join(analysis.get('points_forts', []))[:200]
        )
        
        letter = self._call_groq(prompt, temperature=0.7, max_tokens=1500)
        return letter
    
    def generate_improvement_suggestions(self, cv_text: str, job_offer: str,
                                        analysis: Dict) -> list:
        """
        Génère des suggestions d'amélioration du CV
        """
        missing_skills = analysis.get('competences_techniques', {}).get('manquantes', [])
        
        prompt = SUGGESTIONS_PROMPT.format(
            cv_text=cv_text,
            job_offer=job_offer,
            missing_skills=", ".join(missing_skills[:5]),
            score=analysis.get('score_global', 0)
        )
        
        response = self._call_groq(prompt, temperature=0.5)
        
        # Parser la liste Python
        try:
            # Extraire la liste de la réponse
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                list_str = response[start_idx:end_idx]
                suggestions = eval(list_str)  # Sécurisé car on contrôle le prompt
                return suggestions[:5]
            else:
                # Fallback: retourner les suggestions du point_amelioration
                return analysis.get('points_amelioration', [])[:5]
        except:
            return analysis.get('points_amelioration', [])[:5]
    
    def analyze_multiple_cvs(self, cvs_data: list, job_offer: str) -> Dict:
        """
        Mode recruteur: analyse plusieurs CVs
        
        Args:
            cvs_data: Liste de dict avec 'name' et 'text'
            job_offer: Texte de l'offre
        """
        # Formater les CVs
        cvs_text = "\n\n=== SEPARATION ===\n\n".join([
            f"**CANDIDAT: {cv['name']}**\n{cv['text']}"
            for cv in cvs_data
        ])
        
        prompt = RECRUITER_ANALYSIS_PROMPT.format(
            job_offer=job_offer,
            cvs_text=cvs_text
        )
        
        response = self._call_groq(prompt, temperature=0.3, max_tokens=4000)
        
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                ranking = json.loads(json_str)
                return ranking
            else:
                raise ValueError("Aucun JSON trouvé")
        except Exception as e:
            raise Exception(f"Erreur parsing: {str(e)}")