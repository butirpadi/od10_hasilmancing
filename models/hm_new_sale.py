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
import math

class hm_new_sale(models.Model):
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
									('done','Done'),
									('cancel','Cancelled')
									], string='Status Nota Timbang', default='draft')
	order_line_len = fields.Integer('Order Line Length',compute="_compute_get_order_line_length")
	material = fields.Many2one('product.product', 'Material', compute="_compute_set_material", store=True,)

	state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

	# spesial function 
	# auto confirm semua sale order yang status nya draft
	def action_confirm_all(self):
		sales = self.env.cr.execute("select * from sale_order")
		for sale in self.env.cr.fetchall():
			sales = self.env['sale.order'].search([('id','=',sale[0]),('state','=','draft')])
			# print 'confirm sale'
			for sale in sales:
				print 'Confirm : ' + sale.name
				sale.action_confirm()
				sale.status_nota_timbang == 'open'
				sale.hitung_harga_total()
				sale.write({'status_nota_timbang':'open'})
				sale.action_validate_nota_timbang()
			# 	# print 'Reference : ' + sale.name
			# 	if sale.state == 'draft':
			# 		sale.action_confirm()
			# 	else:
			# 		print 'sale order state not in draft'
			# # print 'inside action confirm all'

	# cancel all sale order
	def action_cancel_all(self):
		sales = self.env.cr.execute("select * from sale_order")
		for sale in self.env.cr.fetchall():
			sales = self.env['sale.order'].search([('id','=',sale[0]),('state','!=','draft')])
			# print 'confirm sale'
			for sale in sales:
				print 'cancel : ' + sale.name
				sale.action_cancel()
				sale.action_draft()
				sale.status_nota_timbang = 'draft'
			# 	# print 'Reference : ' + sale.name
			# 	if sale.state == 'sale':
			# 		sale.action_cancel()
			# 		sale.action_draft()
			# 	else:
			# 		print 'sale order state not in sale'
			


	@api.depends('order_line')
	def _compute_set_material(self):
		for sale in self:
			for line in sale.order_line:
				print line.product_id
				print line.product_id.name
				sale.material = line.product_id


	@api.multi
	def action_confirm(self):
		super(hm_new_sale,self).action_confirm()
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

	# action set status nota timbang
	def action_validate_nota_timbang(self):
		print('Validate Nota Timbang')
		if self.kalkulasi and self.status_nota_timbang == 'open' :
			# set status nota timbang to done
			self.status_nota_timbang = 'done'

			# reset qty on hand
			for line in self.order_line:
				# reset quantity of product
				Inventory = self.env['stock.inventory']
				print 'Product uom qty : ' + str(line.product_uom_qty)
				print 'Self QTY : ' + str(self.quantity)
				new_qty = math.ceil(line.product_id.qty_available+line.product_uom_qty)
				print 'New QTY : ' + str(new_qty)
				inventory = Inventory.create({
					# 'name': ('INV: %s') % tools.ustr(line.product_id.name),
					'name': ('Auto Adjustment: %s') % tools.ustr(line.product_id.name),
					'filter': 'product',
					'product_id': line.product_id.id,
					'location_id': 15,
					# 'lot_id': wizard.lot_id.id,
					'line_ids': [(0, 0, {
				               'product_qty': new_qty,
				               'location_id': 15,
				               'product_id': line.product_id.id,
				               # 'product_uom_id': self.product_id.uom_id.id,
				               'theoretical_qty': new_qty,
				               # 'prod_lot_id': self.lot_id.id,
				        })],
				})
				inventory.action_done() 
				print('Reset Quantity Done')

			# for line in self.order_line:
			# 	print 'QTY Available : ' + str(line.product_id.qty_available)
		else:
			print('Nota timbang already validated atau dalam status "DRAFT"')

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
			print 'compute amount ........................'
			line._compute_amount()

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

		return super(hm_new_sale,self).write(vals)

	# action get order_line cek_order_line_length
	@api.onchange('order_line')
	def _compute_get_order_line_length(self):
		print 'order_line change'
		for order in self:
			order.order_line_len = len(order.order_line)

	@api.model
	def create(self, vals):

		# update date_order sama dengan tanggal
		vals.update({'date_order':vals.get('tanggal')})

		# cek jumlah order_line
		if 'order_line' in vals:
			res = vals['order_line']
			if len(res) > 1:
				raise UserError('Jumlah material melebihi ketentuan, dalam satu transaksi hanya dapat menampung satu material.')
		
		new_record = super(hm_new_sale, self).create(vals)
		return new_record

	def action_cancel(self):
		# set status nota to canceled
		self.status_nota_timbang = 'cancel'
		super(hm_new_sale,self).action_cancel()