import time
from datetime import datetime, timedelta, timezone

from .calendar_get import TimeRangeCalEvent, get_calendar_events
from .camera import camera_active
from .notification import notify
from .text_to_speech import play_text

default_sleep = timedelta(minutes=5)


def main():
    first_step = True
    try:
        # iterate indefinitely looking for events
        while True:
            cal_events = get_calendar_events(first_step)
            first_step = False
            if not cal_events:
                print(f'No upcoming calls, waiting {display_interval(default_sleep)}')
                time.sleep(default_sleep.total_seconds())
                continue

            next_event = cal_events[0]
            time_until_start = next_event.start - datetime.now(tz=timezone.utc)
            if time_until_start > timedelta():
                sleep_time = min(default_sleep, time_until_start)
                print(
                    f'Next calls starts at {next_event.start} in {display_interval(time_until_start)}, '
                    f'waiting {sleep_time.total_seconds():0.0f} seconds'
                )
                time.sleep(sleep_time.total_seconds())
            else:
                event_sequence(next_event)
    except KeyboardInterrupt:
        print('stopped')
    except Exception as e:
        notify('Call Alert Error!', f'Call alert crashed: {e}')
        raise


def event_sequence(event: TimeRangeCalEvent):
    print(f'Starting event sequence for event "{event.summary}" starting at {event.start}...')
    for sleep_time in [120, 360]:
        event_alert(event)
        time.sleep(sleep_time)

    event_alert(event)
    print(f'Ended event sequence for event "{event.summary}".')


def event_alert(event: TimeRangeCalEvent):
    time_since_start = datetime.now(tz=timezone.utc) - event.start
    minutes = int(time_since_start.total_seconds() / 60)
    if camera_active():
        print(f'Skipping {minutes} minute{plural(minutes)} notification for "{event.summary}", camera active')
    else:
        if minutes == 0:
            play_text(f'Your call "{event.summary}" has just started')
        else:
            msg = (
                f'Your call "{event.summary}" started {int_as_word(minutes)} minute{plural(minutes)} ago, JOIN IT NOW!'
            )
            notify('Call Alert', msg)
            play_text(msg)


def display_interval(delta: timedelta) -> str:
    if delta < timedelta(minutes=1):
        return 'less than a minute'
    elif delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() / 60)
        return f'{minutes} minute{plural(minutes)}'
    elif delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f'{int_as_word(hours)} hour{plural(hours)}'
    elif delta < timedelta(days=2):
        hours = int((delta.total_seconds() - 86400) / 3600)
        return f'1 day, {int_as_word(hours)} hour{plural(hours)}'
    else:
        days = int(delta.total_seconds() / 86400)
        return f'{int_as_word(days)} day{plural(days)}'


def int_as_word(v: int) -> str:
    words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    try:
        return words[v]
    except IndexError:
        return str(v)


def plural(n: int) -> str:
    return 's' if n != 1 else ''


if __name__ == '__main__':
    main()
