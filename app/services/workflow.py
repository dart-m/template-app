"""Модуль пайплайна"""

from pathlib import Path
from tqdm import tqdm


from app.utils.llm import LLM, LLMSettings
from app.utils.helpers import get_chunks, parse_response, converter

from app.prompts import SYSTEM_PROMPT
from app.core.logger import logger


############## Настройки ################

CHUNK_LENGTH = 2300

config = {}

config["task"] = "corrector"
config["provider"] = "anthropic"
config["model"] = "claude-3-5-sonnet-20241022"
config["temperature"] = 0.3
config["max_tokens"] = 8192

logger.info(f"{config} CHUNK_LENGTH {CHUNK_LENGTH}")

config["system"] = SYSTEM_PROMPT
config["template"] = ""

llm = LLM(LLMSettings(**config))


############## Пайплайн #################


def workflow(rundir: Path, filename: str) -> Path:
    """
    Пайплайн
    Вход: rundir (Path) путь рабочей директории, filename (str) имя файла
    Выход: out_docx (Path) - путь к файлу с результатом
    """
    # 1. INIT AND GET CHUNKS
    outputname = filename.split(".docx")[0]
    filename_md = filename.replace("docx", "md")

    try:
        converter(rundir / filename, rundir / filename_md, to="md")
    except Exception as e:
        logger.error(f"CONVERTER : failed to convert docx to md {e}")
        raise e

    with open(rundir / filename_md, "r", encoding="UTF-8") as f:
        file = f.read()

    chunks = get_chunks(file, CHUNK_LENGTH)
    logger.info(f"AGENT : getting {len(chunks)} chunks")

    text_output = ""
    raw_output = ""

    # 2. GO OVER CHUNKS . WRITE OUTPUT
    for chunk in tqdm(chunks):
        try:
            completion = llm.run(chunk)
            raw_output += completion
            text_output += parse_response(completion, "answer")
        except Exception as e:
            logger.warning(f"Couldn't complete chunk: {e}")

    # TODO: ADD BAD RESPONSE HANDLING

    # 3. SAVE RAW OUTPUT, CONV TO DOCX, RETURN
    with open(rundir / f"{outputname}_raw.md", "w", encoding="UTF-8") as f:
        f.write(raw_output)

    output_path = rundir / f"{outputname}_out.md"
    out_docx = rundir / f"{outputname}_out.docx"
    with open(output_path, "w", encoding="UTF-8") as f:
        f.write(text_output)

    try:
        converter(output_path, out_docx, to="docx")
    except Exception as e:
        logger.error(f"CONVERTER : failed to convert md to docx {e}")
        return output_path

    return out_docx
