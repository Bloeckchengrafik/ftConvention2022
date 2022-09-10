import subprocess


VERSION = "1.0.0"
HASH = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()