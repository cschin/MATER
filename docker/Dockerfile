FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get install -y build-essential zlib1g zlib1g-dev libbz2-dev
RUN mkdir -p /opt/
WORKDIR /opt/

RUN  git clone https://github.com/cschin/MATER.git
RUN cd MATER && bash install_with_conda.sh 
RUN cp MATER/data/mmer2HLAtype.pickle  /opt/data/mmer2HLAtype.pickle
RUN . /opt/conda/bin/activate; conda clean --all

FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get install -y zlib1g
COPY --from=0 /opt/conda /opt/conda
COPY --from=0 /opt/data /opt/data
RUN . /opt/conda/bin/activate; conda activate mater; python3 -m pip install cffi==1.12.2
COPY bashrc /root/.bashrc
COPY entry.sh /opt/
ENTRYPOINT ["/opt/entry.sh"]
