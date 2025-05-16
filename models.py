from  pydantic import BaseModel

class ModelData(BaseModel):
    product_id: str
    product_title: str
    product_price: str
    product_url: str
    product_rating: str
    brand: str
    color: str
    form_factor: str
    noise_control: str
    headphone_jack: str