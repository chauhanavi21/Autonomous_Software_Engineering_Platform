from app.auth.password import hash_password, verify_password
def test_password_hashing():
    password="correct-horse-battery-staple"; hashed=hash_password(password); assert hashed!=password; assert verify_password(password,hashed); assert not verify_password("wrong-password",hashed)
