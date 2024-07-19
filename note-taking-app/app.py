import logging
import os
from flask import Flask, request, jsonify, render_template
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "L3 Note-taking Assistant"
os.environ["GROQ_API_KEY"] = "your-api-key"

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq LLM
groq_llm = ChatGroq(
    model_name="llama3-8b-8192",  # Adjust if there's a specific LLaMA 3 8B option
    temperature=0,
    max_tokens=4096,
)

# Initialize DuckDuckGo search tool
wrapper = DuckDuckGoSearchAPIWrapper(max_results=25)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)

# Define prompts
generate_prompt = PromptTemplate(
    template="""
    You are an AI assistant for note-taking tasks. Your role is to help users manage, understand, and expand upon their notes.
    Use the following pieces of context to answer the user's question:
    1. The user's existing notes
    2. Web search results (if provided)
    If you don't have enough information to answer, say so honestly.
    Provide concise but informative answers, and suggest ways to organize or enhance the notes when appropriate.
    Question: {question}
    Existing Notes: {context}
    Web Search Results (if any): {web_context}
    Answer:
    """,
    input_variables=["question", "context", "web_context"],
)

router_prompt = PromptTemplate(
    template="""
    You are an expert at determining whether a note-related question can be answered with existing notes or requires additional web research.
    If the question seems to be about managing, organizing, or understanding existing notes, respond with 'generate'.
    If the question requires factual information not likely to be in the notes, or asks about recent events, respond with 'web_search'.
    Respond with only 'generate' or 'web_search', without any additional text.
    Question to route: {question}
    """,
    input_variables=["question"],
)

query_prompt = PromptTemplate(
    template="""
    You are an expert at crafting web search queries to supplement note-taking.
    Transform the user's question into an effective web search query that will provide relevant information to enhance their notes.
    Provide only the search query, without any additional text.
    Question to transform: {question}
    """,
    input_variables=["question"],
)

# Define chain function
def create_chain(prompt_template):
    def chain(inputs):
        formatted_prompt = prompt_template.format(**inputs)
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content=formatted_prompt)
        ]
        response = groq_llm(messages)
        return response.content
    return chain

# Create chains
generate_chain = create_chain(generate_prompt)
question_router = create_chain(router_prompt)
query_chain = create_chain(query_prompt)

# Define graph state
class GraphState(TypedDict):
    question: str
    generation: str
    search_query: str
    context: str
    web_context: str

# Define nodes
def generate(state):
    question = state["question"]
    context = state["context"]
    web_context = state.get("web_context", "")
    logging.info(f"Generating response for question: {question}")
    generation = generate_chain({"context": context, "question": question, "web_context": web_context})
    return {"generation": generation}

def transform_query(state):
    question = state['question']
    logging.info(f"Transforming query: {question}")
    search_query = query_chain({"question": question})
    return {"search_query": search_query}

def web_search(state):
    search_query = state['search_query']
    logging.info(f"Performing web search with query: {search_query}")
    search_result = web_search_tool.invoke(search_query)
    return {"web_context": search_result}

def route_question(state):
    question = state['question']
    logging.info(f"Routing question: {question}")
    output = question_router({"question": question})
    if "web_search" in output.lower():
        return "websearch"
    else:
        return "generate"

# Build the nodes and edges
workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "websearch")
workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)

# Compile the workflow
local_agent = workflow.compile()

def run_agent(question, context):
    output = local_agent.invoke({"question": question, "context": context})
    return output["generation"]

# Define Flask routes
# Path to save notes
NOTES_PATH = "notes.txt"

# Endpoint to save notes
@app.route('/api/save_notes', methods=['POST'])
def save_notes():
    data = request.json
    notes = data.get('notes')
    try:
        with open(NOTES_PATH, 'w') as file:
            file.write(notes)
        return jsonify({'status': 'success', 'message': 'Notes saved successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    context = data.get('context')
    logging.info(f"Received question: {question}")
    response = run_agent(question, context)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)