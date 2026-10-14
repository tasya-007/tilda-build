# TILDA Analyzer

Десктоп-приложение для анализа карт распределения магнитного поля по данным сеточных измерений.

Ввод измерений → анализ (статистика, интерполяция, зоны, градиент) → визуализация (тепловая карта) → отчёт → экспорт PNG/PDF. Проект сохраняется в JSON-файл и открывается обратно для дальнейшей работы.

## Требования к системе

- **Python 3.11** (зафиксировано для одинаковой сборки на macOS и Windows)
- Поддерживаемые ОС: Windows 10/11, macOS
- Зависимости (см. `requirements.txt`):
  - PySide6 — GUI
  - NumPy — работа с массивами
  - SciPy — интерполяция и поиск зон
  - Matplotlib — тепловые карты и отчёты
  - PyInstaller — сборка в исполняемый файл (только для упаковки)

## Установка зависимостей

```bash
cd tilda_analyzer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск из исходников

```bash
python app.py
```

Рабочий поток:

1. **Ввод** — выберите размер сетки (5×5, 7×7, 10×10 или произвольную) и заполните таблицу значений, либо импортируйте CSV-файл (матрица значений, разделитель `;` или `,`), затем «Применить».
2. **Анализ** — тепловая карта поля (RBF-интерполяция thin-plate spline) или градиента, панель статистики, список найденных зон. Поддерживается авто- и фиксированная цветовая шкала.
3. **Отчёт** — предпросмотр отчёта, комментарий, экспорт в PNG/PDF.

Проект: меню «Файл» → «Сохранить проект…» (Ctrl+S) / «Открыть проект…» (Ctrl+O).

## Запуск тестов

```bash
python -m unittest discover -s tests
```

## Сборка Windows .exe

Локально (на Windows):

```bat
build_windows.bat
```

Результат: `dist\TILDA.exe`.

Автоматически через GitHub Actions (`.github/workflows/build_windows.yml`): запускается вручную или по push тега `v*`; артефакт `TILDA-windows` содержит `TILDA.exe`.

## Структура проекта

```
tilda_analyzer/
├── app.py                    # точка входа, сборка зависимостей
├── domain/                   # доменные модели (Point, Measurement, Grid, Experiment, Project)
├── dataio/                   # порты и адаптеры: ручной ввод, CSV, JSON-хранилище проектов
├── analysis/                 # статистика, интерполяция, зоны, градиент, результат анализа
├── visualization/            # рендер тепловых карт (matplotlib)
├── report/                   # сборка отчёта (PNG/PDF)
├── gui/                      # главное окно, контроллер, ввод сетки, панель статистики
├── tests/                    # тесты (unittest)
├── data/projects/            # каталог проектов по умолчанию
├── requirements.txt          # зависимости
├── TILDA.spec                # конфигурация PyInstaller
├── build_windows.bat         # сборка .exe на Windows
├── .github/workflows/        # CI: сборка Windows exe
└── README.md / CHANGELOG.md
```

## Описание основных модулей

| Модуль | Назначение |
|---|---|
| `domain/models.py` | Модели: `Point` (x, y, z), `Measurement`, `Grid` (с валидацией полноты, дублей и диапазона значений), `Experiment`, `Project`. Без логики UI/IO. |
| `dataio/ports.py` | Абстракции: `MeasurementSource` (источник измерений), `ProjectRepository` (хранилище проекта). |
| `dataio/adapters.py` | Адаптеры: `ManualGridSource` (ручной ввод), `CSVImportSource` (импорт матрицы), `JSONProjectRepository` (проект в одном JSON-файле, `schema_version` для будущих миграций формата). |
| `analysis/` | `statistics.py` — min/max/mean/median/std, неоднородность (std/mean×100%), экстремумы, центр концентрации; `interpolation.py` — `RBFInterpolator` (thin-plate spline); `zones.py` — связные зоны по порогу mean±k·std (`scipy.ndimage.label`); `gradient.py` — карта градиента; `result.py` — контейнер результата и координатор анализа. |
| `visualization/heatmap.py` | `HeatmapRenderer` — тепловые карты поля и градиента, наложение точек измерений, авто- и фиксированная цветовая шкала. |
| `report/report_builder.py` | Отчёт: карта + статистика + зоны + сырые данные; экспорт через `savefig` в PNG/PDF. |
| `gui/` | `main_window.py` — окно с вкладками «Ввод / Анализ / Отчёт» и меню «Файл»; `controller.py` — связывает UI с модулями; `grid_input_widget.py` — таблица ввода и CSV; `stats_panel.py` — статистика и зоны; `heatmap_canvas.py` — Qt-виджет matplotlib. |
| `app.py` | Composition root: создаёт адаптеры, контроллер и окно. |

## Формат проекта (project.json)

Один проект — один JSON-файл (UTF-8). Схема версионируется полем `schema_version` (текущая: 1):

```json
{
  "schema_version": 1,
  "project_name": "название",
  "experiments": [
    {
      "id": "exp-2026-08-07-1",
      "date": "2026-08-07",
      "comment": "после доработки катушки",
      "grid_shape": [7, 7],
      "unit": "mT",
      "calibration_offset": 0.02,
      "points": [
        {"x": 0, "y": 0, "z": null, "value": 0.21}
      ]
    }
  ]
}
```
