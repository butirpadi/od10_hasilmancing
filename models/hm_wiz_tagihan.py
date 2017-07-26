from odoo import api, models, fields
from pprint import pprint

class hm_wiz_tagihan(models.TransientModel):
	_name = 'hm_wiz_tagihan'
	_description = 'Wizard Tagihan'

	name = fields.Char('name', default="Report Tagihan")
	order_ids = fields.Many2many('sale.order',string='Sale Order')
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir'		)
	customer_id = fields.Many2one('res.partner',string='Customer')
	pekerjaan_id = fields.Many2one('hm_pekerjaan',string='Pekerjaan')
	product_id = fields.Many2one('product.template',string='Material Org')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  
	# currency_id = fields.Many2one('res.currency', string='Currency')
	grand_total = fields.Float('Grand Total', compute="_compute_grand_total")
	product_selection_id = fields.Many2one('hm_product_selection', string="Material")

	@api.onchange('product_selection_id')
	def on_product_id_change(self):
		if self.customer_id and self.pekerjaan_id:
			self.product_id = self.product_id.search([('id','=',self.product_selection_id.id)]) # bermasalah

	@api.onchange('customer_id','pekerjaan_id')
	def change_product_selection(self):
		# print 'Tanggal awal : ' + str(self.tanggal_awal)
		# print 'Tanggal akhir : ' + str(self.tanggal_akhir)
		if self.customer_id and self.pekerjaan_id:
			# delete old value on hm_product_selection
			self.env.cr.execute('delete from hm_product_selection')
			# self.invalidate_cache()
			by_customer = "true"
			if self.customer_id:
				by_customer = " partner_id = " + str(self.customer_id.id) + " "

			by_pekerjaan = "true"
			if self.pekerjaan_id:
				by_pekerjaan = " pekerjaan_id = " + str(self.pekerjaan_id.id) + " "

			query_get_material = ('select material,product_template.name from sale_order \
						INNER JOIN product_template on (sale_order.material = product_template.id) \
						where tanggal >= %s and tanggal <= %s and ' 
						+ by_customer + ' and ' + by_pekerjaan 
						+ ' group by sale_order.material, product_template.name')
			self.env.cr.execute(query_get_material,(self.tanggal_awal, self.tanggal_akhir))
			for mat in self.env.cr.fetchall():
				self.env.cr.execute('insert into hm_product_selection (id,name) values (%s, %s)',(mat[0],mat[1]))
				# res.append((mat[0],mat[1]))
				# self.invalidate_cache()
			# return res


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

		by_customer = "true"
		if self.customer_id:
			by_customer = " partner_id = " + str(self.customer_id.id) + " "

		by_pekerjaan = "true"
		if self.pekerjaan_id:
			by_pekerjaan = " pekerjaan_id = " + str(self.pekerjaan_id.id) + " "

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
					+ by_customer + ' and ' + by_pekerjaan 
					+ ' and ' + by_product + ' and ' + by_kalkulasi
					+ ' order by (tanggal, name) asc')
		orders = self.env.cr.execute(query,
					(self.tanggal_awal, self.tanggal_akhir))
		for order in self.env.cr.fetchall():
			self.order_ids = [(4,order[0])]

	# Print Report
	def do_print_report(self):
		if not self.product_id:
			# print 'Get Materials on do_print_report'
			# # Get Material/product
			# materials = []
			# query = ("select material from sale_order where tanggal >= %s and tanggal <= %s \
			# 			and partner_id = %s and pekerjaan_id = %s \
			# 			group by material")
			# # get data material
			# self.env.cr.execute(query,
			# 		(self.tanggal_awal, self.tanggal_akhir, self.customer_id.id, self.pekerjaan_id.id))
			# for mat in self.env.cr.fetchall():
			# 	materials.append(mat[0])
			# 	print 'material id : ' + str(mat[0])
			print 'Print Custom Tagihan Report'
			context = dict({}, active_ids=[self.id], active_model=self._name)
			return {
	            'type': 'ir.actions.report.xml',
	            'report_name': 'hasilmancing.hm_wiz_tagihan_custom_report_template',
	            'context': context,
	        }	
		else:
			print 'Print Report ' + str(self.product_id.name)

	# Print Report on PDF
	def do_generate_report(self):
		print 'print pdf report'
		return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hasilmancing.hm_wiz_tagihan_report_template',
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
		
		return res

		
