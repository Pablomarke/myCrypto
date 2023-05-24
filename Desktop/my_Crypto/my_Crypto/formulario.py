from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,SubmitField,HiddenField
from wtforms.validators import DataRequired
from time import strftime


class MovimientosForm(FlaskForm):
    date_select = strftime(" %d/%m/%Y")
    hora_select = strftime(" %H:%M:%S")
    
    from_select = StringField('From',
                              validators=[DataRequired( message="" )])
    quantity = FloatField('Cantidad',
                          validators=[DataRequired("")])
    to_select = StringField('To',
                            validators=[DataRequired( message="" )])
    submit = SubmitField('Guardar en Base de datos')





    