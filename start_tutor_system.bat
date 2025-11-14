@echo off
echo 🎓 JARVIS Tutor System Startup
echo ================================

echo 📦 Step 1: Installing Ollama...
python install_ollama.py

echo.
echo 🧪 Step 2: Testing Tutor System...
python test_tutor_system.py

echo.
echo 🚀 Step 3: Starting JARVIS with Tutor...
echo JARVIS is now ready with AI Tutor capabilities!
echo.
echo Commands to try:
echo - "Jarvis, what is binary search?"
echo - "algorithm kya hai?"
echo - "sorting samjhao"
echo.
pause
python main.py