{
	'name': "Real Estate",
	'depends':[
		'base',
		],
	'data':[
		'views/inherited_res_user_views.xml',
		'views/estate_property_offer_views.xml',
		'views/estate_property_tag_views.xml',
		'views/estate_property_type_views.xml',
		'views/estate_property_views.xml',
		'views/estate_menus.xml',
		'security/ir.model.access.csv',
],
	'application':True,
	'installable':True, 
}
