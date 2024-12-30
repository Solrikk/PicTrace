import logging
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import spacy
import dateparser
from utils import get_ip_address

class ImageMatcher:
    def __init__(self):
        logging.info("Loading ResNet50 model...")
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        logging.info("Loading spaCy model...")
        try:
            self.nlp = spacy.load("ru_core_news_sm")
        except OSError:
            logging.info("spaCy model 'ru_core_news_sm' not found. Downloading...")
            from spacy.cli import download
            download("ru_core_news_sm")
            self.nlp = spacy.load("ru_core_news_sm")
        logging.info("Initializing TF-IDF vectorizer...")
        self.vectorizer = TfidfVectorizer(max_features=10, stop_words='russian')

    def preprocess_image(self, img_path):
        try:
            if isinstance(img_path, str):
                img = image.load_img(img_path, target_size=(224, 224))
            else:
                img = img_path.resize((224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            return preprocess_input(x)
        except Exception as e:
            logging.warning(f"Error during image preprocessing: {str(e)}")
            return None

    def get_embedding(self, img):
        try:
            preprocessed = self.preprocess_image(img)
            if preprocessed is not None:
                return self.model.predict(preprocessed, verbose=0)
            return None
        except Exception as e:
            logging.warning(f"Error obtaining embedding: {str(e)}")
            return None

    def compare_images(self, embedding1, embedding2):
        try:
            similarity = 1 - cosine(embedding1.flatten(), embedding2.flatten())
            return similarity
        except Exception as e:
            logging.warning(f"Error comparing images: {str(e)}")
            return 0.0

    def download_and_process_image(self, url):
        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert('RGB')
            return self.get_embedding(img)
        except Exception as e:
            logging.warning(f"Error processing URL {url}: {str(e)}")
            return None

    def fetch_page_text(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            texts = soup.stripped_strings
            return ' '.join(texts)
        except Exception as e:
            logging.warning(f"Error fetching page {url}: {str(e)}")
            return ""

    def generate_title(self, text):
        try:
            if '—' in text:
                title = text.split('—')[0].strip()
            else:
                title = text.strip()
            if not title:
                logging.warning("Title is empty after extraction.")
                return None
            logging.info(f"Extracted title: {title}")
            return title
        except Exception as e:
            logging.warning(f"Error generating title: {str(e)}")
            return None

    def extract_image_info(self, soup, image_url):
        try:
            img_tags = soup.find_all('img', src=image_url)
            for img in img_tags:
                title = img.get('title')
                alt = img.get('alt')
                if title:
                    return title
                if alt:
                    return alt
            return None
        except:
            return None

    def parse_footer(self, soup):
        footer = soup.find('footer')
        if not footer:
            footer = soup.find(id="footer-wrapper")
        if not footer:
            logging.warning("Footer not found.")
            return {}
        footer_info = {}
        menu = footer.find('nav')
        if menu:
            links = menu.find_all('a')
            footer_info['menu_links'] = {link.text.strip(): link.get('href') for link in links}
        phones = footer.find_all('a', href=True)
        phone_numbers = [phone.get_text().strip() for phone in phones if phone['href'].startswith('tel:')]
        footer_info['phone_numbers'] = phone_numbers
        privacy = footer.find('a', href=lambda x: x and 'privacy' in x.lower())
        oferta = footer.find('a', href=lambda x: x and 'oferta' in x.lower())
        footer_info['privacy_policy'] = privacy.get('href') if privacy else None
        footer_info['public_offer'] = oferta.get('href') if oferta else None
        developer = footer.find('div', class_='developer')
        if developer:
            dev_link = developer.find('a', href=True)
            footer_info['developer'] = {'name': dev_link.text.strip(),
                                        'url': dev_link.get('href')} if dev_link else None
        return footer_info

    def find_and_parse_images(self, soup, driver):
        image_info_list = []
        image_tags = soup.find_all('img')
        for img in image_tags:
            img_src = img.get('src')
            if img_src:
                full_img_url = requests.compat.urljoin(driver.current_url, img_src)
                image_info = {'src': full_img_url, 'alt': img.get('alt'), 'title': img.get('title')}
                image_info_list.append(image_info)
        return image_info_list

    def extract_footer_text(self, soup):
        footer = soup.find('footer')
        if not footer:
            footer = soup.find(id="footer-wrapper")
        if not footer:
            logging.warning("Footer not found for text extraction.")
            return ""
        texts = footer.stripped_strings
        return ' '.join(texts)

    def extract_publication_date(self, soup):
        try:
            meta_date = soup.find('meta', attrs={'property': 'article:published_time'})
            if meta_date and meta_date.get('content'):
                return meta_date.get('content')
            for tag in soup.find_all(['span', 'div', 'p']):
                text = tag.get_text(strip=True)
                date = dateparser.parse(text, languages=['ru'])
                if date:
                    return date.isoformat()
            return None
        except Exception as e:
            logging.warning(f"Error extracting publication date: {str(e)}")
            return None

    def generate_important_info(self, footer_text):
        try:
            doc = self.nlp(footer_text)
            entities = [ent.text for ent in doc.ents]
            important_info = ', '.join(set(entities))
            return important_info if important_info else None
        except Exception as e:
            logging.warning(f"Error generating important information: {str(e)}")
            return None
