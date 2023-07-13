from odoo import fields, models, api, _
from datetime import date
from dateutil import relativedelta
from odoo.exceptions import ValidationError


class AlhilalDoctor(models.Model):
    _name = "alhilal.doctor"
    _description = "Alhilal Doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Personal info
    doctor_id = fields.Char(readonly=True)
    name = fields.Char(string="Name", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", tracking=True, store=True,
                         inverse='_inverse_compute_age', search="_search_age")
    date_of_birth = fields.Date(string="Date Of Birth", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")

    # Professional info
    medical_degree = fields.Selection([('good', 'Good'), ('very good', 'Very good'), ('excellent', 'Excellent')],
                                      string="Medical Degree", tracking=True)
    specialty = fields.Selection([('anesthesiology', 'Anesthesiology'), ('cardiology', 'Cardiology'),
                                  ('dermatology', 'Dermatology'), ('emergency medicine', 'Emergency Medicine'),
                                  ('endocrinology', 'Endocrinology'), ('gastroenterology', 'Gastroenterology'),
                                  ('hematology/oncology', 'Hematology/Oncology'),
                                  ('infectious disease', 'Infectious Disease'),
                                  ('internal medicine', 'Infectious Disease'),
                                  ('nephrology', 'Nephrology')], string="specialty", tracking=True)
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

    image = fields.Image(string="Image")
    work_experience = fields.Selection([('1-2', '1-2'), ('2-4', '2-4'), ('4-8', '4-8'), ('8-10', '8-10')])
    salary = fields.Integer(string="Salary")
    active = fields.Boolean(string="Active", default=True, tracking=True)

    # notebook
    performance_date = fields.Html()
    medical_records = fields.Html()
    training_records = fields.Html()
    research_publications = fields.Html()

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

    # ( Method To Check on Fields )
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date of birth is not acceptable"))

    @api.onchange('specialty')
    def onchange_specialty(self):
        self.job_title = self.specialty

    @api.model
    def create(self, vals_list):
        # create sequence
        vals_list['doctor_id'] = self.env['ir.sequence'].next_by_code('alhilal.doctor')
        return super(AlhilalDoctor, self).create(vals_list)