import datetime


class ModelMixin:
    def to_dict(self, exclude=()):
        att_dict = {}

        # 需要强制转化成字符串的类型
        force_str_types = (datetime.datetime, datetime.date, datetime.time)
        for field in self._meta.fields:
            name = field.attname
            value = getattr(self, field.attname, None)

            if name not in exclude:
                if isinstance(value, force_str_types):
                    value = str(value)
                att_dict[name] = value
        return att_dict
