from fastapi import APIRouter
from app.schemas.terraform import TerraformState
from app.services.terraform_service import get_terraform_state

router = APIRouter(prefix="/api", tags=["Terraform IaC"])

@router.get("/state", response_model=TerraformState)
def terraform_state():
    return get_terraform_state()