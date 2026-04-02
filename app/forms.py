from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional

# Este es el que necesita tu app/auth/routes.py
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class PatientForm(FlaskForm):
    tipo_documento = SelectField('Tipo Doc.', choices=[('V', 'V'), ('E', 'E'), ('J', 'J'), ('P', 'P'), ('RN', 'RN')], validators=[DataRequired()])
    dni = StringField('Cédula/ID', validators=[Optional()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    genero = SelectField('Género', choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[Optional()])
    telefono = StringField('Teléfono')
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Guardar Paciente')

class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre_completo = StringField('Nombre Completo')
    rol = SelectField('Rol', choices=[('admin', 'Administrador'), ('bioanalista', 'Bioanalista'), ('recepcion', 'Recepción')])
    password = PasswordField('Contraseña')
    submit = SubmitField('Guardar Usuario')
