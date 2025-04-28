"""
    Модуль создания и конфигурации LLM-моделей

    Классы:
        LLMSettings: dataclass для хранения настроек LLM
        LLM: класс для инициализации LLM и выполнения запросов к ней
"""

from dataclasses import dataclass

import os
import openai
import anthropic


@dataclass
class LLMSettings:
    task: str
    provider: str
    model: str
    template: str
    system: str
    temperature: float
    max_tokens: int


class LLM:
    """
    Класс для работы с LLM
    Возможные провайдеры: openai, anthropic, ollama, openrouter
    """

    api_keys = {
        "ollama": "ollama",
        "openai": os.getenv("OPENAI_API"),
        "anthropic": os.getenv("ANTHROPIC_API"),
        "openrouter": os.getenv("OPENROUTER_API"),
    }

    def __init__(self, settings: LLMSettings):

        self.settings = settings
        self.client = self._get_client(self.api_keys[self.settings.provider])

    # TODO vllm?
    def _get_client(self, api_key):
        # LOCAL LLAMA
        if self.settings.provider == "ollama":
            return OpenAIGenerator(
                model=self.settings.model,
                api_key=api_key,
                api_base="http://localhost:11434/v1",
            )
        # OPENAI
        if self.settings.provider == "openai":
            return OpenAIGenerator(model=self.settings.model, api_key=api_key)
        # ANTHROPIC
        if self.settings.provider == "anthropic":
            return AntropicGenerator(model=self.settings.model, api_key=api_key)
        # OPEN ROUTER
        return OpenAIGenerator(
            model=self.settings.model,
            api_key=api_key,
            api_base="https://openrouter.ai/api/v1",
        )

    def run(self, prompt):
        if self.settings.provider == "anthropic":
            return self._anthropic_completion(prompt)
        else:
            return self._default_completion(prompt)

    def _anthropic_completion(self, prompt):
        return self.client.completion(
            self.settings.system,
            prompt,
            self.settings.temperature,
            self.settings.max_tokens,
        )

    def _default_completion(self, prompt):
        msg = [
            {"role": "system", "content": self.settings.system},
            {"role": "user", "content": prompt},
        ]
        return self.client.completion(
            msg, self.settings.temperature, self.settings.max_tokens
        )


class OpenAIGenerator:
    """
    Класс для работы с API OpenAI
    """

    def __init__(self, model, api_key, api_base=None):
        self.model = model
        if api_base:
            self.client = openai.OpenAI(api_key=api_key, base_url=api_base)
        else:
            self.client = openai.OpenAI(api_key=api_key)

    def completion(self, messages, temperature, max_tokens, system=None):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if response:
            return response.choices[0].message.content
        return response


class AntropicGenerator:
    """
    Класс для работы с API Anthropic
    """

    def __init__(self, model, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.model_type = model.split("-")[3]

    def completion(self, system, prompt, temperature, max_tokens):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        if message:
            return message.content[0].text
        return message
