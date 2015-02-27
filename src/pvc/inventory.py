"""
Docstring should go here

"""

import pyVmomi
import pvc.virtualmachine

from pvc.menu import Menu, MenuItem

__all__ = ['Inventory']


class Inventory(object):
    def __init__(self, agent, dialog):
        """
        Inventory menu

        Args:
            agent (VConnector): A VConnector instance
            dialog    (Dialog): A Dialog instance

        """
        self.agent = agent
        self.dialog = dialog

    def menu(self):
        items = [
            MenuItem(
                tag='Hosts and Clusters',
                description='Manage hosts and clusters',
            ),
            MenuItem(
                tag='VMs and Templates',
                description='Manage VMs and templates',
                on_select=self.virtual_machine_menu
            ),
            MenuItem(
                tag='Datastores',
                description='Manage Datastores and Datastore Clusters'
            ),
            MenuItem(
                tag='Networking',
                description='Manage Networking'
            ),
        ]

        menu = Menu(
            title='Inventory Menu',
            text='Select an item from the inventory',
            items=items,
            dialog=self.dialog,
            width=70,
        )
        menu.display()

    def virtual_machine_menu(self):
        self.dialog.infobox(
            text='Retrieving Virtual Machines ...',
            width=40
        )

        view = self.agent.get_vm_view()

        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.VirtualMachine,
            path_set=['name', 'runtime.powerState'],
            include_mors=True
        )

        view.DestroyView()

        items = [
            MenuItem(
                tag=vm['name'],
                description=vm['runtime.powerState'],
                on_select=pvc.virtualmachine.VirtualMachine,
                on_select_args=(vm['obj'], self.dialog)
            ) for vm in properties
        ]

        menu = Menu(
            title='Virtual Machines',
            text='Select a Virtual Machine from the menu that you wish to manage',
            items=items,
            dialog=self.dialog
        )
        menu.display()
