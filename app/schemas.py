from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))

class LinkCreateSchema(Schema):
    original_url = fields.Str(required=True)
    title = fields.Str(validate=validate.Length(max=200))
    custom_alias = fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9.\-_]*$'), allow_none=True)
    tag = fields.Str(validate=validate.Length(max=50), allow_none=True)
    expires_at = fields.DateTime(allow_none=True)
