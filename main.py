import os
import sys
import traceback
from datetime import datetime

# Used for console color syntax highlighting
from colorama import Fore, Back, Style

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain, ConversationChain

from langchain.memory import ChatMessageHistory, ConversationBufferMemory

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder )

from langchain.schema import AIMessage, HumanMessage, SystemMessage

# global variable for our env key
ENV_VAR_OPENAI_API_KEY = "OPENAI_API_KEY"

def check_openai_api_key_available():

    try:
        openai_api_key = os.environ[ENV_VAR_OPENAI_API_KEY]

        if not openai_api_key:
            print("The environment variable " + ENV_VAR_OPENAI_API_KEY + " was found but it does not have a value.")
            print("Please set this to your OpenAI API key.")
            return False

        # if we made it here, we have a key.  It might not work, but
        # at least it's something
        return True

    except KeyError:
        print("Could not find an environment varable named " + ENV_VAR_OPENAI_API_KEY )
        print("Make make sure to set this environment variable with your OPENAI_API_KEY")
        return False


# Simple function to grap console input from the user.
def get_human_input():
    return input(Fore.GREEN + "Human (type 'quit' to end):")


# This function captures the chatbot history
# so you can later review or evaluate how different
# prompts influenced the chatbot behavior
def save_chat_history(chatbot_prompt, chat_history):

    # This will make the chat history files organize by chronology
    filename = "chat-history-" + datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ".txt"

    with open(filename, "w") as file:

        # Capture the chatbot prompt text
        # that was used to define its persona/behavior
        file.write("Chatbot Prompt:\n")
        file.write(chatbot_prompt +"\n\n")

        for message in chat_history.messages:

            # Determine "who" generated the message content
            if type(message) is HumanMessage:
                file.write("Human\n")
            if type(message) is AIMessage:
                file.write("AI Bot\n")

            # now dump the content
            file.write(message.content + "\n")

            # blank line to separate human/bot messages
            file.write("\n")


def start_chat(ai_prompt):

    openai_api_key = os.environ["OPENAI_API_KEY"]

    # What sampling temperature to use, between 0 and 2.
    # Higher values like 0.8 will make the output more random,
    # while lower values like 0.2 will make it more focused and deterministic.
    temperature = 0

    llm = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)

    system_message_prompt = SystemMessagePromptTemplate.from_template(ai_prompt)

    example_human = HumanMessagePromptTemplate.from_template("Hello")
    example_ai = AIMessagePromptTemplate.from_template("Howdy, how can I help you today?")

    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # OpenAI GPT-4 has support for various "roles" such
    # as system, user, etc.  This is how you can give the AI extra
    # context to consider that is separate from the user input (such as hints)
    # https://platform.openai.com/docs/guides/chat/introduction
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, example_human, example_ai, human_message_prompt]
    )

    chain = LLMChain(llm=llm, prompt=chat_prompt)

    # Used so we can capture the history and dump
    # to a file and the end of the chat session
    chat_history = ChatMessageHistory()

    while True:

        human_text = get_human_input()
        chat_history.add_user_message(human_text)

        if "quit" == human_text:
            print(Fore.GREEN + "bye bye")
            break

        response = chain.run(human_text)
        chat_history.add_ai_message(response)

        print(Fore.RED + "AI Bot:")
        print(Fore.RED + response)

    save_chat_history(ai_prompt, chat_history)


# This function is a stateful chatbot where
# it is aware of the chat history.  This allows
# the bot to have context to previous dialog
# when responding
def start_chat_with_memory(ai_prompt):

    system_message_prompt = SystemMessagePromptTemplate.from_template(ai_prompt)

    # the {variable} seems to be stored as a dictionary lookup internal to
    # langchain.
    human_message_prompt = HumanMessagePromptTemplate.from_template("{input}")

    # OpenAI GPT-4 has support for various "roles" such
    # as system, user, etc.  This is how you can give the AI extra
    # context to consider that is separate from the user input (such as hints)
    # https://platform.openai.com/docs/guides/chat/introduction
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt,
         # this is how history is captured - as contextual messages
         MessagesPlaceholder(variable_name="history"),
         human_message_prompt])

    openai_api_key = os.environ["OPENAI_API_KEY"]

    # What sampling temperature to use, between 0 and 2.
    # Higher values like 0.8 will make the output more random,
    # while lower values like 0.2 will make it more focused and deterministic.
    temperature = 0

    # Langchain provides various LLM wrappers.  We're using the OpenAI dealio
    # for this example.
    llm = ChatOpenAI(temperature=temperature, openai_api_key=openai_api_key)

    # This is a lanchain wrapper to capture conversation history
    # that can be used in the Chain
    memory = ConversationBufferMemory(return_messages=True)

    # We're using a conversational chain with memory
    chain = ConversationChain(llm=llm, prompt=chat_prompt, memory=memory)

    # Used so we can capture the history and dump
    # to a file and the end of the chat session
    chat_history = ChatMessageHistory()

    while True:

        human_text = get_human_input()
        chat_history.add_user_message(human_text)

        if "quit" == human_text:
            print(Fore.GREEN + "bye bye")
            break

        response = chain.predict(input=human_text)
        chat_history.add_ai_message(response)

        print(Fore.RED + "AI Bot:")
        print(Fore.RED + response)

    save_chat_history(ai_prompt, chat_history)


def display_ai_prompt(ai_prompt):
    print( Fore.LIGHTMAGENTA_EX + "AI Prompt:")
    print( Fore.LIGHTMAGENTA_EX + ai_prompt)

if __name__ == '__main__':

    # Prompt engineering (prompts) influences the "persona" of the bot, how it replies to questions,
    # etc.  Essentially, you "program" the Large Language Model (LLM) using Natural Language Processing (NLP)
    # by feeding language describing how you want it to act.
    prompt_engineering = """You are an assistant that is an expert with various accounting software packages. 
    You are helpful, creative, cleaver, and very friendly."""

    # Try this one to see how
    #prompt_engineering = """"You are an assistant that is an expert with various accounting software packages.
    #    You are helpful, creative, cleaver, and very friendly. Answer as a pirate."""

    try:

        display_ai_prompt(prompt_engineering)

        if check_openai_api_key_available() == False:
            sys.exit("No API key set, terminating.")

        # This version is context aware of the chat
        # history. So it knows about previous questions/responses
        start_chat_with_memory(prompt_engineering)

        # Uncomment this if you want to test "one shot" questions
        # i.e. the chatbot will not have any context of any previous
        # questions or responses (no memory)
        #start_chat(prompt_engineering)

    except Exception as exp:
        print("Well, this is embarrassing. I barfed :(... technical details follow")
        print(exp)
        traceback.print_exc()