from odoo import api, fields, models

class hm_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # order_id_temp = fields.Many2one('sale.order', 
    	# string='Order Reference Temp')