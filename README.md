# csvKata
lets explore techniques to convert objects with different properties into csv files

mkvirtualenv csvKata
pip install -U pytest
pip install pytest-watch
ptw --onfail "./notify.sh Tests Failed" --onpass "./notify.sh PASS\!"
