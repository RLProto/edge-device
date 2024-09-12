# Docker compose with Nodered and PostgreSQL structured to run SODA VISION

## Requisites
You will need docker and docker compose plugin.

Use:
```bash
docker compose build
```

```bash
docker compose up
```

## Usage
Navigate to http://localhost:1880 to access the node-red
Search for opc.tcp://localhost:53880/UA/VisionOPC to access OPCUA Server