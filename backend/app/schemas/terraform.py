from pydantic import BaseModel

class TerraformState(BaseModel):
    workspace: str
    cloud_provider: str
    resources_provisioned: int
    state_status: str