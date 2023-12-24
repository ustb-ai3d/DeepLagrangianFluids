FROM tensorflow/tensorflow:2.3.4-gpu-jupyter
ENV TZ Asia/Shanghai
# ENV http_proxy=...
# ENV https_proxy=...
RUN apt-key del 7fa2af80 && sed -i '/developer\.download\.nvidia\.com\/compute\/cuda\/repos/d' /etc/apt/sources.list.d/* && sed -i '/developer\.download\.nvidia\.com\/compute\/machine-learning\/repos/d' /etc/apt/sources.list.d/*
RUN apt install wget -y && wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && dpkg -i cuda-keyring_1.0-1_all.deb
RUN ln -s libnvidia-ml.so.1 /usr/lib/x86_64-linux-gnu/libnvidia-ml.so
RUN apt update && apt install -y openssh-server git vim cmake xorg-dev freeglut3-dev build-essential libcap-dev libtbb-dev libilmbase-dev libopenexr-dev libbz2-dev && pip install open3d==0.11 msgpack msgpack-numpy zstandard SciPy plyfile pyyaml addict pandas partio python-prctl
RUN pip install --upgrade git+https://github.com/tensorpack/dataflow.git scikit-learn
RUN pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html


RUN sed -i 's/^PermitRootLogin/#PermitRootLogin/g' /etc/ssh/sshd_config && sed -i '$aPermitRootLogin yes' /etc/ssh/sshd_config
VOLUME /workdir
WORKDIR /workdir
CMD source /etc/bash.bashrc && jupyter notebook --notebook-dir=/workdir --ip 0.0.0.0 --no-browser --allow-root
EXPOSE 22 6006
