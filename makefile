
clean:
	find . -type d -name "__pycache__" | xargs rm -rf &
	find . -type d -name ".pytest_cache" | xargs rm -rf

	