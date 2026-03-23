# forms/producto_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción')
    categoria = StringField('Categoría')
    imagen = StringField('Imagen (URL o ruta)')
    submit = SubmitField('Guardar')
