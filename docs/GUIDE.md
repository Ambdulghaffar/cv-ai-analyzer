# 📖 Guide Utilisateur - CV AI Analyzer

## Table des Matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Mode Candidat](#mode-candidat)
4. [Mode Recruteur](#mode-recruteur)
5. [Astuces et Bonnes Pratiques](#astuces)
6. [FAQ](#faq)
7. [Dépannage](#dépannage)

---

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- pip (installé avec Python)
- 50 Mo d'espace disque libre

### Installation Rapide

```bash
# 1. Cloner le repo
git clone https://github.com/votre-username/cv-ai-analyzer.git
cd cv-ai-analyzer

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv

# 3. Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
streamlit run app.py
```

---

## ⚙️ Configuration

### Obtenir une Clé API Groq (Gratuit)

1. Allez sur [console.groq.com](https://console.groq.com)
2. Cliquez sur **"Sign Up"** ou **"Login"**
3. Créez un compte avec votre email
4. Une fois connecté, allez dans **"API Keys"**
5. Cliquez sur **"Create API Key"**
6. Donnez un nom à votre clé (ex: "cv-analyzer")
7. Copiez la clé (elle commence par `gsk_...`)

⚠️ **Important:** Gardez cette clé secrète et ne la partagez jamais !

### Configurer l'Application

**Option 1: Dans l'interface (Recommandé)**
- Lancez l'application
- Dans la barre latérale, collez votre clé dans le champ "🔑 Clé API Groq"
- La clé est sauvegardée pour la session

**Option 2: Fichier .env (Permanent)**
```bash
# Créer le fichier .env
cp .env.example .env

# Éditer et ajouter votre clé
GROQ_API_KEY=gsk_votre_clé_ici
```

---

## 👤 Mode Candidat

### Vue d'Ensemble
Le mode candidat vous permet d'analyser votre CV par rapport à une offre d'emploi spécifique et d'obtenir des recommandations pour l'améliorer.

### Étapes Détaillées

#### 1. Préparer votre CV
- **Format:** PDF uniquement (pas de DOCX ou images)
- **Contenu:** Assurez-vous que le texte est sélectionnable (pas un scan)
- **Taille:** Maximum 10 MB
- **Qualité:** Plus votre CV est détaillé, meilleure sera l'analyse

✅ **Bon exemple de CV:**
- Sections claires (Expérience, Formation, Compétences)
- Dates précises
- Description détaillée des missions
- Technologies et outils mentionnés
- Réalisations quantifiées

❌ **À éviter:**
- CV en format image ou scanné
- CV trop créatif (graphiques complexes)
- PDF protégé par mot de passe
- Informations manquantes

#### 2. Préparer l'Offre d'Emploi
Copiez-collez l'offre complète incluant:
- Titre du poste
- Description de l'entreprise
- Missions principales
- **Compétences requises** (crucial!)
- Compétences souhaitées
- Niveau d'expérience
- Formation requise

💡 **Astuce:** Plus l'offre est détaillée, plus l'analyse sera précise.

#### 3. Lancer l'Analyse
1. Uploadez votre CV (bouton "📄 Votre CV")
2. Collez l'offre d'emploi dans la zone de texte
3. Cliquez sur "🔍 Analyser le Matching"
4. Attendez 10-20 secondes

#### 4. Comprendre les Résultats

**Score Global (0-100)**
- **80-100:** Excellent matching - Postulez maintenant !
- **60-79:** Bon matching - Quelques ajustements mineurs
- **40-59:** Matching moyen - Améliorations recommandées
- **0-39:** Matching faible - Retravailler le CV

**Scores Détaillés**
- **Compétences Techniques (40%):** Hard skills matching
- **Expérience (30%):** Pertinence et durée
- **Formation (20%):** Niveau et adéquation
- **Soft Skills (10%):** Qualités personnelles

**Compétences Présentes vs Manquantes**
- ✅ **Présentes:** Vos atouts pour le poste
- ❌ **Manquantes:** Ce qu'il faut ajouter ou développer

**Points Forts**
- 3-5 éléments qui vous rendent compétitif
- À mettre en avant lors de l'entretien

**Points d'Amélioration**
- 3-5 suggestions concrètes et actionnables
- Priorisez les changements par impact

#### 5. Fonctionnalités Avancées

**Générer une Lettre de Motivation**
1. Après l'analyse, cliquez sur "✍️ Générer une Lettre"
2. Attendez 5-10 secondes
3. Relisez et personnalisez la lettre
4. Téléchargez-la avec le bouton "📥 Télécharger"

**Obtenir des Suggestions d'Amélioration**
1. Cliquez sur "💡 Obtenir des Suggestions"
2. Consultez les 5 recommandations prioritaires
3. Appliquez-les à votre CV
4. Re-analysez pour voir l'amélioration du score !

---

## 👔 Mode Recruteur

### Vue d'Ensemble
Le mode recruteur permet de comparer plusieurs CVs et d'obtenir un classement automatique des candidats.

### Étapes Détaillées

#### 1. Définir l'Offre d'Emploi
Saisissez une offre complète et détaillée:
- Contexte de l'entreprise
- Missions du poste
- Compétences indispensables
- Compétences souhaitées
- Environnement de travail
- Évolution possible

#### 2. Uploader les CVs
1. Cliquez sur "📄 CVs des Candidats"
2. Sélectionnez plusieurs PDFs (Ctrl/Cmd + clic)
3. Maximum recommandé: 10 CVs simultanés
4. Vérifiez la liste des fichiers uploadés

#### 3. Lancer l'Analyse Comparative
1. Cliquez sur "🔍 Analyser et Classer"
2. Attendez (environ 5s par CV)
3. L'IA analyse et compare tous les profils

#### 4. Consulter le Classement

**Pour chaque candidat, vous obtenez:**
- **Score de matching (0-100)**
- **Recommandation:** Recommandé / À considérer / Non retenu
- **Points forts:** 2-3 atouts principaux
- **Réserves:** 2-3 points d'attention
- **Classement:** Position dans la sélection

**Synthèse Globale**
Un paragraphe comparatif vous aide à prendre une décision éclairée.

#### 5. Exporter le Rapport
1. Cliquez sur "📄 Exporter en Texte"
2. Téléchargez le rapport complet
3. Partagez-le avec votre équipe RH

---

## 💡 Astuces et Bonnes Pratiques

### Pour les Candidats

**Optimiser votre CV avant analyse:**
1. **Utilisez des mots-clés** de l'offre d'emploi
2. **Quantifiez vos réalisations** (chiffres, pourcentages)
3. **Mentionnez toutes les technologies** pertinentes
4. **Décrivez vos projets** en détail
5. **Incluez vos soft skills** dans les descriptions

**Améliorer votre score:**
- Si score < 60: Retravailler le CV en profondeur
- Si score 60-79: Ajuster les formulations et ajouter des détails
- Si score > 80: Peaufiner et personnaliser

**Utiliser les suggestions:**
- Appliquez d'abord les suggestions avec le plus d'impact
- Re-testez après chaque modification majeure
- Gardez plusieurs versions de votre CV pour différents postes

### Pour les Recruteurs

**Maximiser l'efficacité:**
1. **Définissez clairement** les critères de sélection
2. **Analysez par batch** de 5-10 CVs maximum
3. **Complétez** l'analyse IA par votre jugement humain
4. **Documentez** vos décisions avec les rapports

**Interpréter les résultats:**
- L'IA détecte le matching technique, pas le fit culturel
- Un score élevé = compétences présentes, pas garantie de performance
- Utilisez le classement comme pré-sélection, pas comme décision finale

**Éviter les biais:**
- L'IA se base uniquement sur le contenu du CV
- Aucune discrimination sur nom, genre, âge, origine
- Focus sur les compétences et l'expérience

---

## ❓ FAQ

**Q: L'analyse est-elle confidentielle ?**
R: Oui, totalement. Les données ne sont jamais stockées sur nos serveurs. Tout reste en local sur votre machine.

**Q: Puis-je analyser plusieurs fois le même CV ?**
R: Oui, sans limite. C'est même recommandé après chaque modification !

**Q: Le score est-il toujours fiable ?**
R: Le score est un indicateur, pas une vérité absolue. Utilisez-le comme guide.

**Q: Puis-je utiliser l'application hors ligne ?**
R: Non, une connexion internet est nécessaire pour l'API Groq.

**Q: L'application fonctionne-t-elle en français ?**
R: Oui, entièrement en français. L'IA comprend et répond en français.

**Q: Combien coûte l'utilisation ?**
R: L'application est 100% gratuite. Groq offre un quota généreux gratuit.

**Q: Puis-je analyser des CVs en anglais ?**
R: Oui, l'IA supporte plusieurs langues, dont l'anglais.

**Q: Les lettres de motivation sont-elles uniques ?**
R: Oui, chaque lettre est générée spécifiquement pour votre profil et l'offre.

---

## 🔧 Dépannage

### Problème: "Erreur API Groq"
**Causes possibles:**
- Clé API invalide
- Quota dépassé (rare)
- Problème de connexion

**Solutions:**
1. Vérifiez votre clé sur console.groq.com
2. Régénérez une nouvelle clé si nécessaire
3. Attendez quelques minutes et réessayez

### Problème: "PDF illisible" ou "CV vide"
**Causes:**
- PDF scanné (image)
- PDF protégé
- Format non standard

**Solutions:**
1. Convertissez le PDF en PDF texte
2. Retirez la protection (si c'est votre CV)
3. Essayez avec un autre PDF viewer
4. Recréez le CV depuis Word/Google Docs

### Problème: "Analyse trop lente"
**Causes:**
- CV très long (>5 pages)
- Serveur Groq saturé
- Connexion lente

**Solutions:**
1. Réduisez la taille du CV (2-3 pages idéal)
2. Réessayez à un autre moment
3. Vérifiez votre connexion internet

### Problème: "Score incohérent"
**Causes:**
- Offre d'emploi trop vague
- CV mal structuré
- Compétences implicites

**Solutions:**
1. Fournissez une offre plus détaillée
2. Rendez vos compétences explicites
3. Ajoutez des mots-clés pertinents

### Problème: Application ne démarre pas
**Solutions:**
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt

# Vérifier la version de Python
python --version  # Doit être 3.9+

# Essayer de lancer avec verbose
streamlit run app.py --logger.level=debug
```

---

## 📧 Support

Besoin d'aide supplémentaire ?

- 📖 **Documentation:** Lisez le README.md
- 🐛 **Bug:** Ouvrez une issue sur GitHub
- 💬 **Question:** Utilisez les discussions GitHub
- 📧 **Contact:** votre.email@example.com

---

**Dernière mise à jour:** Janvier 2026  
**Version:** 1.0.0