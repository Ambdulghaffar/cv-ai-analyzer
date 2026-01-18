"""
Extraction de texte depuis les PDFs
"""
import PyPDF2
import pdfplumber
from typing import Optional

class PDFProcessor:
    """Classe pour extraire le texte des CVs en PDF"""
    
    @staticmethod
    def extract_text_pypdf(pdf_file) -> str:
        """
        Extrait le texte avec PyPDF2 (méthode simple)
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur PyPDF2: {str(e)}")
    
    @staticmethod
    def extract_text_pdfplumber(pdf_file) -> str:
        """
        Extrait le texte avec pdfplumber (plus précis)
        """
        try:
            text = ""
            
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur pdfplumber: {str(e)}")
    
    @classmethod
    def extract_text(cls, pdf_file, method: str = "pdfplumber") -> str:
        """
        Extrait le texte avec la méthode spécifiée
        
        Args:
            pdf_file: Fichier PDF uploadé
            method: 'pdfplumber' ou 'pypdf'
        
        Returns:
            str: Texte extrait du PDF
        """
        if method == "pdfplumber":
            try:
                return cls.extract_text_pdfplumber(pdf_file)
            except:
                # Fallback sur PyPDF2 si pdfplumber échoue
                return cls.extract_text_pypdf(pdf_file)
        else:
            return cls.extract_text_pypdf(pdf_file)
    
    @staticmethod
    def validate_pdf(pdf_file) -> tuple[bool, Optional[str]]:
        """
        Valide que le fichier est un PDF valide et lisible
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Réinitialiser le pointeur
            pdf_file.seek(0)
            
            # Tester la lecture
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            if len(pdf_reader.pages) == 0:
                return False, "Le PDF est vide"
            
            # Réinitialiser à nouveau pour la lecture ultérieure
            pdf_file.seek(0)
            
            return True, None
        except Exception as e:
            return False, f"PDF invalide: {str(e)}"
    
    @staticmethod
    def get_pdf_info(pdf_file) -> dict:
        """
        Récupère les informations du PDF
        
        Returns:
            dict: Informations (nombre de pages, taille, etc.)
        """
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            info = {
                "num_pages": len(pdf_reader.pages),
                "size_bytes": pdf_file.size if hasattr(pdf_file, 'size') else None,
                "encrypted": pdf_reader.is_encrypted
            }
            
            pdf_file.seek(0)
            return info
        except Exception as e:
            return {"error": str(e)}