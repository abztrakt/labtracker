from django import dispatch

changedIssueSignal = dispatch.Signal(providing_args=["data"])
