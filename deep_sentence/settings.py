import inspect
import os
from os import path

from dotenv import load_dotenv


def try_load_dotenv():
    dot_env_path = path.join(PROJECT_ROOT, '.env')
    if path.isfile(dot_env_path):
        load_dotenv(dot_env_path)


APP_NAME = 'deep_sentence'
ENV = os.environ.get('DEEP_SENTENCE_ENV', 'dev')
PROJECT_ROOT = os.environ.get('PROJECT_ROOT',
                              path.dirname(path.dirname(inspect.getfile(inspect.currentframe()))))

try_load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://localhost/deep_sentence_dev')
HTML_EXTRACTOR_BASE_URL = os.environ.get('HTML_EXTRACTOR_BASE_URL',
                                         'http://extractor.deepsentence.com')
HTML_EXTRACTOR_URL = path.join(HTML_EXTRACTOR_BASE_URL, 'extract')

HTML_EXTRACTOR_CREDENTIALS = (
    os.environ.get('HTML_EXTRACTOR_USER', 'deep_sentence'),
    os.environ.get('HTML_EXTRACTOR_PASSWORD', ''),
)

DEFAULT_LANGUAGE = 'japanese'

FIXTURES_PATH = path.join(PROJECT_ROOT, 'deep_sentence', 'fixtures')

WORD_EMBEDDINGS_URL = 'http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/entity_vector.tar.bz2'

ABSTRACTIVE_DATA_URL = 'https://dl.dropboxusercontent.com/s/2b1o9eh82t92ieo/abstractive-data.tar.gz'
ABSTRACTIVE_TRAINED_URL = 'https://dl.dropboxusercontent.com/s/9cfs3ifmfrvbhvc/abtractive-trained.tar.gz'

MODELS_PATH = os.environ.get('MODELS_PATH', path.join(PROJECT_ROOT, 'models'))

GOOGLE_API_CREDENTIALS = path.join(PROJECT_ROOT, 'google-api.json')

GPU_NUMBER = None
