# test_version.py
import groq
print(f"Version Groq: {groq.__version__}")

from groq import Groq
client = Groq(api_key="test")
print("✅ Import réussi sans erreur de proxies")