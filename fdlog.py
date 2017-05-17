#!/usr/bin/python
# fdlog.py Copyright Alan K Biocca (W6AKB) www.fdlog.info

print "\nHigh Sierra Field Day Log Program\n"

prog = "FDLog v4-1-152j 2014/05/26 distributed under the GNU Public License\n"\
       "  Copyright 2002-2014 by Alan Biocca (W6AKB) (www.fdlog.info)\n"
#       "  FDLog is distributed under the GNU Public License\n"
#       "  TCP Remote capable version\n"

print prog,

about = """

FDLog = Field Day Log Program (www.fdlog.info)
  Distributed Synchronized Database Log
  
Copyright by Alan Biocca (W6AKB, formerly WB6ZQZ)
  High Sierra Field Day Group
  about 5K lines of Python Code

"""

# Current Problems and Issues
#
# update is occasionally throwing a disk i/o error in tkinter callback,
#   around update/updateqct/adjust/put, may be dropbox related
#
# qso/data broadcasts do not seem to be working, they are always fixed
#   by 'fills' afterward so not noticed, except when filling is broken
#   low priority since it works anyway, but good to fix
#
# testq seems to be sending both q broadcasts and status broadcasts for each q
#   but the broadcasts don't seem to fill the log for some reason
#   would rather it didn't send the broadcasts
#   but since it does why don't they enter the log?
#
# exit not clean, hangs (fixed)

# port numbers and TCP/UDP (done)
#
# in the address field use 0.0.0.0:123 instead of 0.0.0.0 to denote TCP on port 123
#   if there is no : then it is UDP on standard port
#   if there is a : then TCP on the port following the :

# major version history
#   1 small c version 1984 (H89 multiuser) (Alan WB6ZQZ)
#   2 os9 port (multiuser) (Eric WD6CMU)
#   3 msdos port (single user) (Steve KA6S et al?) (who all worked on this?)
#   4 python 2.2-2.7 rewrite 2002 (networked) (Alan W6AKB/WB6ZQZ)
#   5 future major restructuring??

# new numbering scheme
#   FDLog-<major>-<minor>-<release>
#   and release is monotonic integer, increased when released or checkpointed
#   release may be optionally followed by single letter for finer control
#   and major and minor are manually managed
#   minor is for protocol changes, and other significant changes
#   note this does not affect files, fdlog.py is still the executable

# Release Log below, Suggestion List at end of file

# Known Bug List and Change Plan
#
# udp occasionally lethargic, packets missing unexpectedly
#
# on Mac adding participants doesn't add them to pulldown (only on wa6fxp's mac?)
#
# qso broadcasts rcvd may not be getting to database (maybe)
#
# .ba command not showing stations on the bands (improving in 4-1-152)(fixed?)
#
# probably should limit transmitters to 99 :)
#
# should make version 153 for FD2014 final
# would be nice to discard the poor large status updates for time when possible
#
# debug rapid repeat of fills and broadcasts not making database
#
# make short status packets have better time levels
# have nodes with better time send short status packets, and a little more often
# might want option flag on bells to enable/disable

release_log = """\

4-1-152j

    need to add 'it' version FD Clock options back to this version
    
    added 900 to .band command
    added .timeok to .h help command
    added ? help note to startup
    compacted startup lines on GUI
    adjusted comments
    added signature to console QSTs -logger
    display UDP and TCP ports (only showed UDP before and didn't note protocol)

4-1-152i fingerprint 9738da

    added QST bells (noise) and copy to console
    this was used in FD2014 (also an 'it' version used)

4-1-152h fingerprint 62169f

    made a new packaging program (packager.py), added fingerprinting to it
    reduced writes of offset to database
    added more info at shutdown time, directed user to close console after app finishes
    added more delays during shutdown
    tightened tdwin default to 5 (even over internet 2 is enough)
    added os exit call after shutdown to clear dangling items

4-1-152g fingerprint ends in 146e5

    preparing for FD2014, shared this version to HSFDG for testing 5/26
    added W6AKB's GPS Station Clock
      this is a GPS with PPS, a Teensy2 with USB, a ChronoDot and some displays
      design and PC boards will be available
      it delives millisecond accurate time via USB
      and provides readouts of UTC and Local Time on several displays
      FDLog searches the first 20 COM channels for it
        if either there is no serial library or it doesn't find it
        the GPS Clock it gives up
        FDLot will only use the GPS Clock time when locked to GPS
    separated time master from how the station gets time
      only one master, it advertises level 0
        set by .set tmast <nodeid> as before
        regardless of how the master node gets time
        master node sends time only status broadcasts at 1hz
      if a station is not master and has a GPS clock it can advertise level 1
      if a station has a defined accurate clock it can advertise 2
        turn on with .timeok 1, off with .timeok 0, stored in local database
      stations add 3 to their source to report their own time level
    added defined accurate time flag for each station (.timeok 0/1)
      indicates system time is accurate (and offset is zero)
      stored in local database like operator, logger, power, debug
      smoothly transitions to offset zero
    add gps clock flag for each station (did auto find instead)
      drives local offset from gps clock readings
    it doesn't make sense to have both as this would drive
      the offset to zero and to a value...
      so one must take priority over the other
      the gps clock takes priority since it is verifiable..
      then drops to timeok if true and gps clock not locked
    time master now sends out time-only broadcasts at 1hz
      in addition to the usual 10 second full info status broadcast
    fixed startup clock offset read from database (old bug fixed)
    makes smooth transition between modes (offset transitions at most 0.1s per second

4-1-152f added 900 to band command

    added 900 to .ba command
    band command titles fixed
    comments updated
    probably FD2013 version (for many to most stations)
    
4-1-152e vhf cabrillo output 5/30/2013

    making ba command smarter, filtering for newest info on each station
    limit age growth on info to 999 min (999 minutes old max)
    .ba command shows time since last Q (tslq) in minutes instead of time of last Q (tmlq)
    .ba command tslq now in hhmm units
    added cabrillo for vhf contest to saved entry file
    added .set grid <grid> for 4 character grid entry
    
4-1-152d port change and cleanup 5/2013

    changed shutting down comment
    edited other comments
    added startup info about remote mode capable
    fixing date
    note that dates on version line were 2013/05/12, forgot to edit that
    .ba command formatting improved and information filtered
    changed to tcp port 5100 (yahoo webcam) to be compatible with work firewall
    changed indicatoron in band buttons to 1 which changes look but works better on mac
    detected os.name and made indicatoron for posix os (mac and likely linux)

4-1-152c minor cleanup 5/2013

    made storing globals to database automatic when commands processed
    made shutdown closing socket activity ignore exceptions
    clock tracking is jumping
      slowing clock slew to 0.1s/s
      target half the error each 30 seconds (instead of all)

4-1-152b clock slewing 5/2013

    fixed clock slew (was frozen)
    added fingerprint

4-1-152a remote TCP beta 5/2013

    adding TCP remote synchronization in this version.
    cleaning out old remote sync code
    changing threads to use threading library (slightly higher level)
    reinstated rem_adr and added flags for tcp server and client
    replacing and rewriting network sections to add TCP
    updated to ADIF 2.27
    added countdown to testQ reports
    filtered response of RCVP FAIL as it would flicker in some cases
      when there was no problem
    added "NET OK" when GOTA Q's are zero
    adapted versioning in messages to new scheme (broken since after x.y versions)
    improving .ba command
    problems with utf strings, sockets traced to sqlite unicode, useful article:
      http://stackoverflow.com/questions/2392732/sqlite-python-unicode-and-non-utf-data
    problems with windows firewall, make sure python is allowed
    broadcasts working over tcp
    filling working over tcp, slowed it from 10hz to 5hz to reduce repeats
    added fingerprint function to output md5 hexdigest of fdlog.py at startup
    changed to use real 'from' address for fills to avoid NAT issues
    testing progress thanks to W6AKB and N6OI:
      1-146, 1-149, 4-152a FDLog versions with python 2.6 and 2.7, UDP and TCP
      up to 4 stations at once
      FDGroup testing further
      one problem noted on Mac by RichF, adding participants doesn't add to pulldown
        not reproduced on w6akb mac

4-1-151 more sqlite beta 5/12/2013

    make database fdlog.sq3 for global value storage (replacing textfile)
    store time offset in global database so a restart doesn't jump the time
    added in memory cache for global database to reduce file i/o
    changing build to release, only increments when
      released to others or checkpointed
    added code to ignore short w1aw file placeholder in scoring final entry
    changed FDLOG to FDLog
    various general tidying up (minor)
    changed (c) to Copyright since (c) is not legal
    commented out remote UDP broadcast code (unfinished code)
    considering putting in remote TCP code instead - soon

4-1-150 sqlite beta 2013/05/11 database upgrade

    adding sqlite log database (keeping text file journal, but db is primary)
    conforming to proposed new version numbering system

1-149-02 2011/07/11 bug fix

    allow lowercase contest names
    added 900 mhz to editing validation
    note that report requires 4 chars in editor to save
    editor shows unvalidated fields in yellow after save attempt
    edit dialog box disappears on successful save, else stays with yellow
    fields that need fixing.
    note that this version is not reporting version number in the
      status packets correctly, shows up as 'v' with no value
      likely has been this way since 1.147 due to old regexp
    
1-149 2011/07/02 contest set version

    adding .set contst menu for (FD,VHF)
        set global to contest type .set contst FD|VHF
        adjust dup check to call for FD, and include /<grid> for VHF
    adjust bands for VHF, include 900, (drop below 6m?)
        dropping bands is tricky, leave for later.
        did add 900 band however

    setup for mercurial, opened Google Code project

1-148vf 2011/06/25 fd version

    commented out VHF code but kept other changes for 2011 fday

1-148v 2010/08/18 vhf version

    dup checking includes call/grid
    call column widened by 1 char to handle additional width
    still need to enter something in the report, such as signal strength
    fixed some small bugs in log color and editing due to dependence
    on data in the scrollbox. May be only one line change to
    make compatible with standard Field Day.

    q just needs call/grid & band (use same mode for all Qs)
    got it to work.
    added a column to make call/grid fit
    fixed a few bugs
    newline on log missing, added it, later removed again

    now two bugs. (fixed)
    local log color=blue not working
    - always black
    edit left mouse click for edit on log not working
    - probably getting error at some point and killing that thread/window
    - problem was two functions that pick up chars from msg buffer
    - adjust them by 1 char, worked

    note that python is complaining about md5 and using hashlib instead.
    snap 9, release 3 at this point

    also after space input didn't echo call with full grid. Fixed.
    converted from md5 library to hashlib. done.
    snap 10 release 4

    made call box in edit dig wider to accommodate 11 char call/grid
    added code to disallow editing another node's Qs
    after changing node id and restarting the q's still came up blue? bug?
    test code was still in. fixed.
    snap 11

    comment cleanup. added more notes detail.

1.147 2009/06/20 pre fd (used on FD 2009,2010)

    changed GOTA Q limit from 400 to 500
    demo modes commented out
    80 meter cw frequency for w1aw changed (w1aw.txt)

    qrp 5W from mains or generator has a multiplier 2 - same as 150W.
        This is not scored properly by the program yet.
    max of 20 transmitters is not enforced by the program
    educational activity is not scored by the program.
    complex GOTA bonus points are not handled by the program

1.146B has GOTA call fixed. 6/15/2008 AKB
        gcall will accept a proper call with number, somewhere prior to this
        the number part of the regex got lost. This affects log output.

Revision 1.146  2006/06/11 22:00:57  Alan Biocca
    Documentation - minor cleanup.
    Setup - added web push dir support. (also upload)
    TimeSync - new program derived from Eric's that syncs system time from GPS.

Revision 1.145  2005/09/12 03:41:23  Alan Biocca
    Minor Comment Edits

Revision 1.144  2005/09/12 03:17:11  Alan Biocca
    Added Q Edit Dialog Box. Major Effort

Revision 1.143  2005/07/06 17:26:13  Alan Biocca
    Added Time Zone Chart

Revision 1.142  2005/07/01 12:58:56  Alan Biocca
    Documentation updated, minor edits to prog comments.

Revision 1.141  2005/07/01 05:13:03  Alan Biocca
    Log autolookups added
    Displays log lines matching the current call when duplicates found,
    or by typing in <call><return>
    This shows the info for this callsign collected on the other bands
    Stubbed in the beginnings of the .edit command

Revision 1.140  2005/06/29 22:44:48  Alan Biocca
    Color log text from this node
    Restrict node to lowercase

Revision 1.139  2005/06/29 20:22:56  Alan Biocca
    Youth updated to take 1-2 digits
    Fixing case on set variables like callsigns initials etc

Revision 1.138  2005/06/28 16:25:09  Alan Biocca
    Adjusted Add Participant dialog box.

Revision 1.137  2005/06/28 16:22:06  Alan Biocca
    Add participants case problem fixed
    Added synonyms for ARRL sections for WAS

Revision 1.136  2005/06/26 19:01:10  Alan Biocca
    Fixed time level display. 3500 lines now.
    I ran this version FD 2005 on one node (changed during).

Revision 1.135  2005/06/19 03:44:56  Alan Biocca
    Minor changes to message in fdlog.
    Major upgrades to group_plan.
    Minor updates to group_handbook.

Revision 1.134  2005/06/17 23:56:23  Alan Biocca
    Preparing for 2005-1 release.
    This version used on FD 2005.

Revision 1.133  2005/06/17 23:24:32  Alan Biocca
    Updates to accomodate ARRL rule changes over the past couple of years
    including GOTA, new bonuses, etc. Minor other cleanup. No substantive
    changes.

Revision 1.132  2005/06/13 23:45:20  Alan Biocca
    Fixed power type-in bug (text vs number).
    Changed power var to keep it a string at all times to fix typed-in power
    anomalies. Improved the Add Participants dialog box.
    Moved to new laptop.

Revision 1.131  2004/07/05 18:48:43 akbiocca
    prep for release to web.

Revision log redux - Thinning.

Revision 1.130  2004/07/05 04:15:58  akbiocca
    Time Synch added. Clients track master node. Designate with .set tmast <node>

Revision 1.128  2004/06/29 23:52:43  akbiocca
    Plans for time sync made. some vars defined. minor misc cleanup.

Revision 1.127  2004/06/29 15:51:13  akbiocca
    Natural power bug fixed. My val() function is apparently a subtle problem
    but only in the tkinter case. Perhaps a conflict with TCL? Changed my func
    to ival(). 

Revision 1.126  2004/06/28 18:42:56  akbiocca
    Comments from FD 2004 added.

Revision 1.125  2004/06/14 02:13:12  akbiocca
    added seed to authkey. updated group handbook. Used for FD 2004

Revision 1.124  2004/06/13 15:19:52  akbiocca
    improving documentation on reporting. fixed power command updating screen.
    some testing. no substantive changes.

Revision 1.122  2004/06/10 20:42:46  akbiocca
    adjusting messages. testing. 

Revision 1.121  2004/06/10 03:39:38  akbiocca
    including c.bat and setup.py for the py2exe config. updated handbook.
    minor edits elsewhere. 

Revision 1.120  2004/06/10 02:37:24  akbiocca
    Setup for py2exe, which appears to work. 

Revision 1.119  2004/06/09 18:15:53  akbiocca
    Added GPL. minor doc edits.

Revision 1.118  2004/06/09 16:38:54  akbiocca
    renaming group files. fdlog startup improvement continues. documentation
    cleanup continues. testing continues, is partial at this time. no substantive
    changes have been made.

Revision 1.116  2004/06/09 02:59:21  akbiocca
    checkpoint. fdlog startup altered to be more interactive, straightforward.
    testing minimal at this point, but changes not fundamental. text files
    edited for some 2004 info, but not final. 

Revision 1.115  2003/07/20 21:39:15  akbiocca
    WAS Logic improved to handle can, dx. This likely vsn for 2003 submittal.

Revision 1.114  2003/07/19 05:39:43  akbiocca
    Improved Worked All States display. Fixed bug in Vermont.

Revision 1.113  2003/07/18 21:37:55  akbiocca
    Updating old comments, removing some old code. Improvement in recognizing
    worked all states. Improving report for FD Entry. Partially tested.

Revision 1.112  2003/07/17 05:26:22  akbiocca
    WAS rpt added to fd log.

Revision 1.111  2003/07/16 14:08:20  akbiocca
    Changed text inputs such as w1aw message, nts messages, etc to 'file input'.
    These fixed filenames are searched for and if existing they are included
    in the FD report.

    w1aw_msg.txt
    nts_msg.txt
    nts_rly0.txt to nts_rly9.txt (one msg per file)
    soapbox.txt
    media.txt

    Added example of nts messages in nts_eg.txt to copy and modify.

Revision 1.110  2003/07/15 03:55:06  akbiocca
    Linux improvement. Changed font calcs. Linux needs about size 20,
    Windoze 10. Changed grid argument col to column for increased
    portability. This after FD03, previous vsn was used for FD03.

Revision 1.109  2003/06/22 17:13:27  akbiocca
    Updated for 2003. Authkey sets data filename and port. Used for FD 2003.

Revision 1.108  2003/06/10 13:49:54  akbiocca
    Prep for FD 2003. GOTA bonus changed. Class F added. Untested.

Revision 1.107  2002/06/22 07:01:13  akbiocca
    Rich found bug in socket addr list. Tested partially w Mac, Sony laptops.

Revision 1.106  2002/06/15 16:11:21  akbiocca
    checkpoint. minor changes to prog, plan, handbook. moved manuals to
    subdir. make this beta 6.

Revision 1.105  2002/05/28 13:36:50  akbiocca
    fdlog fixes to help buttonsize. adding remote bcast (incomplete?).
    changed station to node.. prog seems to run, not well tested.

Revision 1.103  2002/05/13 12:23:46  akbiocca
    small mods to handbook & plan.
    addded grid.sticky=NSEW to all buttons hoping to fix the mac.

Revision 1.102  2002/05/12 22:29:25  akbiocca
    updated group plan with meeting info. first draft.
    update group handbook.
    updated program somewhat. chop print fields that were overflowing.
    improved parsing to reject some bad calls. fixed .h command triggering
    on kh6 callsigns. changed a lot of re.search to re.match calls.
    started to work on internet test feature, not complete.
    this version not significantly tested, but probably works.

Revision 1.101  2002/05/11 03:17:00  akbiocca
    Eric fixed linux fail to bcast. Prelim tests on Linux passed. Win2k tested.
    This was Beta 5, tested at the FD 2002 mtg.

Revision 1.99  2002/05/09 05:01:54  akbiocca
    testing. fixed bug w power on first startup. cleaned comments.
    tested w 2 stations wireless. ok so far. fixed site info typo.

Revision 1.97  2002/05/08 13:55:52  akbiocca
    op, log pulldowns. fixed global sets. testing not complete. docn upgraded.
    cleaned up data handling. lots of code commented out in cleanup, will be
    deleted soon. changed to initials for op, log. added space to other column.
    added dialog for adding participants. power select menu and entry w check
    for natural. converted stub view funcs to lambdas. added online equipment
    manuals, 746 and pro. upgraded site info file.

Revision 1.95  2002/04/23 03:30:04  akbiocca
    added ARRL band plan in help menu.

Revision 1.94  2002/04/22 14:51:52  akbiocca
    lots of edits. reorganized revision history, made a menu to display it.
    added equipment help submenu. reorg help menu. reorg and update of much
    of the doc'n. not complete. expanded site info. added access point to
    wireless doc. added root window titles to subwindows.

Revision 1.93  2002/04/21 08:33:30  akbiocca
    dialog + wasrpt cleanup. sfx report improved.

Revision 1.92  2002/04/20 22:36:34  akbiocca
    added Worked All States Report. measures progress to worked all states.
    requires correct abbreviations to be used for ARRL sections.

Revision 1.91  2002/04/19 03:41:30  akbiocca
    added a few files. propagation, site info, nts manual. cleaned up docs
    regarding control-c and control-z. note that the new text files need
    a bit of work, they are frameworks at this time.

Revision 1.90  2002/04/19 03:16:16  akbiocca
    added python web help menu item. disabled control-c,z (suggested by Weo WN6I).
    added set cursor on mouse-1-up to keep it where it belongs.

Revision 1.86  2002/04/17 12:47:06  akbiocca
    improved time on band accuracy. cleanup.

Revision 1.85  2002/04/15 12:38:34  akbiocca
    added time on band indicator in root title bar.

Revision 1.84  2002/04/15 12:09:30  akbiocca
    view text boxes made resizable, and independent (not transient).
    this allows them to be iconified and not on top.

Revision 1.83  2002/04/15 05:28:30  akbiocca
    made main window resizable.

Revision 1.82  2002/04/15 00:30:58  akbiocca
    release prep beta 4. tagged beta 4.

Revision 1.81  2002/04/14 21:26:26  akbiocca
    added bands.pdf, imported group_handbook.txt.

Revision 1.80  2002/04/14 18:46:41  akbiocca
    w1aw schedule added.
    improved set command help.

Revision 1.79  2002/04/14 16:53:29  akbiocca
    changed to UTC time.

Revision 1.78  2002/04/14 15:42:15  akbiocca
    added .testq test qso generator.

Revision 1.75  2002/04/14 02:21:54  akbiocca
    fixed bug in delete, present in beta 3.
    added more .set commands.

Revision 1.74  2002/04/13 20:32:11  akbiocca
    .set commands added. global data sharing, load/reloading.

Revision 1.73  2002/04/13 13:50:47  akbiocca
    prep for beta-3. (Tagged Beta-3)

Revision 1.71  2002/04/12 17:16:39  akbiocca
    fixed bug in qst to allow question mark in char set there without
    triggering help. improved age out message to include both from and
    station the info is about.

Revision 1.70  2002/04/12 13:17:55  akbiocca
    qst messaging working, added to docn, qst log report added.

Revision 1.67  2002/04/12 03:21:19  akbiocca
    improved net error indicators. working fairly well.

Revision 1.66  2002/04/11 13:51:39  akbiocca
    added logs menu w per band/mode filtering.

Revision 1.64  2002/04/11 05:39:19  akbiocca
    changed to age timeout of band data. pkt struct chgd slightly. 

Revision 1.62  2002/04/09 23:37:02  akbiocca
    added need fill message on CW/D button when fill list length is nonzero.
    this and the NO PKTS indicators are on a 10 second update cycle. 

Revision 1.57  2002/04/08 14:22:54  akbiocca
    included about and getting started into the prog file. plan is to keep
    the program self contained in one file for basic minimal doc'n and
    executable in one file. added cvs log into source. improved root title

1.56 redup on sta chg. getting good!

1.54 band buttons hooked to real data. chg station goes to band off
     exits set band off

1.52 exit button cleans up, launches pdf arrl rules (prob only win32)
     most help menus work. properties made larger. single property diags
     added many text doc files. band button array

1.49 win vsn working, property dialogs working. tk continues.

1.46 tk integration begins..

1.44 contest entry to file. effort est 10d. 1500 lines. beta-2?

1.41 many changes. wireless tested. fd entry report output in work
     mac/unix port changes started. dup reports. 1500 lines

1.30 fixed start date conflict in comments. dug out 1984 start date!
     mv todo, etc to notes.txt file. approx 7 days effort in. 915 lines

1.8  sped up fill and rcvr threads
     rcvr blocked on read - no delay. filling works fast now
     debug mode slows fill requestor, otherwist fills at 10hz
     fixed propagation of broadcast info. works fairly well..

1.4  (in cvs) net sync works! approx 5 days fte effort so far

1.1  2002/03/18 23:35:15  akbiocca
     Initial revision (to CVS)

-------------------------------------------------------------

Program History (Pre-CVS)

Re-coding started 3/6/2002 Alan K Biocca WB6ZQZ (wb6zqz@arrl.net)
Design based on fdlog.c, by same author starting in 1984 for CP/M.

Goal: a minimum keystroke field day logging program supporting
      a group of users (a whole FD site) simultaneously

The original program was multitasking and supported multiple
stations on serial terminals, 2000 lines of small C and asm.
With help from Eric Williams WD6CMU and Steve Wilson KA6S, it
devolved to MSDOS but there supported only one user, so the
database had to be manually collated to include all stations.

Plan: use networking, usually 802.11b peer-to-peer wireless,
   to interconnect the stations. use a flood/fill algorithm
   to share data. avoid single point failure, stations can join
   and depart the network with minimal effect.

v0.01 started 3/2002. chose python as it has the features
   to do this project well and efficiently
   after 2.5 days of effort the program is working for a
   single station. useful for single station logging
-------------------------------------------------------------------

"""

key_help = """
FDLog.py Help       File/Exit or Exit Button to Quit
                    ESC to abort input line
                    .h<return> for command help
                     
<suffix><space>                 look up dups by suffix
<prefix><space>                 add prefix to previous suffix
<call><space><report><return>   log a contact

#<message>                      send qst message to all stations

:<dd.hhmm><space><call><space><report><return>  to force a date/time

<call> is <letters><digits><letters> or <digits><letters><digits>
           followed by optional /<alphanumerics>
           
<suffix> is <letters> or <digits>
<prefix> is <letters><digits> or <digits><letters>
"""

def mhelp():
    viewtextv(key_help)

getting_started = """
FDLog = Field Day Logging Program            Copyright 2002-2013 Alan K Biocca

  Welcome to the W6AKB (formerly WB6ZQZ) FDLog program. This getting started
dialog will review the essentials and get you started using the program.

  FDLog is distributed under the GNU Public License. A copy is included
in the distribution package (gnu.txt) or can be found at www.gnu.org.

  Starting the program by either double clicking on fdlog.py, or typing
it on the command line. It will come up and ask for some configuration info.

  The node id is used to identify the database records for each node in
the network of logging computers. These names must be unique - no two nodes
may use the same id at the same time. 
The suggested id is the callsign of the equipment owner followed by a dash
and a single digit, similar to packet radio id's. An example would be:
wb6zqz-1. Valid characters include lowercase letters, numbers, and dash.
An alternate form is to use suffix-digit or just suffix such as 'zqz-1' or
just zqz.

  The node id will be requested as input during the first startup. Thereafter
it may be changed from the Properties menu.

  The authentication key is used to validate packets. Outgoing packets are
signed, and incoming packets are checked for correct signatures. Invalid
packets are not processed. Set the authentication key to the same value
for all nodes during startup.  The authentication key is made up of three
components. The first 3 characters are used as part of the logfile name.
Typically these are set to 'tst' for testing, or the two digit year and a
letter, such as '04a' for 2004, log file version a. This allows multiple
logfiles if desired. The next 3 digits are the port number factor. Characters
beyond that are used for the signature hash: 'yycppphhh...'

  The authentication key is input at each program startup. To change it,
quit and restart the program.

  Host based firewalls (such as Zone Alarm) can be used with FDLog.
The program needs to be a server and client on the internet, so give it
that access (if network/wireless synchronization between stations is
desired).

  The display consists of four areas. The Menu Bar, the Button area,
and the Input Window.

  The window title bar displays a lot of information. Some items may not have
values and so will not display until they do. From left to right:

    FDLog                       program name
    2A SV-Sacramento Valley     field day class and section (the report)
    Node: wb6zqz-1              node id
    Time on Band 0:23           time on this band in hours, minutes
    13:35 UTC 04/23             UTC time and date

  The Menu has many options which will be covered later. In particular,
there are many useful items under the Help menu.

  The Band Buttons are used to set the band of this station. They are in
wavelength (meters) from 160 through 2, and then in frequency from 220
through 1200. Satellite is abbreviated 'sat'. Cw, Digital and Phone are
indicated by a single postfix letter; 'c', 'd', and 'p'. Thus Satellite
Phone is 'satp' and twenty meter cw is '20c'.

  The 'off' selections are to be selected when the station is not on a
band. This allows other stations to use the band.

  The Class indicator shows the number of stations on vs the number allowed.
Thus 0/2 is none on, two allowed. The VHF label indicates the number of
stations on VHF, and the number of Free stations available. Thus 1/1 shows
one station on VHF, one free allowed. Similarly, 2/1 indicates two stations
on, and one free is allowed. The second VHF station will count against the
Class transmitter count.

  The FonQ indicator shows the number of phone contacts. The GOTAq indicator
shows the number of Get On The Air station contacts. This lower right label
gets overwritten with error messages regarding the networking when needed.
These errors are described later.

  This section has color coding. In the Band columns Gray indicates
available bands, Yellow is on occupied bands, Orange an over-occupied
band, White the band this station is on, and Red an over-occupied
band this station is on. In the Class column White indicates no stations,
Yellow is some but not all that are allotted, and Green is full usage of that
station type. Red or Orange indicates too many stations for the current Class.

  Just below the Band Button block is the Operator/Logger/Power button
row. These Menubuttons allow selecting from the participants for Operator and
Logger, Adding new Participants, and entering the Power Level. Participants
are indexed by initials, so they must be unique. The power level may be
selected from the pulldown menu, or typed in. The Natural checkbox is used
to designate Natural Power for proper bonus credit.

  The Central window displays the current log entries. It may be scrolled
back to inspect earlier entries. Log entries and QSTs from other stations
are included in this display.

  The Lower window is the input window. Log Entries are typed there, and it
can be scrolled back to inspect earlier entries. Only local input data
appears in the lower display.
  
  The computer's clock accuracy is important for sorting of reports. The
program uses UTC time, so incorrect time zone settings can cause apparent time
errors. The '.tdwin' command sets the tolerance for time difference in seconds.
Incoming packets showing time differences exceeding this number of seconds
are displayed in the Command Window. One computer on the network can be
designated the time master (.set tmast <nodeid>). This machine should have
good time, all the other FDLogs will measure a time offset and apply this
to their system clocks to make FDLog time. An optional GPS Clock can be
USB connected that will synchronize FDLog to much better than one second.

  The output power in (watts) is recorded in the log. An output power of
0 watts indicates a test, so it will not be included in the final logs. Use
the Power button or Power Entry box to set the power level. Check the Natural
checkbox if the station is using natural power (to get credit for the extra
points).

  The operator and logger are recorded in the log. Use the Operator and Logger
buttons to select.

  The power, operator, logger, and authentication data are stored in a database
with the log program on normal exit, and reloaded on restart to minimize
re-entering. The band is not restored, so it will have to be re-selected after
restarting the program.

  Band is set by clicking on the desired gray band button or typing a command
".band  <band><mode>". Bands are 160/80/40/20/15/10/6/2 meters or 220/440/900/1200
mhz or sat (for satellite) followed by a mode letter c, d or p for cw, digital
or phone. It will warn you if there is another station on that band, but it will
allow the change anyway. Make sure the other station is not using the band
before making contacts.

  There is a special switch for VHF contests that changes a few things.
(.set contst VHF or .set contst FD). The main change is dup checking,
the QSO mode doesn't matter in VHF mode, stations are worked once per
band and grid. There is also a Cabrillo output in the result file. There
is no Cabrillo format defined for Field Day.

  Testing can be done with the band set to 'off' (or by using the 'tst'
authentication code). Contacts made to band 'off' are not counted in the
various scoring outputs, and will be filtered from the final log. Use the
auth key 'tst' to share data with test stations. In this configuration the
band and mode can be set as if operating to fully exercise the system since
the test log is separate from the contest log. When ready to join the actual
field day data net, shut down the fdlog program. Restart the program and use
the key that the group is using for the contest. Note that two groups in the
same physical area can use keys with differing port fields to avoid
authentication error warnings.

  Logging contacts is optimized for minimum keystrokes. Enter the call suffix
followed by a space to do a quick dup check. This will list any calls on this
band/mode  that have that same suffix. To log that call enter the prefix and
a space, and it will automatically pick up the earlier suffix and be ready for
the report. After typing the report, wait for the actual QSL confirmation
before hitting return. Return logs the Q into the database. Study the ARRL
section abbreviations to use the correct ones. This will enable the worked
all states function to be accurate.

  Here is an example using 12 keystrokes to log a Q:

  aw<space> ==> ['w2aw']         <shows w2aw was worked on this band>
  w1<space> ==> w1aw<space>_     <waiting for report, not a dup>
  <report>  ==> w1aw 2a nc_      <waiting for return to log the Q>
  <return>  ==> w1aw 2a nc QSL   <entered into log db>

  ESCape will cancel an entry in progress and clear the input line.

  Wait to hit <return> until tho QSO has been confirmed.

  An incorrectly entered Q can be deleted with:
".delete <node> <sequencenum> <reason>". This command actually places
a 'delete' entry in the log which is used to filter clean logs. The
node and sequence number are the right two log columns. OR an easier
techique is to click on the log entry and select DELETE in the popup
box. Editing of the log entry this way is also possible.

  When taking a break in operations, set the band to 'off' with the "off"
button or the ".off" command. This makes the band available to others.

  If a node is just joining the net, or was off for awhile, it will take time
for it to 'catch up' to the full database. It attempts to do this at 10 items 
per second, so it should not take long. It will display the data as it comes in,
so when it stops streaming data it is probably caught up. The 'Need Fill'
indicator will appear until it is caught up.

  QST broadcast messages can be sent to all nodes and entered into the log
by typing '#<message>' starting in column one. These are visible in the upper
window and scan be reviewed by selecting the log for band *QST, so watch for
them!

Platform Issues

  This program was developed under Windows 2k/7. It also works on Linux,
Unix, and Macintosh due to the portability of Python and Tkinter. There are
some issues that will affect portability, and some functions may not work.
For example, launching the ARRL Rules pdf file may only work on Windows. Font
sizes may be an issue on Linux.

Troubleshooting

  The program checks the networking and if any problems are noted they are
displayed on the lower right button (that usually reads GOTAq), turning it
yellow and putting a short message in it. These messages and what they mean
are detailed below. Note that it will display "NET OK" instead of a zero
GOTA Q count.

  NO NODE    The node identification is missing. This is necessary
             to identify the database records when they are shared.
             It is recommended to set this to the callsign of the owner
             of the station radio or computer (or the suffix), optionally
             followed by a dash and a single digit number if more than one
             id is needed. THIS MUST BE UNIQUE. DO NOT GIVE TWO NODES THE
             SAME NODE ID at the same time. Restart the program
             and answer the query during initialization to set it.

  NO AUTHKEY The authentication key is missing. Restart the program
             and answer the query during initialization to set it.
             It must match the other nodes you are sharing data with.
             
  SNDP FAIL  The Packet Sender has received an error from the operating
             sytem. This may occur when there is a network problem.
             Restarting the program or rebooting may cure it.
             
  RCVP FAIL  Twenty seconds have passed without receiving any packets. This
             indicates that no other packets from a FDLog program are
             being received within the time window. This could indicate
             a problem with the network or auth key, or it could be normal
             if this is the only computer on this network running the
             program. It will occur occasionally if there are only two
             computers on the network running FDLog. Try restarting the
             program after the network is known to be working.

  AUTH FAIL  A packet has been received (on the port) that has the incorrect
             authentication code. It will not be processed. All nodes
             participating must use the same authentication key. Refer to
             the command window for more information about this error. It
             is best if test and production modes use different ports to
             avoid seeing each others packets which have differing
             authentication codes.

  NEED FILL  A node status broadcast has been received, and one or more
             of these nodes have data that this node's database does
             not have. This node will request the missing data until
             it is caught up. The new database items will be displayed in
             the upper display as they come in. If the NEED FILL is
             indicated, and no data is flowing into the upper display,
             the requests for data are not being answered.

  The incoming packets are checked for time skew. If it exceeds '.tdwin'
seconds a message is displayed in the command window. The default is 10
seconds. The message is 'tdel <diff> <host> <ip> <node> <utc date.time>'.
The window can be adjusted with the '.tdwin <seconds> command. (Note -
set the tmast variable to select a time master node - see the .set menu).

Reports

File / Save Entry File    - writes the complete Entry file to the file named
                            'fdlog.log' (including ADIF format log)

File / Preview Entry File - preview the existing entry file.

File / View Raw Logfile   - view the raw database file ('fdlog.fdb')

The following reports are generated from keyboard commands (starting with
'.' (period)). They respond to the command window.

.st     this station's status
.ba     station and band status
.re     log summary report
.pr     save contest entry to 'fdlog.log'

Keyboard Input Syntax for QSOs

call is
  <prefix><suffix><tag>

prefix is
  <letters><digits> or <digits><letters>

suffix is
  <letters or digits>  (different from end of prefix)

tag is
  /<letters or digits>

qso is
  <call> <report>

report is
  <letters or digits or spaces>

commands are
  .help
  .pow <digits><optional 'n'>
  .band <band><mode>           bands are 160..2m, 220..1200, modes are c d p
  .edit <call>                 editing function (in work)
  .delete <node> <seqnum>      delete a database entry
  .st                          this node's status
  .ba                          station band report
  .re                          summary
  .pr                          generate contest entry

Forcing a Contact into the database at a specific time (eg: from paper logs):
  :dd.hhmm <call> <report> (picks up band/mode/oper/log/power)

QST messages to all nodes:
  #<message>
    
eof
"""

import os,sys,time,calendar,string,re,time,thread,threading,socket,hashlib,random,math
from Tkinter import *

def fingerprint():
    t = open('fdlog.py').read()
    h = hashlib.md5()
    h.update(t)
    print "  FDLog Fingerprint",h.hexdigest()
fingerprint()

# Time Conversion Chart
#000 0000 0000 0000 0000
#000  -8   -7   -6   -5
tzchart = """
 UTC       PDT  CDT  EDT
 GMT  PST  CST  EST

"""

for g in range(0,2400,100):
    p = g - 800
    if (p < 0): p += 2400
    c = p + 100
    if (c < 0): c += 2400
    e = c + 100
    if (e < 0): e += 2400
    x = e + 100
    if (x < 0): x += 2400
    tzchart += "%04d %04d %04d %04d %04d\n"%(g,p,c,e,x)

#print tzchart

# font setups (needs different fonts for Linux and Macintosh)
# fontsize on linux works around 18-20 (from Bob W9YA)
# fontsize default was 10 on windoze, interval 2
# fontsize of 18 won't fit on many windoze systems
# should make this user configurable. akb. xx

fontsize = 10
fontinterval = 2
typeface = 'Courier'

fdfont  = (typeface,fontsize)                  # regular fixwidth font
fdmfont = (typeface,fontsize+fontinterval)     # medium  fixwidth font
fdbfont = (typeface,fontsize+fontinterval*2)   # large   fixwidth font

# integer value utility

def ival(s):
    "return value of leading int"
    r = 0
    if s != "":
        m = re.match(r' *(-?[0-9]*)',s)
        if m and m.group(1):
            r = int(m.group(1))
    return r

def getver():
    "get version info"
    m = re.search(r'v[0-9]-[0-9]+-([0-9]+[a-zA-Z]{0,1})',prog)
    version = "v"
    if m: version += m.group(1)
    print "  FDLog version",version,"\n"
    return version
version = getver()

# feature request - built in time correction - use 'master' and offsets
#
# master is designated. marks time as level '0'
#
# time offset is stored in local database, so will return after reboot
# time master designation stored in db as a .set
# move gradually into correct time. speed up or slow by 25% max.
#
# master has zero correction factor - broadcasts system time
#
# local clock adjust procedure is - shutdown fdlog, change, start fdlog
#
# at broadcast reception:
#   if at level then average
#   if above level then restart average with this
#
# every minute:
#   look at what we know and do time correction
#
# time quality levels (0..9)
#   0 = designated master
#   1 = sync'd to master
#   2 = sync'd to level 2
#   ..
#   9 = not sync'd
#
#   consider self synchronized when error <= 2s?
#     then set level to src+1
#
#   new and other nodes will go to level 9
#
# may need a semaphore around these variables..

timeok = 0              # system time is defined to be trusted (NTP etc)

class clock_class:
    
    level = 9           # my time quality level
    offset = 0          # my time offset from system clock, add to system time, sec
    adjusta = 0         # amount to adjust clock now (delta)
    errors = 0          # current error sum wrt best source, in total seconds
    errorn = 0          # number of time values in errors sum
    srclev = 10         # current best time source level
    #systmok = 0         # system time is to be trusted
    clockser = None     # gps clock serial

    # level 0 is time master
    # level 1 is have gps clock
    # level 2 is have accurate system time
    # level 3 is tracking time master
    # level 4 is tracking gps clock
    # level 5 is tracking accurate system time
    # level 6 is tracking time master but not close yet
    # level 7 is tracking gps clock but not close yet
    # level 8 is tracking accurate system time but not close yet
    # level 9 is holding, nothing to track

    #offset = globDb.get('toffset',4)  # get initial from global database
    #print "Initial Time Offset",offset
    
    lock = threading.RLock()    # sharing lock, to protect against overlapping

    def update(self):
        "periodic clock update every 30 seconds"

        gpslock,gpserr = self.gpsclock()          # check for gps clock

        self.lock.acquire()                           # take semaphore
        
##        if node == string.lower(gd.getv('tmast')):    # see if we are master
##            if self.level != 0: print "Time Master"   # yes, now set up for it
##            #self.offset = 0
##            #globDb.put('toffset',0)                  # save in global database
##            self.level = 0
       # else:                                         # not time master
        
        if  gpslock:                              # if we have locked clock (takes priority)
            self.srclev = 1                       #   follow it
            self.errorn = 1                       
            self.errors = gpserr*2                # take the gps error
            
        elif timeok:                              # if system time defined accurate, use it
            self.srclev = 2
            self.errorn = 1
            self.errors = -self.offset            # go gently to zero
           # self.offset = 0

        if self.errorn > 0:                       # calc error average if data
            error = float(self.errors)/self.errorn
        else: error = 0
        
        self.adjusta = error*0.5                  # take part of the error
        mag = abs(error)
        
##            if (err <= 2) & (self.errorn > 0) & (self.srclev < 9):
##                self.level = self.srclev + 3          # if tracking adopt src+3 level
##            else: self.level = 9                      # otherwise level 9

        if mag < 2:
            self.level = self.srclev + 3          # sync'd with something
            if gpslock:
                self.level = 1                    # have our own clock
            elif timeok:
                self.level = 2                    # local clock defined good
        else:
            self.level = self.srclev + 6          # following but not yet sync'd

        if self.srclev > 5: self.adjusta = 0      # require sync'd source to adjust

        #if self.level > 9: self.level = 9

        if node == string.lower(gd.getv('tmast')):    # if we are master
            if mag < 2:                               # and are sync'd
                self.level = 0                        # proclaim it

        if abs(self.adjusta) > 0.1:
            print "Adjusting Clock %.1f S, src level %d, total offset %.1f S, at %s"%\
                  (self.adjusta,self.level,self.offset+self.adjusta,now())

        self.srclev = 20                              # reset for next search cycle
        
        self.lock.release()                           # release sem
        

    def calib(self,fnod,stml,td):
        "process time info in incoming pkt"
        if fnod == node: return                       # ignore self data
        self.lock.acquire()                           # take semaphore
    #    print "time fm",fnod,"lev",stml,"diff",td
        stml = int(stml)                              # src time level
        if stml < self.srclev:                        # find the best time data
            self.errors,self.errorn = 0,0
            self.srclev = stml
        if stml == self.srclev:                       # average data at same level
            self.errorn += 1
            self.errors += td                         # time difference
        self.lock.release()                           # release sem

    def adjust(self):
        "slew the clock each second as needed (called /sec)"
    
        self.lock.acquire();
        rate = 0.1                                    # delta seconds per second limit
        adj = self.adjusta
        #if abs(adj) < 0.001: return                   # close enough, quit NO, WATCH LOCK

        if adj > rate: adj = rate                     # adjustment rate limit
        elif adj < -rate: adj = -rate
        
        self.offset = float(globDb.get('toffset',0))  # get from global database/cache
        self.offset += adj
        
        if abs(adj) > 0.0005:                         # reduce sqlite writes
            globDb.put('toffset',self.offset)         # save in global database

        self.adjusta -= adj                           # account for slewing progress
        
        self.lock.release();
        
        if abs(adj) > 0.5: print "Slewing clock",adj,"to",self.offset

    def offsetinit(self):
        self.offset = float(globDb.get('toffset',0))  # set up offset
        print "    time offset restored",self.offset

        
    def gpsclockinit(self):
        "find and initialize for gps clock"
    
        try:
            import serial
        except:
            print "warning - serial import failed (only needed for gps clock)"
            return
        print "  Searching for W6AKB GPS USB Clock"
        for i in range(20):
            try:
                clockser = None
                clockser = serial.Serial(port=i,baudrate=9600,timeout=2)
                #print "  found serial",i+1
                for j in range(2):
                    clockser.write("t\n")
                    line = clockser.readline()
                    #print "   ",line
                    p = line.split()
                    if p[0] == 'g' or p[0] == 'u':
                        print "    found the clock on COM%d\n"%(i+1)
                        #print "     ",line
                        self.clockser = clockser
                        return
                clockser.close()
            except:
               # print "  fail",i
                if clockser: clockser.close()
        print
            

    def gpsclock(self):                         # read serial gps clock
        gpslock,gpserr = 0,0
        if self.clockser:                       # read gps clock
            self.clockser.write("m\n")          # warm the link
            self.clockser.readline()
            t = time.time()
            self.clockser.write("t\n")          # get seconds and milliseconds
            l1 = self.clockser.readline()
            t2 = time.time()
            t2 += self.offset                   # get current adjusted time
            p = l1.split()
            if p[0] == 'g' and len(p) == 8:     # if locked
                gpslock = 1
                gt = "%02d%02d%02d %02d%02d%02d GMT"% \
                    ( int(p[1]),int(p[2]),int(p[3]),int(p[4]),int(p[5]),int(p[6]) )
                g = calendar.timegm(time.strptime(gt,"%y%m%d %H%M%S %Z")) + int(p[7])/1000.0
                gpserr = g - t2                  # calc clock error
                if debug: print "  gpsClockDbg %.3f %.3f %.3f"%(g-t2,self.offset,t2-self.offset-t)
                else: print "  gpsClock %.3f %.3f"%(g-t2,self.offset)
        return gpslock,gpserr
    
mclock = clock_class()                          # set up clock class
mclock.gpsclockinit()                           # find gps clock

def exin(op):
    "extract operator or logger initials"
    r = ""
    m = re.match(r'([a-z0-9]{2,3})',op)
    if m:
        r = m.group(1)
    return r

# sqlite database upgrade
#
# use sqlite as the primary journal file database
# do the various important transactions there
# should avoid the locking needed now, the database has the locks
# write it out and then read it back from there
# so the database becomes the central collaboration point
#
# do db in parallel w ascii journal, ascii journal becomes a write only file
#   some folks use this file for other purposes

import sqlite3

class SQDB:
    def __init__(self):
        self.dbPath = logdbf[0:-4] + '.sq3'
        print "Using database",self.dbPath
       
        self.sqdb = sqlite3.connect(self.dbPath)  # connect to the database
        self.sqdb.row_factory = sqlite3.Row   # namedtuple_factory
        self.curs = self.sqdb.cursor()      # make a database connection cursor
        sql = "create table if not exists qjournal(src text,seq int,date text,band text,call text,rept text,powr text,oper text,logr text,primary key (src,seq))"
        self.curs.execute(sql)
        self.sqdb.commit()
        #create table qsos, index by call,band,mode (varies by contest)
        #create table score phone, cw, data
        #create table station, operator, logger, power, 
        #return self
    def readLog(self): # ,srcId,srcIdx):            # returns list of log journal items
        print "Loading log journal from sqlite database"
        sql = "select * from qjournal"
        result = self.curs.execute(sql)
        nl = []
        for r in result:
            #print dir(r)
            nl.append("|".join(('q',r['src'],str(r['seq']),r['date'],r['band'],r['call'],r['rept'],r['powr'],r['oper'],r['logr'],'')))
        #print nl
        return nl
    def next(self):                         # get next item from db in text format
        n = self.result
        nl = "|".join(n.src,n['seq'],n['date'],n['band'],n['call'],n['rept'],n['powr'],n['oper'],n['logr'])
        return nl
    def log(self,n):                        # add item to journal logfile table (and other tables...)
        parms = (n.src,n.seq,n.date,n.band,n.call,n.rept,n.powr,n.oper,n.logr)

        sqdb = sqlite3.connect(self.dbPath)  # connect to the database
#        self.sqdb.row_factory = sqlite3.Row   # namedtuple_factory
        curs = sqdb.cursor()      # make a database connection cursor

        #start commit, begin transaction
        sql = "insert into qjournal (src,seq,date,band,call,rept,powr,oper,logr) values (?,?,?,?,?,?,?,?,?)"
        curs.execute(sql,parms)
        #sql = "insert into qsos values (src,seq,date,band,call,sfx,rept,powr,oper,logr),(?,?,?,?,?,?,?,?,?,?)"
        #self.cur(sql,parms)
        # update qso count, scores? or just use q db count? this doesn't work well for different weights
        # update sequence counts for journals?
        sqdb.commit()                       # do the commit

        if n.band == '*QST': print("QST\a "+n.rept+" -"+n.logr) # emit BEEP sound on QST

                                            # might want to use one fixed database, add a column for the sub-set that we're using
                                            # have a pulldown to select the particular contest/db to use

# interesting idea for future, store sql in the journal...
# probably a subset, but basically ready to execute sql with some encapsulation
# for the arguments
# OR perhaps JSON?

# qso database class

class qsodb:
    byid = {}                   # qso database by src.seq
    bysfx = {}                  # call list by suffix.band
    hiseq = {}                  # high sequence number by node
    lock = threading.RLock()    # sharing lock
    
    def new(self, source):
        n = qsodb()
        n.src = source          # source id
        return n
        
    def tolog(self):            # make log file entry
        sqdb.log(self)          # to database
        self.lock.acquire()     # and to ascii journal file as well
        fd = file(logdbf,"a")
        fd.write("\nq|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % \
            (self.src,self.seq,
             self.date,self.band,self.call,self.rept,
             self.powr,self.oper,self.logr))
        fd.close()
        self.lock.release()

    def ldrec(self,line):       # load log entry fm text
        (typ,self.src,self.seq,
             self.date,self.band,self.call,self.rept,
             self.powr,self.oper,self.logr,eol) = string.split(line,'|')
        self.seq = int(self.seq)
        self.dispatch('logf')

    def loadfile(self):
        print "Loading Log File"
        i,s,log = 0,0,[]
        global sqdb                         # setup sqlite database connection
        sqdb = SQDB()
        log = sqdb.readLog()                # read the database
        
##        try:                              # read from journal file (skipping)
##            fd = file(logdbf,"r")           # initialize databases
##            while 1:
##                ln = fd.readline()          # read a line and put in list
##                if not ln: break
##                log.append(ln)
##            fd.close()
##        except IOError,e:
##            s += 1

        #log.sort()                          # process in time order xx??
        
        for ln in log:
            if ln[0] == 'q':                # qso db line
                r = qdb.new(0)
                try:
                    r.ldrec(ln)
                    i += 1
                except ValueError,e:
                    print "  error, item skipped: ",e
                    print "    in:",ln
                    s += 1
##                sqdb.log(r)               # push a copy from the file into the database (temporary for transition)
        if i == 0 and s == 1:
            print "  Log file not found, must be new"
        else:
            print "  ",i,"Records Loaded,",s,"Errors"

    def cleanlog(self):
        "return clean filtered dictionaries of the log"
        d,c,g = {},{},{}
        fdstart,fdend = gd.getv('fdstrt'),gd.getv('fdend')
        self.lock.acquire()
        for i in self.byid.values():        # copy, index by node, sequence
            k = "%s|%s"%(i.src,i.seq)
            d[k] = i
        self.lock.release()
        for i in d.keys():                  # process deletes
            if d.has_key(i):
                iv = d[i]
                if iv.rept[:5] == "*del:":
                    j,st,sn,r = iv.rept.split(':')   # extract deleted id
                    k = "%s|%s"%(st,sn)
                    if k in d.keys():
##                        print iv.rept,; iv.pr()
                        del(d[k])               # delete it
##                    else: print "del target missing",iv.rept
                    del(d[i])
        for i in d.keys():                  # filter time window
            iv = d[i]
            if iv.date < fdstart or iv.date > fdend:
##                print "discarding out of date range",iv.date,iv.src,iv.seq
                del(d[i])
        for i in d.values():                # re-index by call-band
            s,t,p,x,call,x,r = self.qparse(i.call)    # extract call (not /...)
            k = "%s-%s"%(call,i.band)
                                            # filter out noncontest entries
            if ival(i.powr) == 0 and i.band[0] != '*': continue
            if i.band == 'off': continue
            if i.band[0] == '*': continue   # rm special msgs
            if i.src == 'gota': g[k] = i    # gota is separate dup space
            else: c[k] = i
        return (d,c,g)                      # Deletes processed, fully Cleaned
                                            # by id, call-bnd, gota by call-bnd

    def prlogln(s):
        "convert log item to print format"
        # note that edit and color read data from the editor so
        # changing columns matters to these other functions.
        if s.band == '*QST':
            ln = "%8s %5s %-41s %-3s %-3s %4s %s"%\
                (s.date[4:11],s.band,s.rept[:41],s.oper,s.logr,s.seq,s.src)
        elif s.band == '*set':
            ln = "%8s %5s %-11s %-29s %-3s %-3s %4s %s"%\
                (s.date[4:11],s.band,s.call[:10],s.rept[:29],\
                 s.oper,s.logr,s.seq,s.src)
        elif s.rept[:5] == '*del:':
            ln = "%8s %5s %-7s %-33s %-3s %-3s %4s %s"%\
                (s.date[4:11],s.band,s.call[:7],s.rept[:33],\
                 s.oper,s.logr,s.seq,s.src)
        else:
            ln = "%8s %5s %-11s %-24s %4s %-3s %-3s %4s %s"%\
                (s.date[4:11],s.band,s.call[:11],s.rept[:24],\
                 s.powr,s.oper,s.logr,s.seq,s.src)
        return ln

    def prlog(self):
        "print log in time order"
        l = self.filterlog("")
        for i in l:
            print i

# adif specs for eqsl.org   http://www.eqsl.cc/qslcard/adifcontentspecs.cfm ver 2.27
#
# problems - adif digital modes and satellite modes don't fit the fd model
#   even voice.. need 'real' mode field. pulldown menu.
#     add outgoing report to comments in parens
#
# <QSO_DATE:8> YYYYMMDD
# <TIME_ON:4> HHMM only HH and MM are used
# <CALL:6> up to 13 chars
# <BAND:3>
# <MODE:3>
# <SAT_MODE:>
# <LOG_PGM:15>FDLog by WB6ZQZ
# <COMMENT:> up to 240 chars
# <EOR>
#
# .ADI extension

    def pradif(self):
        "print clean log in adif format"
        pgm = "FDLog by W6AKB (formerly WB6ZQZ) (www.fdlog.info)"
        print "<PROGRAMID:%d>%s"%(len(pgm),pgm)
        m,n,g = self.cleanlog()
        for i in n.values() + g.values():
            dat = "20%s"%i.date[0:6]
            tim = i.date[7:11]
            cal = i.call
            bnd = "%sm"%i.band[:-1]
            mod = i.band[-1:]
            if mod == 'p': mod = 'SSB'
            elif mod == 'c': mod = 'CW'
            elif mod == 'd': mod = 'RTTY'
            com = i.rept
            print "<QSO_DATE:8>%s"%(dat)
            print "<TIME_ON:4>%s"%(tim)
            print "<CALL:%d>%s"%(len(cal),cal)
            print "<BAND:%d>%s"%(len(bnd),bnd)
            print "<MODE:%d>%s"%(len(mod),mod)
            print "<QSLMSG:%d>%s"%(len(com),com)
            print "<EOR>"
            print

# vhf contest cabrillo qso output
#
#QSO: freq  mo date       time call              grid   call              grid 
#QSO: ***** ** yyyy-mm-dd nnnn *************     ****** *************     ******

    def vhf_cabrillo(self):
        "output VHF contest cabrillo QSO data"
        band_map = {'6':'50','2':'144','220':'222','440':'432','900':'902','1200':'1.2G'}
        m,n,g = self.cleanlog()
        mycall = string.upper(gd.getv('fdcall'))
        mygrid = gd.getv('grid')
        l = []
        print "QSO: freq  mo date       time call              grid   call              grid "
        for i in n.values(): # + g.values(): no gota in vhf
            freq = "%s"%i.band[:-1]                     #band
            if freq in band_map: freq = band_map[freq]
            mod = i.band[-1:]                           #mode
            if mod == "c": mod = "CW"
            if mod == "p": mod = "PH"
            if mod == "d": mod = "RY"
            date = "20%2s-%2s-%2s"%(i.date[0:2],i.date[2:4],i.date[4:6])
            tim = i.date[7:11]
            call = i.call
            grid = ''
            if '/' in call:  # split off grid from call
                call,grid = call.split('/')
            l.append("%sQSO: %-5s %-2s %-10s %4s %-13s     %-6s %-13s     %-6s"%(i.date,freq,mod,date,tim,mycall,mygrid,call,grid))
        l.sort()                    # sort data with prepended date.time
        for i in l: print i[13:]    # rm sort key date.time

    def filterlog(self,filt):
        "list filtered (by bandm) log in time order, nondup valid q's only"
        l = []
        m,n,g = self.cleanlog()
        for i in n.values() + g.values():
            if filt == "" or re.match('%s$'%filt,i.band):
                l.append(i.prlogln())
        l.sort()
        return l

    def filterlog2(self,filt):
        "list filtered (by bandm) log in time order, including special msgs"
        l = []
        m,n,g = self.cleanlog()
        for i in m.values():
            if filt == "" or re.match('%s$'%filt,i.band):
                l.append(i.prlogln())
        l.sort()
        return l

    def filterlogst(self,filt):
        "list filtered (by nod) log in time order, including special msgs"
        l = []
        m,n,g = self.cleanlog()
        for i in m.values():
            if re.match('%s$'%filt,i.src):
                l.append(i.prlogln())
        l.sort()
        return l

    def qsl(self,time,call,bandmod,report):
        "log a qsl"
        return self.postnewinfo(time,call,bandmod,report)

    def qst(self,msg):
        "put a qst in database + log"
        return self.postnewinfo(now(),'','*QST',msg)

    def globalshare(self,name,value):
        "put global var set in db + log"
        return self.postnewinfo(now(),name,'*set',value)

    def postnewinfo(self,time,call,bandmod,report):
        "post new locally generated info"
        #s = self.new(node)
##        s.date,s.call,s.band,s.rept,s.oper,s.logr,s.powr = \
##            time,call,bandmod,report,exin(operator),exin(logger),power
        #s.seq = -1
        return self.postnew(time,call,bandmod,report,exin(operator),\
                            exin(logger),power)

    def postnew(self,time,call,bandmod,report,oper,logr,powr):
        "post new locally generated info"
        s = self.new(node)
        s.date,s.call,s.band,s.rept,s.oper,s.logr,s.powr = \
            time,call,bandmod,report,oper,logr,powr
        s.seq = -1
        return s.dispatch('user')

    def delete(self,nod,seq,reason):
        "rm a Q by creating a delete record"
##        print "del",nod,seq
        a,b,c = self.cleanlog()
        k = "%s|%s"%(nod,seq)
        if a.has_key(k) and a[k].band[0] != '*':        # only visible q
            tm,call,bandmod = a[k].date,a[k].call,a[k].band
            rept = "*del:%s:%s:%s"%(nod,seq,reason)
            s = self.new(node)
            s.date,s.call,s.band,s.rept,s.oper,s.logr,s.powr = \
               now(),call,bandmod,rept,exin(operator),exin(logger),0
            s.seq = -1
            s.dispatch('user')
            text.insert(END," DELETE Successful %s %s %s\n"%(tm,call,bandmod))
        else:
            text.insert(END," DELETE Ignored [%s,%s] Not Found\n"%\
                        (nod,seq))

    def todb(self):
        "Q record object to db"
        r = None
        self.lock.acquire()
        current = self.hiseq.get(self.src,0)
        self.seq = int(self.seq)
        if self.seq == current+1:       # filter out dup or nonsequential
            self.byid["%s.%s"%(self.src,self.seq)] = self
            self.hiseq[self.src] = current+1
##            if debug: print "todb:",self.src,self.seq
            r = self
        elif self.seq == current:
            if debug: print "dup sequence log entry ignored"
        else:
            print "out of sequence log entry ignored", self.seq,current+1
        self.lock.release()
        return r
       
    def pr(self):
        "print Q record object"
        sms.prmsg(self.prlogln())

    def dispatch(self,src):
        "process new db rec (fm logf,user,net) to where it goes"
        self.lock.acquire()
        self.seq = int(self.seq)
        if self.seq == -1:                              # assign new seq num
            self.seq = self.hiseq.get(self.src,0) + 1
        r = self.todb()
        self.lock.release()
        if  r:                                          # if new
            self.pr()
            if src != 'logf': self.tolog()
            if src == 'user': net.bc_qsomsg(self.src,self.seq)
            if self.band == '*set':
                m = gd.setv(r.call,r.rept,r.date)
                if not m: r = None
            else:
                self.logdup()
        return r

    def bandrpt(self):
        "band report q/band pwr/band, q/oper q/logr q/station"
        qpb,ppb,qpop,qplg,qpst,tq,score,maxp = {},{},{},{},{},0,0,0
        cwq,digq,fonq = 0,0,0
        qpgop,gotaq,nat,sat = {},0,[],[]
        
        x,c,g = self.cleanlog()
        
        for i in c.values()+g.values():

            if re.search('sat',i.band): sat.append(i)
            if 'n' in i.powr: nat.append(i)
            
# stop ignoring above 100 q's per oper per new gota rules. 6/05 akb
# GOTA q's stop counting over 400 (500 in 2009)
            if i.src == 'gota':                     # analyze gota limits
                qpgop[i.oper] = qpgop.get(i.oper,0)+1
                qpop[i.oper] = qpop.get(i.oper,0)+1
                qplg[i.logr] = qplg.get(i.logr,0)+1
                qpst[i.src]  = qpst.get(i.src,0) +1
                if gotaq >= 500: continue           # stop over 500 total
                gotaq += 1
                tq += 1
                score += 1
                if 'c' in i.band:
                    cwq   += 1
                    score += 1
                    qpb['gotac'] = qpb.get('gotac',0)+1
                    ppb['gotac'] = max(ppb.get('gotac',0),ival(i.powr))
                if 'd' in i.band:
                    digq  += 1
                    score += 1
                    qpb['gotad'] = qpb.get('gotad',0)+1
                    ppb['gotad'] = max(ppb.get('gotad',0),ival(i.powr))
                if 'p' in i.band:
                    fonq  += 1
                    qpb['gotap'] = qpb.get('gotap',0)+1
                    ppb['gotap'] = max(ppb.get('gotap',0),ival(i.powr))
                continue
                
            qpb[i.band] = qpb.get(i.band,0)+1
            ppb[i.band] = max(ppb.get(i.band,0),ival(i.powr))
            maxp = max(maxp,ival(i.powr))
            qpop[i.oper] = qpop.get(i.oper,0)+1
            qplg[i.logr] = qplg.get(i.logr,0)+1
            qpst[i.src]  = qpst.get(i.src,0) +1
            score += 1; tq += 1
            if 'c' in i.band:
                score += 1    # extra cw and dig points
                cwq   += 1
            if 'd' in i.band:
                score += 1
                digq  += 1
            if 'p' in i.band:
                fonq  += 1
        
        return (qpb,ppb,qpop,qplg,qpst,tq,score,maxp,cwq,digq,fonq,qpgop,gotaq,nat,sat)

    def bands(self):      # .ba command band status station on, q/band, xx needs upgd
        qpb,tmlq,nod = {},{},{}
        self.lock.acquire()
        for i in self.byid.values():
            if ival(i.powr) < 1: continue
            if i.band == 'off': continue
            v = 1
            if i.rept[:5] == '*del:': v = -1
            qpb[i.band] = qpb.get(i.band,0)+v               # num q's
            tmlq[i.band] = max(tmlq.get(i.band,''),i.date)  # time of last (latest) q
        self.lock.release()

        print
        print "Stations this node is hearing:"
        # scan for stations on bands
        for s in net.si.nodes.values():   #xx
##            print dir(s)
            print s.nod,s.host,s.ip,s.stm
##            nod[s.bnd] = s.nod_on_band()
##            print "%8s %4s %18s %s"%(s.nod,s.bnd,s.msc,s.stm)
            #s.stm,s.nod,seq,s.bnd,s.msc
            #i.tm,i.fnod,i.fip,i.stm,i.nod,i.seq,i.bnd,i.msc

        d = {}
        print
        print "Node Info"
        print "--node-- band --opr lgr pwr----- last"
        for t in net.si.nodinfo.values():
            x1,x2,age = d.get(t.nod,('','',9999))
            if age > t.age: d[t.nod] = (t.bnd,t.msc,t.age)
        for t in d:
            print "%8s %4s %-18s %4s"%(t,d[t][0],d[t][1],d[t][2]) #t.bnd,t.msc,t.age)

        print
        print "  band -------- cw ----- ------- dig ----- ------- fon -----"
        print "          nod  Q's  tslq    nod  Q's  tslq    nod  Q's  tslq"
        #      xxxxxx yyyyyy xxxx xxxxx yyyyyy xxxx xxxxx yyyyyy xxxx xxxxx

        t1 = now()
        for b in (160,80,40,20,15,10,6,2,220,440,900,1200,'Sat'):
            print "%6s"%b,
            for m in 'cdp':
                bm = "%s%s"%(b,m)
                # be nice to do min since q instead of time of last q DONE
                t2 = tmlq.get(bm,'')                # time since last Q minutes
                if t2 == '':
                    tdif = ''
                else:
                    tdif = int(tmsub(t1,t2)/60.)
                    tmin = tdif%60
                    tdhr = tdif/60
                    if tdhr > 99: tdhr = 99
                    tdif = tdhr*100 + tmin
               #     if tdif > 9999: tdif = 9999
               #     tdif = str(int(tdif))           # be nice to make this hhmm instead of mmmm
                
##                t = ""                            # time of latest Q hhmm
##                m = re.search(r"([0-9]{4})[0-9]{2}$",tmlq.get(bm,''))
##                if m: t = m.group(1)
                nob = net.si.nod_on_band(bm) # node now on band
                if len(nob) == 0: nob = ''   # list take first item if any
                else: nob = nob[0]
                print "%6s %4s %5s"%\
                      (nob[0:6],qpb.get(bm,''),tdif),  # was t
##                      (nod.get(bm,'')[0:5],qpb.get(bm,''),t),
            print

    def sfx2call(self, suffix, band):
        "return calls w suffix on this band"
        return self.bysfx.get(suffix+'.'+band,[])

    def qparse(self, line):
        "qso/call/partial parser"
        # check for valid input at each keystroke
        # return status, time, extended call, base call, suffix, report
        # stat: 0 invalid, 1 partial, 2 suffix, 3 prefix, 4 call, 5 full qso
        # example --> :12.3456 wb4ghj/ve7 2a sf Steve in CAN
        stat,tm,pfx,sfx,call,xcall,rept = 0,'','','','','',''

        # break into basic parts: time, call, report
        m = re.match(r'(:([0-9.]*)( )?)?(([a-z0-9/]+)( )?)?([0-9a-zA-Z ]*)$',line)
        if m:
            tm = m.group(2)
            xcall = m.group(5)
            rept = m.group(7)
            stat = 0
            if m.group(1) > '' or xcall > '': stat = 1
##            print; print "tm [%s] xcall [%s] rept [%s]"%(tm,xcall,rept)
            if tm > '':
                stat = 0
                m = re.match(r'([0-3]([0-9]([.]([0-5]([0-9]([0-5]([0-9])?)?)?)?)?)?)?$',tm)
                if m:
                    stat = 1        # at least partial time
            if xcall > '':
                stat = 0            # invalid unless something matches
                m = re.match(r'([a-z]+)$',xcall)
                if m:
                    stat = 2        # suffix
                    sfx = xcall
                
                m = re.match(r'([0-9]+)$',xcall)
                if m:
                    stat = 2        # suffix
                    sfx = xcall
                m = re.match(r'([a-z]+[0-9]+)$',xcall)
                if m:
                    stat = 3        # prefix
                    pfx = xcall
                m = re.match(r'([0-9]+[a-z]+)$',xcall)
                if m:
                    stat = 3        # prefix
                    pfx = xcall
                m = re.match(r'(([a-z]+[0-9]+)([a-z]+))(/[0-9a-z]*)?$',xcall)
                if m:
                    stat = 4        # whole call
                    call = m.group(1)
                    pfx = m.group(2)
                    sfx = m.group(3)
                m = re.match(r'(([0-9]+[a-z]+)([0-9]+))(/[0-9a-z]*)?$',xcall)
                if m:
                    stat = 4        # whole call
                    call = m.group(1)
                    pfx = m.group(2)
                    sfx = m.group(3)
                if (stat == 4) & (rept > ''):
                    stat = 0
                    m = re.match(r'[0-9a-zA-Z]+[0-9a-zA-Z ]*$',rept)
                    if m:
                        stat = 5    # complete qso

                if len(xcall) > 12: stat = 0    # limit lengths
                if len(pfx) > 5: stat = 0
                if len(sfx) > 3: stat = 0
                
                if tm:              # if forced time exists
                    if len(tm)<7:   # it must be complete
                        stat = 0
                    
##        print "stat[%s] time[%s] pfx[%s] sfx[%s] call[%s] xcall[%s] rpt[%s]"%\
##              (stat,tm,pfx,sfx,call,xcall,rept)
                        
        return (stat,tm,pfx,sfx,call,xcall,rept)

    def dupck(self, wcall, band):
        "check for duplicate call on this band"
        stat,tm,pfx,sfx,call,xcall,rept = self.qparse(wcall)
        if gd.getv('contst').upper() == "VHF":
            return xcall in self.sfx2call(sfx, band) # vhf contest
        return call in self.sfx2call(sfx, band) # field day

    def logdup(self):
        "enter into dup log"
        stat,tm,pfx,sfx,call,xcall,rept = self.qparse(self.call)
##        print call,sfx,self.band
        key = sfx + '.' + self.band
        self.lock.acquire()
        if self.rept[:5] == "*del:":
            self.redup()
##            print "proc del",self.rept,self.call,self.band
##            try:
##                self.bysfx[key].remove(call)
##            except:
##                pass
##                print " rm fm dupdb failed -%s-%s-%s-"%(call,sfx,band)
        else:
            # duplog everything with nonzero power, or on band off (test)
            if (self.band == 'off')|(ival(self.powr) > 0):
                # dup only if Q and node type match (gota/not)
                if (node == 'gota') == (self.src == 'gota'):
                    if self.bysfx.has_key(key):     # add to suffix db
                        self.bysfx[key].append(xcall)
                    else:
                        self.bysfx[key] = [xcall]
##                else: print "node type mismatch",node,self.src
        self.lock.release()

    def redup(self):
        "rebuild dup db"
        d,c,g = self.cleanlog()
        self.lock.acquire()
#        print self.bysfx
        qsodb.bysfx = {}
        for i in c.values()+g.values():
#            print i.call,i.band
            i.logdup()
        self.lock.release()
#        print qsodb.bysfx

    def wasrpt(self):
        "worked all states report"
        sectost,stcnt,r,e = {},{},[],[]
        
        try:
            fd = file("arrl_sect.dat","r")  # read section data
            while 1:
                ln = fd.readline()          # read a line and put in db
                if not ln: break
                #if ln == "": continue
                if ln[0] == '#': continue  
                try:
                    sec,st,canum,desc = string.split(ln,None,3)
                    sectost[sec] = st
                    stcnt[st] = 0
##                    print sec,st,desc
                except ValueError,e:
                    print "rd arrl sec dat err, itm skpd: ",e
            fd.close()
        except IOError,e:
            print "io error during arrl section data file load", e

        a,b,c = self.cleanlog()
        for i in a.values():
            sect,state = "",""
            if i.rept[:1] == '*': continue
            if i.band[0] == '*': continue
            if i.band == 'off': continue
            if i.powr == '0': continue
            m = re.match(r' *[0-9]+[a-fA-F] +([A-Za-z]{2,4})',i.rept)
            if m:
                sect = m.group(1)
                sect = string.upper(sect)
                state = sectost.get(sect,"")
#                print "sec",sect,"state",state
                if state: stcnt[state] += 1
            if not state:
##                print "section not recognized in:\n  %s"%i.prlogln()
##                print "sec",sect,"state",state
                e.append(i.prlogln())

        h,n = [],[]                         # make have and need lists
        for i in stcnt.keys():
            if i != "--":
                if stcnt[i] == 0: n.append("%s"%i)
                else: h.append("%s"%i)
        n.sort()
        r.append("Worked All States Report\n%s Warning(s) Below\nNeed %s States:"%(len(e),len(n)))
        for i in n:
            r.append(i)
        h.sort()
        r.append("\nHave %s States:"%len(h))
        for i in h:
            r.append("%s %s"%(i,stcnt[i]))
        if len(e) > 0:
            r.append("\nWarnings - Cannot Discern US Section in Q(s):\n")
            for i in e:
                r.append(i)
        return r

# problem with sqlite
# cannot use sqlite object created in a different thread

# threads and networking section

class node_info:
    nodes = {}
    nodinfo = {}
##    rembcast = {}
    lock = threading.RLock()                    # reentrant sharing lock

    def sqd(self,src,seq,t,b,c,rp,p,o,l):
        "process qso data fm net into db"       # excessive cohesion?
        s = qdb.new(src)
        s.seq,s.date,s.call,s.band,s.rept,s.oper,s.logr,s.powr = \
               seq,t,c,b,rp,o,l,p
        s.dispatch('net')

    def netnum(self,ip,mask):
        "extract net number"
        i,m,r = [],[],{}
        i = string.split(ip,'.')
        m = string.split(mask,'.')
        for n in (0,1,2,3):
            r[n] = ival(i[n]) & ival(m[n])
        return "%s.%s.%s.%s"%(r[0],r[1],r[2],r[3])

    def ssb(self,pkt_tm,host,sip,nod,stm,stml,ver,td):
        "process status broadcast (first line)"
        self.lock.acquire()
        if not self.nodes.has_key(nod):      # create if new
            self.nodes[nod] = node_info()
            if nod != node:
                print "New Node Heard",host,sip,nod,stm,stml,ver,td
        i = self.nodes[nod]
##        if debug: print "ssb before assign",i.nod,i.stm,i.bnd
        i.ptm,i.nod,i.host,i.ip,i.stm,i.age = \
                pkt_tm,nod,host,sip,stm,0
        self.lock.release()
     #   if debug:
      #  print "ssb:",pkt_tm,host,sip,nod,stm,stml,ver,td

    def sss(self,pkt_tm,fnod,sip,nod,seq,bnd,msc,age):
        "process node status bcast (rest of bcast lines)"
        self.lock.acquire()
        key = "%s-%s"%(fnod,nod)
        if not self.nodinfo.has_key(key):
            self.nodinfo[key] = node_info()  # create new
##            if debug: print "sss: new nodinfo instance",key
        i = self.nodinfo[key]
        i.tm,i.fnod,i.fip,i.nod,i.seq,i.bnd,i.msc,i.age = \
              pkt_tm,fnod,sip,nod,seq,bnd,msc,int(age)
        self.lock.release()
##        if debug:
      #  print "sss:",i.age,i.nod,i.seq,i.bnd

    def age_data(self):
        "increment age and delete old band"
        t = now()[7:] # time hhmmss
        self.lock.acquire()
        for i in self.nodinfo.values():
            if i.age < 999: i.age += 1
##            if debug: print "ageing nodinfo",i.fnod,i.nod,i.bnd,i.age
            if i.age > 55 and i.bnd:
                print t,"age out info from",i.fnod,"about",i.nod,"on",i.bnd,"age",i.age
                i.bnd = ""
        for i in self.nodes.values():
            if i.age < 999: i.age += 1
        self.lock.release()

    def fill_requests_list(self):
        "return list of fills needed"
        r = []
        self.lock.acquire()
        for i in self.nodinfo.values():     # for each node
            j = qdb.hiseq.get(i.nod,0)
            if int(i.seq) > j:              # if they have something we need
                r.append((i.fip,i.nod,j+1)) # add req for next to list
##                if debug: print "req fm",i.fip,"for",i.nod,i.seq,"have",j+1
        self.lock.release()
        return r                            # list of (addr,src,seq)

    def node_status_list(self):
        "return list of node status tuples"
        sum = {}                            # summary dictionary
        self.lock.acquire()
        i = node_info()                  # update our info
        i.nod,i.bnd,i.age = node,band,0
        i.msc = "%s %s %sW" % (exin(operator), exin(logger), power)
        sum[node] = i

        for i in qdb.hiseq.keys():          # insure all db nod on list
            if not sum.has_key(i):          # add iff new
                j = node_info()
                j.nod, j.bnd, j.msc, j.age = i, '', '', 999
                sum[i] = j
##                if debug: print "adding nod fm db to list",i
            
        for i in self.nodinfo.values():     # browse bcast data
            if not sum.has_key(i.nod):
                j = node_info()
                j.nod, j.bnd, j.msc, j.age = i.nod, '', '', 999
                sum[i.nod] = j
            j = sum[i.nod]                  # collect into summary
##            if debug:
##                print "have",      j.nod,j.age,j.bnd,j.msc
##                print "inspecting",i.nod,i.age,i.bnd,i.msc
            if i.age < j.age:              # keep latest wrt src time
##                if debug:
##                    print "updating",j.nod,j.age,j.bnd,j.msc,\
##                                "to",      i.age,i.bnd,i.msc
                j.bnd,j.msc,j.age = i.bnd,i.msc,i.age
        self.lock.release()

        r = []                              # form the list (xx return sum?)
        for s in sum.values():
            seq = qdb.hiseq.get(s.nod,0)    # reflect what we have in our db
            if seq or s.bnd:                # only report interesting info
                r.append((s.nod,seq,s.bnd,s.msc,s.age))
        return r                            # list of (nod,seq,bnd,msc,age)

    def nod_on_band(self,band):
        "return list of nodes on this band"
        r = []
        for s in self.node_status_list():
##            print s[0],s[2]                 # (nod,seq,bnd,msc,age)
            if band == s[2]:
                r.append(s[0])
        return r

    def nod_on_bands(self):
        "return dictionary of list of nodes indexed by band and counts"
        r,hf,vhf,gota = {},0,0,0
        for s in self.node_status_list():
##            print s[0],s[2]
            if not r.has_key(s[2]):
                r[s[2]] = []
            r[s[2]].append(s[0])
            if s[2] == 'off' or s[2] == "": continue
            if s[0] == 'gota': gota += 1
            else:
                b = ival(s[2])
                if b > 8 and b < 200: hf  += 1
                if b < 8 or  b > 200: vhf += 1

        return r,hf,vhf,gota

# new message class
# needed for filler to work with tcp

class MESSAGE:
    def __init__(self,host,port,mode,mesg):
        "construct a message"
        self.time = now()               # arrival/creation time
        self.host = host                # remote host dotted ip text
        self.port = port                # remote port text
        self.mode = mode                # tcp or udp or bcast text
        self.mesg = mesg                # message content text
        self.authok = self.ckauth(mesg) # authorization check boolean
        
        if mode == 'udp': self.adr_str = host
        else:             self.adr_str = "%s:%s"%(host,port)
        
        # might want a processing status indicating where the meesage came from, what has been
        # done to it, what needs to be done; has it been broadcast, has it been logged to the journal,
        # etc.
        
    def reply(self,reply_mesg):
        "construct a reply message"
        reply = MESSAGE(self.host,self.port,self.mode,reply_mesg)
        return reply
    def send(self):
        net.send_msg(self)
    def bcast(self):
        self.mode = 'bcast'
        self.send()

# copied the auth methods here, probably will move them
# or set up a relationship between message and network classes
##    def setauth(self,newauth):
##        "set authentication key code base, copy on use"
##        global authk
##        authk = newauth
##        seed = "2004070511111akb"               # change when protocol changes
##        self.authkey = hashlib.md5(newauth+seed)
        
    def auth(self,msg):
        "calc authentication hash"
        h = net.authkey.copy()
        h.update(msg)
        return h.hexdigest()
    
    def ckauth(self,msg):
        "check authentication hash"
        h,m = msg.split('\n',1)
##        print h; print self.auth(m); print
        return h == self.auth(m)

class netsync:
    "network database synchronization"

    netmask = '255.255.255.0'
    
    authkey = hashlib.md5()
    pkts_rcvd,fills,badauth_rcvd,send_errs = 0,0,0,0
    hostname = socket.gethostname()
    my_addr = socket.gethostbyname(hostname)                # fails on some systems
    # linux fix below taken from Scott Hibbs' version from https://github.com/scotthibbs/FDLog_Enhanced
    if my_addr[:3] == '127':   
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
            my_addr = IP    
            print "\n Linux Loopback fix worked ip is:  %s\n" % my_addr
            bc_addr = re.sub(r'[0-9]+$', '255', my_addr)  # calc bcast addr
    # moved this under the linux fix in case our linux is on 10. network - Scott Hibbs Apr/9/2017
    elif my_addr[:3] == '10.':
        bc_addr = '10.255.255.255'
        netmask = '255.0.0.0'
    # proposed fix for 172 networks that need 255.255.0.0 netmask
    # This is untested - Scott Hibbs KD4SIR Apr/9/2017
    elif my_addr[:3] == '172':
        bc_addr = re.sub(r'[0-9]+$', '255', my_addr)  # calc bcast addr
        netmask = '255.255.0.0'
    else:
        bc_addr = re.sub(r'[0-9]+$', '255', my_addr) # calc bcast addr
    
    udp_skt = None
    pkts_prev = 0
    si = node_info()                                        # create node info object

    # new tcp/udp code section
    #
    # tcp penetrates home routers more conveniently
    # so handle remote stations with tcp
    # server listens for any connections, logs them,
    # deletes on error
    # this will retire some of the old code when placed in service
    # reorganizes the flow of data from network sockets of both types
    # refactored old code

    rem_host = "0.0.0.0"                                    # remote tcp address
   # rem_host = "192.168.1.107"                              # test
    
    #rem_cli = 0                                             # tcp client enable flag
    #rem_srv = 0                                             # tcp server enable flag

    tcp_conn = {} # tcp connection dictionary, index by socket_str, store (socket,(host,port))

    def socket_str(self,addr):
        "convert address tuple to string"
        # use this for tcp addresses, if no :port then must be udp
        host,port = addr
        str_addr = '%s:%s'%(host,port)
    
    def tcp_manager(self):
        "tcp service manager thread"
        # this thread should just accept connections and make threads to respond
        self.tcp_thread = {}  # service threads
        time.sleep(1)
        print "starting TCP service manager on",self.my_addr
        while 1:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.bind(("", tcp_port))
            s.listen(1)
            while 1: # incoming tcp connection, launch a handler
                c = s.accept()   # returns socket object and (host,port) tuple
                sock,addr = c
                addr_str = "%s:%d"%addr #self.socket_str(addr)
                self.tcp_conn[addr_str] = c         # store socket and addr tuple
                print "launching TCP service thread",addr_str
                th = threading.Thread(target=self.tcp_server,args=(addr_str,))
                th.start()
                self.tcp_thread[addr_str] = th
            s.close()
            time.sleep(13)
            print "remote TCP service manager restarting"
    
    def tcp_server(self,addr_str):
        "receive tcp stream and process them for one client"
        print "TCP service thread starting on",addr_str
        skt,addr = self.tcp_conn[addr_str]          # get connection socket
        while 1:
            if not self.rcv_tcp(addr_str): break    # quit on error
        del(self.tcp_conn[addr_str])                # socket deleted fm table
        skt.close()                                 # cleanup lost connection
        print "TCP server quitting"
    
    def tcp_client(self):
        "launch client thread and connect to remote TCP server"
        # only one of these, only one remote connection with client
        # this thread which keeps connecting
        # until the remote client mode is disabled
        time.sleep(3)
        while 1:
            rem_host = self.rem_host
            if rem_host == '0.0.0.0':
                time.sleep(11)
                continue
            rem_adr = (rem_host,tcp_port)
            adr_str = "%s:%s"%rem_adr
            print "TCP client connecting to",rem_adr
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.bind(('',self.port+1))
            try:
                s.connect(rem_adr)
                print "TCP client connected to",rem_adr
                self.tcp_conn[adr_str] = s,(rem_adr)        # add to connection list
                print len(self.tcp_conn),"tcp connections"
                while rem_host == self.rem_host:
                    if not self.rcv_tcp(adr_str):           # receive and process messages
                        break
            except:
                print "TCP client exception to",rem_host
                #raise  # normally this is commented out but can be useful for test
            try: del(self.tcp_conn[adr_str])                # indicate connection disabled
            except: pass
            s.close()
            time.sleep(19)                                  # retry interval
        print "tcp_client quitting"

    
    def rcv_tcp(self,adr_str):
        "receive and process one TCP message"
        s,adr = self.tcp_conn.get(adr_str,None)
        mode,msg,hdr = "tcp","",""
       # print "rcv_tcp",adr_str
        if s == None:
            print "rcv_tcp on bad socket"
            return False
        try:
            while len(hdr) < 3:                             # get header
                hdr += s.recv(3-len(hdr))
            if ord(hdr[0]) ^ ord(hdr[1]) != ord(hdr[2]):
                print "rcv_tcp bad header", ord(hdr[0]),ord(hdr[1]),ord(hdr[2])
                return False
            len_read = ord(hdr[0]) + 256*ord(hdr[1])
            if debug: print "rcv_tcp length",len_read
            if len_read > 8200:
                print "rcv_tcp msg too long",len_read
                return False
            while len(msg) < len_read:
                msg += s.recv(len_read-len(msg))            # read exact until have it all
            if debug: print "rcv_tcp msg",adr_str #,msg
           # print msg
        except:
            print "rcv_tcp exception",adr_str,msg
            #raise
            return False
        self.pkts_rcvd += 1
        host,port = adr
        message = MESSAGE(host,port,mode,msg)
        return self.proc_message(message)                   # process if valid

    def rcv_udp(self):
        "receive and process UDP messages"
        # replaces old rcvr thread below
        # need to start this before sending UDP messages
        if debug: print "UDP receiver thread starting"
        r = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        r.bind(('',self.port))
        mode = 'udp'
        while 1:
            # need to handle errors and clean shutdown of ports during exit
            # perhaps terminating the threads will be sufficient if the
            # connections are not cached, have to test it
            # hard to force shutdown since threads are blocked
            # no easy way to terminate threads either
            # so try closing sockets even though threads are waiting
            msg,addr = r.recvfrom(800)                      # get a message
            host,port = addr
            if host != self.my_addr: self.pkts_rcvd += 1    # count other machine pkts
            message = MESSAGE(host,port,mode,msg)
            self.proc_message(message)

    def proc_message(self,message):
        "process received message object"
        pkt_tm = message.time                                   # time of receipt
        msg = message.mesg
        addr = message.adr_str
        host,sip,fnod,stm = '','','',''
        if debug: print "proc_message: %s  %s\n"%(addr,msg)
        if not self.ckauth(msg):                                # authenticate packet
            #if debug: sms.prmsg("bad auth from: %s"%addr)
            print "bad auth from:",addr
            self.badauth_rcvd += 1
            return False
        lines = msg.split('\n')                                 # decode lines
        for line in lines[1:-1]:                                # skip auth hash, blank at end
##            if debug: sms.prmsg(line)
            fields = line.split('|')
            # if message came from tcp the sip (src ip) needs to have port added
            # but this has to be done for each message type
            # in the appropriate place. WRONG, need to pick up
            # real from address and ignore the one in the packet!
            
            if fields[0] == 'b':                                # status bcast
                host,sip,fnod,stm,stml,ver = fields[1:]
                # hostname, source ip, from node, source time, source time level, version
                
##                if message.mode == 'tcp':                       # fix tcp src ip
##                    sip += ":"+str(message.port)
                    #print "tcp sip",sip
               # else:
                    #print "udp sip",sip
##                print
##                print "processing broadcast"
##                print "addr",addr
##                print "sip",sip
##                print
                sip = addr # the real deal
                td = tmsub(stm,pkt_tm)                          # time subtract for error
                self.si.ssb(pkt_tm,host,sip,fnod,stm,stml,ver,td)
                mclock.calib(fnod,stml,td)                      # clock calibration
                if abs(td) >= tdwin:
                    print 'clock err',td,host,sip,fnod,pkt_tm
                if showbc:
                    print "bcast",host,sip,fnod,ver,pkt_tm,td
            elif fields[0] == 's':                              # source status
                nod,seq,bnd,msc,age = fields[1:]
                #if debug: print pkt_tm,fnod,sip,stm,nod,seq,bnd,msc
                self.si.sss(pkt_tm,fnod,sip,nod,seq,bnd,msc,age)
            elif fields[0] == 'r':                              # fill request
                destip,src,seq = fields[1:]
##                if message.mode == 'tcp':                       # if tcp add port
##                    destip += ":"+str(message.port)
                destip = addr
                #if debug: print destip,src,seq
                self.send_qsomsg(src,seq,destip)
            elif fields[0] == 'q':                              # qso data
                src,seq,stm,b,c,rp,p,o,l = fields[1:]
                #if debug: print src,seq,stm,b,c,rp,p,o,l
                self.si.sqd(src,seq,stm,b,c,rp,p,o,l)
            else:
                sms.prmsg("msg not recognized %s"%addr)
                return False
        return True

# another interesting issue (several actually)
#
# fill requests
#   need to pass more info about address and transport (port,...)
#
# status info
#   status needs to store more info about address and transport (port,...)
#
# note that both above issues solved by using addr:port for tcp and addr for udp
#
#
# message info
#   wondering if the message info should be broken down into fields or a sub dictionary of them
#   made to be part of the message object
#   so perhaps 'contents' would be a dictionary of the key,values of a message
#   might want to use json to package up a dictionary as the message instead of the
#   present text format?
#
# JSON thoughts
#   good for encoding dictionary to/from the network
#   could store JSON in the journal directly (maybe better than SQL)
#   short keys would be advisable as they are always sent
#   the JSON should be ADIF compatible, if that makes any sense
#     it may make sense to map the common ADIF field names to shorter values for the JSON efficiency
#
# JSON over TCP/IP only? (possible future idea, didn't do this yet)
#   why JSON?
#     easier to add fields
#     better compatibility with different versions (maybe, somewhat)
#
# JSON keys brainstorming (try to keep to 2/3 letters per key)
#
#   S,N   source journal identifier, journal sequence number
#   T   timestamp when sent?
#   q   qso callsign
#   t   qso time/date
#   b   band
#   f   frequency
#   m   operating mode (see ADIF format)
#   p   power
#   r   report
#   c   notes, comments
#   o   operator
#   l   logger
#
#   I,P,X   message received from ip,port,transport
#   
#
# it begins to look as though the infrastructure for storing this host info should be reworked
#   perhaps we should have a ram based sqlite database for storing transient info?
#   this would have the advantage of avoiding explicit locks in python, allowing transactions
#   to be used instead, if they are needed
#     or just use objects...

    def send_msg(self,message):
        "route and send network message from a message object"
        # form tcp and udp messages
        msg = message.mesg
        if type(msg) == type(u'unicode'):       # convert unicode to ascii
            msg = msg.encode('utf-8')
     #   print "type msg",type(msg)
        adr_str = message.adr_str
        host = message.host
        umsg = self.auth(msg)+'\n'+msg          # make udp message
        tlen = len(umsg)                        # make tcp message
        if tlen > 8200:
            print "error, send_msg too long",tlen,"dropping to",adr_str
            return
        # making 3B header for tcp with two byte length, lsB first, and
        # third byte xor of first two
        i = tlen&255
        j = tlen>>8
        tmsg = chr(i) + chr(j) + chr(i^j) + umsg # umsg must be ascii
        # where did umsg become unicode and what have you done with my ascii?
        # sockets can't take unicode, will convert to bytes, not good if it crashes
        if message.mode == 'bcast':
            if debug: print
##            if len(self.tcp_conn) > 0:
##                print "broadcasting (tcp:%d)"%len(self.tcp_conn)
            if debug: print msg,
            self.send_udp(self.bc_addr,umsg)    # send to udp broadcast
            for a in self.tcp_conn:             # send to tcp clients
                self.send_tcp(a,tmsg)
        elif message.mode == 'tcp':
            if self.tcp_conn.get(adr_str,None):
                self.send_tcp(adr_str,tmsg)     # if in tcp list, send to tcp (priority)
            else:
                print "tcp send fail no conn",adr_str
        else:
            self.send_udp(host,umsg)            # otherwise send to udp

    def send_tcp(self,adr_str,tmsg):
        "send a TCP message"
        c = self.tcp_conn.get(adr_str,None)
        if c == None:                           # dead connection
            print "sent_tcp fail to conn None",adr_str
            return              
        skt,adr = c
        if debug: print "send_tcp to ",adr_str,len(tmsg)
        try:
            skt.sendall(tmsg)                   # send all the bytes of the message
        except socket.error,e:
            self.send_errs += 1
            print "error, send_tcp failed %s %s [%s]"%(now(),e.args,adr_str)

# udp and tcp are fundamentally different (even though they share a lot)
# we do udp on one port, one host per ip
# tcp may be using different ports on the same ip for different hosts (NAT routing)
# how does filler get back to the right host in the tcp case? FIXED
# new message object solves this problem by carrying the extra info needed

    def send_udp(self,host,umsg):
        "send a UDP message either a broadcast or a unicast"
        # two cases, broadcast or directed UDP (fill request response)
        # this is determined by the sender and encoded in the host address
        # the host address is in the x.x.x.x format

        #return # TCP test, silently disable udp transmissions
    
        if debug: print "send_udp to ",host #,self.port #; print umsg

##        print "  udp transmission skipped for debug" # testing
##        return # testing
    
        if self.udp_skt == None:
            print "uninit UDP socket"
            return
        try:
            self.udp_skt.sendto(umsg,(host,self.port))
        except socket.error,e:
            self.send_errs += 1
            print "error, send_udp failed %s %s [%s]"%(now(),e.args,host)

    def close_all(self):
        "close all network sockets"
        print "  closing udp"
        if self.udp_skt:                    # close the shared udp socket if it is open
            s = self.udp_skt
            self.udp_skt = None
            try: s.close()
            except: pass
        print "  closing tcp"
        for a,s in self.tcp_conn.items():   # close all the open tcp sockets
            del(self.tcp_conn[a])
            try: s.close()
            except: pass

    # old udp code from here on
    
    def setport(self,useport):
        "setup network udp port"
        self.port = useport
        self.udp_skt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   # send socket
        self.udp_skt.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) # Erics linux fix
        self.udp_skt.bind((self.my_addr,self.port+1))                    # outbound udp port

# seem to be having a new problem 5/2013
#   error: [Errno 10048] Only one usage of each socket address (protocol/network address/port) is normally permitted
#   perhaps due to a recent windoze update that changed port behavior
#   seems to require a reboot to clear the port
#   or killing pythonw process tree after closing the interpreter
#   this was improved by closing the socket when exiting the program, need
#   to do this for all the sockets that are open
#   this is mostly an IDLE deugger problem

    def setauth(self,newauth):
        "set authentication key code base, copy on use"
        global authk
        authk = newauth
        seed = "2004070511111akb"               # change when protocol changes
        self.authkey = hashlib.md5(newauth+seed)
        
    def auth(self,msg):
        "calc authentication hash"
        h = self.authkey.copy()
        h.update(msg)
        return h.hexdigest()
    
    def ckauth(self,msg):
        "check authentication hash"
        h,m = msg.split('\n',1)
##        print h; print self.auth(m); print
        return h == self.auth(m)

# sndmsg must be taught to send tcp to remote sites
# probably should be split for sending both udp and tcp message types
# will be replaced by new version above

    def sndmsg(self,msg,addr):
        "send message to address replacing old version"
        # interface old messaging to new, handles tcp
        if ':' in addr:                           # tcp addresses include port
            host,port = addr.split(':')
            mode = 'tcp'
        elif addr == 'bcast':
            host,port,mode = '','','bcast'
        else:
            host,port,mode = addr,self.port,'udp' # udp addresses are host only, port is fixed
        message = MESSAGE(host,port,mode,msg)
        message.send()
        
    def sndmsgX(self,msg,addr):
        "send message to address"
        if authk != "" and node != "":
            amsg = self.auth(msg)+'\n'+msg
            #print "auth len",len(self.auth(msg))
            addrlst = []
            if addr == 'bcast':
                addrlst.append(self.bc_addr)
##                addrlst.append(self.rem_adr)
##                for a in node_info.rembcast.keys():
##                    if debug: print "adding dyn remaddr",a
##                    addrlst.append(a)
            else: addrlst.append(addr)
            for a in addrlst:
                if a == "": continue
                if a == '0.0.0.0': continue
                if debug: print "send to ",a ; print msg
                try:
                    self.skt.sendto(amsg,(a,self.port))
                except socket.error,e:
                    self.send_errs += 1
                    print "error, pkt xmt failed %s %s [%s]"%(now(),e.args,a)

    def send_qsomsg(self,nod,seq,destip):
        "send q record"
        key = nod + '.' + str(seq)
        if qdb.byid.has_key(key):
            i = qdb.byid[key]
            msg = "q|%s|%s|%s|%s|%s|%s|%s|%s|%s\n"%\
                (i.src,i.seq,i.date,i.band,i.call,i.rept,i.powr,i.oper,i.logr)
            self.sndmsg(msg,destip)
        
    def bc_qsomsg(self,nod,seq):
        "broadcast new q record"
        self.send_qsomsg(nod,seq,self.bc_addr)

    def bcast_now(self):
        "broadcast node status message now"
        msg = "b|%s|%s|%s|%s|%s|%s\n"%\
              (self.hostname,self.my_addr,node,nowms(),mclock.level,version)
       # print "node",type(node)  # node is unicode, causing problems, probably from dbase
        for i in self.si.node_status_list():
            msg += "s|%s|%s|%s|%s|%s\n" % i     # nod,seq,bnd,msc,age
            #if debug: print i
       # print msg
        self.sndmsg(msg,'bcast')                # broadcast it

    def bcast_time(self):
        "broadcast time"
        msg = "b|%s|%s|%s|%s|%s|%s\n"%\
              (self.hostname,self.my_addr,node,nowms(),mclock.level,version)
       # print "node",type(node)  # node is unicode, causing problems, probably from dbase
##        for i in self.si.node_status_list():
##            msg += "s|%s|%s|%s|%s|%s\n" % i     # nod,seq,bnd,msc,age
##            #if debug: print i

        self.sndmsg(msg,'bcast')                # broadcast it

        #print msg

        
# requesting fills is about to get more complicated
# with tcp involved we need to know not just which host requested the fill
# but also which port
# two ways to go, one is to break the protocol, 
#   but there is a non protocol breaking alternative
# the other is to carry the requesting host, port and mode clear through
# tempting to make a message class to handle this sort of thing
# for now, if the port is there it is tcp otherwise it is udp

    def fillr(self):
        "filler thread requests missing database records"
        time.sleep(0.2)
        if debug: print "filler thread starting"

        while 1:
            time.sleep(.2)                      # periodically check for fills
            if debug: time.sleep(2)             # slow for debug
            r = self.si.fill_requests_list()
            self.fills = len(r)
            if self.fills:
                p = random.randrange(0,len(r))                  # randomly select one
                c = r[p]
                msg = "r|%s|%s|%s\n"%(self.my_addr,c[1],c[2])   # (addr,src,seq)
                self.sndmsg(msg,c[0])                           # send a fill request
                print "req fill",c

# for remote/tcp integration need to split the rcvr thread into receiving and
# received packet processing. No, replacing with new code above.

##    def rcvrX(self):
##        "receiver thread processes incoming packets"
##        if debug: print "receiver thread starting"
##        r = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
##        self.rcvSkt = r
##        r.bind(('', self.port))
##
##        while 1:
##            try: msg, addr = r.recvfrom(800)
##            except: # quit process when socket errors?
##                time.sleep(1)
##                continue
##            if addr[0] != self.my_addr:
##                self.pkts_rcvd += 1
####            if authk == "": continue             # skip till auth set
##            pkt_tm = now()
##            host,sip,fnod,stm = '','','',''
##            if debug: print "rcvr: %s: %s"%(addr,msg),  #xx
##            if not self.ckauth(msg):            # authenticate packet
##                #if debug: sms.prmsg("bad auth from: %s"%addr)
##                print "bad auth from:",addr
##                self.badauth_rcvd += 1
##            else:
##                lines = msg.split('\n')         # decode lines
##                for line in lines[1:-1]:        # skip auth hash, blank at end
####                    if debug: sms.prmsg(line)
##                    fields = line.split('|')
##                    if fields[0] == 'b':        # status bcast
##                        host,sip,fnod,stm,stml,ver = fields[1:]
##                        td = tmsub(stm,pkt_tm)
##                        self.si.ssb(pkt_tm,host,sip,fnod,stm,stml,ver,td)
##                        mclock.calib(fnod,stml,td)
##                        if abs(td) >= tdwin:
##                            print 'clock err',td,host,sip,fnod,pkt_tm
##                        if showbc:
##                            print "bcast",host,sip,fnod,ver,pkt_tm,td
##                    elif fields[0] == 's':      # source status
##                        nod,seq,bnd,msc,age = fields[1:]
##                        #if debug: print pkt_tm,fnod,sip,stm,nod,seq,bnd,msc
##                        self.si.sss(pkt_tm,fnod,sip,nod,seq,bnd,msc,age)
##                    elif fields[0] == 'r':      # fill request
##                        destip,src,seq = fields[1:]
##                        #if debug: print destip,src,seq
##                        self.send_qsomsg(src,seq,destip)
##                    elif fields[0] == 'q':      # qso data
##                        src,seq,stm,b,c,rp,p,o,l = fields[1:]
##                        #if debug: print src,seq,stm,b,c,rp,p,o,l
##                        self.si.sqd(src,seq,stm,b,c,rp,p,o,l)
##                    else:
##                        sms.prmsg("msg not recognized %s"%addr)

    def start(self):
        "launch all net threads"
        global fillrThread,rcvrThread
##        global node
        print "This host:", self.hostname, "IP:",self.my_addr#, "Mask:",self.bc_addr
##        if (self.hostname > "") & (node == 's'):
##            node = self.hostname             # should filter chars
##        print "Node ID:",node
        print "Launching threads"
##        thread.start_new_thread(self.fillr,())
##        thread.start_new_thread(self.rcvr,())
        fillrThread = threading.Thread(target=self.fillr,name="filler")
        fillrThread.start()
#        rcvrThread = threading.Thread(target=self.rcvr,name="receiver")
        rcvrThread = threading.Thread(target=self.rcv_udp,name="udp receiver")
        rcvrThread.start()
        tcpSvcMgrThread = threading.Thread(target=self.tcp_manager,name="tcp manager")
        tcpSvcMgrThread.start()
        tcpClientThread = threading.Thread(target=self.tcp_client,name="tcp client")
        tcpClientThread.start()
        time.sleep(4)                         # let em print
        print "Startup complete"

class global_data:
#global data stored in the journal

    byname = {}

    def new(self,name,desc,defaultvalue,okgrammar,maxlen):
        i = global_data()                       # create
        i.name = name                           # set
        i.val = defaultvalue
        i.okg = okgrammar
        i.maxl = maxlen
        i.ts = ""
        i.desc = desc
        self.byname[name] = i
        return i

    def setv(self,name,value,timestamp):
        if node == "":
            text.insert(END,"error - no node id\n")
            return
        if name[:2] == 'p:':                    # set oper/logr
            i = self.byname.get(name,self.new(name,'','','',0))
        else:
            if not self.byname.has_key(name):   # new
                return "error - invalid global data name: %s"%name
            i = self.byname[name]
            if len(value) > i.maxl:             # too long
                return "error - value too long: %s = %s"%(name,value)
            if not re.match(i.okg,value):       # bad grammar
                return "set error - invalid value: %s = %s"%(name,value)
        if timestamp > i.ts:                    # timestamp later?
            i.val = value
            i.ts = timestamp
            if name[:2] == 'p:':
                ini,name,call = string.split(value,', ')
                participants[ini] = value
                if name == 'delete':
                    del(participants[ini])
                buildmenus()
        #else: print "set warning - older value discarded"

    def getv(self,name):
        if not self.byname.has_key(name):       # new
            return "get error - global data name %s not valid"%name
        return self.byname[name].val

    def sethelp(self):
        l = ["   Set Commands\n\n    eg: .set <parameter> <value>\n"]  # spaced for sort
        for i in self.byname.keys():
            if i[:2] != 'p:':                   # skip ops in help display
                l.append("  %-6s  %-43s  '%s'"%(i,self.byname[i].desc,self.byname[i].val))
        l.sort()
        viewtextl(l)

gd = global_data()
for name,desc,default,okre,maxlen in (
        ('class', '<n><A-F>       FD class (eg 2A)','2A',r'[1-9][0-9]?[a-fA-F]$',3),
        ('contst','<text>         Contest (FD,VHF)','FD',r'fd|FD|vhf|VHF$',3),
        ('fdcall','<CALL>         FD call','',r'[a-zA-Z0-9]{3,6}$',6),
        ('gcall', '<CALL>         GOTA call','',r'[a-zA-Z0-9]{3,6}$',6),
        ('sect',  '<CC-Ccccc...>  ARRL section','<section>',r'[A-Z]{2,3}-[a-zA-Z ]{2,20}$',24),
        ('grid',  '<grid>         VHF grid square','',r'[A-Z]{2}[0-9]{2}$',4),
        ('grpnam','<text>         group name','',r'[A-Za-z0-9 #.:-]{4,35}$',35),
        ('fmcall','<CALL>         entry from call','',r'[a-zA-Z0-9]{3,6}$',6),
        ('fmnam', '<name>         entry from name','',r'[A-Za-z0-9 .:-]{0,35}$',35),
        ('fmad1', '<text>         entry from address line 1','',r'[A-Za-z0-9 #.,:-]{0,35}$',35),
        ('fmad2', '<text>         entry from address line 2','',r'[A-Za-z0-9 #.,:-]{0,35}$',35),
        ('fmem',  '<text>         entry from email','',r'[A-Za-z0-9@.:-]{0,35}$',35),
        ('public','<text>         public location desc','',r'[A-Za-z0-9@.: -]{0,35}$',35),
##        ('demoa', '<text>         FD demo a mode','',r'[A-Za-z0-9.: -]{0,35}$',35),
##        ('demob', '<text>         FD demo b mode','',r'[A-Za-z0-9.: -]{0,35}$',35),
##        ('democ', '<text>         FD demo c mode','',r'[A-Za-z0-9.: -]{0,35}$',35),
        ('infob', '0/1            public info booth','0',r'[0-1]$',1),
        ('svego', '<name>         govt official visitor name','',r'[A-Za-z., -]{0,35}$',35),
        ('svroa', '<name>         agency site visitor name','',r'[A-Za-z., -]{0,35}$',35),
        ('youth', '<n>            participating youth','0',r'[0-9]{1,2}$',2),
        ('websub','0/1            web submission bonus','0',r'[0-1]$',1),
        ('psgen', '0/1            using generator power','0',r'[0-1]$',1),
        ('pscom', '0/1            using commercial power','0',r'[0-1]$',1),
        ('psbat', '0/1            using battery power','0',r'[0-1]$',1),
# add solar xx
        ('psoth', '<text>         desc of other power','',r'[A-Za-z0-9.: -]{0,35}$',35),
        ('fdstrt','yymmdd.hhmm    FD start time (UTC)','020108.1800',r'[0-9.]{11}$',11),
        ('fdend', 'yymmdd.hhmm    FD end time (UTC)',  '990629.2100',r'[0-9.]{11}$',11),
        ('tmast', '<text>         Time Master Node','',r'[A-Za-z0-9-]{0,8}$',8) ):
    gd.new(name,desc,default,okre,maxlen)

class syncmsg:
    "synchronous message printing"
    lock = threading.RLock()
    msgs = []

    def prmsg(self,msg):
        "put message in queue for printing"
        self.lock.acquire()
        self.msgs.append(msg)
        self.lock.release()

    def prout(self):
        "get message from queue for printing"
        self.lock.acquire()
        while self.msgs:
            #print self.msgs[0]
            logw.configure(state=NORMAL)
            logw.see(END)
            nod = self.msgs[0][70:81]               #color local entries
#            print nod,node
            if nod == node:
                logw.insert(END,"%s\n"%self.msgs[0],"b")
#                print "blue '%s' '%s'\n"%(nod,node)
            else:  
                logw.insert(END,"%s\n"%self.msgs[0])
            logw.configure(state=DISABLED)
            del self.msgs[0]
        self.lock.release()

# global functions

def now():
    "return current time in standard string format yymmdd.hhmmss"
    #n = time.localtime(time.time())
    n = time.gmtime(time.time()+mclock.offset) # time in gmt utc
                                               # offset to correct to master/gps clock
    t = time.strftime("%y%m%d.%H%M%S",n)       # compact version YY
    return t

def nowms():
    "return current time in standard string format yymmdd.hhmmss.mmm with milliseconds"
    x = time.time()+mclock.offset           # offset to correct to master/gps clock
    n = time.gmtime(x)                      # time in gmt utc
    t = time.strftime("%y%m%d.%H%M%S",n)    # compact version YY
    f,i = math.modf(x)
    t2 = "%s.%03d"%(t,f*1000)
    return t2

def tmtofl(a):
    "time to float in seconds, allow milliseconds"
    
##    return time.mktime((2000+int(a[0:2]),int(a[2:4]),int(a[4:6]),\
##                       int(a[7:9]),int(a[9:11]),int(a[11:13]),0,0,0))
    
    return calendar.timegm((2000+int(a[0:2]),int(a[2:4]),int(a[4:6]),\
                       int(a[7:9]),int(a[9:11]),float(a[11:]),0,0,0))

def tmsub(a,b):
    "time subtract in seconds"
    return tmtofl(a) - tmtofl(b)

def testcmd(name, rex, default):
    "set global from command, return value and change status"
    global kbuf
    value = default
    s = "%s +(%s)$"%(name,rex)
    m = re.match(s,kbuf)
    if m:
        value = m.group(1)
        text.insert(END,"\n%s set to %s\n"%(name,value))
        kbuf = ""
    return value,default != value

# new sqlite globals database fdlog.sq3 replacing globals file
#
class GlobalDb:
    def __init__(self):
        self.dbPath = globf[0:-4] + '.sq3'
        print "  Using local value database",self.dbPath
       
        self.sqdb = sqlite3.connect(self.dbPath)  # connect to the database
        self.sqdb.row_factory = sqlite3.Row       # row factory
        self.curs = self.sqdb.cursor()            # make a database connection cursor
        sql = "create table if not exists global(nam text,val text,primary key(nam))"
        self.curs.execute(sql)
        self.sqdb.commit()
        self.cache = {}                           # use a cache to reduce db i/o
    def get(self,name,default):
        if name in self.cache:
            #print "reading from globCache",name
            return self.cache[name]
        sql = "select * from global where nam == ?"
        results = self.curs.execute(sql,(name,))
        value = default
        for result in results:
            value = result['val']
            #print "reading from globDb", name, value
            self.cache[name] = value
        return value
    def put(self,name,value):
        now = self.get(name,'zzzzz')
        #print now,str(value),now==str(value)
        if str(value) == now: return              # skip write if same
        sql = "replace into global (nam,val) values (?,?)"
        self.curs.execute(sql,(name,value))
        self.sqdb.commit()
        #print "writing to globDb", name, value
        self.cache[name] = str(value)

def loadglob():
    "load persistent local config to global vars from file"
    global globDb,node,operator,logger,power,tdwin,debug,authk,timeok
    globDb = GlobalDb()
    node = globDb.get('node','')
    operator = globDb.get('operator','')
    logger = globDb.get('logger','')
    power = globDb.get('power','100')
    authk = globDb.get('authk','tst')
    tdwin = int(globDb.get('tdwin',5))
    debug = int(globDb.get('debug',0))
    timeok = int(globDb.get('timeok',0))
    netsync.rem_host = globDb.get('remip','0.0.0.0')

    mclock.offsetinit()
    
##    try:
##        fd = file(globf,"r")
##        line = fd.readline()
##        fd.close()
##        d1,node,operator,logger,power,auth,tdwin,debug,d2 = string.split(line,'|')
##        debug = int(debug)
##        tdwin = int(tdwin)
##        authk = auth
##        print "Loaded persistent configuration data file: %s"%globf
##        print "  Node ID: %s\n  Operator: %s\n  Logger: %s\n  Power: %s"%\
##          (node,operator,logger,power)
##    except:
##        print "Persistent configuration data file not found, using default values"
##        authk = "tst"

    if debug: print "  debug:",debug
    
def saveglob():
    "save persistent local config global vars to file"
    globDb.put('node',node)
    globDb.put('operator',operator)
    globDb.put('logger',logger)
    globDb.put('power',power)
    globDb.put('authk',authk)
    globDb.put('tdwin',tdwin)
    globDb.put('debug',debug)
    globDb.put('timeok',timeok)

##    fd = file(globf,"w")
##    fd.write("|%s|%s|%s|%s|%s|%s|%s|"%(node,operator,logger,power,\
##                                       authk,tdwin,debug))
##    fd.close()

# contest log section

def getfile(fn):
    "get file contents"

    data = ""
    try:
        fd = file(fn,"r")
        data = fd.read()
        fd.close()
    except:
        pass
    if data != "":
        print "Found file",fn
        #print data
    return data
    

participants = {}

def contestlog(pr):
    "generate contest entry and log forms"

    w1aw_msg = getfile("w1aw_msg.txt")          # w1aw bulletin copy
    
    
    # National Traffic System Messages

    nts_orig_msg = getfile("nts_msg.txt")       # status message
    
    nts_msg_relay = []
    for i in range(0,10):                        # relayed messages
        fn = "nts_rly%d.txt"%i
        msg = getfile(fn)
        if msg != "":
            nts_msg_relay.append(msg)

    media_copy = getfile("media.txt")           # media activity

    soapbox = getfile("soapbox.txt")            # soapbox commentary

    fd_call = string.upper(gd.getv('fdcall'))   # prep data
    xmttrs = ival(gd.getv('class'))
    gota_call = string.upper(gd.getv('gcall'))
    if xmttrs < 2: gota_call = ""

    if pr == 0: return                          # only define variables return

    # output the entry, adif & cabrillo log file
    
    datime = now()
    byid,bycall,gotabycall = qdb.cleanlog()     # get a clean log

    qpb,ppb,qpop,qplg,qpst,tq,score,maxp,cwq,digq,fonq,qpgop,gotaq,nat,sat = \
        qdb.bandrpt()                           # and count it
       
    print "..",

    sys.stdout = file(logfile,"w")              # redirect output to file

    print "Field Day 20%s Entry Form"%datime[:2]
    print
    print "Date Prepared:              %s UTC"%datime[:-2]
    print
    print "1.  Field Day Call:         %s"%fd_call
    if gota_call != "":
        print "    GOTA Station Call:      %s"%gota_call
    print "2.  Club or Group Name:     %s"%gd.getv('grpnam')
    print "3.  Number of Participants: %s"%len(participants)
    print "4.  Transmitter Class:      %s"%xmttrs
    print "5.  Entry Class:            %s"%string.upper(gd.getv('class'))[-1:]
    print
    print "6.  Power Sources Used:"
    if int(gd.getv('psgen')) > 0:
        print "      Generator"
    if int(gd.getv('pscom')) > 0:
        print "      Commercial"
    if int(gd.getv('psbat')) > 0:
        print "      Battery"
## add solar! xx
    if gd.getv('psoth') != '':
        print "      Other: %s"%(gd.getv('psoth'))
    print
    print "7.  ARRL Section:           %s"%gd.getv('sect')

    print
    print "8.  Total CW QSOs:      %4s  Points: %5s"%(cwq,cwq*2)
    print "9.  Total Digital QSOs: %4s  Points: %5s"%(digq,digq*2)
    print "10. Total Phone QSOs:   %4s  Points: %5s"%(fonq,fonq)
    qsop = cwq*2 + digq*2 + fonq
    print "11. Total QSO Points:                 %5s"%qsop
        
    print "12. Max Power Used:     %4s  Watts"%maxp
    powm = 5
    if int(gd.getv('psgen')) > 0 or int(gd.getv('pscom')) > 0: powm = 2
    if maxp > 5: powm = 2
    if maxp > 150: powm = 1
    if maxp > 1500: powm = 0
    print "13. Power Multiplier:                  x %2s"%powm

    qso_scor = qsop * powm
    print "14. Claimed QSO Score:                %5s"%qso_scor

    print
    print "15. Bonus Points:"

    tot_bonus = 0

    emerg_powr_bp = 0
    if gd.getv('pscom') == '0':
        emerg_powr_bp = 100 * xmttrs
        if emerg_powr_bp > 2000:
            emerg_powr_bp = 2000
        tot_bonus += emerg_powr_bp
        print "   %4s 100%s Emergency Power (%s xmttrs)"%(emerg_powr_bp,'%',xmttrs)

    media_pub_bp = 0
    if media_copy > "":
        media_pub_bp = 100
        tot_bonus += media_pub_bp
        print "    %3s Media Publicity (copy below)"%media_pub_bp

    public_bp = 0
    public_place = gd.getv('public')
    if public_place != "":
        public_bp = 100
        tot_bonus += public_bp
        print "    %3s Set-up in a Public Place (%s)"%(public_bp, public_place)

    info_booth_bp = 0
    if int(gd.getv('infob')) > 0 and public_bp > 0:
        info_booth_bp = 100       
        tot_bonus += info_booth_bp
        print "    %3s Information Booth (photo included)"%info_booth_bp

    nts_orig_bp = 0
    if nts_orig_msg > "":
        nts_orig_bp = 100
        tot_bonus += nts_orig_bp
        print "    %3s NTS message Originated to ARRL SM/SEC (copy below)"%nts_orig_bp

    n = len(nts_msg_relay)
    nts_msgs_bp = 10 * n
    if nts_msgs_bp > 100:
        nts_msgs_bp = 100
    if nts_msgs_bp > 0:
        tot_bonus += nts_msgs_bp
        print "    %3s Formal NTS messages handled (%s) (copy below)"%(nts_msgs_bp,n)

    sat_qsos = len(sat)
    sat_bp = 0
    if sat_qsos > 0:
        sat_bp = 100
        tot_bonus += sat_bp
        print "    %3s Satellite QSO Completed (%s/1) (list below)"%(sat_bp,sat_qsos)
    
    natural_q = len(nat)
    natural_bp = 0
    if natural_q >= 5:
        natural_bp = 100
        tot_bonus += natural_bp
        print "    %3s Five Alternate power QSOs completed (%s/5) (list below)"%(natural_bp,natural_q)

    w1aw_msg_bp = 0
    if len(w1aw_msg) > 30: # ignore short file place holder
        w1aw_msg_bp = 100
        tot_bonus += w1aw_msg_bp
        print "    %3s W1AW FD Message Received (copy below)"%(w1aw_msg_bp)

##    if gd.getv('demoa') != "":
##        print "        Non-Traditional Demonstration Modes:"
##        tot_bonus += 100
##        print "    %3s A. %s"%(100,gd.getv('demoa'))
##    if gd.getv('demob') != "":
##        tot_bonus += 100
##        print "    %3s B. %s"%(100,gd.getv('demob'))
##    if gd.getv('democ') != "":
##        tot_bonus += 100
##        print "    %3s C. %s"%(100,gd.getv('democ'))

    site_visited_ego_bp = 0
    if gd.getv('svego') > "":
        site_visited_ego_bp = 100
        tot_bonus += site_visited_ego_bp
        print "    %3s Site Visited by elected govt officials (%s)"%(site_visited_ego_bp,gd.getv('svego'))

    site_visited_roa_bp = 0
    if gd.getv('svroa') > "":
        site_visited_roa_bp = 100
        tot_bonus += site_visited_roa_bp
        print "    %3s Site Visited by representative of agency (%s)"%(site_visited_roa_bp,gd.getv('svroa'))

    gota_max_bp = 0
    if gotaq >= 100:
        gota_max_bp = 100
        tot_bonus += gota_max_bp
        print "    %3s GOTA Station 100 QSOs bonus achieved"%(gota_max_bp)

    youth_bp = 0
    if int(gd.getv('youth')) > 0:
        youth_bp = 20 * int(gd.getv('youth'))
        if youth_bp > 5 * 20:
            youth_bp = 5 * 20
        tot_bonus += youth_bp
        print "    %3s Youth Participation Bonus"%(youth_bp)

# keep this last
    web_sub_bp = 0
    if gd.getv('websub') == "1":
        web_sub_bp = 50
        tot_bonus += web_sub_bp
        print "    %3s Web Submission Bonus"%(web_sub_bp)
    print
    print "    Total Bonus Points Claimed: %5s"%tot_bonus
    print
    tot_scor = qso_scor + tot_bonus
    print "    Total Claimed Score:        %5s"%tot_scor
    print
    print "16. We have observed all competition rules as well as all regulations"
    print "    for amateur radio in our country. Our report is correct and true"
    print "    to the best of our knowledge. We agree to be bound by the decisions"
    print "    of the ARRL Awards Committee."
    print
    print "Submitted By:"
    print
    print "    Date:     %s UTC"%datime[:-2]
    print "    Call:     %s"%string.upper(gd.getv('fmcall'))
    print "    Name:     %s"%gd.getv('fmnam')
    print "    Address:  %s"%gd.getv('fmad1')
    print "    Address:  %s"%gd.getv('fmad2')
    print "    Email:    %s"%gd.getv('fmem')
    print
    print
    print "Field Day Call: %s"%string.upper(fd_call)
    print

    print "17. QSO Breakdown by Band and Mode"
    print
    print "        ----CW----  --Digital-  ---Phone--"
    print "  Band  QSOs   PWR  QSOs   PWR  QSOs   PWR"
    print
    qsobm, pwrbm = {}, {}
    for b in (160,80,40,20,15,10,6,2,220,440,1200,'sat','gota'):
        if b == 'gota' and gota_call == "": continue
        print "%6s"%b,
        for m in 'cdp':
            bm = "%s%s"%(b,m)
            print "%5s %5s"%(qpb.get(bm,0),ppb.get(bm,0)),
            qsobm[m] = qsobm.get(m,0) + qpb.get(bm,0)
            pwrbm[m] = max(pwrbm.get(m,0), ppb.get(bm,0))
        print
    print
    print "Totals",
    print "%5s %5s"%(qsobm['c'],pwrbm['c']),
    print "%5s %5s"%(qsobm['d'],pwrbm['d']),
    print "%5s %5s"%(qsobm['p'],pwrbm['p'])
    print
    print

    if gota_call:
        print "18. Callsigns and QSO counts of GOTA Operators"
        print
        print "      Call  QSOs"
        for i in qpgop.keys():
            print "    %6s   %3s"%(i,qpgop[i])
        print "    %6s   %3s"%("Total",gotaq)
        print
        print

    print "Dupe Lists sorted by Band, Mode and Call:"
    print

    print "  Main Station(s) Dupe List (%s)"%fd_call
    l = []
    for i in bycall.values():
        l.append("    %4s %s"%(i.band,i.call))
    l.sort()
    b2,n = "",0
    for i in l:
        b,c = i.split()
        if (b == b2) & (n < 5):         # same band, 5 per line
            print "%-10s"%c,
            n += 1
        else:
            print
            print "    %4s   %-10s"%(b,c),
            b2 = b
            n = 1
    print
    print
    print

    if gota_call > "":
        print "  GOTA Station Dupe List (%s)"%gota_call
        l = []
        for i in gotabycall.values():
            l.append("    %4s %s"%(i.band,i.call))
        l.sort()
        b2,n = "",0
        for i in l:
            b,c = i.split()
            if (b == b2) & (n < 5):     # same band
                print "%-10s"%c,
                n += 1
            else:
                print
                print "    %4s   %-10s"%(b,c),
                b2 = b
                n = 1
        print
        print
        print

    if w1aw_msg != "":
        print "W1AW FD Message Copy"
        print
        print "%s"%w1aw_msg
        print
        print

    if nts_orig_msg != "":
        print "Originated NTS Message"
        print
        print nts_orig_msg 
        print
        print

    if len(nts_msg_relay) > 0:
        print "RELAYED NTS Messages"
        print
        for i in nts_msg_relay:
            print i
            print
        print

    if media_copy != "":
        print "Media Copy"
        print
        print media_copy
        print
        print
        
    if len(nat) > 0:
        print "Natural Power QSOs (show first 10 logged)"
        print
        l = []
        for i in nat:
            ln = "%8s %5s %-10s %-18s %4s %-6s %-6s %4s %s"%\
                 (i.date[4:11],i.band,i.call,i.rept[:18],i.powr,i.oper,i.logr,i.seq,i.src)
            l.append(ln)
        l.sort()
        j = 0
        for i in l:
            print i
            j += 1
            if j > 9: break
        print
        print

    if len(sat) > 0:
        print "Satellite QSOs (show 5)"
        print
        l = []
        for i in sat:
            ln = "%8s %5s %-10s %-18s %4s %-6s %-6s %4s %s"%\
                 (i.date[4:11],i.band,i.call,i.rept[:18],i.powr,i.oper,i.logr,i.seq,i.src)
            l.append(ln)
        l.sort()
        j = 0
        for i in l:
            print i
            j += 1
            if j > 4: break
        print
        print

    if soapbox != "":
        print "Soapbox Comments"
        print
        print soapbox
        print
        print
    
    print "Logging and Reporting Software Used:\n"
    print prog

    print "===================== CLIP HERE ============================"
    print
    print "(do not include below in ARRL submission)"

    print
    print "Submission Notes"
    
    print """
    
    email files as attachments to FieldDay@arrl.org within 30 days!!!
    web entry at www.b4h.net/cabforms
    
        fdlog.log log file, less log detail below 'CLIP HERE'
        proof of bonus points, as needed:
            public info booth picture, visitor list, info
            visiting officials pictures
            media visiting pictures
            natural power pictures
            demo stations pictures
        plus other interesting pictures

    """

    print "Participant List"
    print
    l = []
    for i in participants.values():
        l.append(i)
    l.sort
    n = 0
    for i in l:
        n += 1
        print "  %4s %s"%(n,i)
    print

    print
    print "QSO breakdown by Station"
    print
    for i in qpst.keys():
        print "  %4s %s"%(qpst[i],i)
    print
    print
    print "QSO breakdown by Operator"
    print
    for i in qpop.keys():
        print "  %4s %s"%(qpop[i],i)
    print
    print
    print "QSO breakdown by Logger"
    print
    for i in qplg.keys():
        print "  %4s %s"%(qplg[i],i)
    print
    print

    print "Worked All States during FD Status"
    print
    r = qdb.wasrpt()
    for i in r:
        print i
    print
    print

    print "Detailed Log"
    print
    print "  Date Range",gd.getv('fdstrt'),"-",gd.getv('fdend'),"UTC"
    print
    qdb.prlog()
    print
    print

    print "ADIF Log"
    print
    qdb.pradif()
    print

    print "VHF Cabrillo"
    print
    qdb.vhf_cabrillo()
    print

    print "eof"
    
    sys.stdout = sys.__stdout__                 # revert print to console
    print
    print "entry and log written to file",logfile

# band set buttons
# this can be customized

bands = ('160','80','40','20','15','10','6','2','220','440','900','1200','sat','off')
modes = ('c','d','p')

bandb = {}  # band button handles

def bandset(b):
    global band,tmob
    if node == "":
        b = 'off'
        text.insert(END,"err - no node\n")
    if operator == "":
        b = 'off'
        text.insert(END,"err - no operator\n")
    if b != 'off':
        s = net.si.nod_on_band(b)
        if s: text.insert(END," Already on [%s]: %s\n"%(b,s))
    text.see(END)
    if band != b: tmob = now()      # reset time on band
    band = b
    bandb[b].select()
    renew_title()
    
def bandoff():
    bandset('off')

# new participant setup

class newparticipantdialog:

    def lookup(self):
        # constrain focus to initials until they are ok
        #print "lookup"
        #print self.initials.get()
        initials = string.lower(self.initials.get())
        # if not re.match(r'[a-zA-Z]{2}[a-zA-Z0-9]?$',initials):
        if not re.match(r'[a-zA-Z]{2,3}$',initials):
            #self.initials.delete(0,END)
            self.initials.configure(bg='yellow')
            self.initials.focus()
        else:
            self.initials.configure(bg='white')
            ini,name,call = string.split(participants.get(initials,', , '),', ')
            self.name.delete(0,END)
            self.name.insert(END,name)
            self.call.delete(0,END)
            self.call.insert(END,call)
        return 1
    
    def applybtn(self):
        global participants
        #print "store"
        initials = self.initials.get().lower()
        name = self.name.get()
        call = string.lower(self.call.get())
        self.initials.configure(bg='white')
        self.name.configure(bg='white')
        self.call.configure(bg='white')
        if not re.match(r'[a-zA-Z]{2,3}$',initials):
            text.insert(END,"error in initials\n")
            text.see(END)
            self.initials.focus()
            self.initials.configure(bg='yellow')
            #self.initials.delete(0,END)
        elif not re.match(r'[A-Za-z ]{4,20}$',name):
            text.insert(END, "error in name\n")
            text.see(END)
            self.name.focus()
            self.name.configure(bg='yellow')
            #self.name.delete(0,END)
        #elif not re.match(r'([a-z]{1,2}[0-9][a-z]{1,3})?$',call):
        elif not re.match(r'([a-zA-Z0-9]{3,6})?$',call):
            text.insert(END, "error in call\n")
            text.see(END)
            self.call.focus()
            self.call.configure(bg='yellow')
            #self.call.delete(0,END)
        else:
            initials 
            nam = "p:%s"%initials
            v = "%s, %s, %s"%(initials,name,call)
            participants[initials] = v
            n = qdb.globalshare(nam,v)  # store + bcast
            self.initials.delete(0,END)
            self.name.delete(0,END)
            self.call.delete(0,END)
            self.initials.focus()
            buildmenus()

    def quitbtn(self):
        #print "quit"
        self.t.destroy()
    
    def dialog(self):
        if node == "":
            text.insert(END,"err - no node\n")
            return
        s = newparticipantdialog()
        s.t = Toplevel(root)
        s.t.transient(root)
        s.t.title('FDLog Add New Participant')
        f1 = Frame(s.t)
        f1.grid(row=0,column=0)
        Label(f1,text='Initials',font=fdbfont).grid(row=0,column=0,sticky=W)
        s.initials = Entry(f1,width=3,font=fdbfont,\
                           validate='focusout',validatecommand=s.lookup)
        s.initials.grid(row=0,column=1,sticky=W)
        s.initials.focus()
        Label(f1,text='Name',font=fdbfont).grid(row=1,column=0,sticky=W)
        s.name = Entry(f1,width=20,font=fdbfont)
        s.name.grid(row=1,column=1,sticky=W)
        Label(f1,text='Call',font=fdbfont).grid(row=2,column=0,sticky=W)
        s.call = Entry(f1,width=6,font=fdbfont)
        s.call.grid(row=2,column=1,sticky=W)
        f2 = Frame(s.t)
        f2.grid(row=1,column=0,sticky=EW,pady=3)
        f2.grid_columnconfigure((0,1),weight=1)
        Button(f2,text='Save',font=fdbfont,command=s.applybtn)\
                                        .grid(row=3,column=1,sticky=EW,padx=3)
        Button(f2,text='Quit',font=fdbfont,command=s.quitbtn)\
                                        .grid(row=3,column=0,sticky=EW,padx=3)
newpart = newparticipantdialog()

# property dialogs

cf = {}

def renew_title():
    "renew title and various, called at 10 second rate"
    if node == 'gota': call = string.upper(gd.getv('gcall'))
    else: call = string.upper(gd.getv('fdcall'))
    clas = string.upper(gd.getv('class'))
    sec = gd.getv('sect')
    t = now()
    sob = tmsub(t,tmob)
    mob = sob/60
    h = mob/60
    m = mob%60
    root.title('FDLog %s %s %s (Node: %s Time on Band: %d:%02d) %s:%s UTC %s/%s'%\
       (call,clas,sec,node,h,m,t[-6:-4],t[-4:-2],t[2:4],t[4:6]))
    net.bcast_now()   # this is periodic bcast...

def setnode(new):
    global node
    bandoff()
    node = string.lower(new)
    qdb.redup()
    renew_title()

def applyprop(e=''):
    "apply property"
    global operator,logger,power,node
    new = cf['e'].get()
    if re.match(cf['vre'],new):
##        if   cf['lab'] == 'Operator': operator = new
##        elif cf['lab'] == 'Logger':   logger = new
##        elif cf['lab'] == 'Power':    power = new
        if cf['lab'] == 'Node':  setnode(new)
##        elif cf['lab'] == 'AuthKey':  reauth(new)    #net.setauth(new)
        else: print 'error, no such var'
        saveglob()
        renew_title()
        cf['p'].destroy()
    else:
        print 'bad syntax',new
    
def pdiag(label,value,valid_re,wid):
    "property dialog box"
    cf['p'] = Toplevel(root)
    cf['p'].transient(root)
    Label(cf['p'],text=label,font=fdbfont).grid(sticky=E,pady=20)
    if label == 'AuthKey':
        cf['e'] = Entry(cf['p'],width=wid,font=fdbfont,show='*')
    else:
        cf['e'] = Entry(cf['p'],width=wid,font=fdbfont)
    cf['e'].grid(row=0,column=1,sticky=W)
    cf['e'].insert(END,value)
    Button(cf['p'],text="Apply",command=applyprop,font=fdbfont)\
                                .grid(sticky=W,padx=20)
    Button(cf['p'],text="Cancel",command=cf['p'].destroy,font=fdbfont)\
                                .grid(padx=20,pady=20,row=1,column=1,sticky=E)
    cf['vre'] = valid_re
    cf['lab'] = label
    cf['e'].bind('<Return>',applyprop)
    cf['p'].bind('<Escape>',lambda e:(cf['p'].destroy()))
    cf['e'].focus()

def noddiag():
    pdiag('Node',node,r'[A-Za-z0-9-]{1,8}$',8)

##def authdiag():
##    pdiag('AuthKey',authk,r'.{3,12}$',12)

# view textdocs

def viewprep(ttl=''):
    "view preparation core code"
    w = Toplevel(root)
##    w.transient(root)
    w.title("FDLog - %s"%ttl)
    t = Text(w,takefocus=0,height=20,width=85,font=fdfont,\
             wrap=NONE,setgrid=1)
    s = Scrollbar(w,command=t.yview)
    t.configure(yscrollcommand=s.set)
    t.grid(row=0,column=0,sticky=NSEW)
    s.grid(row=0,column=1,sticky=NS)                  
    w.grid_rowconfigure(0,weight=1)
    w.grid_columnconfigure(0,weight=1)
    t.bind('<KeyPress>',kevent)
    return t

def viewtextv(txt,ttl=''):
    "view text variable"
    w = viewprep(ttl)
    w.insert(END,txt)
    w.configure(state=DISABLED)

def viewtextl(l,ttl=''):
    "view text list"
    w = viewprep(ttl)
    for i in l:
        w.insert(END,"%s\n"%i)
    w.configure(state=DISABLED)

def viewtextf(fn,ttl=''):
    "view text file"
    if ttl == "": ttl = "file %s"%fn
    try:
        fd = file(fn,'r')
        l = fd.read()
        viewtextv(l,ttl)
        fd.close()
    except:
        viewtextv("read error on file %s"%fn)

def viewlogf(bandm):
    "view log filtered by bandmode"
    lg = qdb.filterlog2(bandm)
    viewtextl(lg,"Log Filtered for %s"%bandm)

def viewlogfs(nod):
    "view log filtered by node"
    lg = qdb.filterlogst(nod)
    viewtextl(lg,"Log Filtered for %s"%nod)

def viewwasrpt():
    r = qdb.wasrpt()
    viewtextl(r,"Worked All States Report")

def updatebb():
    "update band buttons"

    r,cl,vh,go = net.si.nod_on_bands()
    
    for i in bands:
        b = 0
        for j in modes:
            bm = "%s%s"%(i,j)
            if i == 'off': continue
            bc = 'gray'
            n = len(r.get(bm,''))
            sc = 'white'
            if   n == 0: bc = 'gray'
            elif n == 1: bc = 'yellow'
            else:        bc = 'orange'; sc = 'red'
            bandb[bm].configure(background=bc,selectcolor=sc)

    cltg = ival(gd.getv('class'))            # class target

    if cltg > 1: vht = 1                    # handle free vhf xmttr
    else: vht = 0

    ts = cl + max(0,vh-vht)                 # total sta = class + excess vhf stations
    
    clc = 'white'
    if ts >  0   : clc = 'yellow'
    if ts == cltg: clc = 'green'
    if ts >  cltg: clc = 'red'
    bandb['Class'].configure(text='Class %s/%s'%(ts,cltg),background=clc)
    
    vhc = 'white'
    if vh > 0: vhc = 'green'
    if vh > vht and ts > cltg: vhc = 'orange'  # 2 vhf is okay, only 1 is free..
    bandb['VHF'].configure(text='VHF %s/%s'%(vh,vht),background=vhc)
    
    if cltg > 1: gotatg = 1
    else: gotatg = 0
    goc = 'white'
    if go == gotatg: goc = 'green'
    if go >  gotatg: goc = 'red'
    bandb['GOTA'].configure(text='GOTA %s/%s'%(go,gotatg),background=goc)

def updateqct():
    "update contact count"
    qpb,ppb,qpop,qplg,qpst,tq,score,maxp,cwq,digq,fonq,qpgop,gotaq,nat,sat = \
        qdb.bandrpt()  #xx reduce processing here

    for i,j in (('FonQ','FonQ %4s'%fonq),\
                    ('CW/D','CW/D %4s'%(cwq+digq)),\
                    ('GOTAq','GOTAq %3s'%gotaq)):
        bandb[i].configure(text=j,background='gray')

    if gotaq == 0:
        bandb['GOTAq'].configure(text='NET OK')

    t = ""                      # check for net config trouble
    if net.fills: t = "NEED FILL"
    if net.badauth_rcvd:
        net.badauth_rcvd = 0
        t = "AUTH FAIL"
    if net.pkts_prev == 0 and net.pkts_rcvd == 0:
        t = "RCVP FAIL"
    net.pkts_prev = net.pkts_rcvd
    net.pkts_rcvd = 0
    if net.send_errs: t = "SENDP FAIL"; net.send_errs = 0
    if authk == '':   t = "NO AUTHKEY"
    if node == '': t = "NO NODE"
    if t: bandb['GOTAq'].configure(text=t,background='yellow')

# band button problems on mac xx
# buttons too small
# local band button is also yellow (backgrounds on buttons problematic on mac)
#print os.name

def bandbuttons(w):
    "create band buttons"
    global sv
    a = 0
    sv = StringVar()                # variable to make radiobuttons cooperate
    sv.set(band)
    mac = os.name == 'posix' # detect the mac
    for i in bands:
        b = 0
        for j in modes:
            bm = "%s%s"%(i,j)
            if i == 'off': bm = 'off'   # indicatoron = 0 makes square button with text inside but
                                        # doesn't work well on mac, with value 1 it makes a
                                        # circle alongside the text and works on both
                                        # so detect mac and change it for mac only
            bandb[bm] = Radiobutton(master=w,text=bm,font=fdfont,indicatoron=mac,\
                variable=sv,value=bm,
                command=lambda b=bm:(bandset(b)))
            bandb[bm].grid(row=b,column=a,sticky=NSEW)
            b += 1
        a += 1

    for i,j,px in (('Class',0,5),\
                         ('VHF',1,13),\
                         ('GOTA',2,9)):
        bandb[i] = Button(w,text=i,font=fdfont)
        bandb[i].grid(row=j,column=a,sticky=NSEW)
    w.grid_columnconfigure(a,weight=1)
        
    a += 1
    for i,j in (('FonQ',0),\
                         ('CW/D',1),\
                         ('GOTAq',2)):
        bandb[i] = Button(w,text=i,font=fdfont)
        bandb[i].grid(row=j,column=a,sticky=NSEW)
    w.grid_columnconfigure(a,weight=1)

def rndlet():
    return chr(random.randrange(ord('a'),ord('z')+1))

def rnddig():
    return chr(random.randrange(ord('0'),ord('9')+1))

def testqgen(n):
    while n:
        call = rndlet()+rndlet()+rnddig()+rndlet()+rndlet()+rndlet()
        rpt = rnddig()+rndlet()+' '+rndlet()+rndlet() + ' testQ ' + str(n)
        print call,rpt
        n -= 1

        qdb.qsl(now(),call,band,rpt)
        time.sleep(0.1)

##def reauth(nkey):
##    "reset authentication key, reload, set port"
##    net.setauth(nkey)
##    port = 7373 + ival(nkey[0:4])
##    #xx net.set_port(port)
##    print "port",port
##    logf = "fdlog%s.fdd"%(nkey[0:2])
##    #xx flush & reload log  loadlog(logf)
##    print "new file",logf
# the above is hard, and not correct. have to restart network thread..
# solve this for now by restarting the program..
# global section, main program
# setup persistent globals before GUI

suffix   = ""
call     = ""
band     = "off"
power    = "0"
operator = ""
logger   = ""
node     = ""
authk    = ""
tcp_port = 5100                 # yahoo webcam, works at work
port_base = 7373
tmob     = now()                # time started on band in min
tdwin    = 10                   # time diff window on displaying node clock diffs
showbc   = 0                    # show broadcast
debug    = 0

logdbf   = "fdlog.fdd"          # persistent file copy of log database
logfile  = "fdlog.log"          # printable log file (contest entry)
globf    = "fdlog.dat"          # persistent global file
            
kbuf     = ""                   # keyboard line buffer

loadglob()                      # load persistent globals from file

print

if node == "":
    print "Enter Unique Node ID (use callsign or suffix, eg k6xyz or xyz)"
    print "  (optionally follow with '-<digit>' eg k6xyz-1 or xyz-2)"
    print "  (Use 'gota' for get on the air station - see rules)"
#    print "  (Previous Node ID: '%s')"%node
    print "  (8 characters max):"
    k = string.lower(string.strip(sys.stdin.readline())[:8])
    if k != "":
        node = k
        print

if node == "": node = socket.gethostname()[:8]

## xxxx the node id should be filtered for proper characters

print "  Using Node ID: '%s', to change see property menu"%node
print

# get auth key  auth xxxpppzzz..  fdlogxxx.fdd  port ppp   hashkey (all)
# allow user to select new one, or re-use previous
print "Enter Authentication Key (Return to re-use previous '%s')"%authk
print "  (use 'tst' for testing, two digit year for contest):"
k = string.strip(sys.stdin.readline())
if k != "":
    print "New Key entered, operator and logger cleared"
    authk = k
    operator = ""
    logger   = ""
    print
print "Using Authentication Key: '%s'"%authk
print "Using",authk[0:3],"for setting port, file"
port_offset = ival(authk[3:6])*7
if port_offset == 0: port_offset = ival(authk[0:3])*7

#for each char in port_offset:  xxx
    #port_offset = ((port_offset << 3) + (char & 15)) & 0x0fff

port_base += port_offset
print "Using Network UDP Port:",port_base
print "Using Network TCP Port:",tcp_port
logdbf = "fdlog%s.fdd"%(authk[0:3])
print "Writing Log Journal file:",logdbf

print "Starting Network"
net = netsync()                 # setup net (may want to do an init method xx)
net.setport(port_base)
net.setauth(authk)
print "Saving Persistent Configuration in",globf
saveglob()

print "Time Difference Window (tdwin):",tdwin,"seconds"

print "Starting GUI"

root = Tk()                     # setup Tk GUI

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu,tearoff=0)
menu.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="Save Entry File",command=lambda:contestlog(1))
filemenu.add_command(label="PreView Saved Entry File",\
                     command=lambda:viewtextf('fdlog.log'))
filemenu.add_command(label="View Log Data File",\
                     command=lambda:viewtextf(logdbf))
filemenu.add_command(label="Exit",command=root.quit)

propmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Properties",menu=propmenu)
#
##propmenu.add_command(label="Power",command=pwrdiag)
propmenu.add_command(label="Set Node ID",command=noddiag)
##propmenu.add_command(label="Set AuthKey",command=authdiag)
propmenu.add_command(label="Add Participants",command=newpart.dialog)

logmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Logs",menu=logmenu)
logmenu.add_command(label='Full Log',command=lambda:viewlogf(""))
logmenu.add_command(label='QSTs',command=lambda:viewlogf(r"[*]QST"))
logmenu.add_command(label='GOTA',command=lambda:viewlogfs("gota"))
logmenu.add_command(label='WAS',command=viewwasrpt)

for j in modes:
    m = Menu(logmenu,tearoff=0)
    if   j == 'c': lab = 'CW'
    elif j == 'd': lab = 'Digital'
    elif j == 'p': lab = 'Phone'
    logmenu.add_cascade(label=lab,menu=m)
    for i in bands:
        if i == 'off': continue
        bm = "%s%s"%(i,j)
        m.add_command(label=bm,command=lambda x=bm:(viewlogf(x)))

#menu.add_command(label="Status",command=exit)
#toolsmenu = Menu(menu,tearoff=0)
#menu.add_cascade(label="Tools",menu=toolsmenu)
#toolsmenu.add_command(label="Status",command=exit)
#toolsmenu.add_command(label="Properties",command=propbox)
#toolsmenu.add_command(label="Network",command=exit)
##toolsmenu.add_command(label="Node",command=exit)
##toolsmenu.add_command(label="Authentication",command=exit)
#toolsmenu.add_command(label="Notes",command=exit)
#toolsmenu.add_command(label="Delete Log Entry",command=exit)

helpmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Help",menu=helpmenu)

helpmenu.add_command(label="ReadMe",command=lambda:viewtextf('readme.txt'))
helpmenu.add_command(label="Getting Started",\
            command=lambda:viewtextv(getting_started,'Getting Started'))

helpmenu.add_command(label="Wireless Network",\
            command=lambda:viewtextf('wireless_net.txt','Wireless Network'))

##helpmenu.add_command(label="Group Meeting Agenda",\
##                command=lambda:viewtextf('group_agenda.txt','Group Plan'))
##helpmenu.add_command(label="Group Plans",\
##                command=lambda:viewtextf('group_plan.txt','Group Plan'))
##helpmenu.add_command(label="Group Site Info",\
##                command=lambda:viewtextf('group_site_info.txt','Site Info'))
##helpmenu.add_command(label="Group Handbook",\
##                command=lambda:viewtextf('group_handbook.txt','Group Handbook'))

helpmenu.add_command(label="ARRL FD Rules (pdf)",\
            command=lambda:os.startfile('fdrules.pdf'))
helpmenu.add_command(label="ARRL Sections",\
            command=lambda:viewtextf('arrl_sect.txt','ARRL Sections'))
helpmenu.add_command(label="W1AW Schedule",\
            command=lambda:viewtextf('w1aw.txt','W1AW Schedule'))
helpmenu.add_command(label="ARRL Band Chart (pdf)",\
            command=lambda:os.startfile('bands.pdf'))
helpmenu.add_command(label="ARRL Band Plan",\
            command=lambda:viewtextf('ARRL_Band_Plans.txt',"ARRL Band Plan"))
helpmenu.add_command(label="FD Frequency List",\
            command=lambda:viewtextf('frequencies.txt',"FD Frequency List"))
helpmenu.add_command(label="Propagation Info",\
            command=lambda:viewtextf('propagation.txt',"Propagation Info"))
helpmenu.add_command(label="Time Conversion Chart",\
            command=lambda:viewtextv(tzchart,"Time Conversion Chart"))

##helpmenu.add_command(label="NTS Info",\
##                     command=lambda:viewtextf('nts_info.txt',"NTS Info"))
##helpmenu.add_command(label="NTS Manual (pdf)",\
##                     command=lambda:os.startfile('pscm.pdf'))

helpmenu.add_command(label="FDLog Release Log",\
                     command=lambda:viewtextv(release_log,"Release Log"))
helpmenu.add_command(label="FDLog Set Commands",command=gd.sethelp)
helpmenu.add_command(label="FDLog Manual",\
                     command=lambda:viewtextf('fdlogman.txt',"Manual"))
helpmenu.add_command(label="About FDLog",\
                     command=lambda:viewtextv(about,"About"))

f1 = Frame(root,bd=1)                           # band buttons
bandbuttons(f1)
f1.grid(row=0,columnspan=2,sticky=NSEW)

def setoper(op):
    "set operator"
    global operator
    #print "setoper",op
    ini,name,call = string.split(op,', ')
    operator = "%s: %s, %s"%(ini,name,call)
    opds.config(text=operator)
    saveglob()

def setlog(logr):
    "set logger"
    global logger
    #print "setlog",logr
    ini,name,call = string.split(logr,', ')
    logger = "%s: %s, %s"%(ini,name,call)
    logds.config(text=logger)
    saveglob()

f1b = Frame(root,bd=1)                          # oper logger power window

# Operator
opmb = Menubutton(f1b,text="Operator",font=fdfont,relief='raised',\
                  background='gray')
opmb.grid(row=0,column=0,sticky=NSEW)

opmu = Menu(opmb,tearoff=0)
opmb.config(menu=opmu,direction='below')
opmu.add_command(label="Add New Participant",command=newpart.dialog)

op = operator
if op == "": op = '<select operator>'
opds = Menubutton(f1b,text=op,font=fdfont,relief='raised',\
                  background='gray')
opds.grid(row=0,column=1,sticky=NSEW)
opdsu = Menu(opds,tearoff=0)
opds.config(menu=opdsu,direction='below')

f1b.grid_columnconfigure(1,weight=1)

# Logger
logmb = Menubutton(f1b,text="Logger",font=fdfont,relief='raised',\
                   background='gray')
logmb.grid(row=0,column=3,sticky=NSEW)

logmu = Menu(logmb,tearoff=0)
logmb.config(menu=logmu,direction='below')
logmu.add_command(label="Add New Participant",command=newpart.dialog)

log = logger
if log == "": log = '<select logger>'
logds = Menubutton(f1b,text=log,font=fdfont,relief='raised',\
                   background='gray')
logds.grid(row=0,column=4,sticky=NSEW)

f1b.grid_columnconfigure(4,weight=1)

logdsu = Menu(logds,tearoff=0)
logds.config(menu=logdsu,direction='below')
logdsu.add_command(label="Add New Participant",command=newpart.dialog)

def buildmenus():
    opdsu.delete(0,END)
    logdsu.delete(0,END)
    l = participants.values()
    l.sort()
    for i in l:
       # if re.match(r'.*, delete,',i): continue
        m = re.match(r'[a-z0-9]+, [a-zA-Z ]+, ([a-z0-9]+)$',i)
        if m: opdsu.add_command(label=i, command=lambda n=i:(setoper(n)))
        logdsu.add_command(label=i, command=lambda n=i:(setlog(n)))
    opdsu.add_command(label="Add New Participant",command=newpart.dialog)
    logdsu.add_command(label="Add New Participant",command=newpart.dialog)

# power

def ckpowr():
    global power
    pwr = ival(pwrnt.get())
    if pwr < 0: pwr = "0"
    elif pwr > 1500: pwr = "1500"
    pwrnt.delete(0,END)
    pwrnt.insert(END,pwr)
    if natv.get(): pwr = "%sn"%pwr
    else: pwr = "%s"%pwr
    power = pwr
    print 'power',power
    return 1

def setpwr(p):
    global power
    pwr = ival(p)
    pwrnt.delete(0,END)
    pwrnt.insert(END,pwr)
    if p[-1:] == 'n': powcb.select()
    else: powcb.deselect()
    power = p

pwrmb = Menubutton(f1b,text="Power",font=fdfont,relief='raised',\
                   background='gray')
pwrmb.grid(row=0,column=6,sticky=NSEW)
pwrmu = Menu(pwrmb,tearoff=0)
pwrmb.config(menu=pwrmu,direction='below')
pwrmu.add_command(label='0 Watts',command=lambda:(setpwr('0')))
pwrmu.add_command(label='5 Watts',command=lambda:(setpwr('5')))
pwrmu.add_command(label='5W Natural',command=lambda:(setpwr('5n')))
pwrmu.add_command(label='50 Watts',command=lambda:(setpwr('50')))
pwrmu.add_command(label='50W Natural',command=lambda:(setpwr('50n')))
pwrmu.add_command(label='100 Watts',command=lambda:(setpwr('100')))
pwrmu.add_command(label='100W Natural',command=lambda:(setpwr('100n')))
pwrmu.add_command(label='150 Watts',command=lambda:(setpwr('150')))
pwrmu.add_command(label='150W Natural',command=lambda:(setpwr('150n')))
pwrmu.add_command(label='500 Watts',command=lambda:(setpwr('500')))
pwrmu.add_command(label='1000 Watts',command=lambda:(setpwr('1000')))
pwrmu.add_command(label='1500 Watts',command=lambda:(setpwr('1500')))

pwrnt = Entry(f1b,width=4,font=fdfont,validate='focusout',validatecommand=ckpowr)
pwrnt.grid(row=0,column=7,sticky=NSEW)

Label(f1b,text="W",font=fdfont).grid(row=0,column=8,sticky=NSEW)

natv = IntVar()
powcb = Checkbutton(f1b,text="Natural",variable=natv,command=ckpowr,\
                    font=fdfont,relief='raised',background='gray')
powcb.grid(row=0,column=9,sticky=NSEW)
setpwr(power)

f1b.grid(row=1,columnspan=2,sticky=NSEW)
                                                # log window
logw = Text(root,takefocus=0,height=11,width=80,font=fdmfont,\
            wrap=NONE,setgrid=1)
logw.configure(cursor='arrow')
scroll = Scrollbar(root,command=logw.yview)
logw.configure(yscrollcommand=scroll.set)
logw.grid(row=2,column=0,sticky=NSEW)
scroll.grid(row=2,column=1,sticky=NS)                  
root.grid_rowconfigure(2,weight=1)
root.grid_columnconfigure(0,weight=1)
                                                # command input window
text = Text(root,takefocus=1,height=10,width=80,font=fdmfont,\
            wrap=NONE,setgrid=1)
scrollt = Scrollbar(root,command=text.yview)
text.configure(yscrollcommand=scrollt.set)
text.grid(row=3,column=0,sticky=NSEW)
scrollt.grid(row=3,column=1,sticky=NS)
root.grid_rowconfigure(3,weight=1)

logw.tag_config("b",foreground="blue")
logw.insert(END,"Log Window\n",("b"))

# startup

contestlog(0)                   # define globals
buildmenus()

sms = syncmsg()                 # setup sync message service

qdb = qsodb()                   # init qso database
qdb.loadfile()                  # read log file

print
if node == gd.getv('tmast'):
    print "This Node is the TIME MASTER!!"
    print "THIS COMPUTER'S CLOCK BETTER BE RIGHT (preferably GPS/NTP locked)"
    print "User should Insure that system time is within a second of the"
    print "  correct time and that the CORRECT TIMEZONE is selected (in the OS)"
    print
else:
    print "User should Insure that System Time is within a few seconds of the"
    print "  correct time and that the CORRECT TIMEZONE is selected (in the OS)"
print "To change system timezone, stop FDLog, change the setting, then restart"
print
             
net.start()                     # start threads

renew_title()

text.insert(END,"%s\n"%prog)
text.insert(END,"Set Operator, Logger, Power and Band/Mode!!\n")
text.insert(END,"Contacts on zero power or off band do not count!!\n? for help\n\nReady\n\n")

text.focus()

def showthiscall(call):
    "show the log entries for this call"
    p = call.split('/')
#    print p[0]
    findany = 0
    m,n,g = qdb.cleanlog()
#    print m.values()
    for i in m.values():
#        print i.call
        q = i.call.split('/')
        if p[0] == q[0]:
            if findany == 0: text.insert(END,"\n")
            text.insert(END,"%s\n"%i.prlogln())
            findany = 1
    return findany

def proc_key(ch):
    "process keystroke"
    global kbuf,power,operator,logger,debug,band,node,suffix,tdwin,timeok
    testq = 0
    if ch == '?' and (kbuf == "" or kbuf[0] != '#'):    # ? for help
        mhelp()
        return
    if ch == '\r':          # return, may be cmd or log entry

        if kbuf[:1] == '#':
            qdb.qst(kbuf[1:])
            kbuf = ""
            text.insert(END,'\n')
            return
        # check for valid commands
        if re.match(r'[.]h$',kbuf):      # help request
            m = """
    .band 160/80/40/20/15/10/6/2/220/440/900/1200/sat c/d/p
    .off               change band to off
    .pow <dddn>        power level in integer watts (suffix n for natural)

    .node <call-n>     set id of this log node
    .testq <n>         gen n test qsos use current band etc
    .tdwin <sec>       display node bcasts exceeding this time skew
    .st                this station status
    .re                summary band report
    .ba                station band report
    .pr                generate entry and log files
    .remip <n.n.n.n>   remote ip to join to (TCP) (0.0.0.0 off)
    .timeok n          declare system time good or not (1/0)
    
    .delete <node> <seq_num> <reason>    delete log entry
            """
            viewtextv(m,'Command Help')
            kbuf = ""
            text.insert(END,'\n')
            return

        pwr,s = testcmd(".pow",r"[0-9]{1,4}n?",power)
        if pwr != power: setpwr(pwr)
        netsync.rem_host,s = testcmd('.remip',r'([0-9]{1,3}[.]){3}[0-9]{1,3}',netsync.rem_host)
        if s: globDb.put('remip',netsync.rem_host)
        
##        v,s = testcmd('.remcli',r'[0-1]',netsync.rem_cli)
##        if s and v == 1:
##            pass # start client thread
##        v,s = testcmd('.remsrv',r'[0-1]',netsync.rem_srv)
##        if s and v == 1:
##            pass # start server thread

        v,s = testcmd(".timeok", r"[0-1]", str(timeok))
        timeok = int(v)
                      
        v,s = testcmd(".debug", r"[0-9]+", str(debug))
        debug = int(v)
                      
        v,s = testcmd(".tdwin", r"[0-9]{1,3}", str(tdwin))
        tdwin = int(v)
                      
        v,s = testcmd(".testq", r"[0-9]{1,2}", str(testq))
        testq = int(v)
        if testq: testqgen(testq)

        saveglob()
        renew_title()

        m = re.match(r"[.]set ([a-z0-9]{3,6}) (.*)$", kbuf)
        if m:
            name,val = m.group(1,2)
            r = gd.setv(name,val,now())
            if r: text.insert(END,"\n%s\n"%r)
            else:
                text.insert(END,"\n")
                qdb.globalshare(name,val)   # global to db
            kbuf = ""
            renew_title()
            return
        
        m = re.match(r"[.]band (((160|80|40|20|15|10|6|2|220|440|900|1200|sat)[cdp])|off)", kbuf)
        if m:
            print
            nb = m.group(1)
            kbuf = ""
            text.insert(END,"\n")
            bandset(nb)
            return

        if re.match(r'[.]off$',kbuf):
            bandoff()
            kbuf = ""
            text.insert(END,"\n")
            return

        if re.match(r'[.]ba$',kbuf):
            qdb.bands()
            kbuf = ""
            text.insert(END,"\n")
            return

        if re.match(r'[.]pr$',kbuf):
            contestlog(1)
            text.insert(END," Entry/Log File Written\n")
            kbuf = ""
            return

        p = r'[.]delete ([a-z0-9-]{1,9}) ([0-9]+) (.+)'
        if re.match(p,kbuf):
            m = re.match(p,kbuf)
            nod,seq,reason = m.group(1,2,3)
            qdb.delete(nod,seq,reason)
            kbuf = ""
            text.insert(END,"\n")
            return

        p = r'[.]edit ([a-z0-9]{1,6})'
        if re.match(p,kbuf):
            m = re.match(p,kbuf)
            call = m.group(1)
#            qdb.delete(nod,seq,reason)
            kbuf = ""
            text.insert(END," to edit use mouse click on log entry\n")
            return

        if re.match(r'[.]node',kbuf):
            if band != 'off':
                text.insert(END,"\nSet band off before changing node id\n")
                kbuf = ""
                return
            node,s = testcmd(".node", r"[a-z0-9-]{1,8}",node)
            if s: renew_title()
            #text.insert(END,"\n")
            return

        if re.match(r'[.]st$',kbuf):           # status  xx mv to gui
            print
            print
            print "FD Call   %s"%string.upper(gd.getv('fdcall'))
            print "GOTA Call %s"%string.upper(gd.getv('gcall'))
            print "FD Report %s %s"%(string.upper(gd.getv('class')),gd.getv('sect'))
            print "Band      %s"%band
            print "Power     %s"%power
            print "Operator  %s"%operator
            print "Logger    %s"%logger
            print "Node      %s"%node
            if authk != "" and node != "": print "Net       enabled"
            else: print "Net       disabled"
            print
            kbuf = ""
            text.insert(END,"\n")
            return

        if re.match(r'[.]re$',kbuf):           # report  xx mv to gui
            print
            print "  band  cw q   pwr dig q   pwr fon q   pwr"
            qpb,ppb,qpop,qplg,qpst,tq,score,maxp,cwq,digq,fonq,qpgop,gotaq,nat,sat = qdb.bandrpt()
            for b in (160,80,40,20,15,10,6,2,220,440,1200,'sat','gota'):
                print "%6s"%b,
                for m in 'cdp':
                    bm = "%s%s"%(b,m)
                    print "%5s %5s"%(qpb.get(bm,0),ppb.get(bm,0)),
                print
            print
            print "%s total Qs, %s QSO points,"%(tq,score),
            print maxp,"watts maximum power"
            kbuf = ""
            text.insert(END,"\n")
            return

        if kbuf and kbuf[0] == '.':                     # detect invalid command
            text.insert(END," Invalid Command\n")
            kbuf = ""
            text.insert(END,"\n")
            return

        # check for valid contact
        
        if (ch == '\r'):
            stat,ftm,pfx,sfx,call,xcall,rept = qdb.qparse(kbuf)
            if stat == 5:                               # whole qso parsed
                kbuf = ""
                if len(node) < 3:
                    text.insert(END," ERROR, set .node <call> before logging\n")
                elif qdb.dupck(xcall, band):             # dup check
                    text.insert(END," DUP on band %s\n"%band)
                else:
                    text.insert(END," QSL")
                    em = ''
                    if band == "off": em += " Band "
                    if ival(power) < 1: em += " Power "
                    if len(operator) < 2: em += " Operator "
                    if len(logger) < 2: em += " Logger "
                    if em: text.insert(END,"- WARNING: ( %s ) NOT SET"%em)
                    text.insert(END,"\n")
                    tm = now()
                    if ftm:                             # force timestamp
                        tm = tm[0:4]+ftm[0:8]+tm[11:]   # yymmdd.hhmmss
                    qdb.qsl(tm,xcall,band,rept)
            elif stat == 4:
                kbuf = ""
                if showthiscall(call) == 0:
                    text.insert(END," none found\n")
            return

    if ch == '\x1b':            # escape quits this input line
        text.insert(END," ESC -aborted line-\n")
        kbuf = ""
        return
        
    if ch == '\b':              # backspace erases char
        if kbuf != "":
            kbuf = kbuf[0:-1]
            text.delete('end - 2 chars')
        return
    
    if ch == ' ':               # space, check for prefix/suffix/call

        stat,tm,pfx,sfx,call,xcall,rept = qdb.qparse(kbuf)
        
        if stat == 2:           # suffix, dup check
            suffix = kbuf
            kbuf = ""
            r = qdb.sfx2call(suffix,band)
            if not r: r = 'None'
            text.insert(END,": %s on band '%s'\n"%(r,band))
            return

        if stat == 3:           # prefix, combine w suffix
            stat,tm,pfx,sfx,call,xcall,rept = qdb.qparse(kbuf+suffix)
            if stat == 4:       # whole call
                kbuf += suffix
                text.insert(END,sfx)# fall into call dup ck
                
        if stat == 4:           # whole call, dup chk
            if qdb.dupck(xcall,band):
                text.insert(END," DUP on band %s"%band)
                showthiscall(call)
                kbuf = ""
            else:
                kbuf += ' '
                text.insert(END,ch)
                if showthiscall(call):      # may want to make this optional due to speed issues
                    text.insert(END,"%s "%xcall)
            return

    buf = kbuf + ch             # echo & add legal char to kbd buf
    if len(buf) < 50:
        if buf[0] == '.':
            if re.match(r'[ a-zA-Z0-9.,/@-]{0,45}$',ch):
                kbuf = buf
                text.insert(END,ch)

        elif buf[0] == '#':
            if re.match(r'#[ a-zA-Z0-9.,?/!@$;:+=%&()-]{0,40}$',buf):
                kbuf = buf
                text.insert(END,ch)

        else:
            stat,tm,pfx,sfx,call,xcall,rept = qdb.qparse(buf)
            if stat > 0 and len(buf) < 50:
                kbuf = buf
                text.insert(END,ch)

def kevent(event):
    "keyboard event handler"
##    print "event '%s' '%s' '%s'"%(event.type,event.keysym,event.keysym_num)
    k = event.keysym_num
    if k > 31 and k < 123:      # space to z
        proc_key(chr(event.keysym_num))
    elif k == 65288:            # backspace
        proc_key('\b')
    elif k == 65307:            # ESC
        proc_key('\x1b')
    elif k == 65293:            # return
        proc_key('\r')
    text.see(END)               # insure that it stays in view
    return "break"              # prevent further processing on kbd events

def focevent(e):
    text.mark_set('insert',END)
    return "break"

class Edit_Dialog(Toplevel):
    'edit log entry dialog'
    def __init__(self,parent,node,seq):
        s = '%s.%s'%(node,seq)
        self.node,self.seq = node,seq
        if qdb.byid[s].band[0] == '*': return
        top = self.top = Toplevel(parent)
        #Toplevel.__init__(self,parent)
        #self.transient(parent)     # avoid showing as separate item
        tl = Label(top,text='Edit Log Entry',font=fdbfont,bg='gray',relief=RAISED)
        tl.grid(row=0,columnspan=2,sticky=EW)
        tl.grid_columnconfigure(0,weight=1)
        Label(top,text='Date',font=fdbfont).grid(row=1,sticky=W)
        #Label(top,text='Time',font=fdbfont).grid(row=2,sticky=W)
        Label(top,text='Band',font=fdbfont).grid(row=3,sticky=W)
        #Label(top,text='Mode',font=fdbfont).grid(row=4,sticky=W)
        Label(top,text='Call',font=fdbfont).grid(row=5,sticky=W)
        Label(top,text='Report',font=fdbfont).grid(row=6,sticky=W)
        Label(top,text='Power',font=fdbfont).grid(row=7,sticky=W)
        #Label(top,text='Natural',font=fdbfont).grid(row=8,sticky=W)
        Label(top,text='Operator',font=fdbfont).grid(row=9,sticky=W)
        Label(top,text='Logger',font=fdbfont).grid(row=10,sticky=W)
        self.de = Entry(top,width=13,font=fdbfont)
        self.de.grid(row=1,column=1,sticky=W,padx=3,pady=2)
        self.de.insert(0,qdb.byid[s].date)
        #self.de.insert(0,qdb.byid[s].date[:6])
##             self.src,self.seq,
##             self.date,self.band,self.call,self.rept,
##             self.powr,self.oper,self.logr
##        self.te = Entry(top,width=6,font=fdbfont)
##        self.te.grid(row=2,column=1,sticky=W,padx=3,pady=2)
##        self.te.insert(0,qdb.byid[s].date[-6:])
        self.be = Entry(top,width=5,font=fdbfont)
        self.be.grid(row=3,column=1,sticky=W,padx=3,pady=2)
        #self.be.configure(bg='yellow') #test yes works
        self.be.insert(0,qdb.byid[s].band)
##        self.me = Entry(top,width=1,font=fdbfont)
##        self.me.grid(row=4,column=1,sticky=W,padx=3,pady=2)
##        self.me.insert(0,qdb.byid[s].band[-1])
        self.ce = Entry(top,width=11,font=fdbfont)
        self.ce.grid(row=5,column=1,sticky=W,padx=3,pady=2)
        self.ce.insert(0,qdb.byid[s].call)
        self.re = Entry(top,width=24,font=fdbfont)
        self.re.grid(row=6,column=1,sticky=W,padx=3,pady=2)
        self.re.insert(0,qdb.byid[s].rept)
        self.pe = Entry(top,width=5,font=fdbfont)
        self.pe.grid(row=7,column=1,sticky=W,padx=3,pady=2)
        self.pe.insert(0,qdb.byid[s].powr)
##        self.ne = Entry(top,width=1,font=fdbfont)
##        self.ne.grid(row=8,column=1,sticky=W,padx=3,pady=2)
##        self.ne.insert(0,'n')
        self.oe = Entry(top,width=3,font=fdbfont)
        self.oe.grid(row=9,column=1,sticky=W,padx=3,pady=2)
        self.oe.insert(0,qdb.byid[s].oper)
        self.le = Entry(top,width=3,font=fdbfont)
        self.le.grid(row=10,column=1,sticky=W,padx=3,pady=2)
        self.le.insert(0,qdb.byid[s].logr)
        bf = Frame(top)
        bf.grid(row=11,columnspan=2,sticky=EW,pady=2)
        bf.grid_columnconfigure((0,1,2),weight=1)
        db = Button(bf,text=' Delete ',font=fdbfont,command=self.dele)
        db.grid(row=1,sticky=EW,padx=3)
        sb = Button(bf,text=' Save ',font=fdbfont,command=self.submit)
        sb.grid(row=1,column=1,sticky=EW,padx=3)
        qb = Button(bf,text=' Quit ',font=fdbfont,command=self.quitb)
        qb.grid(row=1,column=2,sticky=EW,padx=3)
        #self.wait_window(top)
    def submit(self):
        print 'submit edits'
        error = 0
        t = self.de.get().strip()               # date time
        print t
        self.de.configure(bg='white')
        m = re.match(r'[0-9]{6}\.[0-9]{4,6}$',t)
        if m:
            newdate = t + '00'[:13-len(t)]
            print newdate
        else:
            self.de.configure(bg='yellow')
            error += 1
        t = self.be.get().strip()               # band mode
        self.be.configure(bg='white')
        m = re.match(r'(160|80|40|20|15|10|6|2|220|440|900|1200|sat)[cdp]$',t)
        if m:
            newband = t
            print newband
        else:
            self.be.configure(bg='yellow')
            error += 1
        t = self.ce.get().strip()               # call
        self.ce.configure(bg='white')
        m = re.match(r'[a-z0-9/]{3,11}$',t)
        if m:
            newcall = t
            print newcall
        else:
            self.ce.configure(bg='yellow')
            error += 1
        t = self.re.get().strip()               # report
        self.re.configure(bg='white')
        m = re.match(r'.{4,24}$',t)
        if m:
            newrept = t
            print newrept
        else:
            self.re.configure(bg='yellow')
            error += 1
        t = self.pe.get().strip().lower()       # power
        self.pe.configure(bg='white')
        m = re.match(r'[0-9]{1,4}n{0,1}$',t)
        if m:
            newpowr = t
            print newpowr
        else:
            self.pe.configure(bg='yellow')
            error += 1
        t = self.oe.get().strip().lower()       # operator
        self.oe.configure(bg='white')
        if participants.has_key(t):
            newopr = t
            print newopr
        else:
            self.oe.configure(bg='yellow')
            error += 1
        t = self.le.get().strip().lower()       # logger
        self.le.configure(bg='white')
        if participants.has_key(t):
            newlogr = t
            print newlogr
        else:
            self.le.configure(bg='yellow')
            error += 1
        if error == 0:
            # delete and enter new data
            print 'no errors, enter data'
            reason = 'edited'
            qdb.delete(self.node,self.seq,reason)
            qdb.postnew(newdate,newcall,newband,newrept,newopr,newlogr,newpowr)
            self.top.destroy()
            text.insert(END," EDIT Successful\n")
    def dele(self):
        print 'delete entry'
        reason = 'deleteclick'
        qdb.delete(self.node,self.seq,reason)
        self.top.destroy()
    def quitb(self):
        print 'quit - edit aborted'
        self.top.destroy()
        
def edit_dialog(node,seq):
    'edit log entry'
    # validate, make sure entry is not already edited,
    # and that it is a proper entry to edit at all
    ed = Edit_Dialog(root,node,seq)
    #ed.wait_window(ed)
    #wait for it

def log_select(e):
    'process mouse left-click on log window'
##    print e.x,e.y
    t = logw.index("@%d,%d"%(e.x,e.y))
##    print t
    line,col = t.split('.')
    line = int(line)
##    print line
    logtext = logw.get('%d.0'%line,'%d.82'%line)
##    print logtext
    seq = logtext[65:69].strip()
    if len(seq) == 0: return 'break'
    seq = int(seq)
    stn = logtext[69:].strip()
    if len(stn) == 0: return 'break'
    print 'edit',stn,seq
    if stn == node:             # only edit my own Q's
        edit_dialog(stn,seq)
    else: print "Cannot Edit other node's Q"
    return 'break'

updatect = 0

def update():
    "timed updater"
    global updatect

    root.after(1000,update)         # reschedule early for reliability

    sms.prout()                     # 1 hz items
    updatebb()
    net.si.age_data()
    mclock.adjust()

    if mclock.level == 0:           # time master broadcasts time more frequently
        net.bcast_time()

    updatect += 1

   # if (updatect % 5) == 0:         # 5 sec
       # net.bcast_now()
        
    if (updatect %10) == 0:         # 10 sec
        updateqct()   # this updates rcv packet fail
        renew_title() # this sends status broadcast
        
    if (updatect %30) == 0:         # 30 sec
        mclock.update()

    if updatect > 59:               # 60 sec
        updatect = 0

root.bind('<ButtonRelease-1>',focevent)
text.bind('<KeyPress>',kevent)
logw.bind('<KeyPress>',kevent)      # use del key for?xx
logw.bind('<Button-1>',log_select)  # start of log edit

root.after(1000,update)             # 1 hz activity

root.mainloop()                     # gui up, returns on exit

print "\nShutting down"

band = 'off'                        # gui down, xmt band off, preparing to quit
net.bcast_now()                     # push band out
time.sleep(0.2)
saveglob()                          # save globals
print "  globals saved"
time.sleep(0.2)
net.close_all()                     # close ports
time.sleep(0.2)
print "  ports closed"

print "\n\nFDLog is shut down, you should close this console window now"
time.sleep(0.5)

os._exit(1)                         # kill the process somehow?

# this is the end of code, only comments below here
# test procedure (draft)
# test against old standard version (UDP)
# test against self version (UDP and TCP)
# test operator, logger, power, natural, band set, seeing other band
# test qsos
# test editing a qso
# test filling using .testq 10 on each machine (note does bcasts so may need to shut down FDLog, do testq, start up FDLog to get fill testing)
# test generating a report
# test time sync
#   .set tmast <node>

# Suggestions
# FD 2005 pre-meeting
#
#  thought - make the RCVP button bring up a description of the errors there
#  and the other buttons above that similar - bring up descriptions of what
#  they mean..
#
# FD 2004 notes
#   used version 1.125 on FD04.
#   version 1.126 is the same with comments/bugs/etc added
#
# question - where are operator/station scores? make easier to see??
#
# feature request - vhf contest version (Kit) DONE,
#   or general contests (Frank)
#   have a .set contest variable DONE
#
# feature request - editing previous input functionality ***** DONE
#
# feature request - editing current input (out of order input)
#   cursor keys left, right, char->insert, delete
#   tab to cycle words?
#   refrain from syntax checking while editing?
#
# feature request - generate port number w/o field? what happens if port is
#   already in use? dynamic port searching?? done.
#
# suggestion - better frequency chart. (Cal)
#
# issue - probably does not handle the 1d-1d contacts properly?
#
# consider band timeout - 30 minutes w/o contact releases band?
#
# old idea - Eric - balloon popup on band shows who is there

# Short List
#
# add node list display after db read during startup?
#
# raise GUI to front during startup (tried, don't know how)
#
# someday should make any attempt to log q with callsign that is in the
# operator list come up a dup without including them in the dup sheet!

# thoughts 7/30/02
#
# mv info files to info dir
# set up autodiscovery to build menus
# do same for manuals
# actually, let's move most of the doc stuff out
# to a web tree under the program, and take it
# completely out of the program proper

##ToDo, Brainstorming List
##
##  remote test mode (changed to tcp due to firewalls)(DONE 5/2013)
##    .remip <addr>
##    add rem addrs to list
##      time them out
##    bcast to rem addrs
##
##  add phonetic alphabet display
##  
##  .st to popup
##  
##  limit call width in log display (done?)
##  stop log processing every 10 seconds to get score. do less. count.
##  dupcheck on 0 power not working. ok?
##  
##  document .set system better
##  
##  Weo suggested making Control-C text copy/paste work.
##  Eric suggested show stations on band with bubble dialog
##    (also q count etc)
##  do better job of reporting net status & info
##  gui    
##    sta/oper/logr/pwr/q dsply in lower rt?
##    delete log entry dialog box???
##    more reports
##  add natural power comment section to entry
##  code cleanup
##  greplog .grep <match>

# wa6nhc 5/2013 suggests precluding site operators from being logged as Q's

# some foreign callsigns not supported properly (really a feature request)
#   8a8xx
#   need to change the way this works
#   define a suffix as trailing letters
#   prefix as anything ending in digits
#   bring down a previous suffix with a character such as ' or .

# 2014 suggestions
#
# add a comparison to previous year group scores

# Code Parking

### temporary testing for the future (moved from the top)
### may want to use JSON for transport later on
##
##import json
##
##msg = {}
##msg['S'] = 'akb-2'
##msg['N'] = '202'
##msg['T'] = 'Q'
##msg['q'] = 'w1aw'
##msg['d'] = '20130621:0034'
##msg['b'] = '40'
##msg['m'] = 'P'
##
##msg2 = {}
##msg2['T'] = 's'
##msg2['S'] = 'akb-2'
##
##print json.dumps((msg,msg2),separators=(',',':'))
##
##raise"quit"
# eof
