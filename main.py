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
import pickle

ZIP_PATH = 'photos.zip'
MODEL_PATH = 'resnet50_local.h5'
FEATURES_PATH = 'image_features.pkl'
TOP_K = 5
SIMILARITY_THRESHOLD = 0.45
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model(MODEL_PATH)

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
    return features.flatten()

def cosine_similarity(features1, features2):
    num = np.dot(features1, features2)
    den = np.linalg.norm(features1) * np.linalg.norm(features2)
    return num / (den + 1e-9)

def extract_features_from_zip():
    image_features = {}
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        image_keys = [name for name in archive.namelist() if name.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for image_key in image_keys:
            try:
                with archive.open(image_key) as image_file:
                    image = Image.open(image_file).convert('RGB')
                    features = get_image_features(image)
                    image_features[image_key] = features
            except UnidentifiedImageError:
                print(f"Cannot open image: {image_key}")
            except Exception as e:
                print(f"Error processing {image_key}: {e}")
    with open(FEATURES_PATH, 'wb') as f:
        pickle.dump(image_features, f)
    print(f"Features extracted and saved to {FEATURES_PATH}")

def load_precomputed_features():
    if not os.path.exists(FEATURES_PATH):
        extract_features_from_zip()
    with open(FEATURES_PATH, 'rb') as f:
        image_features = pickle.load(f)
    return image_features

image_features = load_precomputed_features()

def find_similar_images(uploaded_image: Image.Image):
    uploaded_image_features = get_image_features(uploaded_image)
    similarities = []
    for image_key, features in image_features.items():
        sim_val = cosine_similarity(uploaded_image_features, features)
        if sim_val >= SIMILARITY_THRESHOLD:
            similarities.append((image_key, sim_val))
    similarities.sort(key=lambda x: x[1], reverse=True)
    similar_images = []
    if similarities:
        with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
            for image_key, sim_val in similarities[:TOP_K]:
                saved_image_name = extract_and_save_image(archive, image_key)
                similar_images.append((saved_image_name, sim_val))
    return similar_images

def extract_and_save_image(archive, image_key):
    with archive.open(image_key) as image_file:
        image = Image.open(image_file).convert('RGB')
        safe_image_name = os.path.basename(image_key)
        image_path = os.path.join(UPLOAD_FOLDER, safe_image_name)
        image.save(image_path)
        return safe_image_name

class PicTraceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PicTrace")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        background_path = r'C:\Users\Solrikk\Documents\GitHub\PicTrace\assets\photo\ui-ux\background\image_back_.jpg'
        if not os.path.exists(background_path):
            messagebox.showerror("Error", f"Background image not found at: {background_path}")
            self.root.destroy()
            return

        try:
            bg_image = Image.open(background_path)
            bg_image = bg_image.resize((1000, 700), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            self.root.destroy()
            return

        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.nav_frame = ttk.Frame(self.root, style="Nav.TFrame")
        self.nav_frame.place(x=0, y=0, relwidth=1, height=50)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Helvetica", 10), background="#3c3f41")
        style.configure("TFrame", background="#3c3f41")
        style.configure("TLabel", background="#3c3f41", foreground="#ffffff", font=("Helvetica", 11))
        style.configure("TButton", background="#5294e2", foreground="#ffffff", font=("Helvetica", 12, "bold"))
        style.map("TButton",
                  background=[("active", "#6aa5ec")],
                  foreground=[("active", "#ffffff")])
        style.configure("Nav.TFrame", background="#2e2e2e")
        style.configure("Nav.TButton", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 11, "bold"))
        style.map("Nav.TButton",
                  background=[("active", "#4a4a4a")],
                  foreground=[("active", "#ffffff")])

        self.create_navigation()

        self.main_frame = ttk.Frame(self.root, style="TFrame")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.title_label = ttk.Label(self.main_frame, text="PicTrace - Find Similar Images", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.upload_button = ttk.Button(self.button_frame, text="Select Image", command=self.on_upload_button)
        self.upload_button.pack()

        self.result_label = ttk.Label(self.main_frame, text="Results will appear here", anchor="center")
        self.result_label.pack(pady=10)

        self.preview_labelframe = ttk.Labelframe(self.main_frame, text="Similar Images (Threshold: 60%)", style="MyLabelframe.TLabelframe")
        self.preview_labelframe.pack(pady=10, fill=tk.BOTH, expand=True)

        self.preview_frame = ttk.Frame(self.preview_labelframe)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(side=tk.BOTTOM, pady=5)

        self.footer_label = ttk.Label(self.footer_frame, text="Created by Svyatoslav Köning aka Solrikk", anchor="center", font=("Helvetica", 8), foreground="#aaaaaa")
        self.footer_label.pack(side=tk.LEFT)

        self.footer_email_label = ttk.Label(self.footer_frame, text="reveni324@gmail.com", anchor="center", font=("Helvetica", 8, "underline"), foreground="#aaaaaa", cursor="hand2")
        self.footer_email_label.pack(side=tk.LEFT, padx=10)
        self.footer_email_label.bind("<Button-1>", self.on_email_click)

    def create_navigation(self):
        nav_buttons = [
            ("Home", self.show_home),
            ("Internet Search", self.internet_search),
            ("Folder Search", self.folder_search),
            ("About Us", self.about_us)
        ]

        for (text, command) in nav_buttons:
            btn = ttk.Button(self.nav_frame, text=text, command=command, style="Nav.TButton")
            btn.pack(side=tk.LEFT, padx=10, pady=10)

    def show_home(self):
        self.main_frame.lift()
        self.result_label.config(text="Results will appear here")
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

    def internet_search(self):
        messagebox.showinfo("Internet Search", "Internet Search functionality is not implemented yet.")

    def folder_search(self):
        messagebox.showinfo("Folder Search", "Folder Search functionality is not implemented yet.")

    def about_us(self):
        messagebox.showinfo("About Us", "PicTrace v1.0\nDeveloped by Svyatoslav Köning aka Solrikk\nContact: revi324@gmail.com")

    def on_email_click(self, event):
        webbrowser.open("mailto:reveni324@gmail.com")

    def on_upload_button(self):
        file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if not file_path:
            return
        try:
            uploaded_image = Image.open(file_path).convert('RGB')
        except UnidentifiedImageError:
            messagebox.showerror("Error", "File is not a valid image")
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.result_label.config(text="Searching for similar images (threshold 60%)...")
        self.root.update_idletasks()

        similar_images = find_similar_images(uploaded_image)
        if similar_images:
            result_text = "Similar images found (similarity ≥ 60%):\n"
            for img_name, sim_val in similar_images:
                result_text += f"- {img_name} (similarity: {sim_val:.2f})\n"
            self.result_label.config(text=result_text)
        else:
            self.result_label.config(text="No matching images found.")

        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        for img_name, sim_val in similar_images:
            full_path = os.path.join(UPLOAD_FOLDER, img_name)
            if os.path.exists(full_path):
                img_pil = Image.open(full_path).resize((150, 150), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img_pil)
                preview_label = ttk.Label(self.preview_frame, image=img_tk)
                preview_label.image = img_tk
                preview_label.pack(side=tk.LEFT, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PicTraceApp(root)
    root.mainloop()
