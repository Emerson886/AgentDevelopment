"""
RAG 知识问答（检索增强生成）实现。

- 向量数据库: Milvus（COSINE 度量，EMBED_DIM 维）
- 嵌入模型: BGE-M3（经 SiliconFlow API 调用，配置见 .env）
- 分块: RecursiveCharacterTextSplitter（chunk_size=200, chunk_overlap=80）

职责划分:
    - 一次性建库/入库: 由独立脚本 build_rag_index.py 完成
      （python build_rag_index.py，会重建 collection 并写入 knowledge.txt 的向量）；
    - 运行时: 本类只负责 init_embedding_model() 与 retrieve()/generate_context()。
"""
from pymilvus import MilvusClient

import os
from pathlib import Path
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


MILVUS_URI = "http://localhost:19530"
DB_NAME = "rag_PCB"
COLLECTION_NAME = "docs"
KNOWLEDGE_FILE = "./knowledge.txt"
EMBED_MODEL_NAME = "Pro/BAAI/bge-m3"
EMBED_DIM = 1024

class RAG:
    def __init__(self):
        self.client = MilvusClient(MILVUS_URI)
        self.embedding_model = None

    def create_db(self):
        # 查找指定数据库，如果没有则创建
        existing_dbs = self.client.list_databases()
        if DB_NAME not in existing_dbs:
            self.client.create_database(DB_NAME)

    def create_collection(self):
        # 切换到当前数据库
        self.client.use_database(db_name=DB_NAME)

        # 查看是否有已存在同名collection，有则删除
        if self.client.has_collection(collection_name=COLLECTION_NAME):
            self.client.drop_collection(collection_name=COLLECTION_NAME)

        # 创建collection
        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            dimension=EMBED_DIM,
            metric_type="COSINE"
        )

    def init_embedding_model(self):
        # 初始化向量模型
        self.embedding_model = init_embeddings(
            model="openai:Pro/BAAI/bge-m3",
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url=os.getenv("SILICONFLOW_BASE_URL"),
        )

    def init_milvus_data(self):
        # 加载本地文档
        loader = TextLoader(KNOWLEDGE_FILE, encoding="utf-8")
        documents = loader.load()

        # 设置分隔符
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=80,
            separators=[
                "\n==============================\n",
                "\n\n",
                "\n",
                "。",
                "，",
                " ",
                ""
            ]
        )

        chunks = splitter.split_documents(documents)

        # 生成向量写入Milvus
        vectors = self.embedding_model.embed_documents([chunk.page_content for chunk in chunks])

        # 构建Milvus数据行格式
        data = [
            {
                "id": i,
                "vector": vectors[i],
                "text": chunks[i].page_content,
                "source": KNOWLEDGE_FILE,
                "chunk_id": i
            } for i in range(len(chunks))
        ]

        # 将数据插入或更新到collection
        upsert_result = self.client.upsert(
            collection_name=COLLECTION_NAME,
            data=data,
        )

        self.client.flush(collection_name=COLLECTION_NAME)


    def retrieve(self, input_text: str, limit: int = 5):
        """向量数据库检索工具

        Args:
            input_text: 输入文本
            limit: 限制返回相似文本的检索数
        """

        query_vector = self.embedding_model.embed_query(input_text)
        self.client.use_database(db_name=DB_NAME)
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            data=[query_vector],
            limit=limit,
            output_fields=["id", "vector", "text", "source", "chunk_id"],
        )

        return results[0]

    def generate_context(self, question: str):
        hits = self.retrieve(question, limit=5)
        context_blocks = []
        for i, hit in enumerate(hits):
            text = hit["entity"]["text"]
            source = hit["entity"].get("source", "unknown")
            chunk_id = hit["entity"].get("chunk_id", "unknown")
            score = hit["distance"]
            context_blocks.append(f"片段{i}: chunk_id: {chunk_id}, source: {source} \n text: {text}")

        context = '\n\n'.join(context_blocks)
        return context