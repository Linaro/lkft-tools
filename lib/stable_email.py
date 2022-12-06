#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This library is used to parse emails from a public-inbox feed. It is used
# specifically for the linux stable mailing list

import email
import email.policy

import git

OLD_MSGS_STREAK = 10


def commit_to_email_message(commit):
    raw_msg = commit.tree["m"].data_stream.read()
    m = email.message_from_bytes(raw_msg, policy=email.policy.EmailPolicy(utf8=True))
    return m


def is_review_request(commit):
    if commit.author.email in ["gregkh@linuxfoundation.org", "sashal@kernel.org"]:
        m = commit_to_email_message(commit)
        if "X-KernelTest-Branch" in m and "in-reply-to" not in m:
            return m
    return False


def is_beyond_time_search(commit, limit):
    if commit.committed_datetime < limit:
        return True
    return False


def get_version(m):
    sub = m["subject"]
    if not sub.endswith(" review"):
        return False
    if not sub.startswith("["):
        return False
    sub = sub.replace("-stable review", "")
    sub1 = sub.replace(" review", "")
    return sub1[sub1.rfind(" ") + 1 :]


def get_review_requests(dt_limit, git_dir="."):
    # print(
    #     "* Looking for review requests since %s..."
    #     % dt_limit.strftime("%Y-%m-%d %H:%M UTC")
    # )
    fg = {}
    x = 0
    repo = git.Repo(git_dir)
    commits = repo.iter_commits("HEAD")

    older_streak = 0
    for commit in commits:
        # Limit search
        if is_beyond_time_search(commit, dt_limit):
            older_streak += 1
        else:
            older_streak = 0

        if older_streak >= OLD_MSGS_STREAK:
            # print("Done. Found %d review requests in %d messages." % (len(fg), x))
            break

        # Look for Greg's stable RC review requests
        msg = is_review_request(commit)
        if msg:
            # print("Found: %s" % commit.summary)
            fg[msg["message-id"]] = {"request": commit}
        x += 1

    return fg


def get_review_replies(oldest, fg, git_dir="."):
    # print("* Looking for replies...")
    x = 0
    repo = git.Repo(git_dir)
    commits = repo.iter_commits("HEAD")

    older_streak = 0
    for commit in commits:
        # Limit search
        if is_beyond_time_search(commit, oldest):
            older_streak += 1
        else:
            older_streak = 0

        if older_streak >= OLD_MSGS_STREAK:
            # print("Done. (Looked at %d messages.)" % x)
            break

        msg = commit_to_email_message(commit)

        if "in-reply-to" in msg and msg["in-reply-to"] in fg:
            inrt = msg["in-reply-to"]
            efrom = msg["from"]
            # if 'gregkh' not in efrom:
            if "linaro.org" in efrom:
                # print("%d: %s %s" % (x, msg["subject"], efrom))
                if "replies" in fg[inrt]:
                    fg[inrt]["replies"].append(commit)
                else:
                    fg[inrt]["replies"] = [commit]

        x += 1

    # print(str(from_greg))
    return fg


def print_email_by_id(email_id, dt_limit, git_dir="."):
    m = get_email_by_id(email_id, dt_limit, git_dir)
    print(m.as_string(policy=email.policy.default))


def get_email_by_id(email_id, dt_limit, git_dir="."):
    x = 0
    repo = git.Repo(git_dir)
    commits = repo.iter_commits("HEAD")

    older_streak = 0
    for commit in commits:
        # Limit search
        if is_beyond_time_search(commit, dt_limit):
            older_streak += 1
        else:
            older_streak = 0

        if older_streak >= OLD_MSGS_STREAK:
            # print("Done. Found %d review requests in %d messages." % (len(fg), x))
            break

        # Look for Greg's stable RC review requests
        m = commit_to_email_message(commit)
        if m["message-id"] == f"<{email_id}>":
            return m

    return None


def quote_email(body, trim_review=False):
    quoted_email_body_list = []
    for s in body.splitlines():
        if trim_review and s == "-------------":
            break
        quoted_email_body_list.append("> " + s)

    return "\n".join(quoted_email_body_list)


class Review(object):
    request = None
    reply = None
    elapsed_time = None

    def __init__(self, req, reply):
        self.request = req
        self.reply = reply

    def calc_elapsed_time(self):
        request_time = self.request.committed_datetime
        if self.reply:
            reply_time = self.reply.committed_datetime

            # This is a datetime.timedelta
            self.elapsed_time = reply_time - request_time

    def get_elapsed_time(self):
        self.calc_elapsed_time()

        if not self.elapsed_time:
            return None

        days = self.elapsed_time.days
        hours = days * 24
        hours += int(self.elapsed_time.seconds / 3600)
        minutes = int((self.elapsed_time.seconds % 3600) / 60)
        return "%d:%02d" % (hours, minutes)

    def get_sla_mark(self):
        self.calc_elapsed_time()
        et = self.elapsed_time

        if not et:
            return None

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
        sub = self.request.summary
        if not sub.endswith(" review"):
            return None
        if not sub.startswith("["):
            return None
        sub = sub.replace("-stable review", "")
        sub1 = sub.replace(" review", "")
        return sub1[sub1.rfind(" ") + 1 :]

    def get_ymd(self):
        return self.request.committed_datetime.strftime("%Y-%m-%d")

    def get_date(self):
        return self.request.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def get_from(self):
        return "%s <%s>" % (self.reply.author.name, self.reply.author.email)

    def get_id(self):
        msg = commit_to_email_message(self.reply)
        return msg["message-id"]

    def get_regressions_detected(self):
        if "linaro.org" not in self.reply.author.email:
            return False

        msg = commit_to_email_message(self.reply)
        payload = msg.get_payload()
        if type(payload) == list:
            payload = payload[0].get_payload()
        body = payload.lower()
        if "no regressions on " in body:
            return False
        else:
            return True

    def get_has_reply(self):
        if self.reply:
            return True
        return False
