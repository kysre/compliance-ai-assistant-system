import asyncio
import os

import nest_asyncio
from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.llm.llama_index_impl import (
    llama_index_complete_if_cache,
    llama_index_embed,
)
from lightrag.utils import EmbeddingFunc
from llama_index.embeddings.litellm import LiteLLMEmbedding
from llama_index.llms.litellm import LiteLLM

nest_asyncio.apply()


GRAPH_RAG_MODES = ["naive", "local", "global", "hybrid"]


class GraphRagService:
    def __init__(self):
        # Model configuration
        self.llm_model = os.environ.get("LLM_MODEL", "gpt-4o")
        self.embedding_model = os.environ.get(
            "EMBEDDING_MODEL", "text-embedding-3-large"
        )
        self.embedding_max_token_size = int(
            os.environ.get("EMBEDDING_MAX_TOKEN_SIZE", 8192)
        )
        self.litellm_url = os.environ.get("LITELLM_URL", "http://localhost:4000")
        self.litellm_key = os.environ.get("LITELLM_KEY", "")
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
    ):
        try:
            # Initialize LiteLLM if not in kwargs
            if "llm_instance" not in kwargs:
                llm_instance = LiteLLM(
                    model=f"openai/{self.llm_model}",  # Format: "provider/model_name"
                    api_base=self.litellm_url,
                    api_key=self.litellm_key,
                    temperature=0.7,
                )
            kwargs["llm_instance"] = llm_instance
            response = await llama_index_complete_if_cache(
                kwargs["llm_instance"],
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                **kwargs,
            )
            return response
        except Exception as e:
            print(f"LLM request failed: {str(e)}")
            raise

    # Initialize embedding function
    async def embedding_func(self, texts):
        try:
            embed_model = LiteLLMEmbedding(
                model_name=f"openai/{self.embedding_model}",
                api_base=self.litellm_url,
                api_key=self.litellm_key,
            )
            return await llama_index_embed(texts, embed_model=embed_model)
        except Exception as e:
            print(f"Embedding failed: {str(e)}")
            raise

    # Get embedding dimension
    async def get_embedding_dim(self):
        test_text = ["This is a test sentence."]
        embedding = await self.embedding_func(test_text)
        embedding_dim = embedding.shape[1]
        print(f"embedding_dim={embedding_dim}")
        return embedding_dim

    async def initialize_rag(self):
        embedding_dimension = await self.get_embedding_dim()
        rag = LightRAG(
            working_dir=self.working_dir,
            llm_model_func=self.llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=embedding_dimension,
                max_token_size=self.embedding_max_token_size,
                func=self.embedding_func,
            ),
            kv_storage="PGKVStorage",
            vector_storage="PGVectorStorage",
            graph_storage="Neo4JStorage",
            doc_status_storage="PGDocStatusStorage",
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
