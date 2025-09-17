import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from llama_index.core.query_pipeline import QueryPipeline as QP, Link, InputComponent, CustomQueryComponent
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse
from few_shots import few_shot_examples

#streamlit
import streamlit as st
import random
import time

# Configure database connection
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

# Initiate the LLM 
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

load_dotenv()

api_key = os.environ.get("API_KEY")
db_connection = os.environ.get("DB_CONNECTION")

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

llm = Groq(model="llama3-8b-8192", api_key=api_key) 
Settings.llm = llm

class TableInfo(BaseModel):
    """Information regarding a structured table."""

    table_name: str = Field(
        ..., description="table name (must be underscores and NO spaces)"
    )
    table_summary: str = Field(
        ..., description="short, concise summary/caption of the table"
    )


prompt_str = """\
Give me a summary of the table with the following JSON format.

- The table name must be unique to the table and describe it while being concise. 
- Do NOT output a generic table name (e.g. table, my_table).

Do NOT make the table name one of the following: {exclude_table_name_list}

Table:
{table_str}

Summary: """

program = LLMTextCompletionProgram.from_defaults(
    output_cls=TableInfo,
    llm=llm,
    prompt_template_str=prompt_str,
)

engine = create_engine(db_connection)

# Query untuk mengidentifikasi account_number dengan transaksi terbanyak
query = """
SELECT account_number, COUNT(*) AS transaction_count
FROM transactions_dummy
GROUP BY account_number 
ORDER BY transaction_count DESC
LIMIT 1;
"""

# Mengambil account_number dengan transaksi terbanyak
with engine.connect() as connection:
    result = connection.exec_driver_sql(query)
    top_account = result.fetchone()[0]
    
print(f"The account number with the most transactions is: {top_account}")

top_account_number = top_account

# Schema table
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import SQLDatabase, VectorStoreIndex

sql_database = SQLDatabase(engine)

table_node_mapping = SQLTableNodeMapping(sql_database) 
# add a SQLTableSchema for each table
table_schema_objs = [ 
    SQLTableSchema(table_name=t.table_name, context_str=t.table_summary)
    for t in [TableInfo(table_name="transactions_dummy", table_summary=(
        "The transactions table contains detailed information about bank customer transactions. "
        "The columns include: account_number (the bank account number associated with the transaction), "
        "type (the type of transaction, such as Transfer, Pembayaran, Transfer International, Pembayaran QRIS), "
        "transaction (a description of the transaction or more detailed information from the type column), "
        "amount (the amount of money involved in the transaction; if it is a debit, the amount is represented with a '-' in front), "
        "debit_credit (indicates whether the transaction is a debit or a credit), "
        "merchant_code (the code identifying the merchant), "
        "subheader (additional subheader information), "
        "detail_information (detailed information about the transaction), "
        "trx_date (the date when the transaction occurred in the format YYYY-MM-DD (year-month-day)), "
        "trx_time (the time the transaction occurred in the format HH:MM:SS (hour-minute-second)), "
        "currency (the currency used in the transaction), "
        "category_id (an identifier for the category of the transaction and a foreign key for the Categories table)."
    ))]
] 

# indexing
obj_index = ObjectIndex.from_objects( 
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
obj_retriever = obj_index.as_retriever(similarity_top_k=3) 

 
from llama_index.core.retrievers import SQLRetriever
from typing import List
from llama_index.core.query_pipeline import FnComponent

sql_retriever = SQLRetriever(sql_database)


def get_table_context_str(table_schema_objs: List[SQLTableSchema]):
    """Get table context string."""
    context_strs = []
    for table_schema_obj in table_schema_objs:
        table_info = sql_database.get_single_table_info(
            table_schema_obj.table_name
        )
        if table_schema_obj.context_str:
            table_opt_context = " The table description is: "
            table_opt_context += table_schema_obj.context_str
            table_info += table_opt_context

        context_strs.append(table_info)
    return "\n\n".join(context_strs)


table_parser_component = FnComponent(fn=get_table_context_str)


## FEW SHOT Example
from llama_index.core import PromptTemplate

text2sql_prompt_template_str = (
    few_shot_examples +
    "\nBased on the input query and table schema, generate an SQL query. "
    "Make sure the SQL query only retrieves data for the specific account number: {account_number}.\n"
    "The SQL query should be written specifically for PostgreSQL.\n"
    "Query: {query_str}\n"
    "Schema: {schema}\n"
    "SQLQuery: "
)

text2sql_prompt = PromptTemplate(
    text2sql_prompt_template_str,
).partial_format(account_number=top_account_number)


## Parse response
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_TO_SQL_PROMPT
from llama_index.core import PromptTemplate
from llama_index.core.query_pipeline import FnComponent
from llama_index.core.llms import ChatResponse

def parse_response_to_sql(response: ChatResponse) -> str:
    response_content = response.message.content
    sql_query_start = response_content.find("```sql")
    sql_query_end = response_content.find("```", sql_query_start + len("```sql"))
    
    if sql_query_start != -1 and sql_query_end != -1:
        sql_query = response_content[sql_query_start + len("```sql"):sql_query_end].strip()
        # Ensure the SQL query ends with a semicolon and correct closing parentheses
        if not sql_query.endswith(");") and not sql_query.endswith(";"):
            sql_query += ";"
        
    else:
        sql_query = "SQL query not found or incomplete."
        
    print('>>>>>>',sql_query)
    return sql_query

def get_final_response(response: ChatResponse) -> str:
    """Get final response from the assistant."""
    response_content = response.message.content
    final_response_start = response_content.find("assistant:")
    if final_response_start != -1:
        final_response = response_content[final_response_start + len("assistant:"):].strip()
    else:
        final_response = "Assistant response not found."

    return final_response

# Assuming you already have `sql_parser_component` as:
sql_parser_component = FnComponent(fn=parse_response_to_sql)

response_synthesis_prompt_str = (
    "Given an input question, synthesize a response from the query results. The response SHOULD always be in Bahasa Indonesia. ONLY give the Bahasa Indonesia version of response.\n"
    "Table: Table `flowise_1` is a list of transactions from multiple users that contains the amount detail, income expenses, category, \n"
    "And user is identified by account_number (customer identification file).\n"
    "The table has 15 columns:\n"
    "- id: identifier for each transaction.\n"
    "- account_number: number of account that a person has. Each person can have multiple accounts.\n"
    "- type: transaction type.\n"
    "- transaction: detail information of the type"
    "- amount: amount of transaction. If it is expenses, the amount will have a negative value.\n"
    "- debit_credit: the value is always D or C. D means the transaction is an expense. C means the transaction is income.\n"
    "- subheader: transaction/merchant explanation.\n"
    "- detail_information: as a notes or more information from the subheader.\n"
    "- trx_date: timestamp of transaction occured with format yyyy-MM-dd HH:mm:ss.SSS.\n"
    "- currency: currency type.\n"
    "- trx_time: time of transaction occurred with format HH:mm:ss.\n"
    "- category_id: category of each transaction represented by number, with list of categories: 1 = Uang Keluar, 2 = Tabungan & Investasi, 3 = Pinjaman, 4 = Tagihan, 5 = Hadiah & Amal, 6 = Transportasi, 7 = Belanja, 8 = Top Up, 9 = Hiburan, 10 = Makanan & Minuman, 11 = Biaya & Lainnya, 12 = Hobi & Gaya Hidup, 13 = Perawatan Diri, 14 = Kesehatan, 15 = Pendidikan, 16 = Uang Masuk, 17 = Gaji, 18 = Pencairan Investasi, 19 = Bunga, 20 = Refund, 21 = Pencairan Pinjaman, 22 = Cashback.\n"
    "- merchant_code: merchant category code.\n"
    "- updated_at: none.\n"
    "- created_at: none.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {context_str}\n"
    "Response: "
)

response_synthesis_prompt = PromptTemplate(
    response_synthesis_prompt_str,
)

from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
    CustomQueryComponent,
)

qp = QP(
    modules={
        "input": InputComponent(),
        "table_retriever": obj_retriever,
        "table_output_parser": table_parser_component,
        "text2sql_prompt": text2sql_prompt,
        "text2sql_llm": llm,
        "sql_output_parser": sql_parser_component,
        "sql_retriever": sql_retriever,
        "response_synthesis_prompt": response_synthesis_prompt,
        "response_synthesis_llm": llm,
    },
    verbose=True,
)

qp.add_chain(["input", "table_retriever", "table_output_parser"])
qp.add_link("input", "text2sql_prompt", dest_key="query_str")
qp.add_link("table_output_parser", "text2sql_prompt", dest_key="schema")
qp.add_chain(
    ["text2sql_prompt", "text2sql_llm", "sql_output_parser", "sql_retriever"]
)
qp.add_link(
    "sql_output_parser", "response_synthesis_prompt", dest_key="sql_query"
)
qp.add_link(
    "sql_retriever", "response_synthesis_prompt", dest_key="context_str"
)
qp.add_link("input", "response_synthesis_prompt", dest_key="query_str")
qp.add_link("response_synthesis_prompt", "response_synthesis_llm")

# Streamlit UI
# st.title("Bank Customer Chatbot")
# st.write("Ask questions about your financial history and get insights from your transactions.")

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# query = st.text_input("Enter your question:")

# if st.button("Submit"):
#     st.session_state['messages'].append({"role": "user", "content": query})
#     response = qp.run(query=query)
#     st.session_state['messages'].append({"role": "assistant", "content": response})

# for msg in st.session_state['messages']:
#     role = msg["role"]
#     content = msg["content"]
#     if role == "user":
#         st.markdown(f"**You:** {content}")
#     else:
#         st.markdown(f"**Assistant:** {content}")


# Streamlit UI
def response_generator(query):
    response = qp.run(query=query)
    response_text = response.message.content  # Ensure we're accessing the text content of the response
    for word in response_text.split():
        yield word + " "
        time.sleep(0.05)

st.title("LiSA Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your financial history:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        assistant_message = ""
        for word in response_generator(prompt):
            assistant_message += word
            response_placeholder.markdown(assistant_message)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

