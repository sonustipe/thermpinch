@echo off
echo Generating Tailwind CSS...

:: Assuming tailwindcss.exe is now in the bin directory at the project root
tailwindcss.exe -i .\thermpinch\tailwind\styles.css -o .\thermpinch\assets\tailwind.css --minify 

echo Tailwind CSS generated successfully.
pause
