"""Пример эндпоинта"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse


from app.utils.file_handler import FileHandler
from app.services.workflow import workflow


router = APIRouter()


@router.post("/app-name")
async def app(file: UploadFile = File(...)):
    """
    Док
    """
    # 1. Init filehandler
    file_handler = FileHandler()
    await file_handler.handle_file(file)
    # 2. Agent call
    output = workflow(file_handler.rundir, file.filename)
    return FileResponse(
        path=output,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=output.name
        )
