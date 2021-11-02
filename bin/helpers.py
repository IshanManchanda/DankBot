from random import randint

from telegram import Update
from telegram.ext import CallbackContext

from .fryer_gif import fry_gif
from .fryer_image import fry_image
from .generator_classic import generate
from .utils.files import Files
from .utils.logs import log_command, log_debug
from .utils.text import bs, excluded, ironic, keys


def get_random(var):
    return var[randint(0, len(var) - 1)]


def helper_b(update, text):
    a = []
    for x in text.split(' '):
        if x in excluded:
            a.append(x)
            continue
        i = 0
        try:
            while x[i] not in bs:
                i += 1
            start, i = i, i + 1
            while x[i] in bs:
                i += 1
            end = i
            a.append(x[:start] + '🅱️' + x[end:])
        except IndexError:
            a.append(x)

    out = ' '.join(a)
    if out == text:
        return
    update.message.reply_text(out, quote=True)
    log_command(update, 'B')


def helper_fry(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return 0

    text = update.message.text.lower()
    n = (
        5 if 'tsar bomba' in text else
        3 if 'nuke' in text or 'nuking' in text else
        1 if 'fry' in text else 0
    )
    if not n:
        return 0

    log_debug(f'Frying requested with command: {text}')
    args = {key: 1 if key in text else 0 for key in keys}
    log_debug(f'Parsed frying args: {args}')

    # FIXME: GIF Fryer
    if update.message.reply_to_message.document:
        log_debug('helper_fry found document')
        url = context.bot.get_file(
            update.message.reply_to_message.document.file_id
        ).file_path
        fry_gif(update, url, n, args)

    elif update.message.reply_to_message.video:
        log_debug('helper_fry found video')
        url = context.bot.get_file(
            update.message.reply_to_message.video.file_id
        ).file_path
        fry_gif(update, url, n, args)

    elif update.message.reply_to_message.photo:
        log_debug('helper_fry found photo')
        url = context.bot.get_file(
            update.message.reply_to_message.photo[::-1][0].file_id
        ).file_path
        fry_image(update, url, n, args)
    log_command(update, 'FRY')
    return 1


def helper_generate(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return 0

    text_c = update.message.text
    text = text_c.lower()

    if ('t:' in text or 'ts:' in text) and ('b:' in text or 'bs:' in text):
        t, tc = (text.find('t:'), 1) if 't:' in text else (text.find('ts:'), 0)
        b, bc = (text.find('b:'), 1) if 'b:' in text else (text.find('bs:'), 0)
        url = context.bot.get_file(
            update.message.reply_to_message.photo[::-1][0].file_id
        ).file_path

        if b > t:
            generate(
                update, url,
                text_c[t + 2:b].upper() if tc else text_c[t + 3:b],
                text_c[b + 2:].upper() if bc else text_c[b + 3:]
            )
        else:
            generate(
                update, url,
                text_c[t + 2:].upper() if tc else text_c[t + 3:],
                text_c[b + 2:t].upper() if bc else text_c[b + 3:t]
            )
        log_command(update, 'GEN')
        return 1
    return 0


def helper_despacito(update, text):
    update.message.reply_animation(Files.despacito[0], quote=True)
    try:
        word = text[text.find('play despacito') + 15:].partition(' ')[0]
        n = int(word)
        update.message.reply_audio(
            Files.dedpacito[min(max(1, n), 11)],
            quote=True
        )
    except (IndexError, ValueError):
        update.message.reply_audio(
            Files.dedpacito['normal' if randint(0, 9) else 'ded'],
            quote=True
        )
    log_command(update, 'DESPACITO')


def helper_gif(update, text, words):
    if 'hmmm' in text:
        update.message.reply_animation(get_random(Files.hmmm), quote=True)
        log_command(update, 'HMMM')

    elif 'boom son' in text:
        update.message.reply_animation(get_random(Files.boom_son), quote=True)
        log_command(update, 'BOOMSON')

    elif 'just do it' in text:
        update.message.reply_animation(get_random(Files.just_do_it), quote=True)
        log_command(update, 'JUSTDOIT')

    else:
        return 0
    return 1


def helper_image(update, text, words):
    if text == 'e':
        update.message.reply_photo(get_random(Files.e), quote=True)
        log_command(update, 'E')

    elif 'hello there' in text:
        update.message.reply_photo(get_random(Files.hello_there), quote=True)
        log_command(update, 'HELLOTHERE')

    elif 'i don\'t think so' in text or 'i dont think so' in text:
        update.message.reply_photo(get_random(Files.dont_think_so), quote=True)
        log_command(update, 'IDONTTHINKSO')

    elif 'wat' in words:
        update.message.reply_photo(get_random(Files.wat), quote=True)
        log_command(update, 'WAT')

    elif 'dude what' in text:
        update.message.reply_photo(get_random(Files.dude_what), quote=True)
        log_command(update, 'DUDEWHAT')

    elif 'wut' in words or 'what even' in text:
        update.message.reply_photo(get_random(Files.wut), quote=True)
        log_command(update, 'WUT')

    elif 'what the' in text:
        update.message.reply_photo(get_random(Files.what_the), quote=True)
        log_command(update, 'WHATTHE')

    else:
        return 0
    return 1


def helper_text(update, text, words):
    if 'ironic' in text or 'darth plagueis' in text:
        update.message.reply_text(ironic, quote=True)
        log_command(update, 'IRONIC')

    elif (
            text.startswith('f ')
            or text.startswith('rip ')
            or text == 'f'
            or text == 'rip'
    ):
        update.message.reply_text('F', quote=True)
        log_command(update, 'F')

    elif 'oof' in words:
        update.message.reply_text('oof indeed.', quote=True)
        log_command(update, 'OOF')

    elif text == '???':
        update.message.reply_text('Profit', quote=True)
        log_command(update, 'PROFIT')

    elif 'tp' in text and 'http' not in text:
        update.message.reply_text(text.replace('tp', '✝️🅿️'), quote=True)
        log_command(update, 'TP')

    else:
        return 0
    return 1
