import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Функция для начала захвата с камеры
def start_capture(camera_index):
    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        messagebox.showerror("Ошибка", "Не удалось открыть камеру.")
        return

    while True:
        success, img = cap.read()

        if not success:
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Face Detection', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # проверяет открыто ли окно с результатом
        if cv2.getWindowProperty('Face Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Функция для получения доступных камер
def get_available_cameras():
    available_cameras = []
    for i in range(10):  # пробуем до 10 камер
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap_name = f"Камера {i}"  # или можно попытаться использовать другие способы получения имени камеры
            available_cameras.append((i, cap_name))
            cap.release()
    return available_cameras

# Функция для открытия окна настроек
def open_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Настройки")

    # Центрируем окно настроек
    settings_window_width = 400
    settings_window_height = 200
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - settings_window_height / 2)
    position_right = int(screen_width / 2 - settings_window_width / 2)
    settings_window.geometry(f'{settings_window_width}x{settings_window_height}+{position_right}+{position_top}')

    # Получаем список доступных камер
    available_cameras = get_available_cameras()

    # Если камеры найдены, заполняем выпадающий список
    if available_cameras:
        camera_names = [name for index, name in available_cameras]
        camera_choice = ttk.Combobox(settings_window, values=camera_names, state="readonly")
        camera_choice.set("Выберите камеру")
        camera_choice.pack(pady=20)
    else:
        camera_choice = ttk.Combobox(settings_window, values=["Нет доступных камер"], state="disabled")
        camera_choice.set("Нет доступных камер")
        camera_choice.pack(pady=20)

    # Кнопка для выбора камеры
    select_button = tk.Button(settings_window, text="Выбрать камеру", command=lambda: select_camera(camera_choice, available_cameras))
    select_button.pack(pady=10)

# Функция для обработки выбора камеры из настроек
def select_camera(camera_choice, available_cameras):
    selected_camera = camera_choice.get()
    if selected_camera != "":
        selected_camera_index = next(index for index, name in available_cameras if name == selected_camera)
        messagebox.showinfo("Выбор камеры", f"Вы выбрали камеру: {selected_camera}")
        window.camera_index = selected_camera_index  # Сохраняем выбранный индекс камеры
    else:
        messagebox.showerror("Ошибка", "Не выбрана камера!")

# Функция для начала работы с выбранной камерой
def start_with_selected_camera():
    if hasattr(window, 'camera_index'):
        start_capture(window.camera_index)
    else:
        messagebox.showerror("Ошибка", "Камера не выбрана! Перейдите в настройки и выберите камеру.")

# Создание основного окна
window = tk.Tk()
window.title("Распознавание лиц Test 0.0.1")

# Центрируем окно
window_width = 400
window_height = 250
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Заголовок
label = tk.Label(window, text="Распознавание лиц\nТест 0.0.1", font=("Helvetica", 14))
label.pack(pady=50)

# Кнопки
start_button = tk.Button(window, text="Начать", command=start_with_selected_camera)
start_button.pack(pady=10)

# Кнопка для открытия настроек
settings_button = tk.Button(window, text="Настройки", command=open_settings)
settings_button.pack(pady=10)

# Запуск окна
window.mainloop()
