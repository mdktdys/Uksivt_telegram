from aiogram.types import FSInputFile, BufferedInputFile
from io import BytesIO
from pathlib import Path


class AssetsService:
    def __init__(self) -> None:
        self._assets_dir = Path("src/assets")
        self._images: dict[str, BufferedInputFile] = {}

        self._load_images()

    def _load_images(self) -> None:
        for file in self._assets_dir.glob("*.*"):
            if file.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue

            data = file.read_bytes()
            name = file.name
            self._images[file.stem] = BufferedInputFile(data=data, filename=name)

    def get_image(self, name: str) -> BufferedInputFile:
        image = self._images.get(name)
        if not image:
            raise ValueError(f"Изображение '{name}' не найдено.")
        return image
