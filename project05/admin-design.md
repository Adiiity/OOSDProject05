# ADMIN DESIGN

This part of the implementation was different from the previous one. Our admin handles the following 

### game_impl.py

**New Updates**

1. setup function to players data.
2. generate_state function to handle states.
3. buy function to perform buy request.
4. place function to perform place actions.
5. done function to perform done action.

**Issues Addressed:**

1. Merge operation - Tie breaker scenarios adressed.
2. Inspect operation - Board state was getting permanently updated. We fixed that.
3. Founding Operation - Singleton tile should be placed if not hotel can be found. This issue is handled properly.

### game_library.py

**New Updates**

1. Hotel class is removed.
2. Share class is introduced.


**Board Representation**

### Client.py
1. We completely changed how our client structure should be from the previous assignment due to change is request structures.

### Testing

1. We moved from pytest to unittest because we felt that its more easier to write multiple test functions into the same python file with unittest rather creating n number of test scripts.
2. To run tests, use the following command "python3 tester.py".
