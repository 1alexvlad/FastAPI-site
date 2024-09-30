# import os

# os.environ["MODE"] = "TEST"
import os

os.environ["MODE"] = "TEST"
os.environ["SECRET_KEY"] = "your_test_secret_key"  # Убедитесь, что все необходимые переменные установлены
os.environ["ALGORITHM"] = "HS256"