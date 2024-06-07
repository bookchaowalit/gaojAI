from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import MetadataFilter, MetadataFilters
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

from utilities.constants import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, VECTOR_DB_NAME
from utilities.logs import (
    database_config_logs,
    embedding_config_logs,
    retrieval_filter_logs,
)


def _init_vector_store(
    table_name: str,
    dimension: int = 1024,
    hybrid_search: bool = False,
    text_search_config: str = "english",
):
    """
    Initialize a vector store with the given table name and dimension.

    Args:
        table_name (str): The name of the table in the database.
        dimension (int, optional): The dimension of the vectors to be stored. The dimension is dependent on the model used. Defaults to 1536.
        hybrid_search (bool, optional): Flag indicating whether to enable hybrid search. Defaults to False.
        text_search_config (str, optional): The text search configuration to be used. Defaults to "english".

    Returns:
        PGVectorStore
    """

    @database_config_logs
    def _vector_store(**kwargs):
        return PGVectorStore.from_params(**kwargs)

    return _vector_store(
        database=VECTOR_DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        table_name=table_name,
        embed_dim=dimension,
        hybrid_search=hybrid_search,
        text_search_config=text_search_config,
    )


def _init_vector_store(
    table_name: str,
    dimension: int = 1024,
    hybrid_search: bool = False,
    text_search_config: str = "english",
):
    @database_config_logs
    def _vector_store(**kwargs):
        return PGVectorStore.from_params(**kwargs)

    return _vector_store(
        database=VECTOR_DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        table_name=table_name,
        embed_dim=dimension,
        hybrid_search=hybrid_search,
        text_search_config=text_search_config,
    )


def _get_embedding(model, device="cpu"):
    """
    Get the HuggingFace embedding.

    Returns:
        HuggingFace Embedding with the preset embedding model.
    """

    @embedding_config_logs
    def _embedding(**kwargs):
        return HuggingFaceEmbedding(**kwargs)

    return _embedding(
        model_name=model["name"],
        max_length=model["tensor_size"],
        device=device,
    )


def insert_nodes(nodes, table_name, model):
    """
    Nodes into Vector

    Returns:
        None
    """
    # Vector DB Initialization
    embed_model = _get_embedding(model)
    vector_store = _init_vector_store(table_name, model["dimensions"])
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Index Nodes into Vector DB
    VectorStoreIndex(
        nodes,
        embed_model=embed_model,
        storage_context=storage_context,
        # show_progress=True,
    )


def upsert_pinecone(nodes, table_name, model):
    """
    Nodes into Vector

    Returns:
        None
    """
    # Vector DB Initialization
    embed_model = _get_embedding(model)
    pc = Pinecone(api_key=api_key)
    pc.create_index(
        name="quickstart",
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    )
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    # vector_store = _init_vector_store(table_name, model["dimensions"])
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Index Nodes into Vector DB
    VectorStoreIndex(
        nodes,
        embed_model=embed_model,
        storage_context=storage_context,
        # show_progress=True,
    )


def get_retriver(model, table_name, filters):
    embed_model = _get_embedding(model)
    vector_store = _init_vector_store(table_name, model["dimensions"])

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )

    @retrieval_filter_logs
    def _run_retriever(index, filters):
        retriever = index.as_retriever(
            similarity_top_k=100,
            filters=filters,
        )
        return retriever

    return _run_retriever(index=index, filters=filters)


def get_chat_engine(model, table_name, filters):
    embed_model = _get_embedding(model)
    vector_store = _init_vector_store(table_name, model["dimensions"])

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )

    @retrieval_filter_logs
    def _run(index, filters):
        retriever = index.as_chat(
            similarity_top_k=100,
            filters=filters,
        )
        return retriever

    return _run(index=index, filters=filters)


def create_node(text: str, **kwargs):
    return TextNode(
        text=text,
        **kwargs,
        # metadata={"created_at": "2024-04-29T12:00:00Z"},
        # excluded_llm_metadata_keys=["created_at"],
        # excluded_embed_metadata_keys=[],
        # metadata_seperator="::",
        # metadata_template="{key}=>{value}",
        # text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
    )


def create_filters(user_filters, condition="and"):
    """
    EQ = "=="  # default operator (string, int, float)
    GT = ">"  # greater than (int, float)
    LT = "<"  # less than (int, float)
    NE = "!="  # not equal to (string, int, float)
    GTE = ">="  # greater than or equal to (int, float)
    LTE = "<="  # less than or equal to (int, float)
    IN = "in"  # metadata in value array (string or number)
    NIN = "nin"  # metadata not in value array (string or number)
    TEXT_MATCH = "text_match"  # full text match (allows you to search for a specific substring, token or phrase within the text field)
    CONTAINS = "contains"  # metadata array contains value (string or number)
    """
    filters = []

    for key, value in user_filters.items():
        formatted_value = value.get("value", "")

        if isinstance(formatted_value, str):
            formatted_value = formatted_value
        elif isinstance(formatted_value, list):
            formatted_value = sorted([item.strip() for item in formatted_value])
            formatted_value = "|".join(formatted_value)

        filters.append(
            MetadataFilter(
                key=key,
                value=formatted_value,
                operator=value.get("operator", "=="),
            )
        )

    return MetadataFilters(filters=filters, condition=condition)


def create_nodes_retriver(model, nodes):
    embed_model = _get_embedding(model)
    index = VectorStoreIndex(nodes, embed_model=embed_model)
    retriever = index.as_retriever(similarity_top_k=20)
    return retriever
