#！/bin/bash
nosetests -sv tests/test_final.py
nosetests -sv tests/test_token.py
nosetests -sv tests/test_kcli/test_ssh_cli.py
#nosetests -s tests/test_confloader/test_confloader.py

