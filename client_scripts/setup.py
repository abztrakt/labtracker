from cx_Freeze import setup, Executable

setup(
	name = "tracker",
	version = "0.8",
	description = "Lab usage statistics gatherer",
	executables = [Executable("tracker.py")])
