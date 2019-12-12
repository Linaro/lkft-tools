#!/usr/bin/env python3

import argparse
import datetime
import os
import pytz
import sys

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import stable_email  # noqa: E402


if __name__ == "__main__":
    # Arguments
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=False)
    g.add_argument(
        "-d",
        "--days",
        help="Number of days back to look at; default is 7.",
        type=int,
        default=7,
    )
    g.add_argument(
        "-s",
        "--since",
        help="Look as far as the given date (UTC).",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").replace(
            tzinfo=pytz.utc
        ),
    )
    args = ap.parse_args()

    NOW = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if not args.since:
        limit = datetime.timedelta(days=args.days)
        DT_LIMIT = NOW - limit
    else:
        DT_LIMIT = args.since

    # Find review requests coming from Greg
    from_greg = stable_email.get_review_requests(DT_LIMIT)

    # Find oldest review request (will stop next search at this point)
    oldest = NOW
    for msgid in from_greg.keys():
        msg = from_greg[msgid]["request"]
        dt = stable_email.msg_get_dt(msg)
        if dt < oldest:
            oldest = dt
    print("Oldest: %s" % oldest)

    # Look for replies to Greg's emails
    from_greg = stable_email.get_review_replies(oldest, from_greg)

    print("* Computing elapsed time...")
    rclog = {}
    for msgid in from_greg.keys():
        request_msg = from_greg[msgid]["request"]

        r = stable_email.Review(request_msg, None)
        ymd = r.get_ymd()
        linux_ver = r.get_linux_version()

        # Did we record any review replies?
        if "replies" in from_greg[msgid]:

            # If so, complete the Review object
            for reply_msg in from_greg[msgid]["replies"]:
                r.reply = reply_msg
                sla = r.get_sla_mark()

                # Print summary
                if not r.get_regressions_detected():
                    regression_summary = "No regressions reported"
                else:
                    regression_summary = "REGRESSIONS REPORTED!"
                    linux_ver += "-REGRESSIONS"

                print(
                    "[%s] %s: %s (%s) %s (from %s)"
                    % (
                        ymd,
                        linux_ver,
                        r.get_elapsed_time(),
                        r.get_sla_mark(),
                        regression_summary,
                        r.get_from(),
                    )
                )

            if ymd not in rclog:
                rclog[ymd] = {sla: [linux_ver]}
            else:
                if sla in rclog[ymd]:
                    rclog[ymd][sla].append(linux_ver)
                else:
                    rclog[ymd][sla] = [linux_ver]

        else:
            print("[%s] %s: No reply yet (%s)" % (ymd, linux_ver, r.get_sla_mark()))

    # cheap json
    print(str(rclog).replace("'", '"'))

    # {'2019-08-09': {'<48h': ['4.4.189']}, '2019-08-08': {'<24h': ['5.2.8', '4.19.66', '4.14.138']}}
    print("")
    for date, slas in rclog.items():
        print("### {}".format(date))
        for sla, releases in slas.items():
            print("#### {}".format(" ".join(releases)))
            print("<!-- sla {} {} -->".format(sla.strip('h'), len(releases)))
            print("- XXX in {}".format(sla))
        print("")
