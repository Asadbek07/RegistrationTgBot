from typing import List
from models.product import Product, session

class ProductService:

    @staticmethod
    def get_all_products() -> List[Product]:
        return list(session.query(Product).all())

    @staticmethod
    def validate_product(product_name: str) -> bool:
        exists = ProductService.get_by_name(product_name)

        if exists is None:
            return False
        
        return True
        

    @staticmethod
    def get_by_name(product_name: str) -> Product:
        # product_name will be in this format - [product_name] ([product cost]) -> [product_name]
        # that is what we need 
        actual_product_name = product_name.split(' ')[0]
        
        product = session.query(Product).filter(Product.name == actual_product_name).first()
        
        return product


    @staticmethod
    def add_product(product_name: str, cost: str, image_id: str) -> Product:
        product = Product(name=product_name, cost=cost, image_id=image_id)
        
        session.add(product)
        session.commit()
        
        return product

    @staticmethod
    def delete_by_name(product_name: str) -> Product:
        product = ProductService.get_by_name(product_name)
        if product is not None:
            session.delete(product)
            session.commit()
        
        return product