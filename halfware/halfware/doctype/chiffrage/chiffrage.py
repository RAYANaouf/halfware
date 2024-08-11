# Copyright (c) 2024, rayan aouf  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Chiffrage(Document):

	def on_change(self):
		total_cost = 0
		additional_bill = 0

		for material       in self.get("materials"):
                 	total_cost += float(material.total_cost or 0 )

		for service        in self.get("services"):
			total_cost += float(service.cost or 0 )

		for human_resource in self.get("human_resources"):
			total_cost += float(human_resource.total_cost or 0 )

		for other_resource in self.get("others"):
			total_cost += float(other_resource.cost or 0 )

		for bill           in self.get("bills"):
			additional_bill += float(bill.cost or 0 )

		marge = 0
		risk  = 0

		if self.risque_type == "Taux" :
			risk  = ( self.risque_taux * total_cost / 100 )
		else:
			risk  = self.risque_montant

		if self.marge_type == "Percent" :
			marge = (  self.marge_percentage * total_cost / 100 )
		else:
			marge = self.marge_montant

		self.total_project_cost = total_cost + risk
		self.billed_amount      = total_cost + risk + marge + additional_bill


