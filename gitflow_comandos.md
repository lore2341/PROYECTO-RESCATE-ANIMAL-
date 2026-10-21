# Gitflow paso a paso (ramas: master, develop, feature/*)
Haz cada paso en días distintos si puedes, para que el historial se vea real.

## 0. Preparar
git init sistema-rescate-animal && cd sistema-rescate-animal
git remote add origin https://github.com/TU_USUARIO/sistema-rescate-animal.git   # crea antes el repo PÚBLICO vacío en GitHub

## 1. master y develop
git checkout -b master
(copia aquí solo README.md)
git add README.md && git commit -m "docs: README inicial"
git push -u origin master
git checkout -b develop && git push -u origin develop

## 2. feature/modelo-uml  (diagramas)
git checkout -b feature/modelo-uml develop
(copia la carpeta docs/ con cu.png y cl.png)
git add docs && git commit -m "docs: diagrama de casos de uso y de clases"
git checkout develop && git merge --no-ff feature/modelo-uml -m "Merge feature/modelo-uml"
git push origin develop feature/modelo-uml

## 3. feature/patron-factory
git checkout -b feature/patron-factory develop
(copia src/rescate/__init__.py, modelo.py y fabrica.py)
git add src && git commit -m "feat: modelo de expedientes y Factory Method"
git checkout develop && git merge --no-ff feature/patron-factory -m "Merge feature/patron-factory"
git push origin develop feature/patron-factory

## 4. feature/patron-observer  (Singleton + Observer)
git checkout -b feature/patron-observer develop
(copia src/rescate/gestor.py)
git add src && git commit -m "feat: GestorCasos Singleton y notificaciones Observer"
git checkout develop && git merge --no-ff feature/patron-observer -m "Merge feature/patron-observer"
git push origin develop feature/patron-observer

## 5. feature/mvc
git checkout -b feature/mvc develop
(copia src/rescate/mvc.py, src/main.py y docs/sq1.png, sq2.png)
git add . && git commit -m "feat: controlador y vista (MVC) + diagramas de secuencia"
git checkout develop && git merge --no-ff feature/mvc -m "Merge feature/mvc"
git push origin develop feature/mvc

## 6. release y publicación en master
git checkout -b release/1.0.0 develop
git commit --allow-empty -m "chore: preparar versión 1.0.0"
git checkout master && git merge --no-ff release/1.0.0 -m "Release 1.0.0"
git tag -a v1.0.0 -m "Versión 1.0.0"
git checkout develop && git merge --no-ff release/1.0.0
git push origin master develop --tags

## 7. Capturas para el PDF
- GitHub > Insights > Network  (ramas)   o   Code > Commits
- En consola:  git log --graph --oneline --all
