import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("800x600")
        
        # Хранилище записей
        self.entries = []
        self.current_filter = "all"
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_list_frame()
        self.create_filter_frame()
        self.create_button_frame()
        
        # Загрузка данных при старте
        self.load_from_file()
        
    def create_input_frame(self):
        """Фрейм для ввода данных"""
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую запись", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Поле Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Поле Температура
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Поле Описание
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        # Чекбокс Осадки
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(input_frame, text="➕ Добавить запись", command=self.add_entry).grid(row=2, column=2, columnspan=2, pady=5)
        
    def create_filter_frame(self):
        """Фрейм для фильтрации"""
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация записей", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=15)
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_date).grid(row=0, column=2, padx=5)
        ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=3, padx=5)
        
        # Фильтр по температуре
        ttk.Label(filter_frame, text="Фильтр по температуре:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_temp_min = ttk.Entry(filter_frame, width=8)
        self.filter_temp_min.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="до").grid(row=1, column=2)
        self.filter_temp_max = ttk.Entry(filter_frame, width=8)
        self.filter_temp_max.grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_temp).grid(row=1, column=4, padx=5)
        
    def create_list_frame(self):
        """Фрейм для отображения записей"""
        list_frame = ttk.LabelFrame(self.root, text="Список записей", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица для отображения
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Настройка заголовков
        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура (°C)")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")
        
        # Настройка ширины колонок
        self.tree.column("date", width=120)
        self.tree.column("temperature", width=100)
        self.tree.column("description", width=350)
        self.tree.column("precipitation", width=80)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_button_frame(self):
        """Фрейм с кнопками управления"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 Сохранить в JSON", command=self.save_to_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="📂 Загрузить из JSON", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑 Очистить все", command=self.clear_all).pack(side="left", padx=5)
        
        # Статусная строка
        self.status_label = ttk.Label(button_frame, text="Готов", relief="sunken")
        self.status_label.pack(side="right", padx=5, fill="x", expand=True)
        
    def validate_date(self, date_str):
        """Проверка корректности даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
            
    def add_entry(self):
        """Добавление новой записи"""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "Да" if self.precip_var.get() else "Нет"
        
        # Валидация
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД")
            return
            
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
            
        if not description:
            messagebox.showerror("Ошибка", "Описание не может быть пустым!")
            return
            
        # Добавление записи
        entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": precipitation
        }
        
        self.entries.append(entry)
        self.update_display()
        
        # Очистка полей
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        self.status_label.config(text=f"Добавлена запись за {date}")
        
    def update_display(self):
        """Обновление отображения записей"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Применение фильтра
        filtered_entries = self.get_filtered_entries()
        
        # Добавление записей
        for entry in filtered_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
            
        self.status_label.config(text=f"Показано записей: {len(filtered_entries)} из {len(self.entries)}")
        
    def get_filtered_entries(self):
        """Получение отфильтрованных записей"""
        if self.current_filter == "by_date":
            filter_value = self.filter_date.get().strip()
            return [e for e in self.entries if e["date"] == filter_value]
        elif self.current_filter == "by_temp":
            try:
                min_temp = float(self.filter_temp_min.get()) if self.filter_temp_min.get() else None
                max_temp = float(self.filter_temp_max.get()) if self.filter_temp_max.get() else None
                
                result = self.entries
                if min_temp is not None:
                    result = [e for e in result if e["temperature"] >= min_temp]
                if max_temp is not None:
                    result = [e for e in result if e["temperature"] <= max_temp]
                return result
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректное значение температуры для фильтра!")
                return self.entries
        else:
            return self.entries
            
    def filter_by_date(self):
        """Фильтрация по дате"""
        date = self.filter_date.get().strip()
        if not date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации")
            return
            
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты для фильтра!")
            return
            
        self.current_filter = "by_date"
        self.update_display()
        
    def filter_by_temp(self):
        """Фильтрация по температуре"""
        min_temp = self.filter_temp_min.get().strip()
        max_temp = self.filter_temp_max.get().strip()
        
        if not min_temp and not max_temp:
            messagebox.showwarning("Предупреждение", "Введите хотя бы одно значение температуры")
            return
            
        self.current_filter = "by_temp"
        self.update_display()
        
    def reset_filter(self):
        """Сброс фильтрации"""
        self.current_filter = "all"
        self.filter_date.delete(0, tk.END)
        self.filter_temp_min.delete(0, tk.END)
        self.filter_temp_max.delete(0, tk.END)
        self.update_display()
        
    def save_to_file(self):
        """Сохранение в JSON файл"""
        filename = "weather_data.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"Сохранено в {filename}")
            messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
            
    def load_from_file(self):
        """Загрузка из JSON файла с обработкой ошибок"""
        filename = "weather_data.json"
        if not os.path.exists(filename):
            messagebox.showwarning("Предупреждение", f"Файл {filename} не найден")
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    messagebox.showwarning("Предупреждение", "Файл пуст, создана новая запись")
                    self.entries = []
                else:
                    self.entries = json.loads(content)
            self.reset_filter()
            self.status_label.config(text=f"Загружено из {filename}")
            messagebox.showinfo("Успех", f"Загружено {len(self.entries)} записей")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл JSON повреждён! Создана новая запись.")
            self.entries = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
            
    def clear_all(self):
        """Очистка всех записей"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ записи?"):
            self.entries = []
            self.reset_filter()
            self.status_label.config(text="Все записи удалены")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
