from odoo import api, models, fields
import datetime
import timestring
import pytz
from pprint import pprint

class hm_payroll_staff(models.Model):
	_name = "hm_payroll_staff"

	name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
    					index=True, select=True, default='New')
	karyawan_id = fields.Many2one('hm_karyawan', required=True)
	tanggal =fields.Date('Tanggal', required=True,default=datetime.date.today())
	periode_awal =fields.Date('Periode Awal', required=True,)
	periode_akhir =fields.Date('Periode Akhir', required=True,)
	total = fields.Float(compute='_compute_total', string='Total', store=True)
	potongan_bon = fields.Float('Potongan Bon')
	sisa_bayaran_kemarin = fields.Float('Sisa Bayaran Kemarin')
	downpayment = fields.Float('DP')
	nett = fields.Float(compute='_compute_nett', string='Nett', store=True)
	notes = fields.Text('Catatan')
	is_generated = fields.Boolean('is generated', default=False )
	payroll_presensi_rel_ids = fields.One2many('hm_payroll_presensi_rel', 'hm_payroll_staff_id', string='Payroll Presensi Rel')
	state = fields.Selection([('draft', 'Draft'),('open', 'Open'),('done','Paid')], default='draft') 
	total_hadir_pagi = fields.Integer('Total kehadiran pagi') 
	total_hadir_siang = fields.Integer('Total kehadiran siang')  
	total_kehadiran = fields.Integer('Total kehadiran')
	gaji_per_shift = fields.Float('Gaji per shift')
	generate_id = fields.Many2one('hm_generate_payroll_staff', string="Generate Id", ondelete='cascade')

	# get default catatan
	def _get_default_catatan(self):
		catatan = self.env['hm_appkonfig'].search([('name','=','catatan_pay_slip')])

	@api.onchange('gaji_per_shift', 'total_kehadiran')
	def onchange_gaji_dan_kehadiran(self):
		self.total = self.total_kehadiran * self.gaji_per_shift
		self._compute_nett()

	@api.depends('total','potongan_bon','sisa_bayaran_kemarin','downpayment', 'gaji_per_shift', 'total_kehadiran')
	def _compute_nett(self):
		for pay in self:
			pay.update({
	                'nett': pay.total - pay.potongan_bon + pay.sisa_bayaran_kemarin + pay.downpayment
	            })

	@api.model
	def create(self, vals):
		if vals.get('name', ('New')) == ('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('hm.payroll.seq') or ('New')
	
		result = super(hm_payroll_staff, self).create(vals)
		return result

	@api.multi
	def write(self,vals):
		if vals.has_key('total_kehadiran'): 
			total_kehadiran = vals['total_kehadiran']
		else:
			total_kehadiran = self.total_kehadiran

		if vals.has_key('gaji_per_shift'): 
			gaji_per_shift = vals['gaji_per_shift']
		else:
			gaji_per_shift = self.gaji_per_shift

		total = gaji_per_shift * total_kehadiran

		vals.update({
			'total' : total,
			'nett' :  total - self.potongan_bon + self.sisa_bayaran_kemarin + self.downpayment,
		})
		return super(hm_payroll_staff,self).write(vals)

	def show_presensi(self):
		if not self.is_generated:
			self.state = "open"
			DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
			akhir = ""
			awal = ""
			awal_utc_str = ""
			akhir_utc_str = ""

			localtz = pytz.timezone('Asia/Jakarta')	
			periode_awal_date = timestring.Date(self.periode_awal)
			periode_akhir_date = timestring.Date(self.periode_akhir)

			periode_awal_local_str = localtz.localize(datetime.datetime.strptime(str(periode_awal_date), DATETIME_FORMAT))
			periode_awal_utc_str = periode_awal_local_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)
			
			periode_akhir_local_str = localtz.localize(datetime.datetime.strptime(str(periode_akhir_date), DATETIME_FORMAT))
			periode_akhir_utc_str = periode_akhir_local_str.astimezone(pytz.utc).strftime(DATETIME_FORMAT)

			# gete data presensi
			presensi = self.env['hm_presensi_karyawan_rel'].search([
														('karyawan_id','=',self.karyawan_id.id),
														('tanggal_org','>=',periode_awal_utc_str),
														('tanggal_org','<=',periode_akhir_utc_str)
													])
			data_presensi_rel = []
			for prs in presensi:
				dt_pres = {
					'name' : prs.name,
					'karyawan_id' : prs.karyawan_id.id,
					'hm_presensi_karyawan_rel_id' : prs.id,
					'tanggal' : prs.tanggal_org,
					'pagi' : prs.pagi,
					'siang' : prs.siang,
				}
				data_presensi_rel.append(dt_pres)
				# hitung total kehadiran
				if prs.pagi :
					self.total_kehadiran +=1
					self.total_hadir_pagi +=1

				if prs.siang : 
					self.total_kehadiran +=1
					self.total_hadir_siang +=1

			self.payroll_presensi_rel_ids.unlink()
			self.payroll_presensi_rel_ids = data_presensi_rel
			# set gegneraete
			self.is_generated = True

			# hitung total
			self.total = self.total_kehadiran * self.gaji_per_shift

			print 'generated hm_peresensi_karyawan_rel'
		else:
			print 'Data has been generated'

	# onchange karyawan_id get data gaji per shift
	@api.onchange('karyawan_id')
	def onchange_karyawan_id(self):
		self.gaji_per_shift = self.karyawan_id.gaji_per_shift
		

	def print_pay_slip_driver(self):
		print 'print pay slip'

	# Open view untuk pay driver list
	def open_record(self):
		# first you need to get the id of your record
	    # you didn't specify what you want to edit exactly
	    rec_id = self
	    # then if you have more than one form view then specify the form id
	    form_id = self.env.ref('hasilmancing.hm_payroll_staff_form')

	    # then open the form
	    return {
	            'type': 'ir.actions.act_window',
	            'name': 'Payroll Driver',
	            'res_model': 'hm_payroll_staff',
	            'res_id': rec_id.id,
	            'view_type': 'form',
	            'view_mode': 'form',
	            'view_id': form_id.id,
	            'context': {},  
	            # if you want to open the form in edit mode direclty            
	            'flags': {'initial_mode': 'edit'},
	            'target': 'current',
	        }

	# set as paid / Done
	def set_as_paid(self):
		print 'set as paid'
		self.state = 'done'
		self.write({
				'state' : 'done'
			})


		

	