# test-reports

Генерация JSON-отчётов из CSV-файлов с информацией о сотрудниках. Поддерживаются отчёты по выплатам и средним ставкам.

---

## Возможности

- Обработка CSV-файлов вручную (без использования внешних библиотек)
- Стандартизация имен полей зарплаты (`salary`, `hourly_rate`, `rate`)
- Генерация:
  - **Payout Report** — расчёт выплат: `payout = rate * hours_worked`
  - **Average Rate Report** — средняя ставка по отделам
- Сохранение отчётов в формате `.json`

---

## Структура проекта
	test-reports/  
	├── defs.py # Основная логика обработки данных и генерации отчётов  
	├── main.py # CLI-обёртка для запуска отчётов  
	├── reports/ # Папка для сохранения отчётов  
	└── tests/  
	└── test_reports.py # Тесты на pytest
		
## Пример запуска
	python main.py example1.csv example2.csv --report report_name --type type
	
|Аргумент|Описание|Пример|
|---|---|---|
|`files`|Путь(и) к CSV-файлам|`employees.csv`|
|`--report`|Название выходного JSON-файла|`--report avg_report`|
|`--type`|Тип отчёта: `payout` или `avg`|`--type payout`|

Готовый отчёт будет сохранён в `reports/report_name.json`

## Пример отчета
### payout
[
  {
	"name": "John",
	"payout": 800
  },
  {
	"name": "Jane",
	"payout": 1050
  }
]
### avg
[
  {
    "IT": 25.0,
    "HR": 50.0
  }
]