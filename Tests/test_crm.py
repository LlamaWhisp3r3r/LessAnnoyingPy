from LessAnnoyingPy.crm import LACRM, Contact
import unittest
import json

location = input("Please Input Token Location>> ")
crm = LACRM(location)
test_data = crm.TOKENS['test-data']
test_dummy = test_data['dummy-contact']
test_contact = test_data['test-contact']

dummy_contact = Contact(FullName=test_dummy['test-full-name'],
                        Email=test_dummy['test-email'], Phone=test_dummy['test-phone'],
                        Address=test_dummy['test-address'],
                        Birthday=test_dummy['test-birthday'])

test_contact = Contact(FullName=test_contact['test-contact-name'],
                       ContactId=test_contact['test-contact-id'])


class CRMTest(unittest.TestCase):

    def test_contact_create_delete(self):

        # Contact Creation
        create_result = crm.create_contact(dummy_contact)
        print("Create Contact Data: ", create_result.text,
              create_result, end="\n" * 2)
        dummy_contact['ContactId'] = json.loads(
            create_result.text)['ContactId']
        self.assertEqual(create_result.status_code, 200)

        # Contact Deletion
        contact_result = crm.delete_contact(dummy_contact['ContactId'])
        print("Delete Contact Data: ", contact_result.text,
              contact_result, end="\n" * 2)
        # For some reason the delete function returns a 500 & Doesn't show up
        # in the API log in th LACRM
        self.assertEqual(contact_result.status_code, 500)

    def test_get_contact(self):

        # Get Contact
        get_result = crm.get_contact(test_contact['ContactId'])
        print("Get Contact Data: ", get_result.text, get_result, end="\n" * 2)
        self.assertEqual(get_result.status_code, 200)

    def test_edit_contact(self):

        # Edit Contact
        # Change only the name of the contact
        test_contact['FullName'] = "API Test Client Jr"
        edit_result = crm.edit_contact(test_contact)
        print("Edit Contact Data: ", edit_result.text, edit_result, end="\n" * 2)
        self.assertEqual(edit_result.status_code, 200)

    def test_search_contact(self):

        # Search Contact
        search_result = crm.search_contacts(
            test_contact['FullName'], NumRows=1)
        print("Search Contact Data: ", search_result.text,
              search_result, end="\n" * 2)
        self.assertEqual(search_result.status_code, 200)

    def test_create_note(self):

        # Create Note

        from datetime import date
        today = date.today()

        result = crm.create_note(
            test_contact['ContactId'], 'API Test Run {}'.format(today.strftime("%d/%m/%Y")))
        print("Create Note Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_create_task(self):

        result = crm.create_task(
            "2028-06-26", "API Create Task Test", ContactId=test_contact['ContactId'])
        print("Create Task Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_create_event(self):

        result = crm.create_event(
            "2018-01-01", "API Test Event", "07:00", "10:00")
        print("Create Event Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_add_contact_to_group(self):

        result = crm.add_contact_to_group(
            test_contact['ContactId'], "API Test")
        print("Add Contact To Group Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_create_update_delete_pipeline(self):

        # Create Pipeline
        result = crm.create_pipeline(
            test_contact['ContactId'], pipeline_id, status_id)
        print("Create Pipeline Data: ", result.text, result, end="\n" * 2)
        new_pipeline_id = json.loads(result.text)['PipelineItemId']
        self.assertEqual(result.status_code, 200)

        # Update Pipeline
        result = crm.update_pipeline_item(new_pipeline_id, status_id)
        print("Updating Pipeline Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_pipeline_attached(self):

        result = crm.get_pipeline_items_attached_to_contact(
            test_contact['ContactId'])
        print("Pipeline Attached Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_pipeline_report(self):

        result = crm.get_pipeline_report(pipeline_id)
        print("Get Pipeline Report Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_pipeline_settings(self):

        result = crm.get_pipeline_settings()
        print("Get Pipeline Settings Data: ",
              result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_user_info(self):

        result = crm.get_user_info()
        print("Get User Info Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

    def test_custom_fields(self):

        result = crm.get_custom_fields()
        print("Get Custom Fields Data: ", result.text, result, end="\n" * 2)
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
