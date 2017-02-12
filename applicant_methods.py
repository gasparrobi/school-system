import random
import string

try:
    from .models import *
except Exception:
    from models import *


class Applicant_methods:

    @staticmethod
    def generate_random():
        existing_ids = Applicant_methods.get_all_applicant_id()
        generated = ''
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.ascii_lowercase)
        generated += random.choice(string.digits)
        generated += random.choice(string.ascii_uppercase)
        generated += random.choice(string.digits)
        if generated in existing_ids:
            Applicant_methods.generate_random()
        return generated

    @classmethod
    def get_all_applicant_id(cls):
        id_list = []
        all_id = Applicant.select().where(Applicant.applicant_id.is_null(False))
        for item in all_id:
            id_list.append(item.applicant_id)
        return id_list

    @classmethod
    def get_applicants_without_id(cls):
        id_list = []
        without_id = Applicant.select().where(Applicant.applicant_id.is_null(True))
        for item in without_id:
            id_list.append(item.id)
        return id_list

    # MAIN FUNCTION ##### checks, generates and assignes new applicant_ids
    @classmethod
    def assign_id_to_applicant(cls, applicant):
        new_id = cls.generate_random()
        applicant.applicant_id = new_id
        applicant.save()

    @classmethod
    def assign_school_to_applicant(cls, applicant):
        city = City.get(City.city_name == applicant.city)
        applicant.school = city.location
        applicant.save()

    @classmethod
    def get_list(cls):
        table = Applicant.select()
        lista = [("APPLICANT ID", "NAME", "CITY", "STATUS")]
        for item in table:
            if len(item.interview)==0:
                lista.append(
                    (item.applicant_id, item.first_name, item.last_name, item.email, item.city, item.status,
                     item.school.name,'False'))
            else:
                lista.append(
                    (item.applicant_id, item.first_name, item.last_name, item.email, item.city, item.status,
                     item.school.name, 'True'))
        return lista
