from fastapi import APIRouter

router = APIRouter()


@router.post("/mint")
async def mint_placeholder():
    return {"detail": "Provenance minting not yet implemented"}
