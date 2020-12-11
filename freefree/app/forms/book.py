from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=25)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(
        'Recipient Name', validators=[
            DataRequired(),
            Length(min=2, max=20,
                   message='Recipient Name should be 2 - 30 characters.')])
    mobile = StringField('Phone', validators=[
        DataRequired(),
        Regexp('^[0-9]{10}$', 0, "Please enter a valid phone number!")])

    message = StringField('Message')
    address = StringField(
        'Shipping Address',
        validators=[
            DataRequired(),
            Length(min=10, max=70,
                   message="Please provide a detailed address.")
        ]
    )
