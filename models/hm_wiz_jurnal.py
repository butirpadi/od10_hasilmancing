from odoo import api, models, fields
from pprint import pprint

class hm_wiz_jurnal(models.TransientModel):
	_name = 'hm_wiz_jurnal'
	_description = 'Wizard Jurnal'

	name = fields.Char('name', default="Jurnal Kas")
	tanggal_awal = fields.Date('Tanggal Awal')
	tanggal_akhir = fields.Date('Tanggal Akhir'		)
	data_kas = fields.Many2many('hm_finance_cash', string='Kas Line')
	total_saldo = fields.Integer('Total')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open')], default='draft')  

	def action_get_data_kas(self):
		res = self.env['hm_finance_cash'].search([('tanggal','>=',self.tanggal_awal),('tanggal','<=',self.tanggal_akhir)], order="tanggal asc")
		self.data_kas = res
		debet = sum(map(lambda x:x.debet,res))
		kredit = sum(map(lambda x:x.kredit,res))
		self.total_saldo = debet-kredit
		self.state = 'open'

	def hm_wiz_jurnal_print(self):
		print 'print wizard jurnal'