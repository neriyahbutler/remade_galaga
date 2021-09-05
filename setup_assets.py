import os

absolute_path = os.path.abspath(__file__)
# directory_value = os.path.dirname(absolute_path)
print("Full path: " + absolute_path)
print("Directory Path: " + os.path.dirname(absolute_path))