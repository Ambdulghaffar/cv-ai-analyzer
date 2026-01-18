# 🤖 CV AI Analyzer

> Analyseur intelligent de CVs et matching emploi propulsé par IA

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-API-green.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Une application web moderne qui utilise l'intelligence artificielle pour analyser les CVs, calculer un score de compatibilité avec des offres d'emploi, et fournir des recommandations personnalisées.

![Demo](assets/demo.gif)

---

## ✨ Fonctionnalités Principales

### 👤 Mode Candidat

- **📊 Score de Matching Intelligent** : Score de 0 à 100 basé sur une analyse multi-critères
- **🎯 Analyse Détaillée** : Compétences techniques, expérience, formation, soft skills
- **💡 Suggestions Personnalisées** : Recommandations concrètes pour améliorer votre CV
- **✍️ Génération de Lettre** : Lettre de motivation personnalisée automatique
- **📥 Export des Résultats** : Téléchargez vos analyses et lettres

### 👔 Mode Recruteur

- **🏆 Classement Automatique** : Compare plusieurs CVs et les classe par pertinence
- **📊 Analyse Comparative** : Vue d'ensemble des forces et faiblesses de chaque candidat
- **⚡ Gain de Temps** : Pré-sélection automatique des meilleurs profils
- **📄 Rapports Exportables** : Documentation complète pour vos dossiers

### 🚀 Fonctionnalités Bonus

- **📚 Historique** : Sauvegarde automatique de toutes vos analyses
- **🎨 Interface Moderne** : Design épuré et intuitif
- **⚡ Ultra Rapide** : Propulsé par Groq (le plus rapide du marché)
- **🔒 100% Gratuit** : Utilise des APIs gratuites

---

## 🛠️ Technologies Utilisées

- **[Streamlit](https://streamlit.io/)** - Framework web Python
- **[Groq API](https://groq.com/)** - Intelligence artificielle ultra-rapide
- **[Llama 3.3 70B](https://ai.meta.com/llama/)** - Modèle d'IA de Meta
- **[PyPDF2](https://pypdf2.readthedocs.io/)** & **[pdfplumber](https://github.com/jsvine/pdfplumber)** - Extraction PDF
- **[Plotly](https://plotly.com/)** - Visualisations interactives
- **Python 3.9+** - Langage de programmation

---

## 📦 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API Groq (gratuite)

### Étape 1 : Cloner le Repo

```bash
git clone https://github.com/votre-username/cv-ai-analyzer.git
cd cv-ai-analyzer
```

### Étape 2 : Créer un Environnement Virtuel (Recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Obtenir une Clé API Groq (Gratuit)

1. Allez sur [console.groq.com](https://console.groq.com)
2. Créez un compte (email + mot de passe)
3. Naviguez vers **"API Keys"**
4. Cliquez sur **"Create API Key"**
5. Donnez un nom à votre clé (ex: "cv-analyzer")
6. Copiez la clé (commence par `gsk_...`)

### Étape 5 : Configuration (Optionnel)

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez votre clé :

```
GROQ_API_KEY=votre_clé_ici
```

> **Note :** Vous pouvez aussi entrer la clé directement dans l'interface de l'application.

### Étape 6 : Lancer l'Application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

---

## 📖 Guide d'Utilisation

### Mode Candidat

1. **Configurer l'API**
   - Entrez votre clé Groq dans la barre latérale
   - Choisissez le modèle IA (Llama 3.3 70B recommandé)

2. **Préparer vos Documents**
   - Uploadez votre CV au format PDF
   - Copiez-collez l'offre d'emploi complète (titre, description, compétences, etc.)

3. **Lancer l'Analyse**
   - Cliquez sur "🔍 Analyser le Matching"
   - Attendez 10-20 secondes (l'IA analyse en profondeur)

4. **Consulter les Résultats**
   - **Score Global** : Votre taux de compatibilité (0-100)
   - **Scores Détaillés** : Compétences, expérience, formation
   - **Compétences** : Ce qui match vs ce qui manque
   - **Points Forts** : Vos atouts pour ce poste
   - **Améliorations** : Suggestions concrètes et actionnables

5. **Aller Plus Loin**
   - Générez une lettre de motivation personnalisée
   - Obtenez des suggestions spécifiques d'amélioration
   - Téléchargez vos documents

### Mode Recruteur

1. **Définir l'Offre**
   - Collez l'offre d'emploi complète dans la zone de texte

2. **Uploader les CVs**
   - Sélectionnez plusieurs CVs (format PDF)
   - Jusqu'à 10 CVs recommandés pour une analyse optimale

3. **Analyser**
   - Cliquez sur "🔍 Analyser et Classer les Candidats"
   - L'IA compare et classe automatiquement

4. **Consulter le Classement**
   - Les candidats sont classés par score décroissant
   - Chaque fiche indique : score, recommandation, points forts, réserves

5. **Exporter**
   - Téléchargez le rapport complet au format texte
   - Archivez ou partagez avec votre équipe

---

## 📊 Architecture du Projet

```
cv-ai-analyzer/
│
├── app.py                     # 🚀 Point d'entrée principal
├── requirements.txt           # 📦 Dépendances
├── README.md                  # 📖 Documentation
├── .env.example              # ⚙️ Configuration exemple
├── .gitignore                # 🚫 Fichiers ignorés
│
├── src/                      # 🧠 Logique métier
│   ├── pdf_processor.py      # 📄 Extraction PDF
│   ├── ai_analyzer.py        # 🤖 Analyse IA
│   ├── prompt_templates.py   # 💬 Templates de prompts
│   └── pdf_generator.py      # 📝 Génération PDF
│
├── ui/                       # 🎨 Interface utilisateur
│   ├── candidate_mode.py     # 👤 Mode Candidat
│   ├── recruiter_mode.py     # 👔 Mode Recruteur
│   └── components.py         # 🧩 Composants réutilisables
│
├── utils/                    # 🛠️ Utilitaires
│   ├── config.py            # ⚙️ Configuration
│   └── helpers.py           # 🔧 Fonctions helpers
│
├── data/                     # 💾 Données (gitignored)
│   ├── uploads/             # CVs uploadés
│   ├── history/             # Historique analyses
│   └── exports/             # Rapports générés
│
└── assets/                   # 🎨 Ressources
    └── demo.gif             # Démo visuelle
```

---

## 🎯 Comment Ça Marche ?

### Processus d'Analyse

1. **Extraction** : Le PDF du CV est converti en texte brut
2. **Préparation** : Le texte et l'offre sont formatés pour l'IA
3. **Analyse IA** : Llama 3.3 70B analyse sémantiquement les documents
4. **Scoring** : Un score multi-critères est calculé :
   - Compétences techniques (40%)
   - Expérience pertinente (30%)
   - Formation adéquate (20%)
   - Soft skills (10%)
5. **Recommandations** : L'IA génère des suggestions actionnables
6. **Export** : Les résultats sont formatés et exportables

### Prompts IA (Prompt Engineering)

L'application utilise des prompts sophistiqués pour :
- Extraire les compétences des CVs
- Identifier les gaps de compétences
- Évaluer la pertinence de l'expérience
- Générer des recommandations personnalisées
- Créer des lettres de motivation naturelles

Les templates de prompts sont dans `src/prompt_templates.py` - vous pouvez les personnaliser !

---

## 🚀 Améliorations Futures (Roadmap)

- [ ] **Mode Coaching** : Sessions interactives de préparation aux entretiens
- [ ] **Analyse Vidéo** : Évaluation des CV vidéos
- [ ] **Support Multi-Formats** : DOCX, images (OCR)
- [ ] **Comparaison de Versions** : Suivre l'évolution de votre CV
- [ ] **Intégrations** : LinkedIn, Indeed, etc.
- [ ] **Mode Hors-Ligne** : Utilisation sans API
- [ ] **Thèmes Personnalisables** : Mode sombre, thèmes colorés
- [ ] **Multi-Langues** : Support EN, ES, AR
- [ ] **Analytics** : Dashboard de statistiques
- [ ] **API REST** : Intégration avec d'autres outils

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/SuperFeature`)
3. **Committez** vos changements (`git commit -m 'Ajout SuperFeature'`)
4. **Pushez** vers la branche (`git push origin feature/SuperFeature`)
5. **Ouvrez** une Pull Request

### Guidelines

- Suivez le style de code existant
- Ajoutez des docstrings à vos fonctions
- Testez vos modifications localement
- Mettez à jour la documentation si nécessaire

---

## 🐛 Problèmes Connus & Solutions

### "Erreur API Groq"
- **Cause** : Clé API invalide ou quota dépassé
- **Solution** : Vérifiez votre clé sur console.groq.com

### "PDF illisible"
- **Cause** : PDF scanné (image) ou protégé
- **Solution** : Convertissez en PDF texte ou supprimez la protection

### "Analyse lente"
- **Cause** : CV très long ou serveur surchargé
- **Solution** : Raccourcissez le CV ou réessayez plus tard

### "Score incohérent"
- **Cause** : Offre d'emploi trop vague
- **Solution** : Fournissez une offre détaillée avec compétences spécifiques

---

## 📜 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

Vous êtes libre de :
- ✅ Utiliser commercialement
- ✅ Modifier le code
- ✅ Distribuer
- ✅ Utiliser en privé

Avec obligation de :
- 📄 Inclure la licence et le copyright

---

## 👨‍💻 Auteur

**Votre Nom**

- 🌐 Portfolio : [votre-site.com](https://votre-site.com)
- 💼 LinkedIn : [votre-profil](https://linkedin.com/in/votre-profil)
- 🐙 GitHub : [@votre-username](https://github.com/votre-username)
- 📧 Email : votre.email@example.com

---

## 🙏 Remerciements

- **Groq** pour leur API ultra-rapide et gratuite
- **Meta** pour le modèle Llama 3.3
- **Streamlit** pour leur framework incroyable
- **La communauté open-source** pour l'inspiration

---

## 📞 Support

Besoin d'aide ? Plusieurs options :

1. 📖 **Documentation** : Lisez ce README attentivement
2. 🐛 **Issues** : [Ouvrir un ticket sur GitHub](https://github.com/votre-username/cv-ai-analyzer/issues)
3. 💬 **Discussions** : [Forum de discussions](https://github.com/votre-username/cv-ai-analyzer/discussions)
4. 📧 **Email** : Contactez-moi directement

---

## 📈 Statistiques

![GitHub stars](https://img.shields.io/github/stars/votre-username/cv-ai-analyzer?style=social)
![GitHub forks](https://img.shields.io/github/forks/votre-username/cv-ai-analyzer?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/votre-username/cv-ai-analyzer?style=social)

---

<div align="center">

### ⭐ Si ce projet vous plaît, n'oubliez pas de mettre une étoile ! ⭐

**Fait avec ❤️ et beaucoup de ☕**

[🏠 Accueil](https://github.com/votre-username/cv-ai-analyzer) • 
[📖 Documentation](https://github.com/votre-username/cv-ai-analyzer/wiki) • 
[🐛 Bugs](https://github.com/votre-username/cv-ai-analyzer/issues) • 
[💡 Suggestions](https://github.com/votre-username/cv-ai-analyzer/discussions)

</div>