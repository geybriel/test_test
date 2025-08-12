import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config
import logging

logger = logging.getLogger(__name__)

def send_digest(to_email: str, jobs: list):
    """Send enhanced job digest email"""
    try:
        subject = f"🚀 {len(jobs)} New Canada Relocation Jobs Found!"
        
        # Create enhanced HTML email
        html = create_email_html(jobs)
        
        message = Mail(
            from_email=Config.EMAIL_FROM,
            to_emails=to_email,
            subject=subject,
            html_content=html
        )
        
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        
        if response.status_code == 202:
            logger.info(f"Email sent successfully to {to_email}")
        else:
            logger.error(f"Failed to send email. Status: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise

def create_email_html(jobs: list) -> str:
    """Create enhanced HTML email content with detailed relocation information"""
    
    # Email header
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .job-card { border: 1px solid #ddd; border-radius: 8px; padding: 15px; 
                       margin-bottom: 15px; background: #f9f9f9; }
            .job-title { font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 5px; }
            .company { color: #7f8c8d; font-weight: bold; }
            .location { color: #95a5a6; font-style: italic; }
            .score { display: inline-block; background: #3498db; color: white; 
                    padding: 3px 8px; border-radius: 12px; font-size: 12px; }
            .relocation { display: inline-block; background: #27ae60; color: white; 
                         padding: 3px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px; }
            .apply-btn { display: inline-block; background: #e74c3c; color: white; 
                        padding: 8px 16px; text-decoration: none; border-radius: 4px; 
                        margin-top: 10px; }
            .footer { margin-top: 30px; padding: 15px; background: #ecf0f1; 
                     border-radius: 8px; font-size: 12px; color: #7f8c8d; }
            .stats { display: flex; justify-content: space-between; margin-bottom: 20px; }
            .stat-box { background: white; padding: 15px; border-radius: 8px; 
                       text-align: center; flex: 1; margin: 0 5px; }
            .relocation-details { background: #e8f5e8; padding: 10px; border-radius: 5px; 
                                 margin: 10px 0; font-size: 12px; }
            .immigration-program { background: #fff3cd; padding: 5px 8px; border-radius: 3px; 
                                  margin: 2px; display: inline-block; font-size: 11px; }
            .relocation-benefit { background: #d1ecf1; padding: 5px 8px; border-radius: 3px; 
                                 margin: 2px; display: inline-block; font-size: 11px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🇨🇦 Canada Relocation Job Alert</h1>
            <p>Found {count} new opportunities matching your skills!</p>
        </div>
    """.format(count=len(jobs))
    
    # Statistics section
    high_confidence = sum(1 for job in jobs if job.get('relocation_confidence') == 'high')
    medium_confidence = sum(1 for job in jobs if job.get('relocation_confidence') == 'medium')
    avg_score = sum(job['match_score'] for job in jobs) / len(jobs) if jobs else 0
    
    html += f"""
        <div class="stats">
            <div class="stat-box">
                <h3>{len(jobs)}</h3>
                <p>New Jobs</p>
            </div>
            <div class="stat-box">
                <h3>{high_confidence}</h3>
                <p>High Confidence</p>
            </div>
            <div class="stat-box">
                <h3>{medium_confidence}</h3>
                <p>Medium Confidence</p>
            </div>
            <div class="stat-box">
                <h3>{avg_score:.1f}%</h3>
                <p>Avg Match Score</p>
            </div>
        </div>
    """
    
    # Job listings
    html += "<h2>🎯 Top Matches</h2>"
    
    for i, job in enumerate(jobs, 1):
        confidence_emoji = {
            'high': '🟢',
            'medium': '🟡', 
            'low': '🔴'
        }.get(job.get('relocation_confidence', 'low'), '⚪')
        
        html += f"""
        <div class="job-card">
            <div class="job-title">{i}. {job['title']}</div>
            <div class="company">🏢 {job['company']}</div>
            <div class="location">📍 {job.get('location', 'Location not specified')}</div>
            <div style="margin: 10px 0;">
                <span class="score">Match: {job['match_score']}%</span>
                <span class="relocation">{confidence_emoji} Relocation: {job.get('relocation_confidence', 'unknown').title()}</span>
            </div>
        """
        
        # Show detailed relocation information
        if job.get('relocation_phrases') or job.get('immigration_programs') or job.get('relocation_benefits'):
            html += '<div class="relocation-details">'
            html += '<strong>🔍 Relocation Analysis:</strong><br>'
            
            if job.get('immigration_programs'):
                html += '<strong>Immigration Programs:</strong> '
                for program in job['immigration_programs']:
                    html += f'<span class="immigration-program">{program}</span> '
                html += '<br>'
            
            if job.get('relocation_benefits'):
                html += '<strong>Relocation Benefits:</strong> '
                for benefit in job['relocation_benefits']:
                    html += f'<span class="relocation-benefit">{benefit}</span> '
                html += '<br>'
            
            if job.get('relocation_phrases'):
                html += f'<strong>Keywords Found:</strong> {", ".join(job["relocation_phrases"])}<br>'
            
            if job.get('canadian_locations'):
                html += f'<strong>Canadian Locations:</strong> {", ".join(job["canadian_locations"])}'
            
            html += '</div>'
        
        html += f"""
            <a href="{job['url']}" class="apply-btn" target="_blank">Apply Now</a>
        </div>
        """
    
    # Footer with enhanced information
    html += """
        <div class="footer">
            <p><strong>💡 Relocation Confidence Guide:</strong></p>
            <ul>
                <li>🟢 <strong>High Confidence:</strong> Direct visa sponsorship, LMIA, or specific immigration programs mentioned</li>
                <li>🟡 <strong>Medium Confidence:</strong> Relocation assistance, housing, or strong Canadian location indicators</li>
                <li>🔴 <strong>Low Confidence:</strong> Canadian location mentioned but no clear relocation support</li>
            </ul>
            <p><strong>🎯 Immigration Programs Detected:</strong></p>
            <ul>
                <li>Express Entry, Federal Skilled Worker, Provincial Nominee</li>
                <li>Global Talent Stream, LMIA, Work Permit Sponsorship</li>
                <li>Relocation packages, housing assistance, family support</li>
            </ul>
            <p><strong>Next alert:</strong> In 6 hours</p>
            <p><em>Reply 'PAUSE' to temporarily stop alerts</em></p>
        </div>
    </body>
    </html>
    """
    
    return html
