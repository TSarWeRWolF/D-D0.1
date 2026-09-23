from pathlib import Path
import pygame


ASSETS_DIR = Path(
    "/home/a/PycharmProjects/PythonProject/D&D/Assetsd&d"
)

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".gif",
}


class AssetManager:

    def __init__(self):
        self.images = {}

    def load_images(self):

        if not ASSETS_DIR.exists():
            print(f"ОШИБКА: папка не найдена:")
            print(ASSETS_DIR)
            return

        print("Загрузка ассетов...")
        print()

        for file_path in ASSETS_DIR.iterdir():

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            try:
                image = pygame.image.load(
                    str(file_path)
                ).convert_alpha()

                name = file_path.stem.lower()

                self.images[name] = image

                print(
                    f"[OK] {file_path.name} "
                    f"-> {name}"
                )

            except pygame.error as error:

                print(
                    f"[ERROR] {file_path.name}: "
                    f"{error}"
                )

        print()
        print(
            f"Загружено изображений: "
            f"{len(self.images)}"
        )

    def get(self, name):

        name = Path(name).stem.lower()

        return self.images.get(name)