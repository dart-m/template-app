"""Модуль содержит вспомогательные функции для обработки текста"""
from pathlib import Path

import re
import subprocess

from app.core.logger import logger


def get_chunks(text: str, max_length: int):
    """
    Функция разбивает текст на части по max_length символов
    и возвращает список частей. Разбиение происходит по абзацам (.\n)

    Вход:
        text (str) - текст для разбиения
        max_length (int) - максимальная длина части
    Выход:
        full_text (list) - список частей текста
    """
    full_text = []
    chunk = ""
    for para in text.split(".\n"):
        chunk_length = len(chunk)
        if chunk_length < max_length:
            chunk += f"{para}.\n"
        else:
            chunk += f"{para}.\n"
            full_text.append(chunk)
            chunk = ""
    if chunk:
        full_text.append(chunk)
    return full_text


def parse_response(text: str, tag: str):
    """
    Функция парсит текст между тегами <tag> и </tag>
    Если найдено несколько совпадений, возвращает первое
    Если не найдено ни одного совпадения, возвращает исходный текст
    Вход:
        text (str) - текст для парсинга
        tag  (str) - тег для поиска
    Выход:
        match[0] (str) - текст между тегами
    """
    pattern = rf"<{tag}>\s*(.*?)\s*</{tag}>"
    match = re.findall(pattern, text, re.DOTALL)
    if len(match) != 1:
        logger.warning("PARSING : failed to parse response (0 or >1 matches)")
        return text
    return match[0]


def spaces_preprocessing(text):
    """
    Функция удаляет лишние пробелы и переносы строк
    Вход: text (str) - текст для обработки
    Выход: text (str) - обработанный текст
    """
    return re.sub(r"\s{2,}", " ", text).strip()


def replace_quotes(text):
    """
    Функция заменяет двойные кавычки на издательские
    Вход: text (str) - текст для обработки
    Выход: text (str) - обработанный текст
    """
    return re.sub(r'\"([^"]+)\"', r"«\1»", text)


def converter(input_path: Path, output_path: Path, to: str) -> None:
    """
    Функция конвертации файла с помощью конвертера pandoc
    """
    match to:
        case "md":  # convert docx to markdown
            subprocess.run(
                [
                    "pandoc",
                    input_path,
                    "-f",
                    "docx",
                    "-t",
                    "markdown",
                    "-s",
                    "-o",
                    output_path,
                ],
                check=True,
            )
        case "docx":  # convert markdown to docx
            subprocess.run(
                [
                    "pandoc",
                    input_path,
                    "-f",
                    "markdown",
                    "-t",
                    "docx",
                    "-s",
                    "-o",
                    output_path,
                ],
                check=True,
            )
