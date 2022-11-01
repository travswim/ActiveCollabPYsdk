- [ ] Finish porting to python
- [ ] use pydantic for python validation
- [ ] Github actions for testing
- [ ] pepy python project download info https://pepy.tech/
- [ ] docstrings: https://queirozf.com/entries/python-docstrings-reference-examples
- [x] Should Token be a dataclass? What comprises of a dataclass?
- [x] Should class member types be defined in the init or as static members?


### Tests to perform:
- test all methods, and raised exceptions
- use `converage.py` to test code coverage
- unit tests
- integration tests
- test coverage

-[ ] Authenticator
-[ ] Client
-[ ] Cloud
-[ ] Token


### Test Commands:
Python unittest command (from root directory):<br>
`python -m unittest discover -s .\test\ -p "test_*.py" -v`<br>
Coverage command:<br>
`coverage run -m unittest discover -s .\test\ -p "test_*.py" -v`