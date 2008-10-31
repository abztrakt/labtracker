from django import dispatch

newIssueSignal = dispatch.Signal(providing_args=["instance",])
