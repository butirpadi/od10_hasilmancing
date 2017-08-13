from odoo import api, fields, models

class hm_account_invoice(models.Model):
	_inherit = "account.invoice"

	# @api.onchange('state')
	# def _onchange_state(self):
	# 	print 'account_invoice state change : ' + str(self.state)

	partner_id = fields.Many2one('res.partner', string='Customer', change_default=True,
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        track_visibility='always')

	@api.multi
	def action_invoice_paid(self):    	
		super(hm_account_invoice,self).action_invoice_paid()

		# jika status invoice paid, maka sale_order harus di lock.
		# print 'invoice_id =' + str(self.id)
		inv = self.env['account.invoice'].search([('id','=',self.id)])
		# print 'invoice state : ' + str(self.state)
		# print 'inv state : ' + str(inv.state)
		if str(inv.state) == 'paid':
			print 'INVOICE STATE-NYA SUDAH PAID'
			for inv_line in self.invoice_line_ids:
				print 'inside invoice line loop'
				print 'invoice_line id : ' + str(inv_line.id)
				for so_line in inv_line.order_line_ids:
					print 'inside SO line loop'
					print 'sale order id : ' + str(so_line.order_id.id)
					print 'sale order name : ' + str(so_line.order_id.name)
					so = so_line.order_id
					print ('Set to Done SO') 
					so.action_done()