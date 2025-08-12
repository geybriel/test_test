#!/usr/bin/env python3
"""
Simple local test for the job alert system
Run this with your secrets to test email functionality
"""
import os
import sys

# Add your secrets here for local testing
os.environ['SENDGRID_API_KEY'] = 'SG.YOUR_API_KEY_HERE'  # Replace with your actual API key
os.environ['EMAIL_FROM'] = 'your.email@gmail.com'  # Replace with your verified email
os.environ['TARGET_EMAIL'] = 'your.email@gmail.com'  # Replace with your target email

def test_simple_email():
    """Test sending a simple email"""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        api_key = os.environ['SENDGRID_API_KEY']
        from_email = os.environ['EMAIL_FROM']
        to_email = os.environ['TARGET_EMAIL']
        
        print(f"Testing email from {from_email} to {to_email}")
        
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='🧪 Test Email - Job Alert System',
            html_content='''
            <h1>Test Email</h1>
            <p>If you receive this email, SendGrid is working correctly!</p>
            <p>This means your job alert system should be able to send emails.</p>
            '''
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        print(f"✅ Email sent successfully! Status code: {response.status_code}")
        print("Check your email inbox (and spam folder) for the test message.")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Job Alert System - Local Test ===")
    print("Make sure to update the secrets in this file before running!")
    print()
    
    # Check if secrets are set
    if 'SG.YOUR_API_KEY_HERE' in os.environ['SENDGRID_API_KEY']:
        print("❌ Please update the SENDGRID_API_KEY in this file!")
        sys.exit(1)
    
    if 'your.email@gmail.com' in os.environ['EMAIL_FROM']:
        print("❌ Please update the EMAIL_FROM in this file!")
        sys.exit(1)
    
    # Test email
    success = test_simple_email()
    
    if success:
        print("\n🎉 Email test successful! Your SendGrid setup is working.")
        print("Now check your GitHub Actions workflow logs for other issues.")
    else:
        print("\n❌ Email test failed. Check your SendGrid configuration.") 