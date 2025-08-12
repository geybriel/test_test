#!/usr/bin/env python3
"""
Simple local test for the job alert system
Run this with your secrets to test email functionality
"""
import os
import sys

def test_simple_email():
    """Test sending a simple email"""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        api_key = os.environ.get('SENDGRID_API_KEY')
        from_email = os.environ.get('EMAIL_FROM')
        to_email = os.environ.get('TARGET_EMAIL')
        
        if not api_key or not from_email or not to_email:
            print("❌ Please set environment variables first:")
            print("   SENDGRID_API_KEY, EMAIL_FROM, TARGET_EMAIL")
            return False
        
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
    print("Set environment variables before running:")
    print("  SENDGRID_API_KEY=your_api_key")
    print("  EMAIL_FROM=your_verified_email")
    print("  TARGET_EMAIL=your_target_email")
    print()
    
    # Test email
    success = test_simple_email()
    
    if success:
        print("\n🎉 Email test successful! Your SendGrid setup is working.")
        print("Now check your GitHub Actions workflow logs for other issues.")
    else:
        print("\n❌ Email test failed. Check your SendGrid configuration.") 