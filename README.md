## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/khylko98/2ch-archivach-downloader.git
cd 2ch-archivach-downloader
```

### 2. Установите зависимости
```bash
chmod +x install.sh
./install.sh
```

Во время установки введите путь до Python (например, `python3.11`).

### 3. Активируйте виртуальное окружение
```bash
source ./venv/bin/activate
```

### 4. Запустите скрипт
```bash
python main.py <папка_для_сохранения> <url1> <url2> ...
```

Пример:
```bash
python main.py ./downloads https://2ch.hk/b/res/123456.html https://arhivach.top/thread/654321
```

Все изображения и видео будут сохранены в указанную папку.
