#!/usr/bin/env python3
"""
Debug script to test the job alert system configuration
"""
import os
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_configuration():
    """Test if all required configuration is present"""
    logger.info("=== Testing Configuration ===")
    
    # Check required environment variables
    required_vars = ['SENDGRID_API_KEY', 'EMAIL_FROM', 'TARGET_EMAIL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: {'*' * (len(value) - 4) + value[-4:] if len(value) > 4 else '***'}")
        else:
            logger.error(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False
    
    # Test configuration validation
    issues = Config.validate()
    if issues:
        logger.error(f"Configuration issues: {issues}")
        return False
    
    logger.info("✅ All configuration looks good!")
    return True

def test_sendgrid():
    """Test SendGrid connection"""
    logger.info("=== Testing SendGrid ===")
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        api_key = os.getenv('SENDGRID_API_KEY')
        if not api_key:
            logger.error("❌ SENDGRID_API_KEY not found")
            return False
        
        # Test connection
        sg = SendGridAPIClient(api_key)
        
        # Create a test email
        message = Mail(
            from_email=os.getenv('EMAIL_FROM'),
            to_emails=os.getenv('TARGET_EMAIL'),
            subject='🧪 Test Email - Job Alert System',
            html_content='<h1>Test Email</h1><p>If you receive this, SendGrid is working correctly!</p>'
        )
        
        response = sg.send(message)
        logger.info(f"✅ SendGrid test email sent! Status: {response.status_code}")
        return True
        
    except Exception as e:
        logger.error(f"❌ SendGrid test failed: {e}")
        return False

def test_job_scraping():
    """Test job scraping functionality"""
    logger.info("=== Testing Job Scraping ===")
    
    try:
        from crawler.aggregator import aggregate_jobs
        
        jobs = aggregate_jobs()
        logger.info(f"✅ Found {len(jobs)} jobs from all sources")
        
        if jobs:
            logger.info("Sample jobs:")
            for i, job in enumerate(jobs[:3]):
                logger.info(f"  {i+1}. {job['title']} @ {job['company']} ({job['source']})")
        
        return len(jobs) > 0
        
    except Exception as e:
        logger.error(f"❌ Job scraping test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting debug tests...")
    
    # Test 1: Configuration
    config_ok = test_configuration()
    
    # Test 2: SendGrid (only if config is ok)
    sendgrid_ok = False
    if config_ok:
        sendgrid_ok = test_sendgrid()
    
    # Test 3: Job Scraping
    scraping_ok = test_job_scraping()
    
    # Summary
    logger.info("=== Test Summary ===")
    logger.info(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    logger.info(f"SendGrid: {'✅ PASS' if sendgrid_ok else '❌ FAIL'}")
    logger.info(f"Job Scraping: {'✅ PASS' if scraping_ok else '❌ FAIL'}")
    
    if not config_ok:
        logger.error("Fix configuration issues first!")
    elif not sendgrid_ok:
        logger.error("SendGrid is not working - check API key and email verification!")
    elif not scraping_ok:
        logger.error("Job scraping is not working - check internet connection and job sites!")
    else:
        logger.info("🎉 All tests passed! The system should work correctly.")

if __name__ == "__main__":
    main() 