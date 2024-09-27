from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

class ImageIDForm(FlaskForm):
    image_ids = TextAreaField('Image IDs', validators=[DataRequired()], render_kw={'placeholder': 'Comma-separated image IDs'})
    submit = SubmitField('Submit')

    def validate_image_ids(self, image_ids):
        if not re.match("([0-9]{6},?)+"):
            raise ValidationError('Invalid image IDs, please enter comma-separated 6-digit MGN image ids')