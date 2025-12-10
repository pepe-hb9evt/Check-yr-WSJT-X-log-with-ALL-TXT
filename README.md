
# Overview

- This repository is under construction.
- The first part in working fine.
- Lets see how far I get with the second part.


## Authors

- This first part developed by Pepe HB9EVT in a one night session in December 2025
- with support from my lovely auntie A.I. Perplexity (Thanks Auntie, I'm hugging you!)
- Contact: github2025  -at-  pepemail.ch


## License

This project is licensed under the MIT License - see the LICENSE file for details.

I would appreciate a short email if you use this software:
github2025  -at-  pepemail.ch


## Main module

Check_yr_WSJT-X_log_with_ALL-TXT.py


## Prepare before starting

1. Copy from the WSJT-X log a part of ALL.TXT to the input file named `Excerpt_from_ALL-TXT.txt`.
2. Edit the `callsign` variable in the main module to your own callsign.
3. Run the main module.


## Features so far implemented

- Filters the input file for a lines with your callsign
- Exports these lines to `Filtered_lines.txt`
- Displays these lines in a Tkinter GUI with navigation features
- Highlights for each QSO having a RR73 message the other callsign in red
- Shows this other callsign in red color in all visible lines
- Shows if this other callsign appears in lines above or below the current window
- With navigation buttons to move through the filtered lines


## Features to be implemented

- WSJT-X log can be imported too.
- The content of ALL.TXT will be compared with the WSJT-X log to detect missing logged QSOs.


## Comments welcome

Any comments and suggestions are welcome.
github2025  -at-  pepemail.ch
Thank you!
