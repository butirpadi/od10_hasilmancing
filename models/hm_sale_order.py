from odoo import api, fields, models, osv, tools
import datetime
import timestring
import pytz
from pprint import pprint
from odoo.exceptions import UserError, ValidationError
import requests
import odoo.addons.decimal_precision as dp
# import pooler
import re
from mako.template import Template
from mako.lookup import TemplateLookup
import time
import os
import locale

class hm_sale_order(models.Model):
	_inherit = 'sale.order'
	_order = 'tanggal desc'

	# data pekerjaan dari setiap orderan
	tanggal = fields.Date('Tanggal')
	pekerjaan_id = fields.Many2one('hm_pekerjaan', string='Pekerjaan')
	galian_id = fields.Many2one('hm_galian', string='Lokasi Galian')
	karyawan_id = fields.Many2one('hm_karyawan', string="Driver")
	armada_id = fields.Many2one(related="karyawan_id.armada_id",string="Nopol")
	picking_id = fields.Many2one('stock.picking',compute="_compute_get_stock_picking", string="Stock Picking", store=True,)
	nomor_nota_timbang = fields.Char('Nomor Nota')
	kalkulasi = fields.Selection([
					('ritase','RITASE'),
					('kubikasi','KUBIKASI'),
					('tonase','TONASE')
				], string='Kalkulasi')
	quantity = fields.Integer('Quantity', default=1)
	panjang = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Panjang')
	lebar = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Lebar')
	tinggi = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Tinggi')
	volume = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Volume')
	gross = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Gross')
	tare = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Tare')
	netto = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Netto')
	harga_satuan = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Unit Price')
	harga_total = fields.Float(digits=dp.get_precision('Product Unit of Measure'),string='Total')
	status_nota_timbang = fields.Selection([
									('draft','Draft'),
									('open','On Delivery'),
									('done','Done')
									], string='Status Nota Timbang', default='draft')
	order_line_len = fields.Integer('Order Line Length',compute="_compute_get_order_line_length")
	material = fields.Many2one('product.product', 'Material', compute="_compute_set_material", store=True,)

	# call php api
	def cetak_surat_jalan(self):
		# Membuat temporary file yang akan dicetak beserta pathnya   
		# filename = '/tmp/odoo-print.txt' 
		
		# Mengisi file tersebut dengan data yang telah dirender
		# nota = ('')

		# condensed = chr(27) + chr(33) + chr(4)
		# bold1 = chr(27) + chr(69)
		# bold0 = chr(27) + chr(70)
		# draft_font = chr(27)+ chr(120)+chr(48)
		# roman_font = chr(27)+ chr(107)+chr(48)
		# initialized = chr(27)+chr(64)
		# condensed1 = chr(15)
		# condensed0 = chr(18)
		# double_width = chr(14)
		# centering = chr(27)+chr(97)+chr(1)
		# left = chr(27)+chr(97)+chr(0)
		# right = chr(27)+chr(97)+chr(2)
		# left_margin = chr(27) + chr(108) +chr(5) 
		# right_margin = chr(27) + chr(81) +chr(5)
		# reverse_linefeed = chr(27)+ chr(106)+ chr(1)
		# page_width_in_line = chr(27)+ chr(67)+ chr(127) #//27 67 n
		# page_width_in_inch = chr(27)+ chr(67)+ chr(48)+ chr(21) #//27 67 48 n

		# # # INITIALISASI PRINTER
		# Data = initialized
		# Data += page_width_in_inch
		# # // Data  += left_margin
		# # // Data  += right_margin
		# Data += draft_font
		# # // Data += condensed1

		# # // HEADER
		# Data += centering
		# Data += double_width
		# Data += bold1+"SALES ORDER\n"
		# Data += condensed1
		# Data += bold0+"UD HASIL MANCING\n"
		# Data += "JL. TAMBONG, KABAT, BANYUWANGI, JAWA TIMUR\n"
		# Data += "T. 0812348762386 | E. info@hasilmancing.com\n"

		# Data += "+-----------------------------------------------------------------------------------------------------+-------------+"
		# Data += "|                                  M A T E R I A L                                                    |    Q T Y    |"
		# Data += "+-----------------------------------------------------------------------------------------------------+-------------+"
		# Data += "|                                  M A T E R I A L                                                    |    Q T Y    |"

		# # nota = Data 

		# MYDIR = os.path.dirname(__file__)
		# with open(os.path.join(MYDIR, 'test.txt')) as f:
		# pass

		# Mendefinikan template report berdasarkan path modul terkait 
		tpl_lookup = TemplateLookup(directories=[os.path.dirname(__file__)])
		tpl = tpl_lookup.get_template('so_main.txt')
		# tpl_line = tpl_lookup.get_template('so_line.txt')

		# Mempersiapkan data-data yang diperlukan                
		# user = self.pool.get('res.users').browse(cr, uid, uid)
		# order = self.browse(cr, uid, ids)[0]            
		# date = time.strftime('%d/%m/%Y %H:%M', time.strptime(order.date,'%Y-%m-%d %H:%M:%S'))   

		# no = 0
		# rows = []
		# for line in self.order_line:
		# 	s = tpl_line.render(MATERIAL=line.product_id.name)
		# 	rows.append(s)
		 
		# Merender data yang telah disiapkan ke dalam template report text
		s = tpl.render(so_name='WH/OUT/'+self.name,
		               cust=self.partner_id.name,
		               pekerjaan=self.pekerjaan_id.name,
		               alamat="ALAMAT CUSTOMERE",
		               tanggal=self.tanggal,
		               nopol=self.armada_id.name,
		               armada=self.armada_id.keterangan,
		               material=self.material.name,
		               dicetak=self.user_id.name,
		               dikirim=self.karyawan_id.name,
		               diterima='(_________________________)',
		               )
		         

		# Membuat temporary file yang akan dicetak beserta pathnya   
		filename = '/tmp/odoo-delivery-tempt.txt'
		 
		# Mengisi file tersebut dengan data yang telah dirender
		f = open(filename, 'w')
		f.write(s)
		f.close()

		# --------------------------------------------------------

		# f = open(filename, "w")
		# f.write(nota)
		# f.close()
		# Proses cetak dijalankan dan pastikan variabel nama_printer adalah nama printer yang anda setting atau tambahkan dengan webmin diatas
		os.system('lpr -PLX-300 %s' % filename)
		# Hapus file yang telah dicetak
		os.remove(filename)
		return True

	def cetak_invoice(self):
		print 'cetak invoice'
		
	def call_api(self):
		url = 'http://localhost/hmapi/public/home'
		# data = '{  "platform": {    "login": {      "userName": "name",      "password": "pwd"    }  } }'
		# response = requests.post(url, data=data,headers={"Content-Type": "application/json"})
		response = requests.get(url, headers={"Content-Type": "application/json"})
		# print(response)
		# sid=response.json()['platform']['login']['sessionId']   //to extract the detail from response
		sid=response.json()
		print sid[0]['name']
		# print sid[0].name
		# print(sid['name'])
		# print(sid.name)
		# print(sid)

	@api.depends('order_line')
	def _compute_set_material(self):
		for sale in self:
			for line in sale.order_line:
				print line.product_id
				print line.product_id.name
				sale.material = line.product_id


	@api.multi
	def action_confirm(self):
		super(hm_sale_order,self).action_confirm()
		print 'ACTION CONFIRMED OVERRIDE'
		self._compute_get_stock_picking()

	@api.depends('write_date')
	def _compute_get_stock_picking(self):
		for order in self:
			picking = self.env['stock.picking'].search([('origin','=',order.name)], limit=1)
			if picking:
				order.picking_id = picking

	@api.onchange('tanggal')
	def _onchange_tanggal(self):
		self.date_order = self.tanggal

	# Tampilkan NOPOL Driver
	@api.onchange('karyawan_id')
	def _onchange_karyawan_id(self):
		print 'on karyawan_id change'
		for so in self:
			so.armada_id = so.karyawan_id.armada_id
	        

	# @api.model
	# def search(self, args, offset=0, limit=0, order=None, count=False):
	# 	DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
	# 	akhir = ""
	# 	awal = ""
	# 	awal_utc_str = ""
	# 	akhir_utc_str = ""
	# 	for doms in args:
	# 		if doms[0] in 'date_order':
	# 			if doms[1] == '=':
	# 				dt = timestring.Date(doms[2])
	# 				# lokalisasi datetime
	# 				localtz = pytz.timezone('Asia/Jakarta')	
	# 				dt_local_str = pytz.utc.localize(datetime.datetime.strptime(doms[2], DATETIME_FORMAT)).astimezone(localtz).strftime(DATETIME_FORMAT)
	# 				dt_local = timestring.Date(dt_local_str)
	# 				awal = str(dt_local.date.date()) + ' ' + '00:00:00'
	# 				akhir = str(dt_local.date.date()) + ' ' + '23:59:00'

	# 				# set to UTC lagi
	# 				awal_utc_str = localtz.localize(datetime.datetime.strptime(awal, DATETIME_FORMAT))
	# 				awal_utc_str = awal_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)

	# 				akhir_utc_str = localtz.localize(datetime.datetime.strptime(akhir, DATETIME_FORMAT))
	# 				akhir_utc_str = akhir_utc_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)
					
	# 			# 	# doms = [('date_order','>=',awal),('date_order','<=',akhir)]
	# 				doms[1] = '>='
	# 				doms[2] = awal_utc_str
	# 				# doms = ['date_order','>=',awal]
	# 				args.append(['date_order','<=',akhir_utc_str])
				
	# 	return super(hm_sale_order,self).search(args,offset,limit,order,count)

	# action set status nota timbang
	def action_validate_nota_timbang(self):
		print('Validate Nota Timbang')
		if self.kalkulasi and self.status_nota_timbang == 'open' :
			# # check has picking
			# set status nota timbang to done
			self.status_nota_timbang = 'done'
			# validate picking/delivery
			print('Validate picking')
			for pick in self.picking_ids:
				# set qt_done
				for operation in pick.pack_operation_product_ids:
					operation.qty_done = operation.product_qty
				# validate picking
				pick.do_new_transfer()

			for line in self.order_line:
				# reset quantity of product
				print('Reset quantity')
				print('=======================================')
				Inventory = self.env['stock.inventory']
				inventory = Inventory.create({
					# 'name': ('INV: %s') % tools.ustr(line.product_id.name),
					'name': ('Auto Adjustment: %s') % tools.ustr(line.product_id.name),
					'filter': 'product',
					'product_id': line.product_id.id,
					'location_id': 15,
					# 'lot_id': wizard.lot_id.id,
					'line_ids': [(0, 0, {
				               'product_qty': 350,
				               'location_id': 15,
				               'product_id': line.product_id.id,
				               # 'product_uom_id': self.product_id.uom_id.id,
				               'theoretical_qty': 350,
				               # 'prod_lot_id': self.lot_id.id,
				        })],
				})
				inventory.action_done() 
				print('Reset Quantity Done')

				# set auto create invoice 
				is_auto_generate_invoice = self.env['ir.config_parameter'].get_param('auto_create_invoice')
				if is_auto_generate_invoice: 
					print 'Auto generate invoice: Call call_action_invoice_create'
					self.call_action_invoice_create()
		else:
			print('Nota timbang already validated atau dalam status "DRAFT"')


	# function to reset sale order & regenerate picking 
	def reset_sale_order(self):
		# set nota timbang status to draft
		self.status_nota_timbang = 'draft'
		self.kalkulasi = None
		self.panjang = None
		self.lebar = None
		self.tinggi = None
		self.volume = None
		self.gross = None
		self.tare = None
		self.netto = None
		self.harga_satuan = None
		self.harga_total = None
		self.quantity = None
		# Delete Picking
		print('Validate picking')
		for pick in self.picking_ids:
			print('Check Backorder nya : ')
			if pick.check_backorder():
				# set operation state to available
				# set qt_done
				for operation in pick.pack_operation_product_ids:
					# operation.state = 'assigned'
					print('Operation State-nya : ' + operation.state)
					# reset product_qty
					if self.kalkulasi == 'kubikasi':
						operation.product_qty = self.volume
					elif self.kalkulasi == 'tonase':
						operation.product_qty = self.netto
					elif self.kalkulasi == 'ritase':
						operation.product_qty = 1
					# set qty done
					operation.qty_done = operation.product_qty

				print('delete backorder')
				# delete other backorders
				print('delete move lines')
				for move in pick.move_lines:
					# move.write({'state','assigned'})
					move.state = 'assigned'
					move.action_cancel()
					move.unlink()
				# print('do the transfer')		
		# Generrate new picking
		if len(self.picking_ids) == 0:
			#delete procurement
			for order_line in self.order_line:
				order_line.kalkulasi = None
				order_line.volume = None
				order_line.netto = None
				order_line.quantity = None
				order_line.harga_satuan = None
				order_line.harga_total = None
				order_line.price_unit = None
				order_line._compute_amount()
				for proc in order_line.procurement_ids:
					proc.write({'state':'confirmed'})
					proc.unlink()

			# unconfirm sale
			# self.state = 'draft'
			print('reset sale order state ')
			self.write({'state':'draft'})
		# Delete Invoices
		print('Deleting invoices')
		if len(self.invoice_ids) > 0:
			for inv in self.invoice_ids:
				print('delete invoice ' + inv.name)
				inv.write({'state':'draft'})
				# delete invoice move
				# inv.move_name = False
				inv.move_id.write({'state':'draft'})
				inv.move_id.unlink()
				# inv.move_id.unlink()
				inv.unlink()
				print('delete invoice ' + inv.name + ' done')

	@api.onchange('kalkulasi')
	def onchange_kalkulasi(self):
		# clear input
		self.panjang = 0
		self.lebar = 0
		self.tinggi = 0
		self.volume = 0
		self.gross = 0
		self.tare = 0
		self.netto = 0


	# hitung kalkulasi kubikasi
	@api.onchange('panjang')
	def onchange_panjang(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('lebar')
	def onchange_lebar(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('tinggi')
	def onchange_tinggi(self):
		vol = 0
		vol = self.panjang * self.lebar * self.tinggi
		self.volume = vol 
		self.hitung_harga_total()

	@api.onchange('gross')
	def onchange_gross(self):
		net = 0
		net = self.gross - self.tare
		self.netto = net
		self.hitung_harga_total()

	@api.onchange('tare')
	def onchange_tare(self):
		net = 0
		net = self.gross - self.tare
		self.netto = net	 
		self.hitung_harga_total()

	@api.onchange('harga_satuan')
	def onchange_harga_satuan(self):
		self.hitung_harga_total()

	# Hitung harga total
	def hitung_harga_total(self):
		ord_qty = 1
		if(self.kalkulasi == 'ritase'):
			self.harga_total = self.harga_satuan 
			# update qty_delivered
			# self.qty_delivered =  
		elif(self.kalkulasi == 'kubikasi'):
			self.harga_total = self.volume * self.harga_satuan
			# update qty_delivered
			self.qty_delivered = self.volume
			ord_qty = self.volume
		elif(self.kalkulasi == 'tonase'):
			self.harga_total = self.netto * self.harga_satuan
			# update qty_delivered
			self.qty_delivered = self.netto 
			ord_qty = self.netto

		# update unit price 
		for line in self.order_line:
			line.price_unit = self.harga_satuan
			# line.kalkulasi = self.kalkulasi
			# set qty
			if(self.kalkulasi == 'ritase'):
				line.product_uom_qty = 1
				line.quantity = 1
			elif(self.kalkulasi == 'kubikasi'):
				line.product_uom_qty = self.volume
				line.volume = self.volume
			elif(self.kalkulasi == 'tonase'):
				line.product_uom_qty = self.netto
				line.netto = self.netto

		# 	# calculate price_total
			line._compute_amount()
			

	@api.model 
	def _compute_get_status_nota_timbang(self):
		self.status_nota_timbang

	# Tampilkan form nota timbang
	@api.multi
	def action_view_nota_timbang(self):
		nota_tbg = self.mapped('nota_timbang_id')
		action = self.env.ref('hm_nota_timbang_tree').read()[0]

		if len(nota_tbg) == 1:
			action['views'] = [(self.env.ref('hm_nota_timbang_form').id, 'form')]
			action['res_id'] = nota_tbg.ids[0]
		else:
			action = {'type': 'ir.actions.act_window_close'}
		
		return action

	# show driver name
	driver = fields.Char('Driver',compute='_compute_get_delivery_driver', readonly=True )

	picking_status = fields.Selection([
        ('draft', 'Draft'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'), ('done', 'Done')],
        string='Delivery Status', compute='_compute_get_picking_status', readonly=True)
	
	@api.model 
	def _compute_get_delivery_driver(self):
		for data in self:
			if len(data.picking_ids) > 0 :
				for pick in data.picking_ids:
				# print(pick.karyawan_id.armada_id.name)
					if pick.karyawan_id.armada_id.name and pick.karyawan_id.name :
						data.driver = pick.karyawan_id.armada_id.name + " - " + pick.karyawan_id.name  
					else:
						data.driver = "-"
					# data.driver = pick.karyawan_id.name  
			else:
				data.driver = "-"

	@api.model
	def _compute_get_picking_status(self):
		# print active_id
		for data in self:
			for pick in data.picking_ids:
				# print(pick.karyawan_id.armada_id.name)
				data.picking_status = pick.state

	# override method write
	@api.multi
	def write(self,vals):
		# update date_order sama dengan tanggal
		if 'tanggal' in vals:
			vals.update({'date_order':vals.get('tanggal')})

		if 'kalkulasi' in vals:
			if vals['kalkulasi']:
				vals.update({'status_nota_timbang':'open'})
				
		# cek jumlah order_line
		if 'order_line' in vals:
			res = vals['order_line']
			if len(res) > 1:
				raise UserError('Jumlah material melebihi ketentuan, dalam satu transaksi hanya dapat menampung satu material.')

		# update harga_total
		harga_satuan = vals.get('harga_satuan',self.harga_satuan)
		# harga_total 
		kalkulasi = vals.get('kalkulasi',self.kalkulasi) 
		panjang = vals.get('panjang',self.panjang)
		lebar = vals.get('lebar',self.lebar)
		tinggi = vals.get('tinggi',self.tinggi)
		volume = float(format(panjang * lebar * tinggi, '.2f'))
		gross = vals.get('gross',self.gross)
		tare = vals.get('tare',self.tare)
		netto = float(format(gross - tare, '.2f'))
		
		if(kalkulasi == 'ritase'):
			vals.update({'harga_total':harga_satuan})
		elif(kalkulasi == 'kubikasi'):
			vals.update({'volume': volume})
			vals.update({'harga_total':harga_satuan * volume})
			print 'harga_total : ' + str(harga_satuan * volume)
		elif(kalkulasi == 'tonase'):
			vals.update({'netto': netto})
			vals.update({'harga_total':harga_satuan * netto})
			print 'harga_total : ' + str(harga_satuan * netto)

		return super(hm_sale_order,self).write(vals)

	# Create Invoice Auto
	@api.multi
	def call_action_invoice_create(self):
		inv_id = self.action_invoice_create()
		inv = self.env['account.invoice'].browse(inv_id)
		inv.action_invoice_open()
		# pprint(inv)


	# action get order_line cek_order_line_length
	@api.onchange('order_line')
	def _compute_get_order_line_length(self):
		print 'order_line change'
		for order in self:
			order.order_line_len = len(order.order_line)

	# Reset Order Line
	def action_reset_order_line(self):
		print 'inside reset order line'

	@api.model
	def create(self, vals):

		# update date_order sama dengan tanggal
		vals.update({'date_order':vals.get('tanggal')})

		# cek jumlah order_line
		if 'order_line' in vals:
			res = vals['order_line']
			if len(res) > 1:
				raise UserError('Jumlah material melebihi ketentuan, dalam satu transaksi hanya dapat menampung satu material.')
		
		new_record = super(hm_sale_order, self).create(vals)
		return new_record

	# Cancel Transaksi
	def action_cancel(self):
		print 'cancel transaksi'
		print '--------------------------------'
		print 'cancel shipping'
		print self.picking_id
		ship = self.env['stock.picking'].search([('id','=',self.picking_id.id)])
		# set draft to stock.move
		for move in ship.move_lines:
			self.env.cr.execute("update stock_move set state = 'draft' where id = " + str(move.id) )
			if self.picking_id:
				self.env.cr.execute("update stock_pack_operation set qty_done = 0 where picking_id = " + str(self.picking_id.id) )
		# cancel shipping
		ship.action_cancel()
		# delete data shipping & stock_pack_operation
		if self.picking_id:
			self.env.cr.execute("delete from stock_pack_operation where picking_id = " + str(self.picking_id.id) )
			self.env.cr.execute("delete from stock_picking where id = " + str(self.picking_id.id) )
		print '================================'
		print '.'
		print '.'
		print '.'
		print '.'
		print 'cancel invoice'
		print '--------------------------------'
		invs = self.invoice_ids
		for inv in invs:
			ac_move = inv.move_id 
			# 1. delete account_partial_reconcile
			# 2. delete account_payment
			# 3. delete account_invoice_payment_rel
			# 4. delete account_move_line
			# 5. delete account_move
			# 6. delete account_invoice
			
			# delete payment_move_line
			print 'delete paymen_move_line = ' + str(len(inv.payment_move_line_ids))
			for pay_move in inv.payment_move_line_ids:
				# delete account_partial_reconcile
				self.env.cr.execute('delete from account_partial_reconcile where credit_move_id = ' + str(pay_move.id))
				
			for pay_move in inv.payment_move_line_ids:
				print 'account_move_line_id : ' + str(pay_move.id)
				print 'move_id : ' + str(pay_move.move_id.id)
				# delete from move
				self.env.cr.execute('delete from account_move where id = ' + str(pay_move.move_id.id))
				# delete from account move line
				self.env.cr.execute('delete from account_move_line where move_id = ' + str(pay_move.move_id.id))
				# delete from account_invoice_account_move_line_rel
				self.env.cr.execute('delete from account_invoice_account_move_line_rel where account_move_line_id = ' + str(pay_move.id))

			# ac_moves = self.env['account_move'].search('')
			print 'account_move_line length : ' + str(len(ac_move.line_ids))
			for ac_move_line in ac_move.line_ids:
				# delete account_partial_reconcile
				# print 'delete account_partial_reconcile'
				# ac_move_line.remove_move_reconcile()
				

				# delete account_payment
				for pay in inv.payment_ids:
					# delete account payment
					print 'delete account_payment'
					sql_delete_account_payment = "delete from account_payment where id = " + str(pay.id)
					self.env.cr.execute(sql_delete_account_payment)
					# delete account_invoice_payment_rel
					print 'delete account_invoice_payment'
					sql_delete_account_invoice_payment_rel = "delete from account_invoice_payment_rel where payment_id = " + str(pay.id)
					self.env.cr.execute(sql_delete_account_invoice_payment_rel)



				# # delete account_invoice_account_move_line_rel
				# print 'delete account_invoice_account_move_line_rel'
				# sql_delete_account_invoice_account_move_line_rel = "delete from account_invoice_account_move_line_rel where account_move_line_id = " + str(ac_move_line.id)
				# self.env.cr.execute(sql_delete_account_invoice_account_move_line_rel)

				# delete move line
				print 'delete account_move_line'
				sql_delete_account_move_line = "delete from account_move_line where id = " + str(ac_move_line.id)
				self.env.cr.execute(sql_delete_account_move_line)
				

			# # ac_move.unlink()
			# delete inv
			print 'delete account_invoice'
			sql_delete_account_invoice = "delete from account_invoice where id = " + str(inv.id)
			self.env.cr.execute(sql_delete_account_invoice)
			# delete account_move
			print 'delete account_move ---> move_id = ' + str(inv.move_id.id)
			# mv = self.env['account.move'].search([('id','=',inv.move_id.id)])
			# if mv:
			sql_delete_account_move = "delete from account_move where id = " + str(inv.move_id.id)
			self.env.cr.execute(sql_delete_account_move)

			print 'xxxxxxxxxxxx END OF MASTER LOOP xxxxxxxxxxxxxxxxx'


		print '================================'
		print '.'
		print '.'
		print '.'
		print 'Delete Sale Order Finally'
		super(hm_sale_order,self).action_cancel()
		print '================================'
		print '.'
		print '.'
		print '.'
		print 'Delete Sale Order'
		print '-----------------------------------'
		self.unlink()

