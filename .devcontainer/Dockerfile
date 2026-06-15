FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/anaconda:1.3.10-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
USER vscode
COPY environment.yml /home/vscode
RUN <<EOF_USERSETUPINSTALL
conda config --add channels conda-forge
conda config --remove channels defaults
conda init bash
conda env create --file /home/vscode/environment.yml
rm /home/vscode/environment.yml
EOF_USERSETUPINSTALL
