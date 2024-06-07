import chainlit as cl
import copy
import datetime
from chainlit.input_widget import Select, TextInput
from utilities.llm import openai_api_call
from utilities.constants import HF_EMBED_MODELS
from llama_index.core import PromptTemplate, SimpleDirectoryReader, VectorStoreIndex
from utilities.vector import get_retriver, create_filters
from utilities.data_retrieval import retrieve_metadata


@cl.on_chat_start
async def start():
    # Store initial values (these might be placeholders or empty)
    cl.user_session.set("selected_name", None)
    cl.user_session.set("selected_old", None)
    cl.user_session.set("selected_gender", None)
    cl.user_session.set("selected_occupation", None)

    # Send the select components to the user
    await cl.ChatSettings(
        [
            Select(
                id="selected_old",
                label="How old are you?",
                values=[
                    "Under 18",
                    "18-24",
                    "25-34",
                    "35-44",
                    "45-54",
                    "55-64",
                    "65 or over",
                ],
                initial_index=None,
            ),
            Select(
                id="selected_gender",
                label="What is your gender?",
                values=["Male", "Female"],
                initial_index=None,
            ),
        ]
    ).send()

    # Instead of immediately trying to load data, display a message
    await cl.Message(
        content="Please Fill the information to start the analysis",
        author="GaojAI",
    ).send()


@cl.on_settings_update
async def handle_settings_update(settings):
    """
    This function is triggered whenever the user changes a setting.
    It updates the session state with the new selected values.
    """
    cl.user_session.set("selected_old", settings["selected_old"])
    cl.user_session.set("selected_gender", settings["selected_gender"])

    # Check if all selections have been made
    if all(
        cl.user_session.get(key)
        for key in [
            "selected_old",
            "selected_gender",
        ]
    ):
        loading_msg = cl.Message(
            content="I'm loading the data from database, Please wait...",
            author="GaojAI",
        )
        await loading_msg.send()
        # Now you can safely proceed with data loading and processing
        await load_and_process_data()


async def load_and_process_data():
    selected_old = cl.user_session.get("selected_old")
    selected_gender = cl.user_session.get("selected_gender")
    loading_msg = cl.Message(
        content="Loading the data...",
        author="GaojAI",
    )
    await loading_msg.send()
    gaojai_text = load_gaojai_texts("psychology")
    loading_msg = cl.Message(
        content="Thank you for waiting. Please feel free to ask any question related to the provided information.",
        author="GaojAI",
    )
    await loading_msg.send()
    gaojai_result = summary_agent(gaojai_text, selected_old, selected_gender)
    cl.user_session.set(
        "message_history",
        [
            {
                "role": "system",
                "content": gaojai_result,
            },
        ],
    )
    # cl.user_session.set("gaojai_result", gaojai_result)


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    output = openai_api_call(message_history)
    msg = cl.Message(content=f"{output}", author="GaojAI")
    message_history.append({"role": "assistant", "content": output})
    await msg.send()


def summary_agent(
    texts,
    selected_old,
    selected_gender,
) -> str:
    prompt_text = """
    User Information template:
    Age: {age}
    Gender: {gender}
    ========================
    Information and Knowledge About Psychology
    {texts}

    Follow these rules:
    1. Analyze this User Information and Knowledge About Psychology and understandit.
    2. Answer the question related User Information.
    3. Please Answer the question In Thai Language.
    4. You can ask for more information if needed.
    5. You need to inform the users that you are friend of users you can talk in style of friend.
    6. The style of the answer based on age and gender the users put in the information.
    7. Please Answer based on the knowledge about psychology If you don't know the answer, please answer the users to go to find the psychologist or doctor.

    ========================

    Now your turn. Based on provided match commentary and task instructions. Please return just the Users Information template from above and write a concise summary in bullet points.
    """
    prompt_template = PromptTemplate(prompt_text)
    prompt = prompt_template.format(
        texts=texts,
        age=selected_old,
        gender=selected_gender,
    )
    return prompt


def load_gaojai_texts(question):
    load_text = []
    model = HF_EMBED_MODELS["MULTILINGUAL"]
    filters = create_filters(
        {
            "data_source": {
                "value": "pdf",
            },
        }
    )
    retriever = get_retriver(model, "pdf_file", filters)
    gaojai_text = retriever.retrieve("All of text related to psychology")
    for t in gaojai_text:
        load_text.append(t.text)
    print(load_text)
    return load_text
