from api.chains.clean_texts_from_url_chain import create_clean_texts_from_url_chain
from langchain_core.runnables.base import RunnableSequence
from typing import List
from langchain.chat_models.base import  BaseChatModel
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.web import SimpleWebPageReader
from langchain.chat_models import ChatOpenAI


class DocumentRefiner:
    def __init__(self, llm: BaseChatModel,
                 chunk_size:int = 3000, 
                 chunk_overlap:int = 0):
        self.chain = create_clean_texts_from_url_chain(llm)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_sentence_splitter(self):
        return SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def refine_html_files(self, docs: List[Document]) -> List[Document]:
        cleaned_docs = []
        splitter = self.get_sentence_splitter()
        for doc in docs:
            cleaned_doc_segments = ""
            doc_segments = splitter.get_nodes_from_documents([doc])

            for seg in doc_segments:
                try:
                    response = self.chain.invoke({"question": seg.text})
                    cleaned_doc_segments += response + "\n"
                except Exception as e:
                    print(f"Error processing segment: {e}")

            doc.text = cleaned_doc_segments
            cleaned_docs.append(doc)

        return cleaned_docs



class WebPagesToDocuments:
    def __init__(self, path: str,
                 llm: BaseChatModel = ChatOpenAI(temperature=0, model_name = "gpt-3.5-turbo", streaming = True),
                 clean_texts: bool = False,
                 chunk_size:int = 3000,
                 chunk_overlap:int = 0):
        self.path = path
        self.clean_texts = clean_texts
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.llm = llm
        self.docs = self.get_all_documents_from_url_file()
    
    def get_document_from_url(self, url:str) -> Document:
        doc = SimpleWebPageReader(html_to_text=True).load_data(
        [url])[0]
        doc.metadata['doc_id'] = doc.doc_id
        return doc
        
    def get_all_documents_from_url_file(self) -> List[Document]:
        docs = []
        with open(self.path) as file:
            urls = file.read().splitlines()
        for url in urls:
            docs.append(self.get_document_from_url(url))
        
        if self.clean_texts:
            text_cleaner = DocumentRefiner(self.llm, chunk_size= self.chunk_size,
                                   chunk_overlap=self.chunk_overlap)
            docs = text_cleaner.refine_html_files(docs)
        return docs
    

