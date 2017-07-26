from odoo import api, models, fields
from pprint import pprint

class hm_wiz_sale(models.TransientModel):
	_name = 'hm_wiz_sale'
	_description = 'Wizard Sale Order'

	name = fields.Char('name', default="Report Sales Order")
	order_ids = fields.Many2many('sale.order',string='Sale Order')
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir'		)
	customer_id = fields.Many2one('res.partner',string='Customer')
	pekerjaan_id = fields.Many2one('hm_pekerjaan',string='Pekerjaan')
	galian_id = fields.Many2one('hm_galian',string='Lokasi Galian')
	karyawan_id = fields.Many2one('hm_karyawan',string='Driver')
	# armada_id = fields.Many2one('Armada', related="karyawan_id.armada_id")
	nopol = fields.Char(' Nopol', related="karyawan_id.armada_id.name")
	product_id = fields.Many2one('product.template',string='Material')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  
	# currency_id = fields.Many2one('res.currency', string='Currency')
	grand_total = fields.Float('Grand Total', compute="_compute_grand_total")

	@api.depends('order_ids')
	def _compute_grand_total(self):
		for order in self.order_ids:
			self.grand_total += order.harga_total

		print 'Grand total : ' + str(self.grand_total)

	# @api.model
	def do_submit_report(self):
		# update state
		self.write({
				'state':'open'
			})

		# orders = self.env['sale.order'].search([('tanggal','>=',self.tanggal_awal),('tanggal','<=',self.tanggal_akhir)])

		by_customer = "true"
		if self.customer_id:
			by_customer = " partner_id = " + str(self.customer_id.id) + " "

		by_pekerjaan = "true"
		if self.pekerjaan_id:
			by_pekerjaan = " pekerjaan_id = " + str(self.pekerjaan_id.id) + " "

		by_galian = "true"
		if self.galian_id:
			by_galian = " galian_id = " + str(self.galian_id.id) + " "

		by_karyawan = "true"
		if self.karyawan_id:
			by_karyawan = " karyawan_id = " + str(self.karyawan_id.id) + " "

		by_product = "true"
		if self.product_id:
			by_product = " material = " + str(self.product_id.id) + " "

		by_kalkulasi = "true"
		if self.kalkulasi:
			by_kalkulasi = " kalkulasi = '" + str(self.kalkulasi) + "' "

		if len(self.order_ids) > 0:
			# clear data sebelumnya
			for old_order in self.order_ids:
				self.order_ids = [(3, old_order.id)]

		query = ('select id,name from sale_order where tanggal >= %s and tanggal <= %s and ' 
					+ by_customer + ' and ' + by_pekerjaan + ' and ' + by_galian + 
					' and ' + by_karyawan + ' and ' + by_product + ' and ' + by_kalkulasi
					+ ' order by (tanggal, name) asc')
		orders = self.env.cr.execute(query,
					(self.tanggal_awal, self.tanggal_akhir))
		for order in self.env.cr.fetchall():
			self.order_ids = [(4,order[0])]

	# Print Report on PDF
	def do_generate_report(self):
		print 'print pdf report'
		return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hasilmancing.hm_sale_order_report_template',
            'context': None,
        }

	# Format Currency on Report
	def _formatLang(self, value):
		lang = self.env.lang
		lang_objs = self.env['res.lang'].search([('code', '=', lang)])
		if not lang_objs:
			lang_objs = self.env['res.lang'].search([], limit=1)
		lang_obj = lang_objs[0]

		res = lang_obj.format('%.' + str(2) + 'f', value, grouping=True, monetary=True)
		currency_obj = self.env.ref('base.main_company').currency_id

		# if currency_obj and currency_obj.symbol:
		# 	if currency_obj.position == 'after':
		# 		res = '%s %s' % (res, currency_obj.symbol)
		# 	elif currency_obj and currency_obj.position == 'before':
		# 		res = '%s %s' % (currency_obj.symbol, res)
		
		return res

		
