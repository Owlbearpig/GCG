from pathlib import Path
import os

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
generation_dir = ROOT_DIR / Path('generation')
mask_dir = generation_dir / Path('gcode_masks')
