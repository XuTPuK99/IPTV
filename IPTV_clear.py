# -*- coding: utf8 -*-
from pathlib import Path

# cleaning directory from *.log
for file in Path('.').glob('*.log'):
    try:
        file.unlink()
    except OSError as e:
        print("Ошибка: %s : %s" % (file, e.strerror))

# cleaning directory from *.ts
for file in Path('.').glob('*.ts'):
    try:
        file.unlink()
    except OSError as e:
        print("Ошибка: %s : %s" % (file, e.strerror))