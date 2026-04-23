# 💪 SportMAN – AthleteManager
<img src="data/readme_images/logo.png" alt="Иконка приложения" width="400">

## 🏁 Вступление

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

> Десктопное GUI-приложение для управления списком спортсменов. 
> Позволяет добавлять, искать, удалять и сортировать записи, а также 
> сохранять и загружать базу из XML-файлов.

> Проект выполнен в рамках лабораторной работы №2 по ППОИС (БГУИР).

## Содержание

- [Установка и запуск](#️-установка-и-запуск)
- [Интерфейс](#️-интерфейс)
- [Функциональность](#функциональность)
- [О проекте](#-о-проекте)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [База данных](#база-данных)
- [Дополнительная информация](#дополнительная-информация)


## ⚙️ Установка и Запуск

### Требования

- Python **3.11+**
- [PySide6](https://pypi.org/project/PySide6/)
- pyinstaller (Для создания реального приложения) 

### Установка

```bash
# Клонируем репозиторий 
# Заходим в директорию athletes_list_manager_app и создаем виртуальное окружение (python3 -m venv .venv)
pip install PySide6
pip install pyinstaller
# Находясь в директории прописываем команду
pyinstaller --windowed --icon=src/images/athlete_manager_logo.icns --add-data "src/images:src/images" src/main.py
```

### Запуск

#### Билд приложения

  Переходим в только что созданную папку dist и находим main.app на Mac (main.exe на Windows). 
  
  И запускаем как обычное приложение :\)

*или*

#### Запуск через main файл 
```bash
cd athletes_list_manager_app/src
python main.py
```

> В этом случае убедитесь, что запускаете из директории `src/`, иначе относительные пути к UI и данным не сработают.

---
## 🖥️ Интерфейс
<img src="data/readme_images/dark_theme_window.png" alt="Темная тема приложения" width="600">
<img src="data/readme_images/light_theme_window.png" alt="Светлая тема приложения" width="600">
<img src="data/readme_images/search_window.png" alt="Поиск спортсменов" width="600">
<img src="data/readme_images/add_window.png" alt="Добавление спортсмена" height="450">
<img src="data/readme_images/remove_window.png" alt="Удаление спортсменов" height="450">
<img src="data/readme_images/settings_window.png" alt="Удаление спортсменов" width="300">
<img src="data/readme_images/save_before_exit.png" alt="Удаление спортсменов" width="450">

## Функциональность

| Возможность | Описание |
|---|---|
| **Просмотр** | Табличный список спортсменов с пагинацией |
| **Добавление** | Диалог с вводом ФИО, вида спорта, разряда, состава, позиции и числа титулов |
| **Поиск** | Фильтрация по ФИО, виду спорта, разряду и диапазону числа титулов; результаты отображаются в отдельной таблице |
| **Удаление** | Удаление по тем же критериям с подтверждением; при удалении всех записей — предупреждение |
| **Сохранение / Загрузка** | Запись и чтение базы в XML-формат через диалог выбора файла |
| **Пагинация** | Переключение страниц (первая / назад / вперёд / последняя), выбор числа записей на странице (5 / 10 / 15 / 20) |
| **Темы оформления** | Светлая, тёмная и системная тема; выбор сохраняется между запусками через `QSettings` |

## 📝 О проекте
> ## Задание лабораторной работы:
> Разработать оконное приложение с одним главным окном и несколькими дочерними диалогами. Диалоги вызываются через соответствующие пункты меню. Команды меню дублируются на панели инструментов.

**Вариант:**
| Атрибут | Значения |
|---|---|
| Тип состава | основной / запасной / n/a |
| Позиция | зависит от вида спорта |
| Титулы | числовое значение |
| Разряд | 1-й юношеский, 2-й разряд, 3-й разряд, КМС, Мастер спорта |

**Условия поиска и удаления:**
- по имени или виду спорта
- по числу завоёванных титулов (верхняя и нижняя граница)
- по имени или разряду

*Список видов спорта и разрядов в диалоге поиска формируется автоматически из имеющихся в базе данных.*

### Архитектура 

Приложение построено по паттерну **MVC** с дополнительными слоями

### Структура проекта

```
athletes_list_manager_app/
├── data/
│   └── save_files/
│       ├── athletes.xml        # Пример базы данных (55 записей)
│       └── athletes2.xml
├── src/
│   ├── main.py                 # Точка входа, сборка компонентов
│   ├── controllers.py          # MainController, PaginationController, ThemeController
│   ├── core/
│   │   ├── athlete.py          # Датакласс Athlete
│   │   ├── model.py            # Бизнес-логика: фильтрация, сортировка, пагинация
│   │   ├── loader.py           # ILoader + SAXLoader (SAX-парсинг XML)
│   │   ├── saver.py            # ISaver + DOMSaver (DOM-генерация XML)
│   │   ├── adapter.py          # AthleteQtModel — адаптер для QTableView
│   │   └── settings.py         # Константы: разряды, составы, позиции, заголовки
│   ├── exceptions/
│   │   └── athlete_manager_exceptions.py  # AthleteManagerError
│   ├── views/
│   │   ├── views.py            # MainView, AddAthleteDialogView, SearchDialogView,
│   │   │                       # DeleteDialogView, SettingsDialogView
│   │   ├── dialog_factory.py   # IDialogFactory + DefaultDialogFactory
│   │   ├── ui_main_window.py   # Сгенерированный UI (Qt Designer → .ui → .py)
│   │   ├── ui_add_window.py
│   │   ├── ui_search_window.py
│   │   ├── ui_delete_window.py
│   │   └── ui_settings_window.py
│   ├── ui/
│   │   ├── main_window.ui      # Исходные .ui файлы Qt Designer
│   │   ├── add_window.ui
│   │   ├── search_window.ui
│   │   ├── delete_window.ui
│   │   └── settings_window.ui
│   └── images/
|       ├── athlete_manager_logo.icns
│       ├── athlete_manager_logo.png
│       ├── combo-icon.png
│       ├── up-arrow.png
│       └── down-arrow.png
```

## База данных

База данных хранится в XML-файлах. Пример структуры:

```xml
<?xml version="1.0" encoding="utf-8"?>
<athletes>
  <athlete>
    <fio>Иванов Дмитрий Сергеевич</fio>
    <team>основной</team>
    <position>нападающий</position>
    <titles>5</titles>
    <sport>Футбол</sport>
    <rank>кмс</rank>
  </athlete>
  <!-- ... -->
</athletes>
```

- **Сохранение** — `DOMSaver` использует `xml.dom.minidom` для форматированного вывода.
- **Загрузка** — `SAXLoader` использует `xml.sax` (потоковый парсинг, эффективен на больших файлах).

---


### Дополнительная информация

## TODOs:
- Сортировка
