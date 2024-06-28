# Instructions for using the calendar

## Preparation
* You need a CSV file similar to ``/files/programm-themenwoche.csv.`` Note the difference between "start"/"end" and "start-ovr"/"end-ovr"! The "start" and "end" times (currently only in 30-min increments) dictate the position and height of the event "block" on the program, but may be different from the actual time of the event. The "start-ovr" and "end-ovr" times ("override") are the actual start and end time of the event. Each event should be assigned an ``id``, e.g. "Auftaktveranstaltung" has the id ``event-auftakt`` defined in the CSV file.
* You need to have an "events directory" HTML file similar to ``/calendar-events/events-dir.html.`` that contains ``div`` elements for all events. The ``id`` attribute of each ``div`` should match the ``id`` of the event exactly. You can do this manually (which takes time), or you can do it automatically by running the file ``/calendar-events/directory-generator.py`` once.

## design template
Phantom by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)


This is Phantom, a simple design built around a grid of large, colorful, semi-interactive
image tiles (of which you can have as many or as few as you like). Makes use of some
SVG and animation techniques I've been experimenting with on that other project of mine
you may have heard about (https://carrd.co), and includes a handy generic page for whatever.

Demo images* courtesy of Unsplash, a radtastic collection of CC0 (public domain) images
you can use for pretty much whatever.

(* = not included)

AJ
aj@lkn.io | @ajlkn


Credits:

	Demo Images:
		Unsplash (unsplash.com)

	Icons:
		Font Awesome (fontawesome.io)

	Other:
		jQuery (jquery.com)
		Responsive Tools (github.com/ajlkn/responsive-tools)
