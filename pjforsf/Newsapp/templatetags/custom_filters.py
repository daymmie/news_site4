from django import template

register = template.Library()


@register.filter()
def censorship(value):
    badwords = ['бяка', 'козявка', 'какашка', 'лох', 'дерьмак']
    badstrs = [',', '.', ':', '-']
    value = ''.join((filter(lambda x: x not in badstrs, value)))
    value = value.lower().split()
    result = ''
    for x in value:
        if x not in badwords:
            result += x + ' '
        elif x in badwords:
            x = x.replace(x, x[:1] + (len(x) - 1) * '*')
            result += x + ' '
    return f'{result}'
