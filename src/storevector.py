from utilities.constants import (
    HF_EMBED_MODELS,
)
from llama_index.core import Document, SimpleDirectoryReader
from utilities.vector import insert_nodes
from llama_index.core.node_parser import SentenceSplitter


def store_pdf():
    text = []
    documents = SimpleDirectoryReader("./data").load_data()
    for doc in documents:
        text.append(doc.text)

    splitter = SentenceSplitter(
        chunk_size=4096,
        chunk_overlap=250,
    )
    for txt in text:
        nodes = splitter.get_nodes_from_documents(
            [
                Document(
                    text=txt,
                    metadata={
                        "data_source": "pdf",
                    },
                )
            ],
            show_progress=True,
        )
        model = HF_EMBED_MODELS["MULTILINGUAL"]
        print("test")
        insert_nodes(nodes, "pdf_file", model)


store_pdf()
