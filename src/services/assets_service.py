from aiogram.types import InputFile
from io import BytesIO
from pathlib import Path


class AssetsService:
    def __init__(self) -> None:
        self._assets_dir = Path("src/assets")
        self._images: dict[str, InputFile] = {}

        self._load_images()

    def _load_images(self) -> None:
        for file in self._assets_dir.glob("*.png"):
            image_bytes = BytesIO(file.read_bytes())
            image_bytes.name = file.name
            self._images[file.stem] = InputFile(image_bytes, filename=file.name)

    def get_image(self, name: str) -> InputFile:
        """
        Получить InputFile по имени без расширения, например: get_image("timings")
        """
        image: InputFile | None = self._images.get(name)
        if not image:
            raise ValueError(f"Изображение '{name}' не найдено в assets.")
        return image
