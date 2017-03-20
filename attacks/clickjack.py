from utils import POST

def clickjack(page, client):
    content_type = page.headers.get('Content-Type', '')

    if not check_for_post_forms(page):
        return  # No active content, so it's fine

    frame_options = page.headers.get('X-Frame-Options')
    if not frame_options:
        print('Clickjacking in page {} - no X-Frame-Options header'.format(page.url))
        return

    if not is_valid_header(frame_options):
        print('Clickjacking in page {} - invalid X-Frame-Options!'.format(page.url))

def check_for_post_forms(page):
    return any(form
               for form in page.get_forms()
               if form.method.lower() == POST.lower())

def is_valid_header(frame_options):
    if frame_options == "DENY":
        return True

    if frame_options == "SAMEORIGIN":
        return True

    first_word, _, url = frame_options.partition(" ")
    if first_word == "ALLOW-FROM":
        netloc = urlparse(url).netloc
        if netloc:
            return True

    return False