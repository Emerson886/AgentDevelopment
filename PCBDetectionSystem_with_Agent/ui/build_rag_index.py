# -*- coding: utf-8 -*-
"""
一次性建库脚本：知识文档分块 → 向量化 → 写入 Milvus。

用法:
    python build_rag_index.py          # 在 ui/ 目录下运行

前置条件:
    - 本地 Milvus 已启动（默认 http://localhost:19530）；
    - ui/.env 已配置 SILICONFLOW_API_KEY / SILICONFLOW_BASE_URL；
    - knowledge.txt 为知识库源文件（与 RAG.py 中 KNOWLEDGE_FILE 一致）。

说明:
    - 每次运行会重建 rag_PCB/docs 集合（drop + create + upsert），
      知识库内容更新后重新执行本脚本即可；
    - 运行时（AnswerAgent 问答）只做检索，不再触发建库。
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

UI_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(UI_DIR))
load_dotenv(UI_DIR / ".env")     # 显式加载 ui/.env，与启动目录无关

from RAG import RAG, DB_NAME, COLLECTION_NAME, KNOWLEDGE_FILE  # noqa: E402


def main() -> None:
    rag = RAG()

    print("[1/4] 创建/切换数据库 ...")
    rag.create_db()

    print("[2/4] 重建 collection ...")
    rag.create_collection()

    print("[3/4] 初始化嵌入模型 ...")
    rag.init_embedding_model()

    print(f"[4/4] 分块并写入 {KNOWLEDGE_FILE} ...")
    rag.init_milvus_data()

    print(f"完成：{DB_NAME}/{COLLECTION_NAME} 已就绪，可启动系统使用 RAG 问答。")


if __name__ == "__main__":
    main()
