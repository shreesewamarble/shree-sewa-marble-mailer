from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# Gmail credentials
SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "contact.shreesewamarble@gmail.com")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
TO_EMAIL = os.environ.get("TO_EMAIL", "contact.shreesewamarble@gmail.com")

SITE_NAME = "Shree Sewa Marble"
SITE_DOMAIN = "https://shreesewamarble.com"
SENDER_NAME = "Shree Sewa Marble"
REPLY_NAME = "Shree Sewa Marble"

# =========================
# STATUS HTML TEST PAGE
# =========================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Shree Sewa Marble — Mailer API</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0b0f19;
            color: #f8fafc;
            padding: 40px 20px;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
        }

        .box {
            max-width: 520px;
            width: 100%;
            background: #111827;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.08);
        }

        h2 {
            color: #d4b942;
            margin-top: 0;
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        p {
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        label {
            display: block;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-bottom: 4px;
            font-weight: 500;
        }

        input, textarea {
            width: 100%;
            padding: 12px 14px;
            margin-bottom: 16px;
            background: #0b0f19;
            border: 1px solid #1f2937;
            color: #fff;
            border-radius: 10px;
            font-size: 14px;
            box-sizing: border-box;
            font-family: inherit;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #d4b942;
            box-shadow: 0 0 0 3px rgba(212, 185, 66, 0.2);
        }

        button {
            background: linear-gradient(135deg, #b99a2d, #d4b942);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
            transition: transform 0.2s ease, opacity 0.2s ease;
        }

        button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }

        #status {
            margin-top: 18px;
            font-weight: bold;
            font-size: 0.9rem;
            text-align: center;
        }
    </style>
</head>

<body>

<div class="box">
    <h2>📧 Mailer API — Shree Sewa Marble</h2>
    <p>Premium email API for Shree Sewa Marble website contact enquiries.</p>

    <label>Sender Name:</label>
    <input type="text" id="name" placeholder="Enter full name">

    <label>Sender Email:</label>
    <input type="email" id="email" placeholder="Enter email address">

    <label>Phone Number:</label>
    <input type="text" id="phone" placeholder="Enter phone number">

    <label>Message:</label>
    <textarea id="message" rows="4" placeholder="Write message here..."></textarea>

    <button onclick="sendMail()">Send Mail 🚀</button>

    <div id="status"></div>
</div>

<script>
async function sendMail() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const message = document.getElementById("message").value;
    const status = document.getElementById("status");

    status.style.color = "#d4b942";
    status.innerHTML = "Sending mail...";

    try {
        const response = await fetch("/send", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, phone, message })
        });

        const data = await response.json();

        if (data.ok) {
            status.style.color = "#38ef7d";
            status.innerHTML = "✅ " + (data.message || "Mail sent successfully!");
        } else {
            status.style.color = "#ff5252";
            status.innerHTML = "❌ " + (data.error || "Failed to send mail");
        }
    } catch(err) {
        status.style.color = "#ff5252";
        status.innerHTML = "❌ " + err.message;
    }
}
</script>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


# =========================
# HELPER: BUILD ADMIN EMAIL (TO SHREE SEWA MARBLE)
# =========================
def build_admin_email_html(name, email, phone, message):
    time_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0; padding:0; background-color:#0b0f19; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      <div style="max-width:600px; margin:30px auto; background-color:#111827; border-radius:16px; border:1px solid #1f2937; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.5);">
        <!-- Header -->
        <div style="background:linear-gradient(135deg, #b99a2d 0%, #d4b942 100%); padding:30px 25px; text-align:center;">
          <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:700; letter-spacing:-0.5px;">📩 New Website Enquiry</h1>
          <p style="color:rgba(255,255,255,0.95); margin:8px 0 0 0; font-size:14px;">Shree Sewa Marble — Contact Form</p>
        </div>
        
        <!-- Content -->
        <div style="padding:30px 25px;">
          <div style="background:#1f2937; border-left:4px solid #d4b942; border-radius:8px; padding:15px; margin-bottom:25px;">
            <p style="margin:0; color:#9ca3af; font-size:13px;">Received On:</p>
            <p style="margin:4px 0 0 0; color:#d4b942; font-weight:600; font-size:15px;">{time_str}</p>
          </div>

          <table style="width:100%; border-collapse:collapse; margin-bottom:20px;">
            <tr>
              <td style="padding:10px 0; color:#9ca3af; font-size:14px; font-weight:600; width:100px;">Name:</td>
              <td style="padding:10px 0; color:#f3f4f6; font-size:15px; font-weight:600;">{name}</td>
            </tr>
            <tr>
              <td style="padding:10px 0; color:#9ca3af; font-size:14px; font-weight:600;">Email:</td>
              <td style="padding:10px 0;"><a href="mailto:{email}" style="color:#d4b942; text-decoration:none; font-weight:600;">{email}</td>
            </tr>
            <tr>
              <td style="padding:10px 0; color:#9ca3af; font-size:14px; font-weight:600;">Phone:</td>
              <td style="padding:10px 0; color:#f3f4f6; font-size:15px;">{phone}</td>
            </tr>
          </table>

          <div style="margin-top:15px;">
            <p style="color:#9ca3af; font-size:14px; font-weight:600; margin-bottom:8px;">Message Content:</p>
            <div style="background:#0b0f19; border:1px solid #374151; border-radius:10px; padding:18px; color:#e5e7eb; font-size:15px; line-height:1.6; white-space:pre-wrap;">{message}</div>
          </div>

          <div style="margin-top:30px; text-align:center;">
            <a href="mailto:{email}" style="display:inline-block; background:linear-gradient(135deg, #b99a2d, #d4b942); color:#ffffff; font-weight:600; text-decoration:none; padding:12px 28px; border-radius:8px; font-size:15px;">Reply to {name} ✉️</a>
          </div>
        </div>

        <!-- Footer -->
        <div style="background:#0b0f19; border-top:1px solid #1f2937; padding:20px; text-align:center;">
          <p style="margin:0; color:#6b7280; font-size:12px;">Shree Sewa Marble &copy; {datetime.now().year} — Tiles & Architectural Surfaces</p>
        </div>
      </div>
    </body>
    </html>
    """


# =========================
# HELPER: BUILD CLIENT CONFIRMATION EMAIL (TO USER)
# =========================
def build_client_confirmation_html(name):
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0; padding:0; background-color:#0b0f19; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      <div style="max-width:600px; margin:30px auto; background-color:#111827; border-radius:16px; border:1px solid #1f2937; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.5);">
        <!-- Header -->
        <div style="background:linear-gradient(135deg, #b99a2d 0%, #d4b942 100%); padding:35px 25px; text-align:center;">
          <h1 style="color:#ffffff; margin:0; font-size:26px; font-weight:700; letter-spacing:-0.5px;">Thank You for Contacting Us ✨</h1>
          <p style="color:rgba(255,255,255,0.95); margin:10px 0 0 0; font-size:15px;">Shree Sewa Marble</p>
        </div>
        
        <!-- Content -->
        <div style="padding:35px 30px;">
          <h2 style="color:#f3f4f6; font-size:20px; margin-top:0;">Hello {name}, 👋</h2>
          <p style="color:#d1d5db; font-size:15px; line-height:1.7;">
            Thank you for reaching out to <strong>Shree Sewa Marble</strong>. We have received your enquiry regarding our tiles and architectural surfaces.
          </p>
          <p style="color:#d1d5db; font-size:15px; line-height:1.7;">
            Our team will review your message and get back to you as soon as possible, usually within <strong>24 hours</strong>.
          </p>

          <!-- Signature Block -->
          <div style="background:#0b0f19; border:1px solid #1f2937; border-radius:12px; padding:20px; margin-top:30px;">
            <p style="margin:0; color:#f3f4f6; font-size:16px; font-weight:700;">Shree Sewa Marble</p>
            <p style="margin:4px 0 14px 0; color:#9ca3af; font-size:13px;">Tiles & Architectural Surfaces</p>
            <table style="width:100%; border-collapse:collapse; font-size:13px;">
              <tr>
                <td style="padding:4px 0; color:#9ca3af; width:80px;">📧 Email:</td>
                <td style="padding:4px 0;"><a href="mailto:contact.shreesewamarble@gmail.com" style="color:#d4b942; text-decoration:none; font-weight:600;">contact.shreesewamarble@gmail.com</a></td>
              </tr>
            </table>
          </div>
        </div>

        <!-- Footer -->
        <div style="background:#0b0f19; border-top:1px solid #1f2937; padding:20px; text-align:center;">
          <p style="margin:0; color:#6b7280; font-size:12px;">Shree Sewa Marble &copy; {datetime.now().year} — All Rights Reserved.</p>
        </div>
      </div>
    </body>
    </html>
    """


# =========================
# SEND MAIL API
# =========================
@app.route("/send", methods=["POST", "OPTIONS"])
def send_mail():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        data = request.get_json() or {}

        name = data.get("name") or "Website Visitor"
        user_email = (data.get("email") or data.get("from_email") or "").strip()
        phone = data.get("phone") or "Not provided"

        target_to = data.get("to") or TO_EMAIL
        subject = data.get("subject") or f"New Enquiry from {name} - Shree Sewa Marble"
        message = data.get("message") or data.get("msg") or ""

        if not message:
            return jsonify({
                "ok": False,
                "error": "Message content is required"
            }), 400

        if not SMTP_PASSWORD:
            return jsonify({
                "ok": False,
                "error": "SMTP_PASSWORD not configured"
            }), 500

        # SMTP Connection
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        # 1. SEND ADMIN NOTIFICATION EMAIL
        admin_html = build_admin_email_html(name, user_email or 'Not provided', phone, message)

        admin_msg = MIMEMultipart("alternative")
        admin_msg["From"] = f"{SENDER_NAME} <{SMTP_EMAIL}>"
        admin_msg["To"] = target_to
        admin_msg["Subject"] = subject
        if user_email:
            admin_msg["Reply-To"] = user_email
        admin_msg.attach(MIMEText(admin_html, "html"))

        server.sendmail(SMTP_EMAIL, target_to, admin_msg.as_string())

        # 2. SEND CLIENT AUTO-CONFIRMATION EMAIL
        if user_email and "@" in user_email and user_email.lower() != SMTP_EMAIL.lower():
            try:
                client_html = build_client_confirmation_html(name)

                client_msg = MIMEMultipart("alternative")
                client_msg["From"] = f"{SENDER_NAME} <{SMTP_EMAIL}>"
                client_msg["To"] = user_email
                client_msg["Subject"] = f"Thank you for contacting {SITE_NAME}"
                client_msg.attach(MIMEText(client_html, "html"))

                server.sendmail(SMTP_EMAIL, user_email, client_msg.as_string())
            except Exception as client_err:
                print("CLIENT CONFIRMATION EMAIL WARNING:", str(client_err))

        server.quit()

        return jsonify({
            "ok": True,
            "message": "Message sent successfully!"
        })

    except Exception as e:
        print("MAIL ERROR:", str(e))
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
