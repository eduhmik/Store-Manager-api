class Sales():
    sales_id = 0
    sales = []
    """initializing the constructor"""
    def __init__(self, product_name, quantity, total, seller):
        self.sales_id = len(Sales.sales) + 1
        self.product_name = product_name
        self.quantity = quantity
        self.total = total
        self.seller = seller

    def create_sale(self):
        """Method to create a new sale into list"""
        sales_item = dict(
            sales_id = self.sales_id,
            product_name = self.product_name,
            quantity = self.quantity,
            total = self.total,
            seller = self.seller
        ) 
        """Adding the sale into sales list"""   
        self.sales.append(sales_item)
        return sales_item

    """method to fetch for all sales records"""
    def get_all_sales (self):
    
        return Sales.sales

    """method to fetch for a single sale record by id"""
    def get_single_sale (self, sales_id):
        sales_item = [sale for sale in Sales.sales if sale['sales_id'] == sales_id]
        if sales_item:
            return sales_item
        return {'message':'sale not found'}
