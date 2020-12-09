import jenkins
import pprint


def build_using_qa(jira_ticket, user_name='dpristavu', user_password='uNIgOpoloCONgLOrLi',
                   feeds_branch='development', firstboot_branch='development',
                   frontend_branch='development', meta_branch='development',
                   pynoceros_branch='development', containers_branch='development',
                   preflight_branch='development', firstbooted='true'):
    pprint.pprint('build_using_QA STARTED!')
    server = jenkins.Jenkins('https://jenkins2.threatq.com/', username=user_name,
                             password=user_password)
    development_branch = 'development'

    if jira_ticket is '':
        pprint.pprint('A jira ticket was not provided')
        return

    jira_ticket = jira_ticket.upper()

    feeds_branch = feeds_branch or development_branch
    firstboot_branch = feeds_branch or development_branch
    frontend_branch = feeds_branch or development_branch
    meta_branch = feeds_branch or development_branch
    pynoceros_branch = feeds_branch or development_branch
    containers_branch = feeds_branch or development_branch
    preflight_branch = feeds_branch or development_branch

    pprint.pprint('Jira ticket: ' + jira_ticket)
    pprint.pprint('Feeds branch: ' + feeds_branch)
    pprint.pprint('FirstBoot branch: ' + firstboot_branch)
    pprint.pprint('Frontend branch: ' + frontend_branch)
    pprint.pprint('Meta branch: ' + meta_branch)
    pprint.pprint('Pynoceros branch: ' + pynoceros_branch)
    pprint.pprint('Containers Branch: ' + containers_branch)
    pprint.pprint('Preflight: ' + preflight_branch)
    pprint.pprint(firstbooted)

    server.build_job('QA', {
        'JIRA_TICKET': jira_ticket, 'FEEDS': feeds_branch, 'FIRSTBOOT': firstboot_branch,
        'FRONTEND': frontend_branch, 'META': meta_branch, 'PYNOCEROS': pynoceros_branch,
        'CONTAINERS': containers_branch, 'PREFLIGHT': preflight_branch,
        'Firstbooted': firstbooted
    })


def destroy_job(ticket_number, server):

    tenant = 'qa'
    os_username = 'jenkins'
    os_host = 'http://openstack2.threatq.com'

    server.build_job('OS-Destroy', {
        'TICKET_ID': ticket_number, 'OS_HOST': os_host, 'OS_USERNAME': os_username,
        'TENANT': tenant
    })


def destroy_machine(ticket_one, ticket_two, ticket_three, ticket_four,
                    user_name='dpristavu', user_password='uNIgOpoloCONgLOrLi'):
    server = jenkins.Jenkins(
        'https://jenkins2.threatq.com/', username=user_name, password=user_password
    )

    tickets = [ticket_one.upper(), ticket_two.upper(), ticket_three.upper(), ticket_four.upper()]

    if set(tickets) == {''}:
        pprint.pprint("A jira ticket was not provided")
        return

    for ticket in tickets:
        if ticket is not '':
            pprint.pprint("Deleting the following machine: " + ticket)
            destroy_job(ticket, server)
