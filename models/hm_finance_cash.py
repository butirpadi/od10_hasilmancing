from odoo import api, fields, models
from pprint import pprint

class hm_finance_cash(models.Model):
	_name = "hm_finance_cash"
	_order = 'tanggal desc, id desc'

	name = fields.Char(string='Cash Number', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	keterangan = fields.Char('Keterangan', required=True,)
	tanggal = fields.Date('Tanggal', required=True)
	tipe = fields.Selection([
        ('debet', 'Debet'),
        ('credit', 'Credit'),
        ], string="Tipe", required=True,)
	jumlah = fields.Float('Jumlah', required=True, default=0.0)

	debet = fields.Float('Debet',compute="_compute_get_tipe", store=True)
	kredit = fields.Float('Kredit',compute="_compute_get_tipe", store=True)

	@api.depends('jumlah')
	def _compute_get_tipe(self):
		for fin in self:
			if fin.tipe == 'debet':
				fin.debet = fin.jumlah
			else:
				fin.kredit = fin.jumlah

	# def _compute_get_debet(self):
	# 	for fin in self:
	# 		if fin.tipe == 'debet':
	# 			fin.debet = fin.jumlah

	# def _compute_get_kredit(self):
	# 	for fin in self:
	# 		if fin.tipe == 'credit':
	# 			fin.kredit = fin.jumlah

	@api.model
	def create(self, vals):
		if vals.get('name', ('New')) == ('New'):
			if vals['tipe'] == 'debet':
				vals['name'] = self.env['ir.sequence'].next_by_code('hm.finance.cash.in') or ('New')
			else:
				vals['name'] = self.env['ir.sequence'].next_by_code('hm.finance.cash.out') or ('New')
	
		result = super(hm_finance_cash, self).create(vals)
		return result
    