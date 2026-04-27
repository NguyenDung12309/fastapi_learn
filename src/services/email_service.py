import smtplib
from email.message import EmailMessage

from src.core.config import Config


class EmailService:
    @staticmethod
    def _init_service(msg: EmailMessage):
        try:
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                if Config.MAIL_STARTTLS:
                    server.starttls()
                    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                    server.send_message(msg)
        except Exception as e:
            print(f"Lỗi gửi email: {e}")

    def send_registration_email(self, to_email: str, username: str):
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
        self._init_service(msg)

    def send_reset_password_email(self, to_email: str, token: str):
        msg = EmailMessage()
        msg["Subject"] = "Đặt lại mật khẩu của bạn"
        msg["From"] = Config.MAIL_FROM
        msg["To"] = to_email

        reset_link = f"{Config.FE_URL}/reset-password?token={token}"

        content = f"""
                <html>
                    <body>
                        <p>Bạn đã yêu cầu đặt lại mật khẩu. Vui lòng nhấn vào link bên dưới:</p>
                        <a href="{reset_link}">Đặt lại mật khẩu</a>
                        <p>Link này sẽ hết hạn sau 10 phút.</p>
                    </body>
                </html>
                """
        msg.add_alternative(content, subtype="html")
        self._init_service(msg)
