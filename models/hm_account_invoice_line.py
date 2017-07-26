from odoo import api, fields, models

class hm_account_invoice_line(models.Model):
	_inherit = "account.invoice.line"


	order_line_ids = fields.Many2many("sale.order.line","sale_order_line_invoice_rel","invoice_line_id","order_line_id", string='Sale Order Lines')
	