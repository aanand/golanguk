#!/usr/bin/env python

import atexit
import math
import os
import random
import re
import sys
import time


# Reset terminal colors at exit
def reset():
    sys.stdout.write('\x1b[0m')
    sys.stdout.flush()

atexit.register(reset)


STRIP_ANSI = re.compile(r'\x1b\[(\d+)(;\d+)?(;\d+)?[m|K]')
COLOR_ANSI = (
    (0x00, 0x00, 0x00), (0xcd, 0x00, 0x00),
    (0x00, 0xcd, 0x00), (0xcd, 0xcd, 0x00),
    (0x00, 0x00, 0xee), (0xcd, 0x00, 0xcd),
    (0x00, 0xcd, 0xcd), (0xe5, 0xe5, 0xe5),
    (0x7f, 0x7f, 0x7f), (0xff, 0x00, 0x00),
    (0x00, 0xff, 0x00), (0xff, 0xff, 0x00),
    (0x5c, 0x5c, 0xff), (0xff, 0x00, 0xff),
    (0x00, 0xff, 0xff), (0xff, 0xff, 0xff),
)

class LolCat(object):
    def __init__(self, mode=256, output=sys.stdout):
        self.mode = mode
        self.output = output

    def _distance(self, rgb1, rgb2):
        return sum(map(lambda c: (c[0] - c[1]) ** 2,
            zip(rgb1, rgb2)))

    def ansi(self, rgb):
        r, g, b = rgb

        if self.mode in (8, 16):
            colors = COLOR_ANSI[:self.mode]
            matches = [(self._distance(c, map(int, rgb)), i) for i, c in enumerate(colors)]
            matches.sort()
            color = matches[0][1]

            return '3%d' % (color,)
        else:
            gray_possible = True
            sep = 2.5

            while gray_possible:
                if r < sep or g < sep or b < sep:
                    gray = r < sep and g < sep and b < sep
                    gray_possible = False

                sep += 42.5

            if gray:
                color = 232 + int(float(sum(rgb) / 33.0))
            else:
                color = sum([16]+[int(6 * float(val)/256) * mod
                    for val, mod in zip(rgb, [36, 6, 1])])

            return '38;5;%d' % (color,)

    def wrap(self, *codes):
        return '\x1b[%sm' % (''.join(codes),)

    def rainbow(self, freq, i):
        r = math.sin(freq * i) * 127 + 128
        g = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
        b = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
        return [r, g, b]

    def cat(self, fd, options):
        if options.animate:
            self.output.write('\x1b[?25l')

        for line in fd:
            options.os += 1
            self.println(line, options)

        if options.animate:
            self.output.write('\x1b[?25h')

    def println(self, s, options):
        s = s.rstrip()
        if options.force or self.output.isatty():
            s = STRIP_ANSI.sub('', s)

        if options.animate:
            self.println_ani(s, options)
        else:
            self.println_plain(s, options)

        self.output.write('\n')
        self.output.flush()

    def println_ani(self, s, options):
        if not s:
            return

        for i in range(1, options.duration):
            self.output.write('\x1b[%dD' % (len(s),))
            self.output.flush()
            options.os += options.spread
            self.println_plain(s, options)
            time.sleep(1.0 / options.speed)

    def println_plain(self, s, options):
        for i, c in enumerate(s):
            rgb = self.rainbow(options.freq, options.os + i / options.spread)
            self.output.write(''.join([
                self.wrap(self.ansi(rgb)),
                c,
            ]))


def detect_mode(term_hint='xterm-256color'):
    '''
    Poor-mans color mode detection.
    '''
    if 'ANSICON' in os.environ:
        return 16
    elif os.environ.get('ConEmuANSI', 'OFF') == 'ON':
        return 256
    else:
        term = os.environ.get('TERM', term_hint)
        if term.endswith('-256color') or term in ('xterm', 'screen'):
            return 256
        elif term.endswith('-color') or term in ('rxvt',):
            return 16
        else:
            return 256 # optimistic default


def run():
    import optparse

    parser = optparse.OptionParser(usage=r'%prog [<options>] [file ...]')
    parser.add_option('-p', '--spread', type='float', default=3.0,
        help='Rainbow spread')
    parser.add_option('-F', '--freq', type='float', default=0.1,
        help='Rainbow frequency')
    parser.add_option('-S', '--seed', type='int', default=0,
        help='Rainbow seed')
    parser.add_option('-a', '--animate', action='store_true', default=False,
        help='Enable psychedelics')
    parser.add_option('-d', '--duration', type='int', default=12,
        help='Animation duration')
    parser.add_option('-s', '--speed', type='float', default=20.0,
        help='Animation speed')
    parser.add_option('-f', '--force', action='store_true', default=False,
        help='Force colour even when stdout is not a tty')

    parser.add_option('-3', action='store_const', dest='mode', const=8,
        help='Force 3 bit colour mode')
    parser.add_option('-4', action='store_const', dest='mode', const=16,
        help='Force 4 bit colour mode')
    parser.add_option('-8', action='store_const', dest='mode', const=256,
        help='Force 8 bit colour mode')

    options, args = parser.parse_args()
    options.os = random.randint(0, 256) if options.seed == 0 else options.seed
    options.mode = options.mode or detect_mode()

    lolcat = LolCat(mode=options.mode)

    if not args:
        args = ['-']

    for filename in args:
        if filename == '-':
            lolcat.cat(sys.stdin, options)
        else:
            with open(filename, 'r') as fp:
                lolcat.cat(fp, options)

if __name__ == '__main__':
    sys.exit(run())
