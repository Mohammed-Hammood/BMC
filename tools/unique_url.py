import unicodedata
import random
import string
from django.utils.functional import keep_lazy
from django.utils.safestring import SafeText, mark_safe


def random_unique_chars_digit_slug_generator(sender=None, instance=None, size=None, **kwargs):
    if not instance.slug:
        if size:
            size = size
        else:
            size = 15

        def random_chars_generator(limited_size=size, chars=string.ascii_letters + string.digits):
            return ''.join(random.choice(chars) for x in range(limited_size))

        random_chars = random_chars_generator()
        lookup = sender.objects.filter(slug=random_chars).exists()
        while lookup is True:
            random_chars = random_chars_generator()
            search_again = sender.objects.filter(slug=random_chars).exists()
            if search_again is False:
                break
        instance.slug = random_chars
        return instance.slug
    else:
        pass


@keep_lazy(str, SafeText)
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    import re
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return mark_safe(re.sub(r'[-\s]+', '-', value))
