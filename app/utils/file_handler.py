"""Модуль обработки входных файлов"""

from pathlib import Path
from datetime import datetime
import os

from fastapi import HTTPException, UploadFile
import docx

from app.core.logger import logger


class FileProcessingError(Exception):
    """
    Класс ошибки для обработки docx файлов
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileHandler:
    """
    Класс для обработки входных файлов
    и создания папки для хранения результатов

    Инициализация: создание папки для хранения результатов
    unpack: сохранение файла в папку
    handle_file: обработка файла
    """

    def __init__(self):
        try:
            now = datetime.now()
            self.run_name = now.strftime("run_%Y%m%d_%H%M%S")
            self.rundir = Path("data/runs") / self.run_name
            os.makedirs(self.rundir)
            logger.info(f"FILE HANDLER : init {self.run_name}")
        except Exception as e:
            logger.critical(
                f"FILE HANDLER : run folder {self.run_name} has not been created : {e}"
            )
            raise

    async def unpack(self, file: UploadFile) -> None:
        """
        Функция сохранения файла в папку
        Проверка docx файла на возможность открытия

        Вход: файл
        Выход: None
        """
        filepath = self.rundir / file.filename

        logger.info("FILE HANDLER : saving single docx file")
        try:
            with open(filepath, "wb") as f:
                f.write(await file.read())
            docx.Document(filepath)
        except Exception as e:
            logger.error(f"FILE HANDLER : {e}")
            raise FileProcessingError(f"Docx файл защищен паролем: {e}") from e

        logger.info("FILE HANDLER : all files saved")

    async def handle_file(self, file: UploadFile):
        """
        Функция обработки файла
        1. Проверка формата файла
        2. Распаковка файла

        Вход: файл
        Выход: None
        """
        try:
            if file.filename.endswith(".docx"):
                await self.unpack(file)
            else:
                logger.error("Handle file : Wrong file input")
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Ошибка"
                        "Неправильный формат файла. "
                        "Загрузите одну книгу в формате docx, "
                    ),
                )
        except FileProcessingError as e:
            raise HTTPException(status_code=500, detail=e.message) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e
