from lib.app_state import AppState

# TODO: move into config
# blue is 4E9FB1
# def is d7d0c7

# ICONS
focused_foreground = '#FFFFFF'
active_foreground = '#E84F4F'
empty_foreground = '#B7B0A7'
dead_foreground = '#979087'

focused_background = '#BB303030'
active_background = '#BB202020'
empty_background = '#BB202020'
dead_background = '#BB202020'

preview_max_length = 35


def render(app: AppState):
    # buffer = _bg(empty_background, '  ')
    buffer = ''

    for connection in app.connections:
        snapshot = app.get_snapshot(connection.id)
        icon_str = '   %s   ' % connection.icon

        if not snapshot:
            # dead
            buffer += _bg(dead_background, _fg(dead_foreground, icon_str))
        elif app.focused_connection == connection.id:
            # focused
            buffer += _bg(focused_background, _fg(focused_foreground, icon_str))
        elif not snapshot.empty:
            # active
            buffer += _bg(active_background, _fg(active_foreground, icon_str))
        else:
            # default
            buffer += _bg(empty_background, _fg(empty_foreground, icon_str))

    # buffer += _bg(empty_background, '  ')


    preview = app.get_preview()

    if preview:
        buffer += '  {title}'.format(title=preview.title)

    print(buffer, flush=True)


def _under(color: str, text: str) -> str:
    return _tag('u', color, text)


def _over(color: str, text: str) -> str:
    return _tag('o', color, text)


def _fg(color: str, text: str) -> str:
    return _tag('F', color, text)


def _bg(color: str, text: str) -> str:
    return _tag('B', color, text)


def _tag(tag: str, value: str, text: str) -> str:
    tag_template = '%{{{tag}{value}}}{text}%{{{tag}-}}'
    return tag_template.format(tag=tag, text=text, value=value)
