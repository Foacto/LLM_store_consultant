import os
from operator import itemgetter
from langchain.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

# from openai import OpenAI
from langchain_openai import OpenAI

# AI setting
MODEL_PATH = "http://localhost:1234/v1"
TEMPLATE = """
You are a Shop Consultant.
You receive the following user question, corresponding SQL query, and SQL result, answer the user question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """


# Connect to database
DB_USER = 'root'
DB_PASSWORD = '27012001'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'db_demo_market'

class LocalChatAgent:
    def __init__(self):
      self.db = self.connect_to_database()
      self.llm = self.connect_to_openai()
      self.answer_prompt = PromptTemplate.from_template(TEMPLATE)
    
    def connect_to_database(self):
        '''Create a connection to database'''
        print('Connecting to database!')

        return SQLDatabase.from_uri(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    def connect_to_openai(self):
       '''Create a connection to OpenAI model'''
       print('Connecting to OpenAI!')
       
       return OpenAI(base_url=MODEL_PATH, api_key="not-needed")

    def answer(self, question):
       '''Answer the question'''
       self.current_question = question

       execute_query = QuerySQLDataBaseTool(db=self.db)
       write_query = create_sql_query_chain(self.llm, self.db)

       answer = self.answer_prompt | self.llm | StrOutputParser()

       chain = (RunnablePassthrough.assign(query=write_query)
                .assign(result=itemgetter("query") | execute_query) | answer)
       
       
       
       return chain.invoke({"question": self.current_question})
