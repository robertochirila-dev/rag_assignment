from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .recommender import BraFittingRAG, InputValidationError, MeasurementExtractionError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

recommender = BraFittingRAG()

@app.post("/api/bra-fitting")
async def get_fitting_recommendation(query: Query):
    if not query.text or not isinstance(query.text, str) or not query.text.strip():
        raise HTTPException(status_code=422, detail="Input must be a non-empty string.")
    try:
        result = recommender.get_recommendation(query.text)
        if "error" in result and result["error"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except (InputValidationError, MeasurementExtractionError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
