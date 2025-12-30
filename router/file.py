

from fastapi import APIRouter, UploadFile, File,Request
import shutil, os

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

# Ensure folder exists
os.makedirs("media/products", exist_ok=True)

@router.post("/uploadfile")
def upload_file(request:Request,upload_file: UploadFile = File(...)):
    filename = upload_file.filename
    path = f"media/products/{filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # URL saved in DB
    # image_url = f"/media/products/{filename}"
    # return {"image_url": image_url}
    image_url = str(request.base_url) + f"media/products/{filename}"
    return {"image_url": image_url}

