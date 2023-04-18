# Langchain Proof-of-Concept

Generative AI is all the hotness right now.  There are multiple large langauge models (LLMs), 
vector dbs, tokenizers, etc.  Langchain provides an abstraction layer.

This project is a PoC to use Langchain + OpenAI to build a simple chatbot.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes.  This code is only
intended to demonstrate the basic concepts and is therefore not intended for
production systems.

### Prerequisites

You will need to create an OpenAI account and generate an API key.
- [OpenAI platform documentation and signup](https://platform.openai.com/overview)


### Installing

A step by step series of examples that tell you how to get a development
environment running

Clone the repo to your host machine

    git clone https://github.com/sean-foley/langchain-poc.git

Generate an OpenAI API Key, then set the environment variable. 
You can add this line to your .bashrc file to make this environment 
variable persistent.

    export OPENAI_API_KEY="your-api-key-here"

### Using

Open the project up in PyCharm and give it a whirl.  The code in 
main.py is heavily commented to explain what's going on.

Play around with changing the variable prompt_engineering text. 

## Built With

  - [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE
  - [LangChain](https://github.com/hwchase17/langchain) - Build applications with LLMs through composability


## Contributing
While I will take pull requests, this is a PoC, so you're better 
off forking it and turning it into whatever you want.

## License

This project is licensed under the MIT License - see 
the [LICENSE.md](LICENSE.md) file for more details.

## Acknowledgments
**Billie Thompson** - *for the README.md template* - [PurpleBooth](https://github.com/PurpleBooth)