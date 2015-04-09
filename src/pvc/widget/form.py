"""
Docstring should go here

"""

__all__ = ['Form', 'FormElement']


class FormElement(object):
    def __init__(self, label, item='', field_length=60, input_length=0, attributes=0x0):
        """
        A form element

        Args:
           label       (str): Label of the element
           item        (str): Initial value for the element
           field_lenght(int): Number of characters used to display the item
           field_input (int): Input field characters
           attributes  (int): A bitmask used for elements used in mixed forms

        """
        self.label = label
        self.item = item
        self.field_length = field_length
        self.input_length = input_length
        self.attributes = attributes


class Form(object):
    def __init__(self, dialog, form_elements, mixed_form=False, **kwargs):
        """
        A form widget

        Args:
            dialog        (dialog.Dialog): A Dialog instance
            form_elements          (list): A list of FormElement instances to display
            mixed_form             (bool): If True then create a mixed form, otherwise
                                           create a standard form
            kwargs                 (dict): Additional args to be passed to dialog(1)

        """
        self.form = None
        self.dialog = dialog
        self.form_elements = form_elements
        self.mixed_form = mixed_form
        self.kwargs = kwargs
        self._labels = [e.label for e in self.form_elements]

        # Starting column at which to display the items' values
        self._xi = len(max(self._labels, key=len)) + 3

        if self.mixed_form:
            self.form = self.dialog.mixedform
            self._elements = [(e.label, row + 1, 1, e.item, row + 1, self._xi, e.field_length, e.input_length, e.attributes) for row, e in enumerate(self.form_elements)]
        else:
            self.form = self.dialog.form
            self._elements = [(e.label, row + 1, 1, e.item, row + 1, self._xi, e.field_length, e.input_length) for row, e in enumerate(self.form_elements)]

    def display(self):
        code, items = self.form(
            elements=self._elements,
            **self.kwargs
        )

        result = (code, {l: i for l, i in zip(self._labels, items)})

        return result
