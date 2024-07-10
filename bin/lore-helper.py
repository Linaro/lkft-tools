#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import sys
import re

sys.path.append(os.path.join(sys.path[0], "../", "lib"))
import stable_email  # noqa: E402


def get_number(s):
    match = re.search(r"(\d+)", s)
    if match:
        return int(match.group(1))
    else:
        return None


def is_superceded(version_ref, version_this):
    if (
        (version_ref["major"] == version_this["major"])
        and (version_ref["minor"] == version_this["minor"])
        and (version_ref["patch"] == version_this["patch"])
        and (version_ref["rc"] > version_this["rc"])
    ):
        return True
    return False


if __name__ == "__main__":
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("action", help="Action to perform: list-rcs, reply, show")
    ap.add_argument(
        "-C",
        "--lore",
        help="Directory with the LORE Git clone.",
        type=str,
        default=".",
    )
    ap.add_argument("-i", "--id", help="Show or reply to this email ID.", type=str)
    ap.add_argument(
        "-g",
        "--review-request",
        help="Get review-request email ID for the given RC. E.g.: 5.10.152-rc1",
        type=str,
    )
    ap.add_argument(
        "--reply-to",
        help="Who should receive the reply. Can be one of 'to', 'all', or 'none'. Default it 'all'.",
        type=str,
        default="all",
    )
    ap.add_argument("--report", help="Text report (file) to include in reply.")
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
            tzinfo=datetime.UTC
        ),
    )
    args = ap.parse_args()

    NOW = datetime.datetime.now(datetime.UTC)
    if not args.since:
        limit = datetime.timedelta(days=args.days)
        DT_LIMIT = NOW - limit
    else:
        DT_LIMIT = args.since

    if args.action == "reply" and args.id:
        msg = stable_email.get_email_by_id(args.id, DT_LIMIT, git_dir=args.lore)
        email_date = msg["Date"]
        email_from = msg["From"]
        email_to = msg["To"]
        email_cc = msg["Cc"]
        email_subject = msg["Subject"]
        email_body = msg.get_payload()

        quoted_email_body = stable_email.quote_email(email_body, trim_review=True)

        recipients = email_from
        if args.reply_to == "all":
            if email_to:
                recipients += ", " + email_to
            if email_cc:
                recipients += ", " + email_cc
        if args.reply_to == "none":
            recipients = ""

        headers = []
        headers.append(f"X-Mailer: lkft-tools")
        headers.append(f"In-reply-to: <{args.id}>")
        headers.append("From: Linux Kernel Functional Testing <lkft@linaro.org>")
        if recipients:
            headers.append(f"To: {recipients}")
        headers.append(f"Subject: Re: {email_subject}")
        body = f"On {email_date}, {email_from} wrote:\n"
        body += quoted_email_body
        body += "\n\n"
        # print(body)
        reply_msg = "\n".join(headers) + "\n\n" + body
        if args.report:
            fh = open(args.report, "r")
            report_content = fh.read()
            reply_msg += report_content
        print(reply_msg)
        sys.exit(0)

    if args.action == "show" and args.id:
        stable_email.print_email_by_id(args.id, DT_LIMIT, git_dir=args.lore)
        sys.exit(0)

    # Find review requests coming from Greg
    from_greg = stable_email.get_review_requests(DT_LIMIT, git_dir=args.lore)

    # Find oldest review request (will stop next search at this point)
    oldest = NOW
    for msgid in from_greg.keys():
        commit = from_greg[msgid]["request"]
        dt = commit.committed_datetime
        if dt < oldest:
            oldest = dt

    # Look for replies to Greg's emails
    from_greg = stable_email.get_review_replies(oldest, from_greg, git_dir=args.lore)

    if args.review_request:
        for msgid in from_greg.keys():
            request_commit = from_greg[msgid]["request"]
            r = stable_email.Review(request_commit, None)
            if r.get_linux_version() == args.review_request:
                print(msgid.strip("<>"))
                sys.exit(0)
        print("Message not found: " + args.review_request)
        sys.exit(1)

    # print("* Computing elapsed time...")
    rclog = {}
    for msgid in from_greg.keys():
        request_commit = from_greg[msgid]["request"]

        r = stable_email.Review(request_commit, None)
        date = r.get_date()
        linux_ver_dict = r.get_linux_version_dict()
        linux_ver = linux_ver_dict["str"]

        replies = "Pending"

        # See if this has been superceded
        for in_msgid in from_greg.keys():
            in_request_commit = from_greg[in_msgid]["request"]
            in_r = stable_email.Review(in_request_commit, None)
            in_linux_ver_dict = in_r.get_linux_version_dict()
            if is_superceded(in_linux_ver_dict, linux_ver_dict):
                replies = "Superceded"
                break

        # Did we record any review replies?
        if "replies" in from_greg[msgid]:

            # If so, complete the Review object
            for reply_msg in from_greg[msgid]["replies"]:
                replies = "Replied"
                r.reply = reply_msg
                sla = r.get_sla_mark()

                # Print summary
                if r.get_regressions_detected():
                    replies = "Regressions"

        print(
            "%s,stable,%s,%s,%s"
            % (
                date,
                linux_ver,
                replies,
                r.get_sla_mark(),
            )
        )
