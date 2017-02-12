from models import *
import random


class interview_methods:
    @staticmethod
    def random_slot(applicant):
        print(applicant.school)

        if applicant.school is not None:
            free_slots = InterviewSlot.select().join(Mentor).where(
                (InterviewSlot.reserved == False) & (Mentor.school == applicant.school.id))
        else:
            print('Applicant has no school yet,please assign school first')
            return None
        try:
            free_slot = random.choice(free_slots)
        except IndexError:
            return None
        return free_slot

    @classmethod
    def assign_interviews(cls):
        sub = interview_methods.select_applicant_wo_interview()
        for applicant in sub:
            slot = cls.random_slot(applicant)
            if slot is None:
                print('There is no available interview slot for ', applicant.first_name, applicant.last_name)
                return False
            Interview.create(applicant=applicant.id, slot=slot.id)
            InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @classmethod
    def assign_second_mentor(cls, interview):
        sub = InterviewSlot.select().join(Interview, join_type=JOIN_LEFT_OUTER).switch(InterviewSlot).join(
            Mentor).where((InterviewSlot.start == interview.slot.start) & (InterviewSlot.reserved == False) &
                          (Mentor.school == interview.applicant.school))
        if len(sub) == 0:
            print('Impossibru')
        else:
            slot = random.choice(sub)
            Interview.update(slot_mentor2=slot.id).where(Interview.id == interview.id).execute()
            InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()

    @classmethod
    def assign_interview(cls, applicant):
        slot = cls.random_slot(applicant)
        if slot is None:
            print('There is no available interview slot for ', applicant.first_name, applicant.last_name)
            return False
        Interview.create(applicant=applicant.id, slot=slot.id)
        InterviewSlot.update(reserved=True).where(InterviewSlot.id == slot.id).execute()
    @classmethod
    def get_interviews(cls):
        return  Interview.select()
