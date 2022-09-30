import subprocess


VERSION = "1.0.0"
HASH = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
SORTER_IP="192.168.188.24"
CALIB_IN_PROGRESS=False