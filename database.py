# database.py
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

LANCEDB_PATH = "./lancedb"
COLLECTION_NAME = "knowledge_vectors"

model = get_registry().get("colbert").create(name="colbert-ir/colbertv2.0")

class TextModel(LanceModel):
    key: str
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()

db = None

def get_db():
    global db
    if db is not None:
        return db
    db = lancedb.connect(LANCEDB_PATH)
    return db

def get_table():
    db = get_db()
    available_tables = db.table_names()
    if COLLECTION_NAME not in available_tables:
        db.create_table(COLLECTION_NAME, schema=TextModel)
    table = db.open_table(COLLECTION_NAME)
    return table

def create_entry(key, text, upsert=False):
    table = get_table()
    result = find_by_key(key)
    if len(result) > 0 and not upsert:
        return None, f"Key '{key}' already exists."
    
    entry = {
        "key": key,
        "text": text
    }
    
    if upsert and len(result) > 0:
        delete_entry(key)
    
    table.add([entry])
    return entry, None

def delete_entry(key):
    get_table().delete(f"key == '{key}'")


def find_by_key(key):
    table = get_table()
    result = table.search().where(f"key == '{key}'").to_pydantic(TextModel)
    return result

def find_by_text(text):
    table = get_table()
    result = table.search(text).limit(1).to_pydantic(TextModel)
    return result

