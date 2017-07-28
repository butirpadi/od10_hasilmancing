from odoo import api, models, fields

class hm_purchase_order(models.Model):
	_inherit = "purchase.order"
	tanggal = fields.Date('Tanggal', required=True,)
	state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
	READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
	partner_id = fields.Many2one('res.partner', string='Supplier', required=True, states=READONLY_STATES, change_default=True, track_visibility='always')

	@api.onchange('tanggal')
	def _onchange_tanggal(self):
		self.date_order = self.tanggal