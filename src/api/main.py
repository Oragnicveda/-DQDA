"""FastAPI application for DQDA"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

from src.core.agent import DQDAAgent
from src.core.models.schemas import AnalysisResult


app = FastAPI(
    title="DQDA - Deal Qualification & Due Diligence Agent",
    description="AI-powered deal evaluation platform",
    version="0.1.0"
)

# Initialize agent
agent = DQDAAgent()


class AnalysisRequest(BaseModel):
    """Request model for analysis"""
    name: str
    founder: Dict[str, Any]
    market: Dict[str, Any]
    competition: Dict[str, Any]
    tokenomics: Optional[Dict[str, Any]] = None
    technical: Optional[Dict[str, Any]] = None
    pitch_deck_path: Optional[str] = None
    whitepaper_path: Optional[str] = None
    website_url: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok", version="0.1.0")


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_deal(request: AnalysisRequest):
    """Perform DQDA analysis on a deal
    
    Args:
        request: Analysis request with deal information
    
    Returns:
        Complete analysis result
    """
    try:
        # Convert request to dict
        deal_data = request.model_dump()
        
        # Remove None values for optional fields
        deal_data = {k: v for k, v in deal_data.items() if v is not None}
        
        # Run analysis
        result = agent.analyze(deal_data)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-batch")
async def analyze_batch(requests: list[AnalysisRequest]):
    """Perform batch analysis on multiple deals
    
    Args:
        requests: List of analysis requests
    
    Returns:
        List of analysis results
    """
    results = []
    errors = []
    
    for i, request in enumerate(requests):
        try:
            deal_data = request.model_dump()
            deal_data = {k: v for k, v in deal_data.items() if v is not None}
            result = agent.analyze(deal_data)
            results.append(result)
        except Exception as e:
            errors.append({
                "request_index": i,
                "deal_name": request.name,
                "error": str(e)
            })
    
    return {
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors
    }


@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "DQDA - Deal Qualification & Due Diligence Agent",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
            "batch_analyze": "/analyze-batch",
            "docs": "/docs"
        },
        "description": "AI-powered deal evaluation and founder qualification system"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
