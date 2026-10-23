# 📧 Shree Sewa Marble — Mailer API

A Flask-based SMTP Mailer API built for **Shree Sewa Marble** (Tiles & Architectural Surfaces). Ready to deploy on **Vercel** with CORS enabled and dual email dispatch.

## 🚀 Features
- ⚡ **Flask REST API**: POST endpoint `/send` to forward website contact enquiries
- 🔐 **Gmail SMTP Ready**: Uses App Password with SMTP over TLS
- ✉️ **Dual Mail Dispatch**:
  1. Sends a premium HTML **Admin Alert** to `contact.shreesewamarble@gmail.com`
  2. Sends an auto-confirmation email to the visitor (if different email)
- 🎨 **Branded HTML Templates**: Clean gold/dark theme matching Shree Sewa Marble
- ☁️ **Vercel Serverless Ready**: Pre-configured with `vercel.json`
- 🌐 **CORS Enabled**: Works from any frontend

## 📁 Structure
```
shree-sewa-marble-mailer/
├── app.py           # Main app
├── requirements.txt # Dependencies
├── vercel.json      # Vercel config
├── .env.example     # Environment variable template
├── .gitignore
└── README.md
```

## 💻 Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in SMTP_PASSWORD
python app.py
```

The app reads `.env` automatically and runs at `http://localhost:5000`.

## 🛠️ API Usage

### Endpoint: `POST /send`

#### Request Body
```json
{
  "name": "Customer Name",
  "email": "customer@example.com",
  "phone": "+91 XXXXX XXXXX",
  "message": "I would like to enquire about tiles for my project.",
  "subject": "Website Enquiry - Shree Sewa Marble"
}
```

#### Success Response
```json
{
  "ok": true,
  "message": "Message sent successfully!"
}
```

## ⚙️ Environment Variables (Vercel)
Set these on Vercel:

| Variable | Value | Notes |
|---|---|---|
| `SMTP_HOST` | `smtp.gmail.com` | Default |
| `SMTP_PORT` | `587` | Default |
| `SMTP_EMAIL` | `contact.shreesewamarble@gmail.com` | Gmail/App Password account |
| `SMTP_PASSWORD` | `your-app-password` | Gmail App Password (16 chars) |
| `TO_EMAIL` | `contact.shreesewamarble@gmail.com` | Where enquiries go |

## 🚀 Deploy to Vercel
1. Push to GitHub
2. Import repo in [vercel.com](https://vercel.com)
3. Add environment variables
4. Deploy
5. Use `https://your-app.vercel.app/send` in your website
