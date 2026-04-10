import json
import os

path = "d:/GenAI/medical-chatbot/trails.ipynb"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for cell in data.get("cells", []):
    if cell["cell_type"] == "code":
        new_source = []
        for line in cell.get("source", []):
            if "from langchain.embeddings import HuggingFaceEmbeddings" in line:
                new_source.append("from langchain_community.embeddings import HuggingFaceEmbeddings\n")
            elif "from langchain.vectorstores import Pinecone" in line:
                new_source.append("from langchain_pinecone import PineconeVectorStore\n")
            elif "from langchain.document_loaders import PyMuPDFLoader, DirectoryLoader" in line:
                new_source.append("from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader\n")
            elif "from langchain.llms import CTransformers" in line:
                new_source.append("from langchain_community.llms import CTransformers\n")
            elif "from pinecone import Pinecone" in line:
                pass
            else:
                new_source.append(line)
        cell["source"] = new_source

        # check if it is the pinecone init cell
        if any("pinecone.init" in line for line in cell["source"]):
            cell["source"] = [
                "\n",
                "import os\n",
                "os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY\n",
                "\n",
                "docsearch = PineconeVectorStore.from_texts(\n",
                "    [t.page_content for t in text_chunks],\n",
                "    embeddings,\n",
                "    index_name=\"medical-chatbot\"\n",
                ")"
            ]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1)

print("Notebook patched successfully!")
