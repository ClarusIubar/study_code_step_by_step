def approved_product(product):
    product_table = {
    "비타500" : 1000, 
    "코코팜" : 1500, 
    "TOP커피" : 2000,
}
    # price_for_product
    price_product = product_table[product]
    return product, price_product

