import json


def load_db():
  try:
    with open("images.json", "r") as file:
      return json.load(file)
  except FileNotFoundError:
    return []


def save_db(data):
  with open("images.json", "w") as file:
    json.dump(data, file, indent=4)


def add_image_to_db(file_path, image_hash):
  db_data = load_db()
  if isinstance(db_data, list):
    db_data.append({"file_path": file_path, "hash": image_hash})
    save_db(db_data)


def init_db():
  db_data = load_db()
  if not isinstance(db_data, list):
    db_data = []
    save_db(db_data)
