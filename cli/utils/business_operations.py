
class BusinessToggleReadiness:

    def __init__(self, business_id: str, table_style: str):
        self.token = HonulabsToken()
        self.api_client = HonulabsAPIClient(self.token.token)
        self.business_id = business_id
        self.table_style = table_style

    def run(self):
        """
        Toggle the product readiness in project
        """
        self.api_client.toggle_product_readiness()
