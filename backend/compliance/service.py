import asyncio
import os

import nest_asyncio
import numpy as np
from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.llm.openai import openai_complete_if_cache
from lightrag.utils import EmbeddingFunc
from openai import OpenAI

nest_asyncio.apply()


GRAPH_RAG_MODES = ["naive", "local", "global", "hybrid"]


class GraphRagService:
    def __init__(self):
        # Embedding configuration
        self.embedding_model = os.environ.get(
            "EMBEDDING_MODEL", "text-embedding-3-large"
        )
        self.embedding_dimensions = int(os.environ.get("EMBEDDING_DIM", 3072))
        self.embedding_max_token_size = int(
            os.environ.get("EMBEDDING_MAX_TOKEN_SIZE", 8192)
        )
        self.embedding_base_url = os.environ.get(
            "EMBEDDING_BASE_URL", "https://api.openai.com/v1"
        )
        self.embedding_api_key = os.environ.get("EMBEDDING_API_KEY", "")
        # LLM Model configuration
        self.llm_model = os.environ.get("LLM_MODEL", "gpt-4.1-mini")
        self.llm_base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self.llm_api_key = os.environ.get("LLM_API_KEY", "")
        self.working_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "data",
            "index",
            f"{self.embedding_model}",
        )
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir, exist_ok=True)

    # Initialize LLM function
    async def llm_model_func(
        self, prompt, system_prompt=None, history_messages=[], **kwargs
    ) -> str:
        return await openai_complete_if_cache(
            self.llm_model,
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=self.llm_api_key,
            base_url=self.llm_base_url,
            **kwargs,
        )

    # Initialize embedding function
    async def embedding_func(self, texts):
        client = OpenAI(
            base_url=self.embedding_base_url,
            api_key=self.embedding_api_key,
        )
        embedding = client.embeddings.create(
            model=self.embedding_model,
            input=texts,
            dimensions=self.embedding_dimensions,
        )
        embeddings = [item.embedding for item in embedding.data]
        return np.array(embeddings)

    async def initialize_rag(self):
        rag = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=self.llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=self.embedding_dimensions,
                max_token_size=self.embedding_max_token_size,
                func=self.embedding_func,
            ),
            kv_storage="PGKVStorage",
            vector_storage="ChromaVectorDBStorage",
            graph_storage="Neo4JStorage",
            doc_status_storage="PGDocStatusStorage",
            vector_db_storage_cls_kwargs={
                "host": "localhost",
                "port": 8000,
                "cosine_better_than_threshold": 0.2,
                "auth_token": "token",
                "auth_header_name": "X-Chroma-Token",
                "auth_provider": "chromadb.auth.token_authn.TokenAuthClientProvider",
            },
        )
        await rag.initialize_storages()
        await initialize_pipeline_status()
        return rag


graph_rag_service = None


def get_graph_rag_service():
    global graph_rag_service
    if graph_rag_service is None:
        graph_rag_service = GraphRagService()
        graph_rag_service = asyncio.run(graph_rag_service.initialize_rag())
    return graph_rag_service
