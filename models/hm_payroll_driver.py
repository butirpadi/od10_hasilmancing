from odoo import api, models, fields
import datetime
import timestring
import pytz
from pprint import pprint

class hm_payroll_driver(models.Model):
	_name = "hm_payroll_driver"

	name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	karyawan_id = fields.Many2one('hm_karyawan', required=True)
	tanggal =fields.Date('Tanggal', required=True,default=datetime.date.today())
	periode_awal =fields.Date('Periode Awal', required=True,)
	periode_akhir =fields.Date('Periode Akhir', required=True,)
	#stock_picking_rel_ids = fields.One2many('hm_payroll_driver_stock_picking_rel','payroll_id','Delivery Order')
	total = fields.Float(compute='_compute_total', string='Total', store=True)
	potongan_bahan = fields.Float('Potongan Bahan')
	potongan_bon = fields.Float('Potongan Bon')
	sisa_bayaran_kemarin = fields.Float('Sisa Bayaran Kemarin')
	downpayment = fields.Float('DP')
	nett = fields.Float(compute='_compute_nett', string='Nett', store=True)
	notes = fields.Text('Catatan')
	# pay_week_id = fields.Many2one('hm_pay_week')
	# bulan = fields.Selection([ 
				# (0,'JANUARI'),
				# (1, 'FEBRUARI'),
				# (2, 'MARET'),
				# (3, 'ARPIL'),
				# (4, 'MEI'),
				# (5, 'JUNI'),
				# (6, 'JULI'),
				# (7, 'AGUSTUS'),
				# (8, 'SEPTEMBER'),
				# (9, 'OKTOBER'),
				# (10, 'NOVEMBER'),
				# (11, 'DESEMBER'),
				# ],required=True, default=1)
	# tahun = fields.Many2one('hm_generate_pay_week', required=True)
	generate_id = fields.Many2one('hm_generate_pay_driver', ondelete='cascade')

	# revisi
	material_rel_ids= fields.One2many('hm_payroll_driver_material_rel','payroll_id','Delivery Order')
	# order_ids = fields.Many2many('sale.order', string="Sale Order")

	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  

	def direct_print_slip_gaji(self):
		print 'direct print slip gaji'

	# get default catatan
	def _get_default_catatan(self):
		catatan = self.env['hm_appkonfig'].search([('name','=','catatan_pay_slip')])

	# @api.onchange('tahun'):
	# def tahun_bulan_change(self):
	# 	print 'change tahun'

	@api.depends('material_rel_ids')
	def _compute_total(self):
		for pay in self:
			total_jumlah = 0
			for line in pay.material_rel_ids:
				total_jumlah += line.jumlah

			pay.update({
	                'total': total_jumlah
	            })

	@api.depends('total','potongan_bahan','potongan_bon','sisa_bayaran_kemarin','downpayment')
	def _compute_nett(self):
		for pay in self:
			pay.update({
	                'nett': pay.total - pay.potongan_bahan - pay.potongan_bon + pay.sisa_bayaran_kemarin + pay.downpayment
	            })

	@api.model
	def create(self, vals):
		if vals.get('name', ('New')) == ('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hm.payroll.seq') or ('New')
	
		result = super(hm_payroll_driver, self).create(vals)
		return result

	def show_delivery_order(self):
		self.state = "open"
		DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
		akhir = ""
		awal = ""
		awal_utc_str = ""
		akhir_utc_str = ""

		localtz = pytz.timezone('Asia/Jakarta')	
		# print 'Periode Awal ' + self.periode_awal
		# print 'Periode Akhir ' + self.periode_akhir
		periode_awal_date = timestring.Date(self.periode_awal)
		periode_akhir_date = timestring.Date(self.periode_akhir)

		periode_awal_local_str = localtz.localize(datetime.datetime.strptime(str(periode_awal_date), DATETIME_FORMAT))
		periode_awal_utc_str = periode_awal_local_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)
		
		periode_akhir_local_str = localtz.localize(datetime.datetime.strptime(str(periode_akhir_date), DATETIME_FORMAT))
		periode_akhir_utc_str = periode_akhir_local_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)


		# get data sale orders
		orders = self.env['sale.order'].search([
														('karyawan_id','=',self.karyawan_id.id),
														('tanggal','>=',periode_awal_utc_str),
														('tanggal','<=',periode_akhir_utc_str)
													])
		data_materials = []
		data_materials_opt = []
		for sale_order in orders:
			rit = 1 if sale_order.kalkulasi == 'ritase' else 0
			vol = sale_order.volume if sale_order.kalkulasi == 'kubikasi' else 0
			net = sale_order.netto if sale_order.kalkulasi == 'tonase' else 0


			
			for sale_order_line in sale_order:
				mat = {
						'material_id' : sale_order_line.product_id.id,
						'kalkulasi' : sale_order.kalkulasi,
						'pekerjaan_id' : sale_order.pekerjaan_id.id,
						'rit' :  rit,
						'vol' : vol,
						'netto' : net
					}

				if len(data_materials) == 0:
					data_materials.append(mat)
				else:
					ketemu = False
					for dtm in data_materials:
						if dtm['material_id'] == sale_order_line.product_id.id and dtm['kalkulasi'] == sale_order.kalkulasi and dtm['pekerjaan_id'] == sale_order.pekerjaan_id.id:
							# # update data sekarang
							rit = dtm['rit'] + 1 if sale_order.kalkulasi == 'ritase' else 0
							vol = dtm['vol'] + sale_order.volume if sale_order.kalkulasi == 'kubikasi' else 0
							net = dtm['netto'] + sale_order.netto if sale_order.kalkulasi == 'tonase' else 0

							dtm['rit'] = rit
							dtm['vol'] = vol
							dtm['netto'] = net
							
							ketemu = True
							break

					if not ketemu:
						data_materials.append(mat)

		# delete data sebelumnya
		self.material_rel_ids.unlink()
		# add the new data
		self.material_rel_ids = data_materials


		# pickings = self.env['stock.picking'].search([
		# 												('karyawan_id','=',self.karyawan_id.id),
		# 												('min_date','>=',periode_awal_utc_str),
		# 												('min_date','<=',periode_akhir_utc_str)
												# ])

		# data_materials = []
		# data_materials_opt = []
		# for pick in pickings:
		# 	stock_move = pick.move_lines[0]
		# 	procurement = stock_move.procurement_id
		# 	sale_order_line = procurement.sale_line_id
		# 	sale_order = sale_order_line.order_id

		# 	rit = 1 if sale_order.kalkulasi == 'ritase' else 0
		# 	vol = sale_order.volume if sale_order.kalkulasi == 'kubikasi' else 0
		# 	net = sale_order.netto if sale_order.kalkulasi == 'tonase' else 0

		# 	mat = {
		# 				'material_id' : sale_order_line.product_id.id,
		# 				'kalkulasi' : sale_order.kalkulasi,
		# 				'pekerjaan_id' : sale_order.pekerjaan_id.id,
		# 				'rit' :  rit,
		# 				'vol' : vol,
		# 				'netto' : net
		# 			}

		# 	if len(data_materials) == 0:
		# 		data_materials.append(mat)
		# 	else:
		# 		ketemu = False
		# 		for dtm in data_materials:
		# 			if dtm['material_id'] == sale_order_line.product_id.id and dtm['kalkulasi'] == sale_order.kalkulasi and dtm['pekerjaan_id'] == sale_order.pekerjaan_id.id:
		# 				# # update data sekarang
		# 				rit = dtm['rit'] + 1 if sale_order.kalkulasi == 'ritase' else 0
		# 				vol = dtm['vol'] + sale_order.volume if sale_order.kalkulasi == 'kubikasi' else 0
		# 				net = dtm['netto'] + sale_order.netto if sale_order.kalkulasi == 'tonase' else 0

		# 				dtm['rit'] = rit
		# 				dtm['vol'] = vol
		# 				dtm['netto'] = net
						
		# 				ketemu = True
		# 				break

		# 		if not ketemu:
		# 			data_materials.append(mat)

		# # delete data sebelumnya
		# self.material_rel_ids.unlink()
		# # add the new data
		# self.material_rel_ids = data_materials
		# print '----------------------------------------------'

	def print_pay_slip_driver(self):
		print 'print pay slip'


		

	