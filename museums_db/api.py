from fastapi import FastAPI
from museums_db.db import get_museum_city_data
from museums_db.model import run_regression

app = FastAPI()

@app.get("/regression")
def regression():
	df = get_museum_city_data()
	model, coef, intercept, score = run_regression(df)
	return {
		"coefficient": coef.tolist(),
		"intercept": intercept,
		"r2_score": score
	}
