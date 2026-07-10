# --- Voice RAG bot demo ------------------------------------------------
# Pipeline: PDF -> Azure Document Intelligence (text extraction)
#        -> Azure OpenAI embeddings + in-memory vector store (retrieval)
#        -> Azure OpenAI chat model (answer generation, LangChain "RAG chain")
#        -> Azure Speech SDK (voice in via STT, voice out via TTS)
# All credentials are pulled from environment variables (see .env) - never
# hardcode real keys/endpoints in source when sharing this code.
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import numpy as np
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (ConfigurableField, RunnablePassthrough)
from langchain.chat_models import AzureChatOpenAI
from langchain_core.documents import Document
from langchain_community.vectorstores import InMemoryVectorStore
from azure.ai.inference import EmbeddingsClient
from langchain_core.embeddings import Embeddings
from langchain_openai import AzureOpenAIEmbeddings
from typing  import Literal , List
from pydantic import create_model , model_validator
import json
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

# azure_oai_endpoint='XXXX'
# azure_oai_key='XXXX'
# azure_oai_deployment='XXXX'
# api_version = "2024-02-01"
# embedding_key = 'XXXX'
# endpoint = "XXXX"
# model_name = "text-embedding-3-small"
# doc_endpoint = "XXXX"
# doc_key = "XXXX"

# Create a .env file (never commit it) with these keys instead of hardcoding
# values above - load_dotenv() reads it into os.environ for you.
azure_oai_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key=os.getenv("AZURE_OAI_KEY")
azure_oai_deployment=os.getenv("AZURE_OAI_DEPLOYMENT")
api_version = "2024-02-01"
embedding_key = os.getenv('EMBEDDING_KEY')
endpoint = os.getenv("AZURE_EMBEDDING_ENDPOINT")
model_name = os.getenv('EMBEDDING_MODEL_NAME')
doc_endpoint = os.getenv('DOC_INTELLIGENCE_ENDPOINT')
doc_key = os.getenv('DOC_INTELLIGENCE_KEY')


# Embedding model used to turn document text into vectors for similarity search.
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=embedding_key,
    model=model_name,
    openai_api_version=api_version
)

# Store connection information


# fileUri = "https://github.com/MicrosoftLearning/mslearn-ai-document-intelligence/blob/main/Labfiles/01-prebuild-models/sample-invoice/sample-invoice.pdf?raw=true"
fileLocale = "en-US"
# fileModelId = "prebuilt-invoice"
# "prebuilt-read" = generic OCR/text-extraction model (works on any PDF/image).
# Swap for a domain-specific prebuilt model (e.g. "prebuilt-invoice") if you
# know the document type in advance - you'll get structured fields for free.
fileModelId = 'prebuilt-read'

print(f"\nConnecting to Forms Recognizer at: {doc_endpoint}")
# print(f"Analyzing invoice 


# document_analysis_client = DocumentAnalysisClient(
#     endpoint=doc_endpoint, credential=AzureKeyCredential(doc_key)
# )


def analyze_read(fileUri):
    """Send a local PDF to Azure Document Intelligence and get back one
    LangChain Document per page, ready to be embedded into the vector store."""

    document_analysis_client = DocumentAnalysisClient(
        endpoint=doc_endpoint, credential=AzureKeyCredential(doc_key)
    )

    with open(fileUri, "rb") as f:
        pdf_bytes = f.read()

    # begin_analyze_document is async under the hood - poller.result() blocks
    # until Azure finishes OCR/layout analysis on the uploaded bytes.
    poller = document_analysis_client.begin_analyze_document(
        model_id=fileModelId,
        document=pdf_bytes,
        locale=fileLocale
    )

    result = poller.result()

    print ("Document contains content: ", result.content)

    docs = []
    # pages_text = []
    for index_page, page in enumerate(result.pages):
        page_lines = [line.content for line in page.lines]  # get all lines for this page
        page_text = "\n".join(page_lines)  # join lines to form page text
        # pages_text.append(page_text)
        print("----------------------------------------------")
        # print(page_text)
        docs.append(
            Document(
                page_content=page_text,
                metadata=dict(
                    {
                        "source":str(fileLocale),
                        "file_path":str(fileLocale),
                        "page":index_page,
                        "total_pages":len(result.pages)
                    }
                )
            )
        )
    return docs


def return_vars():
    """Build a fresh (empty) vector store + retriever + prompt template.
    Called once per question so each query starts from a clean store."""

    # InMemoryVectorStore = simplest possible vector DB - good for demos/
    # learning, but not persisted; swap for Chroma/FAISS/Azure AI Search
    # once you need the index to survive a restart.
    vectorstore_dense = InMemoryVectorStore(
        embedding=embeddings
    )
    retriever_dense = vectorstore_dense.as_retriever(search_type="similarity",search_kwargs={"k":5})
    # configurable_fields lets us override search_kwargs (e.g. k, filters)
    # per-invocation via chain.invoke(..., config={"configurable": {...}})
    # instead of baking one fixed k into the retriever.
    configurable_retriever_dense = retriever_dense.configurable_fields(
        search_kwargs=ConfigurableField(
            id='search_kwargs',
            name="Search_kwargs",
            description="The search kwargs to use",
        )
    )
    retriever_chain_dense = (lambda x : x["search"]) | configurable_retriever_dense

    # The core RAG prompt: retrieved chunks go into {context}, the user's
    # question goes into {question}. Keep answers short - see note below.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                """you are an assistant for question-answering tasks. use the following pieces of retrived context to answer the questions.
                if you dont know the answer ,just say that you dont know, always print a single number or very few words since your answers are stored 
                in varchar(128).
                Question : {question}
                Context: {context}
                Answer:"""
            )
        ]
    )
    return vectorstore_dense, retriever_chain_dense, prompt


def query_generator():
    """Hardcoded library of "known questions" for this specific document type
    (Belgian energy performance certificates). Each entry pairs:
      - a Pydantic schema (the shape of the expected answer)
      - a retriever config (how/where to search, e.g. first page only)
      - q_search (keywords used to retrieve relevant chunks)
      - q_generate (the actual instruction sent to the LLM)
    This is the "structured RAG" pattern: instead of one open-ended question,
    you predefine the questions you expect and force JSON-shaped answers."""
    cfg_force_first_page = {"filter": lambda d: d.metadata["page"] == 0}
    qq = [

        {"schema": create_model(
            "regionSchema",
            region=(Literal["Wallonia","Flanders","Brussels"], None),
        ),
        "prompt_based_schema": True,
        "retriever_config":cfg_force_first_page,
        "q_search": "region , Flanders, Vlaams, Vlaanderen, Wallonie, Wallonia, Brussels , Bruxelles",
        "q_generate": "What is the region? One of Flanders, Wallonia or Brussels.",
        },        
        {"schema": create_model(
            "buildingSchema",
            buildingtype=(Literal["building","appartment","non-residential"], None),
        ),
        "prompt_based_schema": True,
        "retriever_config":{"k": 2},
        "q_search": "appartment , appartement, building, woning , mainson unifamiliale, eenheid",
        "q_generate": 'Is this certificate issued for a building or for an individual apartment? Print "building","appartment" or "non-residential"',
        },      

        {
        "only_in_region" : ["Flanders"],    
        "schema": create_model(
            "Vlaanderen_certID_Schema",
            certID=(str,""),
            dateIssued=(str,""),
            dateValid=(str,""),
            zip=(str,""),
            municipality=(str,""),
            street=(str,""),
            num=(str,""),
        ),
        "prompt_based_schema": True,
        "retriever_config":cfg_force_first_page,
        "q_search": "",
        "q_generate": 'Find unique ID of this certificate , date it was issued , its validity date and the address of the dwelling.',
        },

        {"schema": create_model(
            "heating_type_text_Schema",
            heating_type_text=(str,""),
        ),
        "prompt_based_schema": True,
        "retriever_config":{"k": 2},
        "q_search": "verwarming , heating type, performance des installation de chauffage",
        "q_generate": 'What is the type of heating in use in this dwelling? gas/mazout/stookolie/electricititeit/gaz natural/etc.',
        },      
        {"schema": create_model(
            "area_square_metere_Schema",
            are_square_meter_text=(str,""),
        ),
        "prompt_based_schema": True,
        "retriever_config":{"k": 2},
        "q_search": "area , usable space, bruikbare vloeroppervlakte",
        "q_generate": 'What is area in square metere of the dwelling? area/usable space/bruikbare vloeroppervlakte/etc.',
        },      
    ]
    return qq


def TranscribeCommand():
    """Speech-to-text: record one utterance from the default mic and return
    the recognized text (this is the "voice in" half of the voice bot)."""
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # recognize_once_async() captures a single phrase then stops listening -
    # for continuous/always-on listening use start_continuous_recognition()
    # with event callbacks instead.
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)


    # Return the command
    return command



def pick_query_from_voice(command: str, QQ: list):
    """
    Takes voice command text and returns one entry from the QQ list.
    (Router pattern: ask the LLM to classify free-text speech into one of a
    fixed set of predefined queries, by index, rather than generating a new
    schema on the fly - simpler and more predictable than generate_query_from_instruction below.)
    """
    system_prompt = """
You are an AI that decides which query definition should be triggered.

Given a natural language instruction, choose the BEST MATCHING query object from the provided list.
Return ONLY the index as a JSON number.

Example:
Input: "Find region"
Output: {"index": 0}
"""

    # Prepare a readable summary for the LLM
    queries_for_llm = "\n".join(
        f"{i}: q_generate = {q['q_generate']}"
        for i, q in enumerate(QQ)
    )

    user_prompt = f"""User command: "{command}"
                Available queries:{queries_for_llm}
                Which query index matches best?
                Return: {{ "index": number }}
                """

    llm = AzureChatOpenAI(
        openai_api_key=azure_oai_key,
        openai_api_base=azure_oai_endpoint,
        deployment_name=azure_oai_deployment,
        openai_api_version="2024-02-15-preview",
        temperature=0,
    )

    result = llm.invoke([{"role": "system", "content": system_prompt},
                         {"role": "user", "content": user_prompt}])

    import json
    try:
        idx = json.loads(result.content)["index"]
        return QQ[idx]
    except:
        print("Could not parse LLM response:", result.content)
        return None


def generate_query_from_instruction(instruction: str):
    """
    Ask the LLM to produce a JSON query_config matching the QQ structure.
    Returns a dict suitable to pass into process_docs(...) as selected_query.
    Unlike pick_query_from_voice (fixed list), this dynamically invents a new
    schema/question for whatever the user asks - more flexible, but relies on
    eval() below so only use this with trusted input / trusted LLM output.
    """
    llm = AzureChatOpenAI(
        openai_api_key=azure_oai_key,
        openai_api_base=azure_oai_endpoint,
        deployment_name=azure_oai_deployment,
        openai_api_version="2024-02-15-preview",
        temperature=0
    )


    system_prompt = """
You are an assistant that converts a user's natural-language request 
into a structured JSON that fills out this template:

{
    "schema_name": "",
    "fields": {},
    "prompt_based_schema": true,
    "retriever_config": {"k": 5},
    "q_search": "",
    "q_generate": ""
}

Rules:
- Fill only the values.
- Always return valid JSON.
- Fields types must be 'str', 'Literal[...]', or other Python types.
- If a value is unknown, use empty string or default.
"""


    user_prompt = f"""
You will receive a natural-language question from me about extracting information
from a document (PDF, invoice, contract, report, etc.). Based on my question,
produce a structured JSON configuration following the instructions in the system prompt.

My question will look like normal conversation, for example:
- "What is the region?"
- "Can you tell me the invoice date?"
- "I need to know the total amount"
- "What is the square meter area of this building?"
- "Find the customer name and address"

Here is my request:
"{instruction}"
"""


    response = llm.invoke([{"role": "system", "content": system_prompt},
                         {"role": "user", "content": user_prompt}])

    # Extract JSON from response (be tolerant)
    text = response.content if hasattr(response, "content") else str(response)
    # Try to find the first '{' ... '}' block
    try:
        js = "{" + text.split("{", 1)[1].rsplit("}", 1)[0] + "}"
        config = json.loads(js)
    except Exception:
        # fallback: try parsing the entire text
        config = json.loads(text)


    fields = {}
    for k, v in config["fields"].items():
        # Evaluate type strings safely (Literal or str)
        fields[k] = (eval(v), None if "Literal" in v else "")

    # Create the Pydantic model dynamically
    schema_model = create_model(config["schema_name"], **fields)

    # Final structured object
    query_config = {
        "schema": schema_model,
        "prompt_based_schema": config["prompt_based_schema"],
        "retriever_config": config["retriever_config"],
        "q_search": config["q_search"],
        "q_generate": config["q_generate"]
    }

    # Post-process: if retriever_config contains string 'lambda', convert
    # to callable or keep as dict expected by your pipeline.
    # We'll keep as dict; your process_docs expects dicts.
    return query_config


def TranscribeAndRoute(command):
    # command = TranscribeCommand()   # speech → text
    # if not command:
    #     return None

    print("Routing voice command:", command)

    QQ = query_generator()
    selected_query = pick_query_from_voice(command, QQ)

    if selected_query:
        print("Selected query:", selected_query["q_generate"])
    else:
        print("No query matched.")

    return selected_query

def format_docs(docs):
    """Flatten retrieved Document chunks into one text blob for the {context} slot in the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

def process_docs(fileLocale,docs,q):
    """The actual RAG step: embed docs -> retrieve top-k relevant chunks for
    q['q_search'] -> ask the LLM q['q_generate'] using only that context ->
    parse the JSON-shaped answer back into a plain dict."""
    vectorstore_dense, retriever_chain_dense, prompt = return_vars()
    res = {"pdf_file":fileLocale}
    vectorstore_dense.store = {}
    vectorstore_dense.add_documents(docs)

    
    # if "only_in_region" in q and "region" in res and res["region"] not in q["only_in_region"]:
    #     continue

    schema = q["schema"]
    is_prompt_based_schema = q.get("prompt_based_schema", False)

    extra_body = None
    prompt_suffix = ""
    if is_prompt_based_schema:
        prompt_suffix = f"Reply with JSON with keys {json.dumps(list(schema.model_fields))}"
    else:
        extra_body = {
            "guided_decoding_backend": "lm-format-enforcer",
            "guided_json": schema.model_json_schema()
        }
    print("prompt_suffix",prompt_suffix)

    llm = AzureChatOpenAI(
        openai_api_key=azure_oai_key,
        openai_api_base=azure_oai_endpoint,
        deployment_name=azure_oai_deployment,
        openai_api_version="2024-02-15-preview",
        temperature=0,
        # extra_body=extra_body
    )

    rag_chain_from_docs = (
        {
            "context": lambda x : format_docs(x["context"]),
            "question": lambda x : (x["generate"] + prompt_suffix)
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    chain = RunnablePassthrough.assign(
        context = (
            retriever_chain_dense
        ),
    ).assign(answer=rag_chain_from_docs)

    chain_res = chain.invoke(
        {"search": q["q_search"], "generate": q["q_generate"]},
        config={"configurable": {"search_kwargs": q["retriever_config"]}}
    )

    source_pages = ",".join(str(d.metadata["page"]) for d in chain_res["context"])
    print("source_pages",source_pages)

    ans = chain_res["answer"]
    print("ans", ans)
    js_ans = "{" + ans.split("{", maxsplit=1)[-1].rsplit("}", maxsplit=1)[0]+"}"
    try :
        js_ans = json.loads(js_ans)
    except json.JSONDecodeError:
        print("error jsondecoder")
    res|= js_ans
    res["pages_" + schema.__name__] = source_pages
    return res

def natural_language_answer(key, value):
    # region
    if key.lower() in ["region", "regionSchema"]:
        return f"The dwelling is located in {value}."
    
    # building type
    if key.lower() in ["buildingtype", "buildingSchema"]:
        return f"The certificate is issued for a {value}."

    # certificate info
    if "certid" in key.lower():
        return f"The certificate ID is {value}."
    if "dateissued" in key.lower():
        return f"The certificate was issued on {value}."
    if "datevalid" in key.lower():
        return f"The certificate is valid until {value}."

    # address parts
    if key.lower() in ["zip", "municipality", "street", "num"]:
        return f"The {key.replace('_',' ')} is {value}."

    # heating type
    if "heating" in key.lower():
        return f"The heating type used in this dwelling is {value}."

    # square meter area
    if "area" in key.lower():
        return f"The usable floor area is {value} square meters."

    # fallback
    return f"The answer is {value}."



def speak_response_from_result(result_dict):
    """
    Takes the RAG result (a dict) and turns it into a conversational sentence.
    Then speaks it using Azure TTS. This is the "voice out" half of the bot -
    pairs with TranscribeCommand() for the "voice in" half.
    """
    if not result_dict:
        text = "Sorry, I could not find the answer."
    else:
        # Find first actual answer key (skip pdf_file or metadata keys)
        key = next((k for k in result_dict.keys() if k != "pdf_file"), None)

        if key is None:
            text = "Sorry, I could not determine the answer."
        else:
            value = result_dict[key]

            # Map key → natural sentence
            text = natural_language_answer(key, value)

    # Speak it aloud
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    synthesizer.speak_text_async(text).get()

    print("Spoken:", text)
    return text



def speak_text(text):
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis failed:", result.reason)



def main():
    """Entry point: load one PDF, extract+index it once, then loop forever
    listening for voice questions about that document until the user says
    an exit word. Students: swap fileUri for your own document/local path."""
    # fileUri = r"C:\Users\SSHE\OneDrive - NORRIQ\Documents\AZURE AI102\az-cog\az-cog\mslearn-ai-document-intelligence\Labfiles\01-prebuild-models\sample-invoice\1.pdf"
    fileUri = r"C:\Users\SSHE\OneDrive - NORRIQ\Documents\AZURE AI102\az-cog\az-cog\mslearn-ai-document-intelligence\Labfiles\01-prebuild-models\sample-invoice\sample-invoice.pdf"
    docs = analyze_read(fileUri)  # OCR the PDF once up front; kept in memory for the whole session

    try:
        global speech_config

        # Load Azure Speech credentials
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Initialize speech service
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print("Ready for voice assistant. Say something...")

        while True:
            print("\nListening... (say 'terminate' to exit)")
            spoken = TranscribeCommand()

            if not spoken:
                continue

            # --- Exit conditions ---
            if spoken.lower() in ["stop.", "quit.", "exit.", "terminate.", "goodbye."]:
                speak_text("Okay, shutting down. Goodbye!")
                print("Assistant terminated.")
                break

            # Process query
            selected_query = generate_query_from_instruction(spoken)
            print("selected_query_dynamic",selected_query)

            # selected_query = TranscribeAndRoute(spoken)  # <-- your router
            # print("Selected Query:", selected_query)

            output_res = process_docs(fileLocale, docs, selected_query)
            print("output_res:", output_res)

            # Turn model result into natural spoken answer
            response_text = speak_response_from_result(output_res)
            # print("Assistant:", response_text)

            speak_text(response_text)

    except Exception as ex:
        print("Error:", ex)




if __name__ == "__main__":
    main()