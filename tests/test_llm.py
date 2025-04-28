from app.utils.llm import LLM, LLMSettings


PROMPT = ""

config = {}
config["task"       ] = ""
config["temperature"] = 0.3
config["max_tokens" ] = 50
config["system"     ] = ""
config["template"   ] = ""


def test_ollama():
    config["provider"   ] = "ollama"
    config["model"      ] = "qwen2:1.5b"
    llm = LLM(LLMSettings(**config))
    completion = llm.run(PROMPT)
    print(completion)
    assert isinstance(completion, str)

def test_openai():
    config["provider"   ] = "openai"
    config["model"      ] = "gpt-4o-mini"
    llm = LLM(LLMSettings(**config))
    assert isinstance(llm.run(PROMPT), str)

def test_anthropic():
    config["provider"   ] = "anthropic"
    config["model"      ] = "claude-3-5-haiku-20241022"
    llm = LLM(LLMSettings(**config))
    assert isinstance(llm.run(PROMPT), str)

def test_openrouter():
    config["provider"   ] = "openrouter"
    config["model"      ] = "deepseek/deepseek-r1-distill-llama-70b:free"
    llm = LLM(LLMSettings(**config))
    assert isinstance(llm.run(PROMPT), str)
