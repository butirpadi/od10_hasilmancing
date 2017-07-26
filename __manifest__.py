# -*- coding: utf-8 -*-
{
    'name': "UD Hasil Mancing",

    'summary': """
        Aplikasi UD Hasil Mancing""",

    'description': """
        Aplikasi UD Hasil Mancing
        Pembelian
        Penjualan
        Pengiriman
        Keuangan
        Kepegawaian
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
        # 'views/hm_demo_data.xml',
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
        'views/hm_sale_view.xml',
        'views/hm_report_paper_format.xml',
        'views/hm_delivery_report_view.xml',
        'views/hm_wiz_sale_report.xml',
        'views/hm_wiz_sale_view.xml',
        'views/hm_wiz_tagihan_report.xml',
        'views/hm_wiz_tagihan_custom_report.xml',
        'views/hm_wiz_tagihan_view.xml',
        'views/hm_account_invoice_view.xml',
        'views/menu.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}