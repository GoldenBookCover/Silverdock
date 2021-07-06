FROM elasticsearch:7.6.2
# COPY ./ik /usr/share/elasticsearch/plugins/ik
WORKDIR /usr/share/elasticsearch
RUN yum -y -q install wget unzip \
    && mkdir plugins/ik \
    && cd plugins/ik \
    && wget https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.6.2/elasticsearch-analysis-ik-7.6.2.zip \
    && unzip elasticsearch-analysis-ik-7.6.2.zip
# RUN && echo yes | ./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.6.2/elasticsearch-analysis-ik-7.6.2.zip