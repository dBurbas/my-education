import pygame
from src.core.game_config import AppConfig
from src.visual.scenes import SceneManager, MainMenuScene


def main():
    pygame.init()

    config = AppConfig("config/config.json")

    pygame.display.set_caption("FallBlock Game")

    manager = SceneManager(config)
    manager.switch_scene(MainMenuScene(manager))

    manager.run()


if __name__ == "__main__":
    main()
