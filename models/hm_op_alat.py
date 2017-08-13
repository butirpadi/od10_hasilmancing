from odoo import api, models, fields
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

class hm_op_alat(models.Model):
	_name = "hm_op_alat"

	name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	tanggal = fields.Date('Tanggal', required=True)
	alat_berat_id = fields.Many2one('hm_alat_berat',string="Alat Berat", required=True,)
	lokasi_galian_id = fields.Many2one('hm_galian', string='Lokasi Galian' , required=True,)
	pengawas_id = fields.Many2one('hm_karyawan', string="Pengawas", required=True)
	operator_id = fields.Many2one('hm_karyawan', string="Operator", required=True)
	jam_kerja_start = fields.Char(required=True,)
	jam_kerja_end = fields.Char(required=True,)
	istirahat_start = fields.Char(required=True,)
	istirahat_end = fields.Char(required=True,)
	total_jam_kerja = fields.Char('Total Jam Kerja')
	solar = fields.Float('Solar', required=True,)
	oli = fields.Float('Oli', required=True,)
	keterangan = fields.Text('Keterangan')

	@api.model
	def create(self, vals):
		# Generate Reference number
		if vals.get('name', ('New')) == ('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hm.op.alat') or ('New')

		# calculate total jam Kerja
		tgl = datetime.strptime(vals['tanggal'] + " 00:00:00", DEFAULT_SERVER_DATETIME_FORMAT)
		ttl_jm_krja = 0
		jam_awal_str = vals['jam_kerja_start']
		jam_awal_str = jam_awal_str.split(':')
		jam_awal = datetime(tgl.year, tgl.month, tgl.day, int(jam_awal_str[0]),int(jam_awal_str[1]),0)

		jam_akhir_str = vals['jam_kerja_end']
		jam_akhir_str = jam_akhir_str.split(':')
		jam_akhir = datetime(tgl.year, tgl.month, tgl.day, int(jam_akhir_str[0]),int(jam_akhir_str[1]),0)

		istrht_aw_str = vals['istirahat_start']
		istrht_aw_str = istrht_aw_str.split(':')
		istrht_aw = datetime(tgl.year, tgl.month, tgl.day, int(istrht_aw_str[0]),int(istrht_aw_str[1]),0) 

		istrht_ak_str = vals['istirahat_end']
		istrht_ak_str = istrht_ak_str.split(':')
		istrht_ak = datetime(tgl.year, tgl.month, tgl.day, int(istrht_ak_str[0]),int(istrht_ak_str[1]),0) 

		jam_kerja_pagi = istrht_aw - jam_awal
		jam_kerja_siang = jam_akhir - istrht_ak
		ttl_jm_krja = jam_kerja_pagi + jam_kerja_siang

		# if vals.has_key('total_jam_kerja'):
		# 	vals['total_jam_kerja'] = ttl_jm_krja
		# else:
		vals['total_jam_kerja'] = ttl_jm_krja
			
		result = super(hm_op_alat, self).create(vals)
		return result

	def calculate_jam_kerja(self):
		total_jam_kerja = 0
		if self.tanggal and self.jam_kerja_start and self.jam_kerja_end and self.istirahat_start and self.istirahat_end:
			tgl = datetime.strptime(self.tanggal, DEFAULT_SERVER_DATETIME_FORMAT)
			
			jam_awal_str = self.jam_kerja_start
			jam_awal_str = jam_awal_str.split(':')
			jam_awal = datetime(tgl.year, tgl.month, tgl.day, int(jam_awal_str[0]),int(jam_awal_str[1]),0)

			jam_akhir_str = self.jam_kerja_end
			jam_akhir_str = jam_akhir_str.split(':')
			jam_akhir = datetime(tgl.year, tgl.month, tgl.day, int(jam_akhir_str[0]),int(jam_akhir_str[1]),0)

			istrht_aw_str = self.istirahat_start
			istrht_aw_str = istrht_aw_str.split(':')
			istrht_aw = datetime(tgl.year, tgl.month, tgl.day, int(istrht_aw_str[0]),int(istrht_aw_str[1]),0) 

			istrht_ak_str = self.istirahat_end	
			istrht_ak_str = istrht_ak_str.split(':')
			istrht_ak = datetime(tgl.year, tgl.month, tgl.day, int(istrht_ak_str[0]),int(istrht_ak_str[1]),0) 

			## date diff untuk mendapatkan jam_kerja_alat
			jam_kerja_pagi = istrht_aw - jam_awal
			# print jam_kerja_pagi
			jam_kerja_siang = jam_akhir - istrht_ak
			# print jam_kerja_siang
			total_jam_kerja = jam_kerja_pagi + jam_kerja_siang
			# print total_jam_kerja
			print('totalnya dalam : ' + str(total_jam_kerja))	
			self.total_jam_kerja = total_jam_kerja
		print('totalnya luar : ' + str(total_jam_kerja))	
		return total_jam_kerja


	@api.onchange('jam_kerja_start')
	def jam_kerja_start_change(self):
		self.calculate_jam_kerja()

	@api.onchange('jam_kerja_end')
	def jam_kerja_end_change(self):
		self.calculate_jam_kerja()

	@api.onchange('istirahat_start')
	def istirahat_start_change(self):
		self.calculate_jam_kerja()

	@api.onchange('istirahat_end')
	def istirahat_end_change(self):
		self.calculate_jam_kerja()
