from wtforms import SubmitField, SelectField


def form_open(form_name, f_id=None, enctype=None, f_action=""):
    f_open = """<form action="%s" method="post" name="%s" """ % (f_action, form_name,)

    if f_id:
        f_open += """ id="%s" """ % (f_id,)
    if enctype:
        f_open += """ enctype="%s" """ % (enctype,)

    f_open += """class="main-form full">"""

    return f_open


def form_close():
    return """</form>"""


class SubmitField(SubmitField):
    def __call__(self, *args, **kwargs):
        return '<button name="' + self.id + '" type="submit" class="btn-color right-side">' + \
               self.label.text + '</button>'


# Normalde;
#  (value='', label='Seçiniz',) olarak formu kabul etmiyor, fakat şu an ediyor.
class SelectField(SelectField):
    def iter_choices(self):
        for value, label in self.choices:
            if self.coerce is int and value == '':
                yield (value, label, False)
            else:
                yield (value, label, self.coerce(value) == self.data)
