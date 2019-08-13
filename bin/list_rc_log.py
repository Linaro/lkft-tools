#!/usr/bin/env python3

import argparse
import datetime
import email
import email.policy
import subprocess

import dateutil.parser
import pytz


def is_greg_request(m):
    if "X-KernelTest-Branch" in m and "in-reply-to" not in m:
        return True
    return False


def is_beyond_time_search(m, limit):
    dt = msg_get_dt(m)
    if dt < limit:
        return True
    return False


def msg_get_dt(m):
    if "date" in m:
        return dateutil.parser.parse(m["date"])
    else:
        return None


def get_version(m):
    sub = m["subject"]
    if not sub.endswith("-stable review"):
        return False
    if not sub.startswith("["):
        return False
    sub1 = sub.replace("-stable review", "")
    return sub1[sub1.rfind(" ") + 1 :]


def get_email_from_git_ref(ref):
    email_bytes = subprocess.check_output(["/usr/bin/git", "show", ref])
    return email.message_from_bytes(
        email_bytes, policy=email.policy.EmailPolicy(utf8=True)
    )


def get_review_requests(dt_limit):
    print(
        "* Looking for review requests after %s..."
        % dt_limit.strftime("%Y-%m-%d %H:%M UTC")
    )
    fg = {}
    x = 0
    while True:
        headn = "HEAD~%d:m" % x

        # Get the email message proper
        msg = get_email_from_git_ref(headn)

        # Limit search
        if is_beyond_time_search(msg, DT_LIMIT):
            print("Done. Found %d review requests in %d messages." % (len(fg), x))
            break

        # Look for Greg's stable RC review requests
        if is_greg_request(msg):
            print("Found: %s" % msg["subject"])
            fg[msg["message-id"]] = {"request": msg}
        x += 1

    # print(str(fg))
    return fg


def get_review_replies(dt_limit, fg):
    print("* Looking for replies...")
    x = 0
    while True:
        headn = "HEAD~%d:m" % x

        # Get the email message proper
        msg = get_email_from_git_ref(headn)

        # Limit search
        if is_beyond_time_search(msg, oldest):
            print("Done. (Looked at %d messages.)" % x)
            break

        if "in-reply-to" in msg and msg["in-reply-to"] in fg:
            inrt = msg["in-reply-to"]
            efrom = msg["from"]
            # if 'gregkh' not in efrom:
            if "linaro.org" in efrom:
                print("%d: %s" % (x, efrom))
                if "replies" in fg[inrt]:
                    fg[inrt]["replies"].append(msg)
                else:
                    fg[inrt]["replies"] = [msg]

        x += 1

    # print(str(from_greg))
    return fg


class Review(object):
    request = None
    reply = None
    elapsed_time = None

    def __init__(self, req, reply):
        self.request = req
        self.reply = reply

    def calc_elapsed_time(self):
        request_time = msg_get_dt(self.request)
        if self.reply:
            reply_time = msg_get_dt(self.reply)
        else:
            reply_time = NOW

        # This is a datetime.timedelta
        diff = reply_time - request_time
        self.elapsed_time = diff

    def get_elapsed_time(self):
        self.calc_elapsed_time()

        days = self.elapsed_time.days
        hours = days * 24
        hours += int(self.elapsed_time.seconds / 3600)
        minutes = int((self.elapsed_time.seconds % 3600) / 60)
        return "%d:%02d" % (hours, minutes)

    def get_sla_mark(self):
        self.calc_elapsed_time()
        et = self.elapsed_time
        hours = et.seconds / 3600
        if et.days >= 2:
            return ">48h"
        elif et.days < 2 and et.days >= 1:
            return "<48h"
        elif et.days < 1 and hours >= 8:
            return "<24h"
        else:
            return "<8h"

    def get_linux_version(self):
        sub = self.request["subject"]
        if not sub.endswith("-stable review"):
            return None
        if not sub.startswith("["):
            return None
        sub1 = sub.replace("-stable review", "")
        return sub1[sub1.rfind(" ") + 1 :]

    def get_ymd(self):
        dt = msg_get_dt(self.request)
        return dt.strftime("%Y-%m-%d")

    def get_from(self):
        return self.reply["from"]

    def get_id(self):
        return self.reply["message-id"]

    def get_regressions_detected(self):
        mfrom = self.reply["from"]
        if "linaro.org" not in mfrom:
            return False

        body = self.reply.get_payload().lower()
        if "no regressions on " in body:
            return False
        else:
            return True

    def get_has_reply(self):
        if self.reply:
            return True
        return False


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
    from_greg = get_review_requests(DT_LIMIT)

    # Find oldest review request (will stop next search at this point)
    oldest = NOW
    for msgid in from_greg.keys():
        msg = from_greg[msgid]["request"]
        dt = msg_get_dt(msg)
        if dt < oldest:
            oldest = dt
    print("Oldest: %s" % oldest)

    # Look for replies to Greg's emails
    from_greg = get_review_replies(oldest, from_greg)

    print("* Computing elapsed time...")
    rclog = {}
    for msgid in from_greg.keys():
        request_msg = from_greg[msgid]["request"]

        r = Review(request_msg, None)
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
            print("<!-- sla {} {} -->".format(sla, len(releases)))
            print("- XXX in {}".format(sla))
        print("")
