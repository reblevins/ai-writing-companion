import datetime as dt

from marshmallow import Schema, fields


class Story(object):
    def __init__(self, title, content, author, created_at=None):
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at or dt.datetime.utcnow()

    def __repr__(self):
        return '<Story(title={self.title!r})>'.format(self=self)


class StorySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'story'
        strict = True