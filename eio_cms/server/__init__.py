# -*- coding: utf-8 -*-
"""
EIO-CMS - adaptations of CMS for EIO.

Author: Konstantin Tretyakov
License: MIT
"""
import logging
import json
logger = logging.getLogger(__name__)

def get_score_class(score, max_score, details=None):
    """Return a CSS class to visually represent the score/max_score

    score (float): the score of the submission.
    max_score (float): maximum score.

    return (unicode): class name

    """
    if details is not None:
        try:
            d = json.loads(details)
            ncorrect = 0
            nincorrect = 0
            if "testcases" in d[0]:
                d = reduce(lambda x,y: x+y, [ts["testcases"] for ts in d])
            for t in d:
                if "outcome" in t:
                    if t["outcome"] == "Correct":
                        ncorrect += 1
                    elif t["outcome"] == "Not correct":
                        nincorrect += 1
                    else:
                        ncorrect += 1
                        nincorrect += 1
            if ncorrect > 0 and nincorrect == 0:
                return "score_100"
            elif ncorrect == 0 and nincorrect > 0:
                return "score_0"
            else:
                return "score_0_100"
        except Exception, e:
            log.info(e)
    if score <= 0:
        return "score_0"
    elif score >= max_score:
        return "score_100"
    else:
        return "score_0_100"



