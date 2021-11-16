from pathlib import Path
import os

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
mask_dir = ROOT_DIR / Path('generation') / Path('gcode_masks')

print(mask_dir)
