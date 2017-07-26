from odoo import api, models, fields

class hm_product(models.Model):
    _inherit = "product.product"


    stock_ids = fields.One2many('stock.inventory', 'product_id' , string='Stock')