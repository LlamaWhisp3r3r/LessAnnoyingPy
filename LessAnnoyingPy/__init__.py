"""
Communicates to the Less Annoying CRM API using python

Classes
-------
CRM(token_location='config.json', url="https://api.lessannoyingcrm.com")
    API connecter for Less Annoying CRM
Contact(FullName=None, Salutation=None, FirstName=None, MiddleName=None,
             LastName=None, Suffix=None, CompanyName=None, CompanyId=None,
             Title=None, Industry=None, NumEmployees=None, BackgroundInfo=None,
             Email=None, Phone=None, Address=None, Website=None, Birthday=None,
             CustomFields=None, AssignedTo=None, ContactId=None)
    Contact template to ease the process of the CRM class
"""

__version__ = "1.0.0"
