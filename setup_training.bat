@echo off
echo 🔥 JARVIS Training Setup
echo ========================

echo 📦 Installing training dependencies...
python install_training_deps.py

echo.
echo 📁 Creating Books folder...
if not exist "d:\Code\Books" mkdir "d:\Code\Books"
echo ✅ Books folder created at d:\Code\Books

echo.
echo 🎉 Setup Complete!
echo.
echo Next Steps:
echo 1. Add PDF/TXT/EPUB/DOCX books to d:\Code\Books\
echo 2. Run: python train_with_data.py
echo 3. Start training JARVIS with your books!
echo.
pause