import stress

class PersonNumber:
  def __init__(self, person, number):
    self.person = person
    self.number = number

class Verb:
  def __init__(self,
      stem,
      ppn, apn=PersonNumber(0, 1),
      ):
    pass