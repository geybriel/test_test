import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from config import Config
import logging
import base64

logger = logging.getLogger(__name__)

def _build_attachment(file_path: str) -> Attachment:
    with open(file_path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('text/plain')
    attachment.file_name = FileName(os.path.basename(file_path))
    # Use plain string to avoid JSON serialization issues
    attachment.disposition = 'attachment'
    return attachment

def send_digest(to_email: str, jobs: list, log_file_path: str | None = None):
    """Send enhanced job digest email, optionally with log attachment"""
    try:
        subject = f"🚀 {len(jobs)} New Canada/US/China Relocation Jobs Found!"
        html = create_email_html(jobs)

        message = Mail(
            from_email=Config.EMAIL_FROM,
            to_emails=to_email,
            subject=subject,
            html_content=html
        )

        # Attach logs if provided
        if log_file_path and os.path.exists(log_file_path):
            attachment = _build_attachment(log_file_path)
            # Attachments must be a list
            message.attachment = attachment

        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code == 202:
            logger.info(f"Email sent successfully to {to_email}")
        else:
            logger.error(f"Failed to send email. Status: {response.status_code}")

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise

def send_no_matches_email(to_email: str, reason: str, log_file_path: str | None = None):
    """Send email when no matches are found, with optional log attachment"""
    try:
        subject = f"📊 Job Alert Run Report - No New Matches"
        html = create_no_matches_html(reason)

        message = Mail(
            from_email=Config.EMAIL_FROM,
            to_emails=to_email,
            subject=subject,
            html_content=html
        )

        # Attach logs if provided
        if log_file_path and os.path.exists(log_file_path):
            attachment = _build_attachment(log_file_path)
            message.attachment = attachment

        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code == 202:
            logger.info(f"No matches email sent successfully to {to_email}")
        else:
            logger.error(f"Failed to send no matches email. Status: {response.status_code}")

    except Exception as e:
        logger.error(f"Error sending no matches email: {e}")
        raise

def create_no_matches_html(reason: str) -> str:
    """Create HTML for no matches email without using Python .format on CSS blocks"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .header { background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                     color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .content { background: #f8f9fa; padding: 20px; border-radius: 8px; }
            .footer { margin-top: 30px; padding: 15px; background: #ecf0f1;
                     border-radius: 8px; font-size: 12px; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Job Alert Run Report</h1>
            <p>No new matches found this time</p>
        </div>
        
        <div class="content">
            <h2>🔍 What happened?</h2>
            <p><strong>Reason:</strong> {REASON}</p>
            
            <h3>📋 Current Settings:</h3>
            <ul>
                <li><strong>Minimum Match Score:</strong> {MIN_SCORE}%</li>
                <li><strong>Search Locations:</strong> {LOCATIONS}</li>
                <li><strong>Relocation Required:</strong> Yes</li>
            </ul>
            
            <h3>💡 What to check:</h3>
            <ul>
                <li>Are the job sites accessible?</li>
                <li>Are there enough relocation keywords in job descriptions?</li>
                <li>Should we lower the minimum match score?</li>
                <li>Should we add more job sources?</li>
            </ul>
            
            <p><em>Check the attached log file for detailed information about what was found.</em></p>
        </div>
        
        <div class="footer">
            <p><strong>Next run:</strong> In 6 hours</p>
            <p><strong>To adjust settings:</strong> Update GitHub secrets or modify config.py</p>
        </div>
    </body>
    </html>
    """
    html = (
        html
        .replace("{REASON}", reason)
        .replace("{MIN_SCORE}", str(Config.MIN_MATCH_SCORE))
        .replace("{LOCATIONS}", ", ".join(Config.SEARCH_LOCATIONS))
    )
    return html

def create_email_html(jobs: list) -> str:
    """Create enhanced HTML email content without using Python .format on CSS blocks"""

    # Use sentinel {COUNT} then replace after the multi-line string is closed
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
            <h1>🌏 Canada, US & China Relocation Job Alert</h1>
            <p>Found {COUNT} new opportunities matching your skills!</p>
        </div>
    """
    html = html.replace("{COUNT}", str(len(jobs)))

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
            <div style="margin: 6px 0;">
                🔗 <a href="{job['url']}" target="_blank">Open job posting</a>
            </div>
        """

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
                html += f'<strong>Locations:</strong> {", ".join(job["canadian_locations"])}'

            html += '</div>'

        html += """
            <a href="{job['url']}" class="apply-btn" target="_blank">Apply Now</a>
        </div>
        """

    html += """
        <div class="footer">
            <p><strong>💡 Relocation Confidence Guide:</strong></p>
            <ul>
                <li>🟢 High: Direct visa sponsorship, LMIA, or specific immigration programs</li>
                <li>🟡 Medium: Relocation assistance, housing, or strong location indicators</li>
                <li>🔴 Low: Location mentioned but no explicit relocation support</li>
            </ul>
            <p><strong>Next alert:</strong> In 6 hours</p>
            <p><em>Logs</em>: This email may include a log attachment if enabled.</p>
        </div>
    </body>
    </html>
    """

    return html
