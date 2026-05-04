from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

MESSENGER_LINK = "https://m.me/61573336556464"
TELEGRAM_LINK = "https://t.me/Negma369"

def send_professional_email(subject, recipient_email, message_text=None, context=None, template_name=None):
    """
    إرسال بريد إلكتروني احترافي مع تصميم HTML وإضافة روابط المسنجر والتليجرام
    """
    if context is None:
        context = {}
    
    # إضافة روابط الاتصال إلى السياق
    context.update({
        'messenger_link': MESSENGER_LINK,
        'telegram_link': TELEGRAM_LINK,
        'platform_name': 'Services Pro',
        'support_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@servicespro.com'),
    })
    
    # إذا لم يتم تحديد قالب، استخدم قالب افتراضي
    if template_name:
        html_message = render_to_string(template_name, context)
    else:
        html_message = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                    direction: rtl;
                    text-align: right;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 30px;
                    line-height: 1.8;
                    color: #333;
                    font-size: 16px;
                }}
                .message-text {{
                    margin-bottom: 20px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                .footer {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-top: 1px solid #e0e0e0;
                    text-align: center;
                    font-size: 14px;
                    color: #666;
                }}
                .social-links {{
                    margin: 20px 0;
                    text-align: center;
                }}
                .social-links a {{
                    display: inline-block;
                    margin: 0 10px;
                    padding: 10px 15px;
                    background-color: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }}
                .social-links a:hover {{
                    background-color: #764ba2;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 15px 0;
                    font-weight: bold;
                }}
                .button:hover {{
                    background-color: #764ba2;
                }}
                .divider {{
                    height: 1px;
                    background-color: #e0e0e0;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📧 {context.get('platform_name', 'Services Pro')}</h1>
                </div>
                <div class="content">
                    <div class="message-text">{message_text if message_text else ''}</div>
                    
                    <div class="divider"></div>
                    
                    <p><strong>للتواصل معنا:</strong></p>
                    <div class="social-links">
                        <a href="{context.get('messenger_link', '#')}" target="_blank">📱 Messenger</a>
                        <a href="{context.get('telegram_link', '#')}" target="_blank">✈️ Telegram</a>
                        <a href="mailto:{context.get('support_email', '#')}" target="_blank">📧 البريد الإلكتروني</a>
                    </div>
                </div>
                <div class="footer">
                    <p>© 2024 {context.get('platform_name', 'Services Pro')}. جميع الحقوق محفوظة.</p>
                    <p>لا تجب على هذا البريد. إذا كان لديك أسئلة، يرجى التواصل معنا عبر المنصة.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    # إنشاء بريد متعدد الأجزاء
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_text if message_text else "انظر نسخة HTML من البريد",
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@servicespro.com'),
        to=[recipient_email]
    )
    
    # إضافة نسخة HTML
    email.attach_alternative(html_message, "text/html")
    
    # إرسال البريد
    return email.send(fail_silently=False)
