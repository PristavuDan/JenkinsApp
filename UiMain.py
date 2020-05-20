import tkinter as tk
import Main
from tkinter import ttk


class JenkinsUi(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Jenkins Builder")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (QaPage, QaDeleteServersPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(QaPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class QaPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        qa_delete_jobs_page = ttk.Button(self, text="Delete QA jobs page",
                                         command=lambda: controller.
                                         show_frame(QaDeleteServersPage))

        qa_job_button = ttk.Button(self, text=">Run QA job<", command=self.call_build_jenkins)

        jira_ticket = tk.Label(self, text="Ticket")
        feeds_branch = tk.Label(self, text="Feeds Branch")
        firstboot_branch = tk.Label(self, text="Firstboot Branch")
        frontend_branch = tk.Label(self, text="Frontend Branch")
        pynoceros_branch = tk.Label(self, text="Pynoceros Branch")
        meta_branch = tk.Label(self, text="Meta Branch")
        containers_branch = tk.Label(self, text="Containers Branch")

        self.firstbooted = ttk.Checkbutton(self, text="Firstbooted")
        self.jira_ticket_input = ttk.Entry(self)
        self.feeds_branch_input = ttk.Entry(self)
        self.firstboot_input = ttk.Entry(self)
        self.frontend_input = ttk.Entry(self)
        self.pynoceros_input = ttk.Entry(self)
        self.meta_branch_input = ttk.Entry(self)
        self.containers_input = ttk.Entry(self)

        jira_ticket.grid(row=0, sticky=tk.E)
        feeds_branch.grid(row=1, sticky=tk.E)
        firstboot_branch.grid(row=2, sticky=tk.E)
        frontend_branch.grid(row=3, sticky=tk.E)
        pynoceros_branch.grid(row=4, sticky=tk.E)
        meta_branch.grid(row=5, sticky=tk.E)
        containers_branch.grid(row=6, sticky=tk.E)
        self.firstbooted.grid(columnspan=2)

        qa_job_button.grid(columnspan=2)
        qa_delete_jobs_page.grid(columnspan=2)

        self.jira_ticket_input.grid(row=0, column=1)
        self.feeds_branch_input.grid(row=1, column=1)
        self.firstboot_input.grid(row=2, column=1)
        self.frontend_input.grid(row=3, column=1)
        self.pynoceros_input.grid(row=4, column=1)
        self.meta_branch_input.grid(row=5, column=1)
        self.containers_input.grid(row=6, column=1)

    def call_build_jenkins(self):
        ticket_number = self.jira_ticket_input.get()
        feeds_branch = self.feeds_branch_input.get()
        first_boot_branch = self.firstboot_input.get()
        frontend_branch = self.frontend_input.get()
        pynoceros_branch = self.pynoceros_input.get()
        meta_branch = self.meta_branch_input.get()
        containers_branch = self.containers_input.get()
        first_booted = self.firstbooted.state()

        try:
            if first_booted[0] == 'alternate':
                first_booted = True
            elif first_booted[0] == 'selected':
                first_booted = True
        except IndexError:
            first_booted = False

        Main.build_using_qa(jira_ticket=ticket_number, feeds_branch=feeds_branch,
                            firstboot_branch=first_boot_branch, frontend_branch=frontend_branch,
                            pynoceros_branch=pynoceros_branch, meta_branch=meta_branch,
                            containers_branch=containers_branch, firstbooted=first_booted)


class QaDeleteServersPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        qa_page = ttk.Button(self, text="QA Job page",
                             command=lambda: controller.show_frame(QaPage))

        qa_job_button = ttk.Button(self, text=">Delete targeted jobs<", command=self.destroy_jenkins_machines)

        jira_ticket_one = tk.Label(self, text="Jira Ticket 1: ")
        self.ticket_input_one = ttk.Entry(self)

        jira_ticket_one.grid(row=0, sticky=tk.E)
        self.ticket_input_one.grid(row=0, column=1)

        jira_ticket_two = tk.Label(self, text="Jira Ticket 2: ")
        self.ticket_input_two = ttk.Entry(self)

        jira_ticket_two.grid(row=1, sticky=tk.E)
        self.ticket_input_two.grid(row=1, column=1)

        jira_ticket_three = tk.Label(self, text="Jira Ticket 3: ")
        self.ticket_input_three = ttk.Entry(self)

        jira_ticket_three.grid(row=2, sticky=tk.E)
        self.ticket_input_three.grid(row=2, column=1)

        jira_ticket_four = tk.Label(self, text="Jira Ticket 4: ")
        self.ticket_input_four = ttk.Entry(self)

        jira_ticket_four.grid(row=3, sticky=tk.E)
        self.ticket_input_four.grid(row=3, column=1)

        qa_job_button.grid(columnspan=2)
        qa_page.grid(columnspan=2)

    def destroy_jenkins_machines(self):
        ticket_one_value = self.ticket_input_one.get()
        ticket_two_value = self.ticket_input_two.get()
        ticket_three_value = self.ticket_input_three.get()
        ticket_four_value = self.ticket_input_four.get()

        Main.destroy_machine(ticket_one=ticket_one_value, ticket_two=ticket_two_value,
                             ticket_three=ticket_three_value, ticket_four=ticket_four_value)


app = JenkinsUi()
app.mainloop()
