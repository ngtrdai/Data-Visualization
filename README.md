# $${\textsf{\color{green}DATA}}{\textsf{\color{black}VIZ}}$$

[![DATAVIZ API CI](https://github.com/ngtrdai/Data-Visualization/actions/workflows/backend-ci.yaml/badge.svg)](https://github.com/ngtrdai/Data-Visualization/actions/workflows/backend-ci.yaml)
[![DATAVIZ ANALYZER API CI](https://github.com/ngtrdai/Data-Visualization/actions/workflows/analyzer-ci.yaml/badge.svg)](https://github.com/ngtrdai/Data-Visualization/actions/workflows/analyzer-ci.yaml)
[![DATAVIZ FRONTEND CI](https://github.com/ngtrdai/Data-Visualization/actions/workflows/frontend-ci.yaml/badge.svg)](https://github.com/ngtrdai/Data-Visualization/actions/workflows/frontend-ci.yaml)

**DATAVIZ** is a modern data exploration and data visualization platform.
## Tentative technologies and frameworks
- Laravel 10
- FastAPI
- NuxtJs 3
- GitHub Actions
- SonarCloud
## Local development architecture
![DataViz - local development architecture](https://github.com/ngtrdai/Data-Visualization/blob/main/DataViz-Architecture.png)
## Getting started with Docker Compose
1. Get the latest source code
2. Add the following records to your host file: 
```
127.0.0.1 api.dataviz.local
127.0.0.1 analyzer.dataviz.local
127.0.0.1 identity.dataviz.local
127.0.0.1 pgadmin.dataviz.local
127.0.0.1 dataviz.local
```
3. Open terminal of your choice, go to `Data-Visualiztion` directory, run `docker compose up`, wait for all the containers up and running
4. Open your browser, now you can access the websites via `http://dataviz.local/` login with admin/admin
#### You might also want to explore:
1. `http://pgadmin.dataviz.local/`. Account login: `admin@dataviz.io.vn` / admin. Register a server: postgres, port 5432, username admin, password admin. The Postgresql server is also exposed to the host machine: servername: localhost, port: 5432, username: admin, password: admin
2. `http://identity.dataviz.local/`. Account login: `admin` / `admin`
3. `http://api.dataviz.local` for API documentation
4. `http://analyzer.dataviz.local/docs` for Analyzer API documentation
