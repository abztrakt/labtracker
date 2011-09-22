from django import dispatch

newIssueSignal = dispatch.Signal(providing_args=["data"]) 
changedIssueSignal = dispatch.Signal(providing_args=["data"])
