from odoo import api, models, fields
# from hm_finance_cash import hm_finance_cash

class hm_jurnal_kas(models.Model):
	_name = "hm_jurnal_kas"

	name = fields.Char(default='Jurnal Kas',readonly=True)
	tanggal_awal = fields.Date('Tanggal Awal', required=True)
	tanggal_akhir = fields.Date('Tanggal akhir', required=True)

	def _get_data_kas(self):
		# count = Task.search_count([('is done', '=', False)])
		res = self.env['hm_finance_cash'].search([('tanggal','between',(tanggal_awal,tanggal_akhir))])
		return res

	# data_kas = fields.Function(_get_data_kas,string='Kas Line')
	data_kas = fields.One2many('hm_finance_cash',compute="_compute_get_data_kas",string='Kas Line')
	total_saldo = fields.Float('Total',compute="_compute_get_total_saldo")

	@api.multi
	def _compute_get_data_kas(self):
		for data in self:
			# Show data line
			res = self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir)], order="tanggal asc")
			data.data_kas = res
			
	@api.multi
	def _compute_get_total_saldo(self):
		for data in self:
			# show total saldo
			data_debet = self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir),('tipe','=','debet')], order="tanggal asc")
			total_debet = sum(data_debet.mapped('jumlah'))

			data_credit = self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir),('tipe','=','credit')], order="tanggal asc")
			total_credit = sum(data_credit.mapped('jumlah'))
			# kredit = sum(jumlah in self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir),('tipe','=','credit')], order="tanggal asc"))
			# data.total_saldo = debet - kredit

			# data_debet = self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir),('tipe','=','debet')], order="tanggal asc")
			# total_debet = 0
			# for dbt in data_debet:
			# 	total_debet += dbt.jumlah

			# data_credit = self.env['hm_finance_cash'].search([('tanggal','>=',data.tanggal_awal),('tanggal','<=',data.tanggal_akhir),('tipe','=','credit')], order="tanggal asc")
			# total_credit = 0
			# for dbt in data_credit:
			# 	total_credit += dbt.jumlah

			data.total_saldo = total_debet - total_credit


	# @api.onchange('tanggal_akhir')
	# def get_data_kas(self):
	# 	self._compute_get_data_kas()


	def action_submit(self):
		self._compute_get_data_kas()
		self._compute_get_total_saldo()
