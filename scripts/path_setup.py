import sys
from pathlib import Path
'''
Make Python prioritize the parent directory of the current script file’s parent directory when importing modules.
'''
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))