from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Create AI Models
llm = ChatOpenAI()
embeddings = OpenAIEmbeddings()

# Index vector store
documents = ...
vector_store = FAISS.from_documents(documents, embeddings)

# Create prompt
prompt = ChatPromptTemplate.from_template("""
Answer the following question based on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Create a chain
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(vector_store.as_receiver(), document_chain)

# Send request
response = retrieval_chain.invoke({"input": "Lorem ipsum?"})
print(response["answer"])
