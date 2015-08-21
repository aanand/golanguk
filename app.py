from time import sleep
from sys import stdout
from itertools import cycle, count
from os import popen
from io import StringIO
from lolcat import LolCat

banner = """ ____            _               ____             _
|  _ \ _   _ ___| |__     __ _  |  _ \  ___   ___| | _____ _ __
| |_) | | | / __| '_ \   / _` | | | | |/ _ \ / __| |/ / _ \ '__|
|  __/| |_| \__ \ | | | | (_| | | |_| | (_) | (__|   <  __/ |
|_|    \__,_|___/_| |_|  \__,_| |____/ \___/ \___|_|\_\___|_|

 ___                                 ____      _
|_ _|_ __ ___   __ _  __ _  ___     / ___| ___| |_    __ _
 | || '_ ` _ \ / _` |/ _` |/ _ \   | |  _ / _ \ __|  / _` |
 | || | | | | | (_| | (_| |  __/_  | |_| |  __/ |_  | (_| |
|___|_| |_| |_|\__,_|\__, |\___( )  \____|\___|\__|  \__,_|
                     |___/     |/
 _____    ____  _     _      _   _
|_   _|  / ___|| |__ (_)_ __| |_| |
  | |____\___ \| '_ \| | '__| __| |
  | |_____|__) | | | | | |  | |_|_|
  |_|    |____/|_| |_|_|_|   \__(_)"""

frames = [
    """        ,_---~~~~~----._
  _,,_,*^____      _____``*g*\\"*,
 / __/ /'     ^.  /      \ ^@q   f
[  @f | @))    |  | @))   l  0 _/
 \`/   \~____ / __ \_____/    \\
  |           _l__l_           I
  }          [______]           I
  ]            | | |            |
  ]             ~ ~             |
  |                            |
   |                           |""",
    """        ,_---~~~~~----._
  _,,_,*^____      _____``*g*\\"*,
 / __/ /'     ^.  /      \ ^@q   f
[  @f |  (@)   |  | (@)   l  0 _/
 \`/   \~____ / __ \_____/    \\
  |           _l__l_           I
  }          [______]           I
  ]            | | |            |
  ]             ~ ~             |
  |                            |
   |                           |""",
    """        ,_---~~~~~----._
  _,,_,*^____      _____``*g*\\"*,
 / __/ /'     ^.  /      \ ^@q   f
[  @f |   (@)  |  |  (@)  l  0 _/
 \`/   \~____ / __ \_____/    \\
  |           _l__l_           I
  }          [______]           I
  ]            | | |            |
  ]             ~ ~             |
  |                            |
   |                           |""",
    """        ,_---~~~~~----._
  _,,_,*^____      _____``*g*\\"*,
 / __/ /'     ^.  /      \ ^@q   f
[  @f |    @)) |  |   @)) l  0 _/
 \`/   \~____ / __ \_____/    \\
  |           _l__l_           I
  }          [______]           I
  ]            | | |            |
  ]             ~ ~             |
  |                            |
   |                           |""",
]


def colourise(s, start):
    lolcat = LolCat()
    stringio = StringIO()
    for i, c in enumerate(s):
        rgb = lolcat.rainbow(0.1, start + i / 20.0)
        stringio.write(''.join([
            lolcat.wrap(lolcat.ansi(rgb)),
            c,
        ]))
    return stringio.getvalue()


terminal_width = int(popen('stty size', 'r').read().split()[1])
lines = frames[0].split("\n")
offsets = range(terminal_width - max(len(line) for line in lines))
offsets = cycle(list(offsets) + list(reversed(offsets)))

for (offset, i, frame) in zip(offsets, count(), cycle(frames)):
    stringio = StringIO()
    stringio.write(banner)
    stringio.write("\n\n")
    stringio.write("\n".join(
        "".join(" " for _ in range(offset)) + line
        for line in frame.split("\n")
    ))
    stringio.write("\n")

    stdout.write("\033[2J" + colourise(stringio.getvalue(), i*5))
    stdout.flush()
    sleep(0.1)
