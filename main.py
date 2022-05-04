from database import DatabaseMananger
from dotenv import load_dotenv
from decimal import Decimal

if __name__ == "__main__":
    load_dotenv()

    manager = DatabaseMananger()
    # result = manager.insert("northwind.products", {
    #     "productid": 101,
    #     "productname": "Teste", 
    #     "supplierid": 12, 
    #     "categoryid": 4, 
    #     "quantityperunit": 12,
    #     "unitprice": Decimal(10),
    #     "unitsinstock": 50,
    #     "unitsonorder": 0,
    #     "reorderlevel": 100,
    #     "discontinued": "N"
    # })
    # print(result)

    products = manager.find("northwind.products", { "productid": 1 })
    product = manager.findOne("northwind.products", { "productid": 101 })
    print(product)

    manager.close()

