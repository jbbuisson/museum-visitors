# Museum Visitors Analysis

This project builds a harmonized database of the world's most visited museums (over 2 million annual visitors) and correlates their attendance with the population of their respective cities. Data is retrieved from Wikipedia and a reliable city population source, stored in SQLite, and analyzed using linear regression (scikit-learn). The project is containerized with Docker and includes a Jupyter notebook for interactive analysis.

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
## Docker
```bash
docker-compose up -d
docker-compose down
docker stop museum_db
docker rm museum_db
```

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
- config file + .env
- tests ???
- Use pathlib instead of os.path

## Docker
- secrets in docker compose

## Database
- visitors could be extracted to another table containing the museum id, the year, and the visitor count
- keep active connection

