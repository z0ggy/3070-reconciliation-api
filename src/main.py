from fastapi import FastAPI

from utils.match import match_data

result = match_data("dubln")
print(result)
