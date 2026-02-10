from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TelField, EmailField
from wtforms.validators import DataRequired, Optional, Length, Email


class PatientForm(FlaskForm):
    tipo_documento = SelectField('Tipo Documento', choices=[('V','V'),('E','E'),('P','P'),('N','N'),('RN','RN')], validators=[DataRequired()])
    dni = StringField('DNI', validators=[Optional(), Length(max=30)])
    genero = SelectField('Género', choices=[('Masculino','Masculino'),('Femenino','Femenino')], validators=[DataRequired()])
    nombre = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=120)])
    apellido = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=120)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=30)])
    email = EmailField('Correo', validators=[Optional(), Email(), Length(max=120)])

class SampleForm(FlaskForm):
    tipo_muestra = SelectField('Tipo de Muestra', choices=[
        ('Sangre Total','Sangre Total'),('Suero','Suero'),('Plasma','Plasma'),('Orina','Orina'),
        ('Hisopado Nasofaríngeo','Hisopado Nasofaríngeo'),('Heces','Heces'),('Líquido Cefalorraquídeo','Líquido Cefalorraquídeo')
    ], validators=[DataRequired()])
    codigo = StringField('Código', validators=[Optional(), Length(max=100)])


class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    password = StringField('Contraseña', validators=[Optional(), Length(min=4, max=120)])
    nombre_completo = StringField('Nombre Completo', validators=[Optional(), Length(max=150)])
    email = EmailField('Email', validators=[Optional(), Email(), Length(max=120)])
    rol = SelectField('Rol', choices=[('bioanalista','Bioanalista'), ('admin','Admin')], validators=[DataRequired()])
