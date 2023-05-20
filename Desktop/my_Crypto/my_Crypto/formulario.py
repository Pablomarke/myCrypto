from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,SubmitField
from wtforms.validators import DataRequired
from time import strftime
from my_Crypto.pruebas import valorCrypto


class MovimientosForm(FlaskForm):
    
    date_select = strftime(" %d/%m/%Y")
    hora_select = strftime(" %H:%M:%S")
    
    from_select = StringField('From',validators=[DataRequired( message="La fecha es requerida" )])
    quantity = FloatField('Cantidad',validators=[DataRequired("El monto es requirido, debe ser mayor a 0")])
    to_select = StringField('To',validators=[DataRequired( message="El concepto es requerido" )])
    quantity2 = valorCrypto("ETH")

    submit = SubmitField('Guardar en Base de datos')
