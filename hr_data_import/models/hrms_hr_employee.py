# -*- coding: utf-8 -*-

from odoo import models, fields, api, _





class HrmsHrEmployee(models.Model):
    _name = "hrms.hr.employee"
    _description = 'HR Employee HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one(
        'hr.data.dashboard', string="HRMS Instance", required=True)
    created_at = fields.Datetime()
    updated_at = fields.Datetime()
    active = fields.Boolean(default=True)
    hrms_external_id = fields.Char(string="HRMS Employee ID")
    employee_id = fields.Many2one('hr.employee', string="Employee", ondelete="cascade")
    exported_in_hrms = fields.Boolean(default=False)
    email = fields.Char(string='Email')
    job_id = fields.Many2one('hr.job', string='Position')
    residence = fields.Char(string='Residence')
    residence_comment = fields.Text(string='Residence Comment')
    country = fields.Many2one('res.country', string='Country')
    city = fields.Char(string='City')
    birth_date = fields.Date(string='Birth Date')
    linked_in = fields.Char(string='LinkedIn')
    skype = fields.Char(string='Skype')
    phone = fields.Char(string='Phone')
    telegram = fields.Char(string='Telegram')
    additional_email = fields.Char(string='Additional Email')
    additional_phone = fields.Char(string='Additional Phone')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
    start_date = fields.Date(string="Start Date")
    relocate = fields.Boolean(string="Relocate")
    duties = fields.Text(string="Duties")
    description = fields.Text(string="Description")
    additional_info = fields.Text(string="Additional Info.")
    skills = fields.Char(string="Skills")
    skill_ids = fields.Many2many('hr.skill', string='Skills')
    languages = fields.Char(string="Languages")
    language_ids = fields.Many2many('res.lang', string='Languages')
    team_ids = fields.Many2many('hr.department', string='Teams')
    career_ids = fields.One2many('hrms.hr.career', 'hrms_employee_id', string='Career')
    contact_ids = fields.One2many('hrms.hr.contact', 'hrms_employee_id', string='Contacts')
    awards = fields.Char(string="Awards")
    educations = fields.Char(string="Educations")


    class HRCareer(models.Model):
        _name = 'hrms.hr.career'
        _description = 'HR Career'

        start_date = fields.Date(string="Start Date")
        end_date = fields.Date(string="End Date")
        test_period_start_date = fields.Date(string="Test Period Start Date")
        test_period_end_date = fields.Date(string="Test Period End Date")
        company_name = fields.Char(string="Company Name")
        department = fields.Char(string="Department")
        position = fields.Char(string="Position")
        grade = fields.Char(string="Grade")
        place = fields.Char(string="Place")
        team = fields.Char(string="Team")
        comment = fields.Text(string="Comment")
        employee_id = fields.Many2one('hr.employee', string="Employee")
        hrms_employee_id = fields.Many2one('hrms.hr.employee', string="HRMS Employee")

    class HRContact(models.Model):
        _name = 'hrms.hr.contact'
        _description = 'HR Contact'

        type_id = fields.Integer(string="Type ID")
        type_name = fields.Char(string="Type Name")
        value = fields.Char(string="Value")
        employee_id = fields.Many2one('hr.employee', string="Employee")
        hrms_employee_id = fields.Many2one('hrms.hr.employee', string="HRMS Employee")


    # def shopify_create_contact_partner(self, vals, instance, queue_line):
    #     """
    #     This method is used to create a contact type customer.
    #     @author: Maulik Barad on Date 09-Sep-2020.
    #     @change : pass category_id as tag on vals by Nilam Kubavat for task id : 190111 at 19/05/2022
    #     """
    #     partner_obj = self.env["res.partner"]
    #     common_log_line_obj = self.env["common.log.lines.ept"]

    #     shopify_instance_id = instance.id
    #     shopify_customer_id = vals.get("id", False)
    #     first_name = vals.get("first_name", "")
    #     last_name = vals.get("last_name", "")
    #     email = vals.get("email", "")

    #     if not first_name and not last_name and not email:
    #         message = "First name, Last name and Email are not found in customer data."
    #         common_log_line_obj.create_common_log_line_ept(shopify_instance_id=instance.id, message=message,
    #                                                        model_name='res.partner',
    #                                                        shopify_customer_data_queue_line_id=queue_line.id
    #                                                        if queue_line else False)
    #         return False

    #     name = ""
    #     if first_name:
    #         name = "%s" % first_name
    #     if last_name:
    #         name += " %s" % last_name if name else "%s" % last_name
    #     if not name and email:
    #         name = email

    #     partner = self.search_shopify_partner(shopify_customer_id, shopify_instance_id)
    #     tags = vals.get("tags").split(",") if vals.get("tags") != '' else vals.get("tags")
    #     tag_ids = []
    #     for tag in tags:
    #         tag_ids.append(partner_obj.create_or_search_tag(tag))

    #     if partner:
    #         if not partner.parent_id:
    #             partner = self.update_partner_with_company(instance, vals.get("default_address", {}), False, partner)
    #         partner.write({"category_id": tag_ids})
    #         return partner

    #     shopify_partner_values = {"shopify_customer_id": shopify_customer_id,
    #                               "shopify_instance_id": shopify_instance_id}
    #     if email:
    #         partner = partner_obj.search_partner_by_email(email)

    #         if partner:
    #             partner.write({"is_shopify_customer": True, "category_id": tag_ids})
    #             shopify_partner_values.update({"partner_id": partner.id})
    #             self.create(shopify_partner_values)
    #             return partner

    #     partner_vals = self.shopify_prepare_partner_vals(vals.get("default_address", {}), instance)
    #     partner_vals.update({
    #         "name": name,
    #         "email": email,
    #         "customer_rank": 1,
    #         "is_shopify_customer": True,
    #         "type": "contact",
    #         "category_id": tag_ids,
    #         "phone": vals.get("phone", "") if not partner_vals.get("phone") else partner_vals.get("phone")
    #     })
    #     partner = partner_obj.create(partner_vals)

    #     shopify_partner_values.update({"partner_id": partner.id})
    #     self.create(shopify_partner_values)
    #     partner = self.update_partner_with_company(instance, vals.get("default_address", {}), False, partner)
    #     return partner

    # def search_shopify_partner(self, shopify_customer_id, shopify_instance_id):
    #     """ This method is used to search the shopify partner.
    #         :param shopify_customer_id: Id of shopify customer which receive from customer response.
    #         @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 27 October 2020 .
    #         Task_id: 167537
    #     """
    #     partner = False
    #     shopify_partner = self.search([("shopify_customer_id", "=", shopify_customer_id),
    #                                    ("shopify_instance_id", "=", shopify_instance_id)], limit=1)
    #     if shopify_partner:
    #         partner = shopify_partner.partner_id
    #         return partner

    #     return partner

    # def shopify_prepare_partner_vals(self, vals, instance=False):
    #     """
    #     This method used to prepare a partner vals.
    #     @param : self,vals
    #     @return: partner_vals
    #     @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 29 August 2020 .
    #     Task_id: 165956
    #     @change : pass lang on vals by Nilam Kubavat for task id : 190111 at 19/05/2022
    #     """
    #     partner_obj = self.env["res.partner"]

    #     first_name = vals.get("first_name")
    #     last_name = vals.get("last_name")
    #     name = "%s %s" % (first_name, last_name)

    #     zipcode = vals.get("zip")
    #     state_code = vals.get("province_code")

    #     country_code = vals.get("country_code")
    #     country = partner_obj.get_country(country_code)

    #     state = partner_obj.create_or_update_state_ept(country_code, state_code, zipcode, country)

    #     partner_vals = {
    #         "email": vals.get("email") or False,
    #         "name": name,
    #         "phone": vals.get("phone"),
    #         "street": vals.get("address1"),
    #         "street2": vals.get("address2"),
    #         "city": vals.get("city"),
    #         "zip": zipcode,
    #         "state_id": state and state.id or False,
    #         "country_id": country and country.id or False,
    #         "is_company": False,
    #         'lang': instance.shopify_lang_id.code if instance != False else None,
    #     }
    #     update_partner_vals = partner_obj.remove_special_chars_from_partner_vals(partner_vals)
    #     return update_partner_vals