import os
import zipfile
import webbrowser
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

ZIP_PATH = 'photos.zip'
MODEL_PATH = 'resnet50_local.h5'
TOP_K = 5
SIMILARITY_THRESHOLD = 0.6
model = load_model(MODEL_PATH)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))
    image_array = np.array(image)
    if image_array.shape[-1] == 4:
        image_array = image_array[..., :3]
    image_array = np.expand_dims(image_array, axis=0)
    image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
    return image_array

def get_image_features(image: Image.Image):
    preprocessed_image = preprocess_image(image)
    features = model.predict(preprocessed_image)
    return features

def cosine_similarity(features1, features2):
    f1 = features1.flatten()
    f2 = features2.flatten()
    num = np.dot(f1, f2)
    den = np.linalg.norm(f1) * np.linalg.norm(f2)
    return num / (den + 1e-9)

def get_images_from_zip():
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        image_keys = [name for name in archive.namelist() if name.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return image_keys

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file).convert('RGB')
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

def find_similar_images(uploaded_image: Image.Image):
    uploaded_image_features = get_image_features(uploaded_image)
    image_keys = get_images_from_zip()
    similarities = []
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        for image_key in image_keys:
            try:
                with archive.open(image_key) as image_file:
                    compare_img = Image.open(image_file).convert('RGB')
                    compare_img_features = get_image_features(compare_img)
                    sim_val = cosine_similarity(uploaded_image_features, compare_img_features)
                    if sim_val >= SIMILARITY_THRESHOLD:
                        similarities.append((image_key, sim_val))
            except UnidentifiedImageError:
                pass
            except Exception:
                pass
        similarities.sort(key=lambda x: x[1], reverse=True)
        similar_images = []
        for image_key, sim_val in similarities[:TOP_K]:
            saved_image_name = extract_and_save_image(archive, image_key)
            similar_images.append((saved_image_name, sim_val))
    return similar_images

class PicTraceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicTrace")
        self.root.geometry("1000x700")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            ".",
            font=("Helvetica", 10),
            background="#3c3f41"
        )
        style.configure(
            "TFrame",
            background="#3c3f41"
        )
        style.configure(
            "TLabel",
            background="#3c3f41",
            foreground="#ffffff",
            font=("Helvetica", 11)
        )
        style.configure(
            "TButton",
            background="#5294e2",
            foreground="#ffffff",
            font=("Helvetica", 12, "bold")
        )
        style.map(
            "TButton",
            background=[("active", "#6aa5ec")]
        )
        style.configure(
            "MyLabelframe.TLabelframe",
            background="#3c3f41",
            borderwidth=2
        )
        style.configure(
            "MyLabelframe.TLabelframe.Label",
            background="#3c3f41",
            foreground="#ffffff",
            font=("Helvetica", 12, "bold")
        )

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.main_frame,
            text="PicTrace - Find Similar Images",
            font=("Helvetica", 18, "bold")
        )
        self.title_label.pack(pady=20)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.upload_button = ttk.Button(
            self.button_frame,
            text="Select Image",
            command=self.on_upload_button
        )
        self.upload_button.pack()

        self.result_label = ttk.Label(
            self.main_frame,
            text="Results will appear here",
            anchor="center"
        )
        self.result_label.pack(pady=10)

        self.preview_labelframe = ttk.Labelframe(
            self.main_frame,
            text="Similar Images (Threshold: 60%)",
            style="MyLabelframe.TLabelframe"
        )
        self.preview_labelframe.pack(pady=10, fill=tk.BOTH, expand=True)

        self.preview_frame = ttk.Frame(self.preview_labelframe)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(side=tk.BOTTOM, pady=5)

        self.footer_label = ttk.Label(
            self.footer_frame,
            text="Created by Svyatoslav Köning aka Solrikk",
            anchor="center",
            font=("Helvetica", 8),
            foreground="#aaaaaa"
        )
        self.footer_label.pack(side=tk.LEFT)

        self.footer_email_label = ttk.Label(
            self.footer_frame,
            text="reveni324@gmail.com",
            anchor="center",
            font=("Helvetica", 8, "underline"),
            foreground="#aaaaaa",
            cursor="hand2"
        )
        self.footer_email_label.pack(side=tk.LEFT, padx=10)
        self.footer_email_label.bind("<Button-1>", self.on_email_click)

    def on_email_click(self, event):
        webbrowser.open("mailto:reveni324@gmail.com")

    def on_upload_button(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not file_path:
            return
        try:
            uploaded_image = Image.open(file_path)
        except UnidentifiedImageError:
            messagebox.showerror("Error", "File is not a valid image")
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.result_label.config(
            text="Searching for similar images (threshold 60%)..."
        )
        self.root.update_idletasks()

        similar_images = find_similar_images(uploaded_image)
        if similar_images:
            result_text = "Similar images found (similarity ≥ 60%):\n"
            for img_name, sim_val in similar_images:
                result_text += f"- {img_name} (similarity: {sim_val:.2f})\n"
            self.result_label.config(text=result_text)
        else:
            self.result_label.config(
                text="No matching images found."
            )

        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        for img_name, sim_val in similar_images:
            full_path = os.path.join(UPLOAD_FOLDER, img_name)
            if os.path.exists(full_path):
                img_pil = Image.open(full_path).resize(
                    (150, 150), Image.Resampling.LANCZOS
                )
                img_tk = ImageTk.PhotoImage(img_pil)
                preview_label = ttk.Label(self.preview_frame, image=img_tk)
                preview_label.image = img_tk
                preview_label.pack(side=tk.LEFT, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PicTraceApp(root)
    root.mainloop()
