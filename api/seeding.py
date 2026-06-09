from api.database import realtors_collection, properties_collection
from core.logger import get_logger
from core.security import get_password_hash
from core.env import DEFAULT_PASSWORD

logger = get_logger("imob_seeding")

async def seed_database():
    """Populates the database with 1 realtor and 4 properties if it is empty."""
    if await realtors_collection.count_documents({}) == 0:
        logger.info("Empty database. Seeding Properties and Realtors...")
        
        corretor = {
            "document_number": "123456789-10", "name": "Glovis Moglubis",
            "email": "realtor@jadno.tech", "phone": "+5511999999999",
            "password": get_password_hash(DEFAULT_PASSWORD),
            "address": {"street": "Av Paulista", "city": "São Paulo", "state": "SP", "zip_code": "01310-000", "country": "BR"}
        }
        await realtors_collection.insert_one(corretor)

        imoveis_iniciais = [
            {
                "title": "Mansão Contemporânea", 
                "address": {"street": "Rua Oscar Freire", "city": "São Paulo", "state": "SP", "zip_code": "01426-001", "country": "BR"}, 
                "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800", 
                "realtor_email": "realtor@jadno.tech"
            },
            {
                "title": "Cobertura Duplex", 
                "address": {"street": "Av. Delfim Moreira", "city": "Rio de Janeiro", "state": "RJ", "zip_code": "22441-000", "country": "BR"}, 
                "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800", 
                "realtor_email": "realtor@jadno.tech"
            },
            {
                "title": "Casa de Campo Premium", 
                "address": {"street": "Condomínio Fazenda", "city": "Itu", "state": "SP", "zip_code": "13300-000", "country": "BR"}, 
                "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800", 
                "realtor_email": "realtor@jadno.tech"
            },
            {
                "title": "Apartamento Boutique", 
                "address": {"street": "Batel", "city": "Curitiba", "state": "PR", "zip_code": "80420-090", "country": "BR"}, 
                "image_url": "https://images.unsplash.com/photo-1502672260266-1c1e52416453?auto=format&fit=crop&w=800", 
                "realtor_email": "realtor@jadno.tech"
            }
        ]
        await properties_collection.insert_many(imoveis_iniciais)
        logger.info("Seeding completed successfully.")
