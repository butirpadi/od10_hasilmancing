from odoo import api, models, fields
from pprint import pprint

class hm_wiz_purchase(models.TransientModel):
	_name = 'hm_wiz_purchase'
	_description = 'Wizard Purchase Order'

	name = fields.Char('name', default="Report Purchase Order")
	order_ids = fields.Many2many('purchase.order',string='Purchase Order')
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir'		)
	supplier_id = fields.Many2one('res.partner',string='Supplier')
	sparepart_id = fields.Many2one('product.template',string='Sparepart')

	@api.depends('order_ids')
	def _compute_grand_total(self):
		for order in self.order_ids:
			self.grand_total += order.harga_total

		print 'Grand total : ' + str(self.grand_total)

	# # @api.model
	def do_submit_report(self):
		print 'submit report'
		# # update state
		# self.write({
		# 		'state':'open'
		# 	})

		by_supplier = "true"
		if self.supplier_id:
			by_supplier = " partner_id = " + str(self.supplier_id.id) + " "

	# 	by_product = "true"
	# 	if self.product_id:
	# 		by_product = " material = " + str(self.product_id.id) + " "

	# 	if len(self.order_ids) > 0:
	# 		# clear data sebelumnya
	# 		for old_order in self.order_ids:
	# 			self.order_ids = [(3, old_order.id)]

		query = ('select id,name from purchase_order where tanggal >= %s and tanggal <= %s and ' 
					+ by_supplier + ' order by (tanggal, name) asc')
		orders = self.env.cr.execute(query,
					(self.tanggal_awal, self.tanggal_akhir))
		for order in self.env.cr.fetchall():
			self.order_ids = [(4,order[0])]

	# # Print Report on PDF
	# def do_generate_report(self):
	# 	print 'print pdf report'
	# 	return {
 #            'type': 'ir.actions.report.xml',
 #            'report_name': 'hasilmancing.hm_purchase_order_report_template',
 #            'context': None,
 #        }

	# # Format Currency on Report
	# def _formatLang(self, value):
	# 	lang = self.env.lang
	# 	lang_objs = self.env['res.lang'].search([('code', '=', lang)])
	# 	if not lang_objs:
	# 		lang_objs = self.env['res.lang'].search([], limit=1)
	# 	lang_obj = lang_objs[0]

	# 	res = lang_obj.format('%.' + str(2) + 'f', value, grouping=True, monetary=True)
	# 	currency_obj = self.env.ref('base.main_company').currency_id

	# 	# if currency_obj and currency_obj.symbol:
	# 	# 	if currency_obj.position == 'after':
	# 	# 		res = '%s %s' % (res, currency_obj.symbol)
	# 	# 	elif currency_obj and currency_obj.position == 'before':
	# 	# 		res = '%s %s' % (currency_obj.symbol, res)
		
	# 	return res

		
