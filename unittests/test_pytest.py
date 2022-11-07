import subprocess
import os

def test_run_bash_pressure_1D():
    os.getcwd()
    subprocess.call("bash ../make_dataset_2.sh 1 test_bash_1D 1D", shell=True)
    assert _fcount("test_bash_1D") == 1, "1D created too little runs"
    os.system("rm -r test_bash_1D")

def test_run_bash_pressure_2D():
    os.getcwd()
    subprocess.call("bash ../make_dataset_2.sh 1 test_bash_2D 2D", shell=True)
    assert _fcount("test_bash_2D") == 4, "2D created too little runs"
    os.system("rm -r test_bash_2D")

def _fcount(path):
  count = 0
  for f in os.listdir(path):
    child = os.path.join(path, f)
    if os.path.isdir(child):
      count += + 1
  return count