from django import template

register = template.Library()


@register.filter
def to_string(value):
    return str(value)

@register.filter
def arabic_numbers(value):
    arabic_numbers_map = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    return str(value).translate(arabic_numbers_map)

@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def unread_messages(user):
    return user.notification_set.filter(is_read=False).count()
    #replace the messages_set with the appropriate related_name, and also the filter field. (I am assuming it to be "read")

register.simple_tag(unread_messages)