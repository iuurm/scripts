import os
import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image
from fpdf import FPDF

def extract_frames(video_path, output_folder, fps_interval):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = int(fps * fps_interval)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_folder = os.path.join(output_folder, video_name)
    os.makedirs(video_folder, exist_ok=True)

    frame_count = 0
    saved_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(video_folder, f"frame_{saved_frames:03d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_frames += 1
        frame_count += 1

    cap.release()
    return video_folder

def create_pdf(image_folder, output_pdf):
    pdf = FPDF()
    for img_file in sorted(os.listdir(image_folder)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(image_folder, img_file)
            img = Image.open(img_path)
            img = img.convert("RGB")

            pdf.add_page()
            pdf.image(img_path, x=10, y=10, w=190)

    pdf.output(output_pdf, "F")

def process_videos(video_folder, output_folder, screenshots_per_minute):
    for file in os.listdir(video_folder):
        if file.endswith((".mp4", ".avi", ".mov", ".mkv")):
            video_path = os.path.join(video_folder, file)
            pdf_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.pdf")

            screenshots_interval = 60 / screenshots_per_minute
            img_folder = extract_frames(video_path, output_folder, screenshots_interval)
            create_pdf(img_folder, pdf_path)

            print(f"Готово: {pdf_path}")

def select_folder():
    folder = filedialog.askdirectory(title="Выберите папку с видео")
    if folder:
        output_folder = os.path.join(folder, "screenshots_pdf")
        os.makedirs(output_folder, exist_ok=True)
        screenshots_per_minute = simpledialog.askinteger("Настройка", "Сколько скринов в минуту?", minvalue=1, maxvalue=60)
        if screenshots_per_minute:
            print('start screenshot...')
            process_videos(folder, output_folder, screenshots_per_minute)

root = tk.Tk()
root.withdraw()
select_folder()
