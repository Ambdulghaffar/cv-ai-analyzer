"""
Logique d'analyse IA avec Groq
"""
import json
from groq import Groq
from typing import Dict, Optional
from utils.config import GROQ_API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS
from src.prompt_templates import (
    SYSTEM_PROMPT,
    ANALYSIS_PROMPT,
    COVER_LETTER_PROMPT,
    SUGGESTIONS_PROMPT,
    RECRUITER_ANALYSIS_PROMPT
)

class CVAnalyzer:
    """Analyseur de CV avec IA"""
    
    def __init__(self, api_key: str = GROQ_API_KEY, model: str = DEFAULT_MODEL):
        if not api_key:
            raise ValueError("Clé API Groq non configurée")
        
        self.client = Groq(api_key=api_key)
        self.model = model
    
    def _call_groq(self, prompt: str, system_prompt: str = SYSTEM_PROMPT, 
                   temperature: float = TEMPERATURE, 
                   max_tokens: int = MAX_TOKENS) -> str:
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
    
    def stream_analysis(self, cv_text: str, job_offer: str):
        """
        Analyse avec streaming (pour affichage progressif)
        """
        prompt = ANALYSIS_PROMPT.format(
            cv_text=cv_text,
            job_offer=job_offer
        )
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=MAX_TOKENS,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Parser le résultat final
            try:
                start_idx = full_response.find('{')
                end_idx = full_response.rfind('}') + 1
                json_str = full_response[start_idx:end_idx]
                analysis = json.loads(json_str)
                yield {"final_analysis": analysis}
            except:
                yield {"error": "Erreur parsing JSON"}
                
        except Exception as e:
            yield {"error": str(e)}