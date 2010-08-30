from django import dispatch

changedAssigneeSignal = dispatch.Signal(providing_args=["old_assignee",])
changedIssueSignal = dispatch.Signal(providing_args=["old_issue"])
