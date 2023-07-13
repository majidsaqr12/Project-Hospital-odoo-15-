from odoo import fields, models, api
from datetime import date
from dateutil import relativedelta


class AlhilalNurse(models.Model):
    _name = 'alhilal.nurse'
    _description = 'Alhilal Nurse'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal info
    name = fields.Char(string="Name", tracking=True)
    nurse_id = fields.Char(readonly=True)
    age = fields.Integer(string="Age", compute="_compute_age", tracking=True,
                         inverse='_inverse_compute_age', search="_search_age")
    date_of_birth = fields.Date(string="Date Of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    image = fields.Image(string="Image")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")
    active = fields.Boolean(string="Active", default=True, tracking=True)

    job_title = fields.Char(string="Job Title", tracking=True)
    department = fields.Selection(
        [('emergency', 'Emergency Department'), ('intensive care unit', 'Intensive Care Unit (ICU)'),
         ('surgery ', 'Surgery Department'), ('pediatrics', 'Pediatrics Department:'),
         ('obstetrics and gynecology', 'Obstetrics and Gynecology Department'),
         ('cardiology', 'Cardiology Department'), ('oncology', 'Oncology Department'),
         ('neurology', 'Neurology Department:'), ('psychiatry', 'Psychiatry Department'),
         ('radiology', 'Radiology Department')], string="Department", tracking=True)
    employment_status = fields.Selection([('full time', 'Full-time'), ('part time', 'Part-time')],
                                         string="Employment Status", tracking=True)
    work_experience = fields.Selection([('1-2', '1-2'), ('2-4', '2,4'), ('4-8', '4-8'), ('8-10', '8-10')])
    salary = fields.Integer(string="Salary")

    # Notebooks
    educational_qualifications = fields.Html()
    performance_evaluations = fields.Html()
    medical_records = fields.Html()
    criminal_background_checks = fields.Html()
    training_records = fields.Html()
    disciplinary_actions = fields.Html()
    professional_licenses_and_certifications = fields.Html()

    @api.model
    def create(self, vals_list):
        # create sequence
        vals_list['nurse_id'] = self.env['ir.sequence'].next_by_code('alhilal.nurse')
        return super(AlhilalNurse, self).create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
