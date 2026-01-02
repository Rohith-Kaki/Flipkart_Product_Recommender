from langchain_groq import ChatGroq
# from langchain.chains.history_aware_retriever import createHistoryAwareRetriever
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory #includes the chat history in rag-pipeline
from langchain_community.chat_message_histories import ChatMessageHistory #responsible for forming the message history
from langchain_core.chat_history import BaseChatMessageHistory #responsible for forming the message history
from flipkart.config import Config

class RagChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)
        self.history_store = {} #store history of all sessions

    #private method
    def _get_history(self, session_id:str) -> BaseChatMessageHistory:
    #relation between BaseChatMessageHistory and ChatMessageHistory are Datatype and value (IN VAGUE TERMS)
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory() #creates a new chat history
        return self.history_store[session_id] #return chat history of particular session_id
    
    def build_chain(self):
        #convert vectorstore into retriever
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3}) #retrieve top 3 matches
        context_prompt = ChatPromptTemplate([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        qa_prompt = ChatPromptTemplate([
            ("system", """ You're an e-commerce bot answering product-related quries using reviews and titles.
                            Stick to the content. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION:{input}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])    

        #retriever for chat_history
        history_aware_retriever = create_history_aware_retriever(
            self.model, retriever, context_prompt
        )
        question_answer_chain = create_stuff_documents_chain(
            self.model, qa_prompt
        )
    
        #combine the history_aware_retriever and question_answer_chain to create the rag model
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )