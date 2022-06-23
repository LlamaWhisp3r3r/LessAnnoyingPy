import requests
import json


class LACRM:
    """API connecter for Less Annoying CRM

    Methods
    -------
    create_contact(contact)
        Add a new contaact or company to CRM
    get_contact(ContactId)
        Use to retrieve a contact's information
    edit_contact(contact)
        Use to edit an existing contact
    delete_contact(ContactId)
        Use to remove a contact
    search_contacts(SearchTerm, SortType="Relevance", NumRows=1, Page=1, RecordType="Contacts")
        Search for one or more contact(s)
    """

    def __init__(self, token_location='config.json',
                 url="https://api.lessannoyingcrm.com"):
        """
        Parameters
        ----------
        token_location : str, optional
            Location of token file used to authenticate with LACRM API
        url : str, optional
            LACRM API endpoint

        Returns
        -------
        CRM
            CRM instance
        """
        self.__URL = url
        self.__TOKENLOCATION = token_location
        self.__set_tokens()

    def __set_tokens(self):
        with open(self.__TOKENLOCATION) as f:
            self.TOKENS = json.load(f)['crm-tokens']

    def __add_api_function(self, parameters, function):
        try:
            del parameters['self']
        except KeyError:
            pass

        parameters["UserCode"] = self.TOKENS['user-token']
        parameters["APIToken"] = self.TOKENS['api-token']
        parameters['Function'] = function

    def __remove_none_params(self, parameters):
        for i in list(parameters):
            if not parameters[i]:
                del parameters[i]

        return parameters

    def create_contact(self, contact):
        """Add a new contact or company to CRM

        Parameters
        ----------
        contact : Contact
            Contact object containing all the needed information to pass to the crm API

        Returns
        -------
        requests.models.Response
            Results form the API request
        """

        parameters = self.__remove_none_params(contact.contact_info)

        self.__add_api_function(parameters, 'CreateContact')

        return requests.post(self.__URL, json=parameters)

    def get_contact(self, ContactId):
        """Use to retrieve a contact's information

        Parameters
        ----------
        ContactId : str
            Id of the contact

        Returns
        -------
        requests.models.Response
            Results form the API request
        """

        parameters = locals()

        self.__add_api_function(parameters, 'GetContact')

        return requests.post(self.__URL, json=parameters)

    def edit_contact(self, contact):
        """Use to edit an existing contact

        Parameters
        ----------
        contact : Contact
            Contact object containing all the needed information to pass to the
            crm API. Needs to make sure that this contact has ContactId set

        Returns
        -------
        requests.models.Response
            Results form the API request
        """

        parameters = self.__remove_none_params(contact.contact_info)

        self.__add_api_function(parameters, 'EditContact')

        return requests.post(self.__URL, json=parameters)

    def delete_contact(self, ContactId):
        """Use to remove contacts
            NOTE: This returns a 500 code when successful

        Parameters
        ----------
        ContactId : str
            Id of a the contact

        Returns
        -------
        requests.models.Response
            Results form the API request
        """

        parameters = locals()

        self.__add_api_function(parameters, 'DeleteContact')

        return requests.post(self.__URL, json=parameters)

    def search_contacts(self, SearchTerms, Sort=None, NumRows=None, Page=None, RecordType=None):
        """Search for one or more contact(s)

        Parameters
        ----------
        SearchTerm : str
            The terms you want to search for (contact name, email, phone, etc.)
        SortType : str, optional
            Can be FirstName, LastName, DateEntered, DateEdited, or Relevance (Default is Relevance)
        NumfRows : int, optional
            The maximum number of rows you want returned. Can be between 1 and 500
        Page : int, optional
            Use this if your results are limited by the number of Rows
        RecordType : str, optional
            By default, contacts and companies will be returned by this function.
            You can pass "Contacts" or "Companies" into this function if you
            want to filter to only get one record type or the other

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = locals()

        self.__add_api_function(parameters, 'SearchContacts')

        return requests.post(self.__URL, json=parameters)

    def create_note(self, ContactId, Note):
        """Use to add a note to a contact's history

        Parameters
        ----------
        ContactId : str
            Id of the contact
        Note : str
            Text that should appear in the note field

        Returns
        -------
        requests.models.Response
            Requests results
        """

        parameters = locals()

        self.__add_api_function(parameters, 'CreateNote')

        return requests.post(self.__URL, json=parameters)

    def create_task(self, DueDate, Name, Description=None, ContactId=None,
                    AssignedTo=None):
        """Use to add a task in your CRM. You can optionally attach tasks to
        contacts and assign them to other users

        Parameters
        ----------
        DueDate : str
            The date the task is due. If you enter it in the past, it will show
            up as an overdue task. The format should be YYYY-MM-DD
        Name : str
            The name of the task
        Description : str, optional
            Any additional information related to this task
        ContactId : str, optional
            The Id of a the contact this task is related to
        AssignedTo : int, optional
            If you want to assign this task to another user, pass their UserId using this parameter

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = self.__remove_none_params(locals())

        self.__add_api_function(parameters, 'CreateTask')

        return requests.post(self.__URL, json=parameters)

    def create_event(self, Date, Name, StartTime, EndTime, Description=None,
                     Contacts=None, Users=None):
        """Use to add an event to your calendar. Optionally can attach contacts and other users to the event of choosing

        Parameters
        ----------
        Date : str
            The date of the event. The format should be YYYY-MM-DD
        Name : str
            The name of the event
        StartTime : str, optional
            The start time of the event. The format should be hh:mm (24 hour format).
            Enter this in the local time based on the timezone set in your CRM account
        EndTime : str, optional
            The end time of the event. The format should be hh:mm (24 hour format).
            Enter this in the local time based on the timezone set in your CRM account
        Description : str, optional
            A text field for entering any other details about the event
        Contacts : dict, optional
            An array with the Ids of the contacts you want to attach to the event:
            E.x. [ContactId1, ContactId2]
        Users : type, optional
            And array with the Ids of the users that are attending the event.
            If you leave this parameter out, it will automatically be assigned to you.
            If you use this parameter, the event will only be assigned to you if you include your own Id in the array
            E.x. [UserId1, UserId2]

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = self.__remove_none_params(locals())

        self.__add_api_function(parameters, 'CreateEvent')

        return requests.post(self.__URL, json=parameters)

    def add_contact_to_group(self, ContactId, GroupName):
        """Use to add a contact to one of the groups in your CRM. Before calling
        this function, make sure you have already created the group

        Parameters
        ----------
        ContactId : str
            The Id of the contact that should be added to the group
        GroupName : str
            The name of the group. NOTE: If there are any spaces in the group
            name, you must replace them with underscores (_)

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = locals()

        self.__add_api_function(parameters, 'AddContactToGroup')

        return requests.post(self.__URL, json=parameters)

    def create_pipeline(self, ContactId, PipelineId, StatusId, Priority=None, CustomFields=None, Note=None):
        """Use to attach a new pipeline to a contact or company in your CRM

        Parameters
        ----------
        ContactId : str
            The Id of the contact or company you want to attach this pipeline to
        PipelineId : str
            The Id of the pipeline type you want to create
        StatusId : str
            The Id of the status for this pipeline
        Priority : int, optional
            Priority can be 1 (low), 2 (medium), or 3 (high)
        CustomFields : dict, optional
            You can save information to any custom pipeline fields you've created:
            {
                'UserCreatedFieldId': 'DataToSetFieldTo',
                ...
            }
        Note : str, optional
            A note to include with the first update

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = self.__remove_none_params(locals())

        self.__add_api_function(parameters, 'CreatePipeline')

        return requests.post(self.__URL, json=parameters)

    def get_pipeline_items_attached_to_contact(self, ContactId):
        """The GetPipelineItemsAttachedToContact function is used to retrieve a
            list of all pipeline items that have been attached to a contact.
            For example, if you have a "Lead" pipeline and you attach a lead to a contact,
            this function will return the info associated with that lead.

            If successful, this function will return an array of pipeline items.
            Each pipeline item will contain information about that specific item
            include the PipelineId (e.g. the Id corresponding to the "Lead" pipeline),
            the PipelineItemId (e.g. the Id corresponding to this particular lead) and
            information about the pipeline item such as the status and custom field values

        Parameters
        ----------
        ContactId : str
            Id of the contact you want to retrieve the pipeline items for

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = locals()

        self.__add_api_function(
            parameters, 'GetPipelineItemsAttachedToContact')

        return requests.post(self.__URL, json=parameters)

    def update_pipeline_item(self, PipelineItemId, StatusId, Priority=None,
                             CustomFields=None, Note=None):
        """Use to edit an existing pipeline item in the CRM

        Parameters
        ----------
        PipelineItemId : str
            Id of the pipeline item you want to update
        StatusId : str
            Id of the status for this pipeline
        Priority : int, optional
            Priority can be 1 (low), 2 (medium), or 3 (high)
        CustomFields : dict, optional
            You can save information to any custom pipeline fields you've created.
            NOTE: we will only update the custom fields that you pass us in this array.
            For example, if you have two custom fields defined but you only pass us one,
            we'll update that field and leave the other one alone
            {
                'UserCreatedFieldId': 'DataToSetFieldTo',
                ...
            }
        Note : str
            A note to include with the first update

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = self.__remove_none_params(locals())

        self.__add_api_function(parameters, 'UpdatePipelineItem')

        return requests.post(self.__URL, json=parameters)

    def get_pipeline_report(self, PipelineId, SortBy=None, NumRows=None, Page=None,
                            SortDirection=None, UserFilter=None, StatusFilter=None):
        """Retrieve data from a pipeline report. It will include the contact and
            pipeline data for any contacts/companies in the pipeline

        Parameters
        ----------
        PipelineId : str
            Unique identifier of the pipeline you want to retrieve
        SortBy : str, optional
            The field you'd like to sort the results by. Can be Priority,
            DateNote (the date of the last pipeline update), ContactName, or Status
        NumRows : int, optional
            The number of records returned. The default is 100,
            but you can set it to any number between 1 and 500.
            Note that if a contact has more than one pipeline attached to them,
            they might appear more than once
        Page : int, optional
            Use this if your results are limited by the number of Rows.
            For example, if your first search is capped at NumRows, you can then
            run a second search with Page = 2, and then another with Page = 3 in
            order to retrieve even more results
        SortDirection : str, optional
            Can be ASC to sort from low to high or DESC to sort from
            high to low. Defaults to ASC
        UserFilter : str, optional
            Defaults to show all records the API user has access to,
            but you can pass in a specific UserId to only show contacts assigned to that user
        StatusFilter : str, optional
            Set which statuses to return. By default, only open statuses will
            be returned but you can set this to "all" to show all statuses (open and closed),
            "closed" to only show closed statuses, or pass a specific StatusId
            to only show that particular status

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = self.__remove_none_params(locals())

        self.__add_api_function(parameters, 'GetPipelineReport')

        return requests.post(self.__URL, json=parameters)

    def get_pipeline_settings(self):
        """The GetPipelineSettings function will return a list of all of your
            pipelines along with each pipeline's ID and a list of statuses.
            This can be helpful for retrieving pipeline and status IDs so that
            you can attach pipeline items to your contacts via the API.

            Note: This function does not return individual pipeline items
            (e.g. a list of your leads).
            It returns the pipeline categories themselves (e.g. if you have a
            lead pipeline, a trouble ticket pipeline, and an invoices pipeline,
            this will return three results)

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = dict()

        self.__add_api_function(parameters, 'GetPipelineSettings')

        return requests.post(self.__URL, json=parameters)

    def get_user_info(self):
        """Retrieve meta information about your CRM account

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = dict()

        self.__add_api_function(parameters, 'GetUserInfo')

        return requests.post(self.__URL, json=parameters)

    def get_custom_fields(self):
        """Retrieve a list of all the custom contact/company
            fields you've created in your CRM

        Returns
        -------
        requests.models.Response
            Request results
        """

        parameters = dict()

        self.__add_api_function(parameters, 'GetCustomFields')

        return requests.post(self.__URL, json=parameters)


class Contact:

    def __init__(self, FullName=None, Salutation=None, FirstName=None, MiddleName=None,
                 LastName=None, Suffix=None, CompanyName=None, CompanyId=None,
                 Title=None, Industry=None, NumEmployees=None, BackgroundInfo=None,
                 Email=None, Phone=None, Address=None, Website=None, Birthday=None,
                 CustomFields=None, AssignedTo=None, ContactId=None):
        """Contact template to ease the process of the CRM class

        Parameters
        ----------
        FullName : str
            This is the contact's full name. If you use this parameter, don't
            use the next five name fields (they are redundant)
        Salutation : str
            The prefix of the contact's name (Mr, Dr, Mrs, etc.)
        FirstName : str
            The contact's first name. If you are using these name parts insead
            of the FullName, you must either fill out a FirstName or a LastName
        MiddleName : str
            The contact's middle name
        LastName : str
            The contact's last name
        Suffix : str
            The contact's suffix (Jr, Sr, etc)
        CompanyName : str
            The name of the company. If you have a contact name and a company
            name, we'll create both records. If you only have a company name,
            we'll only create that record
        CompanyId : str
            You can use this INSTEAD OF the CompanyName
        Title : str
            The contact's title (CEO, Sales Rep, etc.). Don't use this if you're
            only creating a company
        Industry : str
            The company's industry. Only use this if you are creating a solo
            company
        NumEmployees : str
            The number of employees at the company. Only use this if you are
            creating a solo company
        BackgroundInfo : str
            A long text field where you can store any additional data. Line
            break characters (\\n) work in this field
        Email : dict
            A dictionary of email addresses. Here is how it's organized:
            '0': {
                'Text': 'example@email.com',
                'Type': 'Work' (Can be Work, Personal, Other)
            },
            '1': ...
        Phone : dict
            A dictionary of phone numbers. Here is how it's organized:
            '0': {
                'Text': '888-888-8888',
                'Type': Work (Can be Work, Personal, Other)
            },
            '1': ...
        Address : dict
            A dictionary of addresses. Here is how it's organized:
            '0': {
                'Street': '123 Example St. \\n Apt #321',
                'City': 'St. Example',
                'State': 'EX',
                'Zip': '84321',
                'Country': 'U.S.',
                'Type': 'Shipping' (Can be Work, Billing, Shipping, Home, Other)
            },
            '1': ...
        Website : dict
            A dictionary of websites. Here is how it's organized:
            '0': {
                'Text': 'example.com'
            },
            '1': ...
        Birthday : str
            The contact's birthday. You can use any format you want, but we read
            "xx/xx/xxxx" as "mm/dd/yyyy" (the American format) so if you prefer
            the European format you should use something different like
            "yyyy-mm-dd" or "October 31st, 1981"
        CustomFields : dict
            A dictionary of any additional data you want to enter.
            The values in the dictionary should follow the format FIELD_NAME=>VALUE
        AssignedTo : str
            The userid of who the contact is assigned to
        ContactId : str
            The ContactId that the crm uses to keep track of this contact

        Returns
        -------
        Contact
            Contact object

        """

        self.contact_info = locals()
        del self.contact_info['self']

    def __setitem__(self, key, value):
        self.contact_info[key] = value

    def __getitem__(self, key):
        return self.contact_info[key]

    def __str__(self):
        return str(self.contact_info.items())

    def items(self):
        return self.contact_info.items()
