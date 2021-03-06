from pprint import pprint
import csv
import re

def get_separate_names(contact):  #  for contact in contacts_list
    contact_string = ' '.join([contact['lastname'], contact['firstname'], contact['surname']]) # ln: "Усольцев Олег Валентинович", fn: None, sn: None
    contact_pattern = r'^(?P<lastname>\w+)\s?(?P<firstname>\w+)\s?(?P<surname>\w+)*\s*$'
    regex_name = re.compile(contact_pattern)
    contact_match = regex_name.match(contact_string).groupdict()  #  {'lastname': 'Усольцев', 'firstname': 'Олег', 'surname': 'Валентинович'}
    lastname = contact_match['lastname']  #  'Усольцев'
    firstname = contact_match['firstname']  #  'Олег'
    surname = contact_match['surname']  #  'Валентинович'

    if surname:
        return lastname, firstname, surname
    else:
        return lastname, firstname, ''


def get_edited_phones(contact): #  for contact in contacts_list
    phone = contact['phone']
    regex_phone = re.compile(r'^(?P<group1>[+7|8]+)\s?[\(]?'
                               r'(?P<group2>\d{3})[\)|-]?\s?'
                               r'(?P<group3>\d{3})[-]?'
                               r'(?P<group4>\d{2})[-]?'
                               r'(?P<group5>\d{2})\s?[\(]?'
                               r'(?P<group6>\w{3}\.)?\s?'
                               r'(?P<group7>\d{4})?[\)]?$'
                               )

    if phone:
        phone_match = regex_phone.match(phone).groupdict()
        country_code = phone_match['group1']
        city_code = phone_match['group2']
        first_number = phone_match['group3']
        second_number = phone_match['group4']
        third_number = phone_match['group5']
        ext_flag = phone_match['group6']
        extension_number = phone_match['group7']

        if ext_flag:
            return f'+7({city_code}){first_number}-{second_number}-{third_number} {ext_flag}{extension_number}'
        else:
            return f'+7({city_code}){first_number}-{second_number}-{third_number}'

    else:
        return ''


def get_edited_contacts_list(contacts_list):
    edited_contacts_list = []

    for contact in contacts_list:
        lastname, firstname, surname = get_separate_names(contact)
        phone = get_edited_phones(contact)

    # скопировать/объединить словари, #параллельно перезаписывая определённые значения
        edited_contacts_list.append({**contact, 'lastname': lastname,
                                'firstname': firstname,
                                'surname': surname,
                                'phone': phone})

    return edited_contacts_list


def get_complete_contacts(edited_contacts_list):
    complete_contacts = {}
    for contact in edited_contacts_list:
        contact_key = (contact['lastname'], contact['firstname'])
        contact_values = [contact['surname'], contact['organization'], contact['position'],
                         contact['phone'], contact['email']]

        if contact_key in complete_contacts:
            for i in range(len(contact_values)):
                if not complete_contacts[contact_key][i] and contact_values[i]:
                    complete_contacts[contact_key][i] = contact_values[i]
        else:
            complete_contacts.update({contact_key: contact_values})
    return complete_contacts


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.DictReader(f, delimiter=",")
        contacts_list = list(rows)

    edited_contacts_list = get_edited_contacts_list(contacts_list)
    complete_contacts = get_complete_contacts(edited_contacts_list)

    headers = list(contacts_list[0].keys())

    edited_contacts_list = list()
    edited_contacts_list.append(headers)

    for k, v in complete_contacts.items():
        x = list(k) + list(v)
        edited_contacts_list.append(x)

    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(edited_contacts_list)

