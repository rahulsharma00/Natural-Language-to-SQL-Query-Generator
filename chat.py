import os 
os.environ['OPENAI_API_KEY'] = "YOUR API KEY"
from langchain_core.prompts import ChatPromptTemplate

template = """
    Based on the table schema below, write a SQL query that would answer the users question: {schema}

    Question: {question}
    SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)
# prompt.format(schema="my schema", question = "how many users are there?")
from langchain_community.utilities import SQLDatabase

db_uri = "mysql+mysqlconnector://root:Pitbull%402000@localhost:3306/Chinook"
db = SQLDatabase.from_uri(db_uri)
# db.run('SELECT * FROM Album LIMIT 5')
def get_schema(_):
    return db.get_table_info()

from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt 
    | llm.bind(stop = "\nSQL Result:")
    | StrOutputParser()
)   

# sql_chain.invoke({"question":"how many albumid are there?"})
template = """
Based on the table schema below, question, sql query, and sql response, write natural language response: 
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
"""

prompt = ChatPromptTemplate.from_template(template)
def run_query(query):
    return db.run(query)
# run_query('SELECT COUNT(AlbumId) AS TotalAlbums FROM Album;')
full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response=lambda vars: run_query(vars["query"]),
    )
    | prompt
    | llm

)

result = full_chain.invoke({"question": "how many albums are there in the database?"})
print(result.content)