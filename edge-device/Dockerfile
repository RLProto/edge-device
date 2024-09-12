FROM nodered/node-red:latest-debian
COPY flows.json /data/flows.json

USER root

RUN npm install --save node-red-contrib-opcua
RUN npm install --save @mnn-o/node-red-rabbitmq

# User configuration directory volume
VOLUME ["/data"]
EXPOSE 1880
EXPOSE 53880
EXPOSE 5432

# Environment variable holding file path for flows configuration
ENV FLOWS=flows.json

CMD ["npm", "start", "--", "--userDir", "/data"]