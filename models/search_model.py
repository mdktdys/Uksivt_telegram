from pydantic import BaseModel, ConfigDict 


class SearchResult(BaseModel):
    model_config = ConfigDict(strict=True)
    
    search_type: str
    search_id: int
    search_image: str
    search_name: str
