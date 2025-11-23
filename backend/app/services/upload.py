import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from PIL import Image
from ..core.config import settings


class UploadService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_image(self, file: UploadFile) -> bool:
        """Validate image file"""
        # Check extension
        ext = file.filename.split('.')[-1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        return True
    
    async def save_image(self, file: UploadFile, folder: str = "images") -> str:
        """Save uploaded image and return URL"""
        self.validate_image(file)
        
        # Create unique filename
        ext = file.filename.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        
        # Create folder path
        folder_path = self.upload_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = folder_path / filename
        
        try:
            # Read file content
            content = await file.read()
            
            # Validate it's a real image
            try:
                img = Image.open(file.file)
                img.verify()
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid image file")
            
            # Reset file pointer and save
            await file.seek(0)
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # Optimize image
            self._optimize_image(file_path)
            
            # Return relative URL
            return f"/uploads/{folder}/{filename}"
        
        except Exception as e:
            # Clean up on error
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
    
    def _optimize_image(self, file_path: Path):
        """Optimize image for web"""
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large (max 1920px width)
                max_width = 1920
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save optimized
                img.save(file_path, optimize=True, quality=85)
        except Exception:
            # If optimization fails, keep original
            pass
    
    def delete_file(self, file_url: str):
        """Delete a file"""
        try:
            file_path = self.upload_dir / file_url.lstrip('/uploads/')
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass


upload_service = UploadService()
