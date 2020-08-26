import jenkins
import pprint
import time
import asyncio


def build_using_qa(jira_ticket, user_name="dpristavu", user_password="uNIgOpoloCONgLOrLi",
                   feeds_branch="development", firstboot_branch="development",
                   frontend_branch="development", meta_branch="development",
                   pynoceros_branch="development", containers_branch="development",
                   preflight_brench='development', firstbooted="true"):
    pprint.pprint("build_using_QA STARTED!")
    server = jenkins.Jenkins('https://jenkins2.threatq.com/', username=user_name,
                             password=user_password)
    development_branch = "development"

    if jira_ticket is '':
        pprint.pprint("A jira ticket was not provided")
    else:
        jira_ticket = jira_ticket.upper()

        if feeds_branch is '':
            feeds_branch = development_branch
        if firstboot_branch is '':
            firstboot_branch = development_branch
        if frontend_branch is '':
            frontend_branch = development_branch
        if meta_branch is '':
            meta_branch = development_branch
        if pynoceros_branch is '':
            pynoceros_branch = development_branch
        if containers_branch is '':
            containers_branch = development_branch
        if preflight_brench is '':
            preflight_brench = development_branch

        pprint.pprint("Jira ticket: " + jira_ticket)
        pprint.pprint("Feeds branch: " + feeds_branch)
        pprint.pprint("FirstBoot branch: " + firstboot_branch)
        pprint.pprint("Frontend branch: " + frontend_branch)
        pprint.pprint("Meta branch: " + meta_branch)
        pprint.pprint("Pynoceros branch: " + pynoceros_branch)
        pprint.pprint("Containers Branch: " + containers_branch)
        pprint.pprint("Preflight: " + preflight_brench)
        pprint.pprint(firstbooted)

        server.build_job("QA", {'JIRA_TICKET': jira_ticket, 'FEEDS': feeds_branch,
                                'FIRSTBOOT': firstboot_branch, 'FRONTEND': frontend_branch,
                                'META': meta_branch, 'PYNOCEROS': pynoceros_branch,
                                'CONTAINERS': containers_branch, 'PREFLIGHT': preflight_brench,
                                'Firstbooted': firstbooted})

        # wait_for_build_complete Will be used once the async functionality will be implemented
        # wait_for_build_complete(jira_ticket,user_name, user_password)


def wait_for_build_complete(jira_ticket, user_name="dpristavu",
                            user_password="uNIgOpoloCONgLOrLi"):
    pprint.pprint("wait_for_build_complete STARTED!")

    server = jenkins.Jenkins('https://jenkins2.threatq.com/', username=user_name,
                             password=user_password)
    while True:
        time.sleep(1)
        last_build_number = server.get_job_info("QA").get("lastBuild").get("number")
        build_info = server.get_build_info('QA', last_build_number)
        for x in build_info.get("actions"):
            if "parameters" in x:
                ticket_name = x.get("parameters")[0].get("value")
            elif "causes" in x:
                user_id = x.get("causes")[0].get("userId")

        if (user_id == user_name and build_info.get("building") is True
                and ticket_name == jira_ticket):
            break

    build_complete = build_info.get("building")
    build_result = build_info.get("result")

    print("Waiting for the build to be completed")
    while build_complete is True:
        time.sleep(15)
        build_info = server.get_build_info('QA', last_build_number)
        build_complete = build_info.get("building")
        build_result = build_info.get("result")
        pprint.pprint("Build is still in progress...")

    pprint.pprint(build_info)
    print(build_result)


def destroy_machine(ticket_one, ticket_two, ticket_three, ticket_four,
                    user_name="dpristavu", user_password="uNIgOpoloCONgLOrLi"):
    server = jenkins.Jenkins('https://jenkins2.threatq.com/', username=user_name,
                             password=user_password)

    def destroy_job(ticket_number):

        tenant = "qa"
        os_username = "jenkins"
        os_host = "http://openstack2.threatq.com"

        server.build_job("OS-Destroy",
                         {'TICKET_ID': ticket_number, 'OS_HOST': os_host,
                          'OS_USERNAME': os_username, 'TENANT': tenant})

    # pprint.pprint(server.get_job_info("OS-Destroy"))

    if ticket_one is '' and ticket_two is '' and ticket_three is '' and ticket_four is '':
        pprint.pprint("A jira ticket was not provided")
    else:
        jira_ticket_one = ticket_one.upper()
        jira_ticket_two = ticket_two.upper()
        jira_ticket_three = ticket_three.upper()
        jira_ticket_four = ticket_four.upper()

        if jira_ticket_one is not '':
            pprint.pprint("Deleting the following machine: " + jira_ticket_one)
            destroy_job(jira_ticket_one)

        if jira_ticket_two is not '':
            pprint.pprint("Deleting the following machine: " + jira_ticket_two)
            destroy_job(jira_ticket_two)

        if jira_ticket_three is not '':
            pprint.pprint("Deleting the following machine: " + jira_ticket_three)
            destroy_job(jira_ticket_three)

        if jira_ticket_four is not '':
            pprint.pprint("Deleting the following machine: " + jira_ticket_four)
            destroy_job(jira_ticket_four)
