# -*- coding: utf-8 -*-
{
    'name': "UD Hasil Mancing",

    'summary': """
        Aplikasi UD Hasil Mancing""",

    'description': """
        Aplikasi UD Hasil Mancing meliputi Pembelian, Penjualan, Pengiriman, Keuangan, Kepegawaian
    """,

    'author': "butirpadi",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','sale','account','inputmask_widget','odoo_web_login'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/hm_data_demo.xml',
        'views/hm_resource.xml',
        'views/hm_data_system_parameter.xml',
        'views/hm_data_provinsi_kabupaten_kecamatan.xml',
        'views/hm_appconfig_data.xml',
        'views/hm_provinsi_view.xml',
        'views/hm_kabupaten_view.xml',
        'views/hm_kecamatan_view.xml',
        'views/hm_galian_view.xml',
        'views/hm_alat_berat_view.xml',
        'views/hm_armada_view.xml',
        'views/hm_karyawan_view.xml',
        'views/hm_appconfig_view.xml',
        'views/hm_material_view.xml',
        'views/hm_sparepart_view.xml',
        'views/hm_customer_view.xml',
        'views/hm_supplier_view.xml',
        # 'views/hm_sale_view.xml',
        'views/hm_report_paper_format.xml',
        'views/hm_delivery_report_view.xml',
        'views/hm_wiz_sale_report.xml',
        'views/hm_wiz_sale_view.xml',
        'views/hm_wiz_tagihan_report.xml',
        'views/hm_wiz_tagihan_custom_report.xml',
        'views/hm_wiz_tagihan_view.xml',
        'views/hm_account_invoice_view.xml',
        'views/hm_purchase_view.xml',
        'views/hm_wiz_purchase_view.xml',
        'views/hm_new_sale_view.xml',
        'views/hm_op_alat_berat_views.xml',
        'views/hm_report_payroll_driver.xml',
        'views/hm_payroll_driver_view.xml',
        'views/hm_presensi_views.xml',
        'views/hm_presensi_rekap_view.xml',
        'views/hm_finance_cash_pendapatan_views.xml',
        'views/hm_finance_cash_pengeluaran_views.xml',
        'views/hm_finance_jurnal_kas_form.xml',
        'views/hm_finance_jurnal_kas_views.xml',
        'views/hm_report_jurnal.xml',
        'views/hm_wiz_jurnal_view.xml',

        'views/hm_pay_week_view.xml',
        'views/hm_setting_view.xml',
        'views/hm_generate_pay_week.xml',
        'views/hm_generate_pay_driver_view.xml',
        
        'views/hm_report_payroll_staff.xml',
        'views/hm_payroll_staff_view.xml',        
        'views/hm_generate_payroll_staff_view.xml',

        'views/hm_report_op_alat.xml',
        'views/hm_wiz_report_operasional_alat.xml',
        
        'views/hm_ir_sequence_data.xml',
        'views/menu.xml',
        # 'views/templates.xml',
    ],
    'css': [
        'static/source/css/form_sheet.css'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}