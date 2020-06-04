cd C:\Users\thale\Documents\Pessoais\programming
mkdir %1
cd %1
git init
python C:\Users\thale\Documents\Pessoais\programming\Project_Initializer\create.py %1
git remote add origin https://github.com/thalesnunes/%1.git
cd.> README.md
git add .
git commit -m "Initial commit"
git push -u origin master
code .