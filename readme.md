# Instructions

Just download the dataset from https://zenodo.org/records/13983082

make a docker-compose.yaml

paste this in there 

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:17
    command: postgres -c 'max_connections=1000'
    container_name: morefixes_db
    restart: always
    env_file:
      - .env
    ports:
      - "${POSTGRES_PORT}:${POSTGRES_PORT}"
    volumes:
      - postgres_data2:/var/lib/postgresql/data
      - ./postgrescvedumper-2024-09-26.sql:/docker-entrypoint-initdb.d/postgrescvedumper-2024-09-26.sql
      

volumes:
  postgres_data2:

```
Access the postgres dump using 

docker exec -it 73554d20a66f755fe9d6b06fefef051524a85e480b44f786835924168488f495 bash

psql -U postgrescvedumper