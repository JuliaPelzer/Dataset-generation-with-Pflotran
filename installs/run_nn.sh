pyenv activate test_nn
module load cuda-11.2.1
cd ~/test_nn/3D_FCN/
python3 /home/pelzerja/pelzerja/test_nn/3D_FCN/main_remote.py 1

# nohup damit es weiterläuft, wenn ich die verbindung trenne