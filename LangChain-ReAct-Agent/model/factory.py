import sys
import os

# 添加当前项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.embeddings import Embeddings
from langchain_core.caches import BaseCache
from langchain_core.callbacks import Callbacks
from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseLanguageModel]:
        pass





class ChatModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings | BaseLanguageModel]:
        # 使用自定义的简单聊天模型，不需要 API 密钥
        return SimpleChatModel()


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseLanguageModel]:
        # 使用自定义的简单嵌入模型，不需要 API 密钥
        return SimpleEmbeddings()


chat_model = ChatModelFactory().generator()

embed_model = EmbeddingsFactory().generator()
