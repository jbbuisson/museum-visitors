# Museum Visitors Analysis

This project builds a harmonized database of the world's most visited museums (over 2 million annual visitors) and correlates their attendance with the population of their respective cities.

The project is containerized with Docker and includes a MySQL database and Jupyter notebook for interactive analysis.

## Overview
- Data:
    - is retrieved from:
        - Wikipedia for museum data
        - GeoNames for city population
    - stored in a MySQL database
- Analysis is done:
    - in a Jupyter notebook
    - using linear regression (scikit-learn).
    
## Prerequisites
- A free personal API token from Wikipedia (https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs)
- 

## Features
- Automated data retrieval from Wikipedia API
- City population data integration
- SQLite database for rapid prototyping
- Linear regression model to correlate city population and museum visitors
- Flask/FastAPI API for future scalability
- Jupyter notebook for data exploration and visualization
- Docker & Docker Compose setup

## Rationale
- Wikipedia API ensures authoritative, up-to-date museum data
- SQLite is lightweight and easy to scale up
- scikit-learn is standard for rapid ML prototyping
- Docker ensures reproducibility and easy deployment

## Usage
See the Jupyter notebook in `notebooks/` for analysis and instructions. Run the project using Docker Compose.

# Notes
## MySQL
1. Connexion au docker
```bash
docker exec -it museum_db mysql -uroot -p
```

2. Selection de la BD
```sql
use museum_db
```

3. Create table
```sql
create table my_example(my_col char);
show tables;
```

4. Quit Mysql
```sql
\q
```

# Design

## Application
- Design patterns ????
- Cache
- assert
- config file + .env (WIKIMEDIA_API_KEY not found in jupyter. To be added to docker secrets ????)
- tests ???
- Use pathlib instead of os.path
- Gestion des erreurs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
- log ??

## Docker
- secrets in docker compose

## Database
- visitors could be extracted to another table containing the museum id, the year, and the visitor count
- keep active connection

