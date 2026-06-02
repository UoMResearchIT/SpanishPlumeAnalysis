FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/anaconda:1.3.10-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN <<EOF_COMPILE
rm /opt/conda/.condarc
conda config --add channels conda-forge
umask 0002
/opt/conda/bin/conda env create --file /tmp/conda-tmp/environment.yml
rm -rf /tmp/conda-tmp
EOF_COMPILE

USER vscode
RUN <<EOF_USERSETUP
conda config --add channels conda-forge
conda config --remove channels defaults
conda init bash
EOF_USERSETUP
