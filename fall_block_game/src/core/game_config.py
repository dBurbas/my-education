import json
from dataclasses import dataclass


# TODO: docstrings
# TODO: typehints
@dataclass
class LogicConfig:
    grid_width: int
    grid_height: int
    lines_per_level: int
    max_level: int
    score_rewards: dict[str, int]
    blocks_data: list[dict]
    block_start_offset: dict
    speed_curve: dict[str, float]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            grid_width=data.get("grid_width", 10),
            grid_height=data.get("grid_height", 20),
            lines_per_level=data.get("lines_per_level", 10),
            max_level=data.get("max_level", 20),
            score_rewards=data.get(
                "score_rewards",
                {
                    "line_cleared": 100,
                    "hard_drop": 2,
                    "soft_drop": 1,
                },
            ),
            blocks_data=data.get("blocks", []),
            block_start_offset=data.get("start_offset", {"row": 0, "column": 3}),
            speed_curve=data.get(
                "speed_curve",
                {"base_time_sec": 0.8, "reduction_per_level": 0.007, "min_time_ms": 0},
            ),
        )


@dataclass
class VisualConfig:
    fps: int
    cell_size: int
    window_settings: dict
    colors: dict
    fonts: dict
    images: dict

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            fps=data.get("fps", 60),
            cell_size=data.get("cell_size_px", 30),
            window_settings=data.get("window", {}),
            colors=data.get("colors", {}),
            fonts=data.get("fonts", {}),
            images=data.get("images", {}),
        )


class AppConfig:
    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            raw_data: dict = json.load(f)

        self.logic = LogicConfig.from_dict(raw_data.get("logic", {}))
        self.visual = VisualConfig.from_dict(raw_data.get("visual", {}))
