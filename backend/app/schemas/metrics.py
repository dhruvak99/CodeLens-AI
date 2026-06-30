from pydantic import BaseModel

from app.schemas.common import Metrics


class MetricsRequest(BaseModel):
    code: str


class MetricsResponse(Metrics):
    pass
