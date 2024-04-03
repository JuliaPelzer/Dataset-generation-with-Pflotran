# git clone --depth=100 --branch=releases/v0.21 https://github.com/spack/spack.git ~/spack
# cd ~/spack
## in destination folder for venv (cd DESTINATION):
# . share/spack/setup-env.sh
# spack install python
# spack install py-pip
# pip install -r requirements.txt
# spack install petsc
# spack install pflotran
# copy (petsc and) pflotran, (python, pip) link to ~/.bashrc.my