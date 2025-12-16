
import os
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()


class OMSConfigs:
    def __init__(self):
        # Database settings
        oms_host = os.getenv("OMS_DATABASE_HOST", "host.docker.internal")
        oms_port = os.getenv("OMS_DATABASE_PORT", "5432")
        oms_name = os.getenv("OMS_DATABASE_NAME", "oms_db")
        oms_user = os.getenv("OMS_DATABASE_USER", "user")
        oms_password = os.getenv("OMS_DATABASE_PASSWORD", "password")

        default_db_url = f"postgresql://{oms_user}:{oms_password}@{oms_host}:{oms_port}/{oms_name}"

        self.DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)
        self.DATABASE_READ_URL = os.getenv("DATABASE_READ_URL", self.DATABASE_URL)

        # Redis settings
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.REDIS_CACHE_DB = int(os.getenv("REDIS_CACHE_DB", "3"))
        self.FIREBASE_AUTH_CACHE_ENABLED = os.getenv("FIREBASE_AUTH_CACHE_ENABLED", "true").lower() == "true"
        self.FIREBASE_AUTH_CACHE_TTL_SECONDS = int(os.getenv("FIREBASE_AUTH_CACHE_TTL_SECONDS", "300"))
        self.FIREBASE_AUTH_CACHE_PREFIX = os.getenv("FIREBASE_AUTH_CACHE_PREFIX", "firebase:id_token")
        self.SAFETY_QUANTITY = int(os.getenv("SAFETY_QUANTITY", "10"))

        # Product validation flags
        self.PRICE_CHECK_ENABLED = os.getenv("PRICE_CHECK_ENABLED", "true").lower() == "true"

        # RTO threshold to disable COD (app channel only)
        self.COD_DISABLE_RTO_THRESHOLD = int(os.getenv("COD_DISABLE_RTO_THRESHOLD"))

        # Typesense settings
        self.TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "localhost")
        self.TYPESENSE_PORT = os.getenv("TYPESENSE_PORT", "8108")
        self.TYPESENSE_PROTOCOL = os.getenv("TYPESENSE_PROTOCOL", "http")
        self.TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY", "")
        self.TYPESENSE_COLLECTION_NAME = os.getenv("TYPESENSE_COLLECTION_NAME", "facility_products")
        self.TYPESENSE_FREEBIES_COLLECTION_NAME = os.getenv("TYPESENSE_FREEBIES_COLLECTION_NAME", "freebies_products")
        self.TYPESENSE_INDEX_SIZE = int(os.getenv("TYPESENSE_INDEX_SIZE", "10"))
