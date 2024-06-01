from fastapi import APIRouter
from worldcup_maker.service import generate_candidates, extract_bracketed_strings
from worldcup_simulator.schemas import GenerateCandidatesRequest, GenerateCandidatesResponse

router = APIRouter(tags=['worldcup'])

@router.post("/generate_candidates", response_model=GenerateCandidatesResponse)
async def generate_candidates_endpoint(request: GenerateCandidatesRequest):
    candidates_text = generate_candidates(request.prompt, request.num_candidates)
    new_description, candidates = extract_bracketed_strings(candidates_text)
    return GenerateCandidatesResponse(new_description=new_description, candidates=candidates)
