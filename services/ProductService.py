from typing import List
from models.product import Product, session

class ProductService:

    @staticmethod
    def get_all_products() -> List[Product]:
        return list(session.query(Product).all())

    @staticmethod
    def validate_product(product_name: str) -> bool:
        # product_name will be in this format - [product_name] ([product cost]) -> [product_name]
        # that is what we need 
        actual_product_name = product_name.split(' ')[0]
        exists = session.query(Product).filter(Product.name == actual_product_name).first()
        
        if exists is None:
            return False
        
        return True
        

    @staticmethod
    def add_product(product_name: str, cost: str) -> Product:
        product = Product(name=product_name, cost=cost)
        
        session.add(product)
        session.commit()
        
        return product
