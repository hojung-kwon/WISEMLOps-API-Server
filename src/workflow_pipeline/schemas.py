from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Pipeline(BaseModel):
    pipeline_name : str
    nodes : str
    edges : str
    position : str
    zoom : str
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()