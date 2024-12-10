import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import os
import PyPDF2
import time


# Функция для чтения текста из файла
def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    text = ""
    try:
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        elif ext == ".pdf":
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        else:
            messagebox.showerror("Ошибка", "Неподдерживаемый формат файла!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")
    return text

# Функция для настройки голоса pyttsx3
def set_voice_pyttsx3(engine, gender="male"):
    voices = engine.getProperty('voices')
    if gender.lower() == "male":
        engine.setProperty('voice', voices[0].id)  # Первый голос (мужской)
    elif gender.lower() == "female":
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Второй голос (женский)
        else:
            messagebox.showerror("Ошибка", "Женский голос недоступен в системе!")

# Функция для синтеза речи с паузами
def text_to_audio_pyttsx3(text, output_file):
    try:
        # Инициализация pyttsx3
        engine = pyttsx3.init()

        # Настройка скорости речи
        engine.setProperty('rate', 150)  # Регулировка скорости речи (меньше значение - медленнее)

        # Открытие файла для записи речи
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        messagebox.showinfo("Готово", f"Аудиофайл сохранен: {output_file}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось создать аудиофайл: {e}")

# Функция для обработки текста с паузами
def process_text_with_pauses(text):
    processed_text = ""
    
    for char in text:
        if char == ",":
            processed_text += char
            time.sleep(0.3)  # Пауза 0.3 сек после запятой
        elif char == ".":
            processed_text += char
            time.sleep(0.5)  # Пауза 0.5 сек после точки
        else:
            processed_text += char

    return processed_text

# Функция для обработки файла
def process_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("PDF файлы", "*.pdf")]
    )
    if not file_path:
        return

    text = read_file(file_path)
    if not text.strip():
        messagebox.showerror("Ошибка", "Файл пуст или не содержит текста!")
        return

    # Обработка текста с паузами
    processed_text = process_text_with_pauses(text)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".mp3", filetypes=[("MP3 файлы", "*.mp3")]
    )
    if not save_path:
        return

    # Преобразование текста в аудио
    text_to_audio_pyttsx3(processed_text, save_path)

# Создание графического интерфейса
app = tk.Tk()
app.title("Конвертер книги в аудиокнигу")
app.geometry("400x200")

tk.Label(app, text="Конвертер текста в аудиокнигу", font=("Arial", 16)).pack(pady=10)

tk.Button(app, text="Выбрать файл и конвертировать", command=process_file).pack(pady=20)

app.mainloop()
