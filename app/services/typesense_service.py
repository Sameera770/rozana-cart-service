from typing import Dict, Optional
import httpx
from httpx_retry import AsyncRetryTransport, RetryPolicy
from fastapi import HTTPException

# Logger
from app.logging.utils import get_app_logger
logger = get_app_logger('typesense_service')

# Settings
from app.config.settings import OMSConfigs
configs = OMSConfigs()

TYPESENSE_API_KEY = configs.TYPESENSE_API_KEY
TYPESENSE_HOST = configs.TYPESENSE_HOST
TYPESENSE_PORT = configs.TYPESENSE_PORT
TYPESENSE_PROTOCOL = configs.TYPESENSE_PROTOCOL
TYPESENSE_COLLECTION_NAME = configs.TYPESENSE_COLLECTION_NAME
TYPESENSE_FREEBIES_COLLECTION_NAME = configs.TYPESENSE_FREEBIES_COLLECTION_NAME
TYPESENSE_INDEX_SIZE = configs.TYPESENSE_INDEX_SIZE


class TypesenseService:

    def __init__(self):
        self.host = TYPESENSE_HOST
        self.port = TYPESENSE_PORT
        self.protocol = TYPESENSE_PROTOCOL
        self.api_key = TYPESENSE_API_KEY
        self.collection_name = TYPESENSE_COLLECTION_NAME
        self.freebies_collection_name = TYPESENSE_FREEBIES_COLLECTION_NAME

        if not self.api_key:
            logger.error("typesense_api_key_missing")
            raise ValueError("TYPESENSE_API_KEY environment variable is required")

        self.base_url = f"{self.protocol}://{self.host}:{self.port}"
        self.headers = {
            "X-TYPESENSE-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        retry_policy = RetryPolicy(
            max_retries=5,
            initial_delay=0.5,
            multiplier=2.0,
            retry_on=[429, 500, 502, 503, 504]
        )
        retry_transport = AsyncRetryTransport(policy=retry_policy)
        self.client = httpx.AsyncClient(transport=retry_transport, timeout=60.0)

    async def close(self):
        await self.client.aclose()

    def _get_bulk_headers(self) -> Dict[str, str]:
        return {
            'X-TYPESENSE-API-KEY': self.api_key,
            'Content-Type': 'text/plain'
        }

    async def make_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        content: Optional[str] = None,
        json_data: Optional[Dict] = None,
        timeout: Optional[float] = None,
        raise_for_status: bool = True
    ) -> httpx.Response:
        try:
            response = await self.client.request(method=method, url=url, headers=headers, params=params, content=content, json=json_data, timeout=timeout)
            if raise_for_status:
                response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [429, 500, 502, 503, 504]:
                logger.error(f"Typesense API: All retries exhausted - HTTP {e.response.status_code} for {method} {url}")
            else:
                logger.error(f"Typesense API: HTTP {e.response.status_code} error for {method} {url}")
            raise
        except Exception as e:
            logger.error(f"Typesense API: Unexpected error for {method} {url}: {str(e)}")
            raise

    def _build_filter_query(self, base_conditions: list, product_filter_conditions: list) -> str:
        if not product_filter_conditions:
            return " && ".join(base_conditions)

        base_filter = " && ".join(base_conditions)
        product_filter = " || ".join(product_filter_conditions)
        return f"{base_filter} && ({product_filter})"

    async def search_documents(self, query_params: Dict[str, str], collection: str = None) -> Dict:
        target_collection = collection or self.collection_name
        url = f"{self.base_url}/collections/{target_collection}/documents/search"

        try:
            response = await self.make_request(method="GET", url=url, headers=self.headers, params=query_params, timeout=60.0)
            return response.json()
        except Exception as e:
            logger.error(f"TYPESENSE_API_ERROR: Error searching documents: {e}")
            raise ValueError(f"Failed to search documents in Typesense: {e}")


