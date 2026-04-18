import smtplib
from email.message import EmailMessage

from src.core.config import Config


class EmailService:
    @staticmethod
    def send_registration_email(to_email: str, username: str):
        msg = EmailMessage()
        msg["Subject"] = "Chào mừng bạn đến với Book Management System!"
        msg["From"] = Config.MAIL_FROM
        msg["To"] = to_email

        content = f"""
                <html>
                    <body>
                        <h1>Chào {username},</h1>
                        <p>Cảm ơn bạn đã đăng ký thành viên tại hệ thống quản lý sách của chúng tôi.</p>
                        <p>Tài khoản của bạn đã được khởi tạo thành công!</p>
                    </body>
                </html>
                """
        msg.add_alternative(content, subtype="html")

        try:
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                if Config.MAIL_STARTTLS:
                    server.starttls()
                    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                    server.send_message(msg)
        except Exception as e:
            print(f"Lỗi gửi email: {e}")
