from fastapi import FastAPI,Depends
from models import Product
from database import sessionmaker,session
from database import engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
#from database import SessionLocal

#db = SessionLocal()
import database_models
#backend


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello "

# list of products with 4 products like phones, laptops, pens, tables
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db =  session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = session()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

    db.close()

init_db()

@app.get("/products/")
def get_all_products(db:Session = Depends(get_db)):
    db_products =  db.query(database_models.Product).all()
    #db = session()
    #db.query()
    return db_products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
            return db_product
    return {"error": "Product not found"}

@app.post("/products/")
def create_product(product: Product):
    products.append(product)
    return {"message": "Product created successfully", "product": product}
    
@app.put("/products/{id}")
def update_product(id:int, product:Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return"product added sucessfully"
        


@app.delete("/products")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return"product deleted"
        
    return"product not found"