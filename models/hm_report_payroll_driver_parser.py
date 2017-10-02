from odoo import api, models

class hm_report_payroll_driver_parser(models.AbstractModel):
    _name = 'report.hasilmancing.pay_slip_report_template'
    _template = 'hasilmancing.pay_slip_report_template'

    def _get_catatan_slip_gaji(self):
        # code = self.pool.get('ir.sequence').next_by_code(self.cr, self.uid, seq_code)
        hmset = self.env['hm_setting'].search([('id','=',1)])
        # hmset = self.pool.get('hm_setting').search([('id','=',1)])
        return hmset.catatan_slip_gaji
        # return 'eries hermanto'
        # field = self.pool.get('hm_setting')._fields['catatan_slip_gaji']
        # env = api.Environment(self.cr, self.uid, self.localcontext)
        # val = dict(field.get_description(env)['selection'])[value]
        # return self._translate(val)

    @api.model
    def render_html(self, docids, data=None):
        payslips = self.env['hm_payroll_driver'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'hm_payroll_driver',
            'docs': payslips,
            'data': data,
            '_get_catatan_slip_gaji': self._get_catatan_slip_gaji,
        }
        return self.env['report'].render('hasilmancing.pay_slip_report_template', docargs)

