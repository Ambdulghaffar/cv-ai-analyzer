"""
Templates de prompts pour l'analyse IA
"""

SYSTEM_PROMPT = """Tu es un expert RH et recruteur senior avec 15 ans d'expérience dans l'analyse de CV et le matching emploi.
Tu es spécialisé dans l'évaluation objective des compétences et l'identification des gaps.
Tes analyses sont précises, constructives et actionnables."""

ANALYSIS_PROMPT = """Analyse ce CV par rapport à l'offre d'emploi fournie.

**CV DU CANDIDAT:**
{cv_text}

**OFFRE D'EMPLOI:**
{job_offer}

**MISSION:**
Fournis une analyse détaillée au format JSON avec la structure suivante:

{{
  "score_global": <nombre entre 0 et 100>,
  "competences_techniques": {{
    "presentes": [<liste des compétences techniques du candidat qui matchent>],
    "manquantes": [<liste des compétences techniques requises mais absentes>],
    "score": <nombre entre 0 et 100>
  }},
  "experience": {{
    "annees_experience": <nombre d'années estimé>,
    "pertinence": "<court texte sur la pertinence de l'expérience>",
    "score": <nombre entre 0 et 100>
  }},
  "formation": {{
    "niveau": "<niveau de formation du candidat>",
    "adequation": "<court texte sur l'adéquation avec le poste>",
    "score": <nombre entre 0 et 100>
  }},
  "soft_skills": {{
    "identifies": [<liste des soft skills identifiées>],
    "manquantes": [<liste des soft skills souhaitées mais non mentionnées>]
  }},
  "points_forts": [<3-5 points forts du candidat pour ce poste>],
  "points_amelioration": [<3-5 suggestions concrètes d'amélioration du CV>],
  "synthese": "<paragraphe de synthèse de 3-4 phrases>"
}}

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""

COVER_LETTER_PROMPT = """Génère une lettre de motivation professionnelle et personnalisée.

**CV DU CANDIDAT:**
{cv_text}

**OFFRE D'EMPLOI:**
{job_offer}

**ANALYSE DU MATCHING:**
Score global: {score}/100
Points forts: {strengths}

**INSTRUCTIONS:**
- Ton professionnel mais chaleureux
- Structure classique: intro, corps (2-3 paragraphes), conclusion
- Met en avant les compétences qui matchent
- Montre l'enthousiasme pour le poste
- Reste concis (250-300 mots max)
- Utilise des exemples concrets du CV
- Ne mentionne PAS le score

Génère la lettre en français, prête à être utilisée."""

SUGGESTIONS_PROMPT = """En tant qu'expert RH, donne 5 suggestions concrètes et actionnables pour améliorer ce CV spécifiquement pour ce poste.

**CV ACTUEL:**
{cv_text}

**OFFRE D'EMPLOI:**
{job_offer}

**ANALYSE:**
Compétences manquantes: {missing_skills}
Score actuel: {score}/100

**FORMAT:**
Retourne une liste Python de 5 strings, chaque suggestion doit:
- Commencer par un verbe d'action
- Être spécifique et actionnable
- Viser à augmenter le score de matching
- Être réaliste (pas de mensonges)

Exemple: ["Ajouter une section 'Projets' avec 2-3 réalisations concrètes en Python", ...]

Réponds UNIQUEMENT avec la liste Python, sans texte supplémentaire."""

RECRUITER_ANALYSIS_PROMPT = """En tant que recruteur, analyse ces multiples CVs par rapport à l'offre d'emploi.

**OFFRE D'EMPLOI:**
{job_offer}

**CVS DES CANDIDATS:**
{cvs_text}

**MISSION:**
Classe les candidats par ordre de pertinence et fournis un JSON:

{{
  "classement": [
    {{
      "candidat": "<nom ou CV1, CV2, etc>",
      "score": <0-100>,
      "points_forts": [<2-3 points forts>],
      "reserves": [<2-3 réserves>],
      "recommandation": "<Recommandé/À considérer/Non retenu>"
    }}
  ],
  "synthese": "<paragraphe comparatif>"
}}

Réponds UNIQUEMENT avec le JSON."""