# 🚀 Complete Deployment Guide - Canada Relocation Job Alert

This guide will walk you through setting up the enhanced job alert system on GitHub with full automation.

## Prerequisites

- GitHub account
- SendGrid account (free tier available)
- Basic understanding of GitHub Actions

## Step 1: Create GitHub Repository

1. **Create New Repository**
   - Go to [GitHub](https://github.com)
   - Click "New repository"
   - Name it: `canada-relocation-job-alert`
   - Make it **Public** (for GitHub Actions)
   - Don't initialize with README (we'll push our own)

2. **Clone Repository Locally**
   ```bash
   git clone https://github.com/YOUR_USERNAME/canada-relocation-job-alert.git
   cd canada-relocation-job-alert
   ```

## Step 2: Set Up SendGrid

1. **Create SendGrid Account**
   - Go to [SendGrid](https://sendgrid.com)
   - Sign up for free account (100 emails/day)
   - Verify your email

2. **Create API Key**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Name: `Job Alert Bot`
   - Permissions: "Restricted Access" → "Mail Send"
   - Copy the API key (starts with `SG.`)

3. **Verify Sender Email**
   - Go to Settings → Sender Authentication
   - Choose "Single Sender Verification"
   - Add your email (e.g., `alerts@yourdomain.com`)
   - Verify the email

## Step 3: Configure GitHub Secrets

1. **Go to Repository Settings**
   - In your GitHub repo, click "Settings" tab
   - Click "Secrets and variables" → "Actions"

2. **Add Required Secrets**
   ```
   SENDGRID_API_KEY = SG.your_api_key_here
   EMAIL_FROM = alerts@yourdomain.com
   TARGET_EMAIL = your.email@gmail.com
   ```

3. **Add Optional Secrets** (for customization)
   ```
   MIN_MATCH_SCORE = 70
   REQUEST_TIMEOUT = 10
   REQUEST_DELAY = 1.0
   MAX_JOBS_PER_SOURCE = 5
   ```

## Step 4: Push Code to GitHub

1. **Add All Files**
   ```bash
   git add .
   git commit -m "Initial commit: Enhanced Canada relocation job alert system"
   git push origin main
   ```

2. **Verify Files Are Uploaded**
   - Check that all files are in your repository
   - Ensure `.github/workflows/job_alert.yml` is present

## Step 5: Enable GitHub Actions

1. **Go to Actions Tab**
   - Click "Actions" tab in your repository
   - You should see the workflow listed

2. **Enable Workflow**
   - Click on "Canada Relocation Job Alert"
   - Click "Enable workflow" if prompted

3. **Test Manual Run**
   - Click "Run workflow" button
   - Select "main" branch
   - Click "Run workflow"
   - Monitor the execution

## Step 6: Monitor and Debug

1. **Check Workflow Runs**
   - Go to Actions tab
   - Click on the latest run
   - Check each step for errors

2. **Common Issues & Solutions**

   **Issue: "No module named 'config'"**
   - Solution: Ensure `config.py` is in the root directory

   **Issue: "SENDGRID_API_KEY not found"**
   - Solution: Check GitHub secrets are set correctly

   **Issue: "No jobs found"**
   - Solution: Check logs for scraping errors
   - May need to adjust search terms in `config.py`

3. **Download Database Artifact**
   - In workflow run, scroll to bottom
   - Click "job-database" artifact
   - Download to inspect stored jobs

## Step 7: Customize Configuration

1. **Edit Skills Keywords**
   ```bash
   # Edit config.py locally
   nano config.py
   
   # Update SKILLS_KEYWORDS array with your skills
   git add config.py
   git commit -m "Update skills keywords"
   git push origin main
   ```

2. **Adjust Match Score Threshold**
   - Set `MIN_MATCH_SCORE` secret to desired value (0-100)
   - Higher = more selective, Lower = more results

3. **Modify Search Terms**
   - Edit search terms in `config.py`
   - Add/remove job sources as needed

## Step 8: Advanced Configuration

### Add Slack Notifications (Optional)

1. **Create Slack Webhook**
   - Go to [Slack Apps](https://api.slack.com/apps)
   - Create new app
   - Enable "Incoming Webhooks"
   - Add webhook URL to GitHub secrets as `SLACK_WEBHOOK_URL`

### Customize Email Schedule

1. **Edit Workflow Schedule**
   ```yaml
   # In .github/workflows/job_alert.yml
   schedule:
     - cron: '0 */4 * * *'  # Every 4 hours
     - cron: '0 9,17 * * *'  # 9 AM and 5 PM daily
   ```

### Add More Job Sources

1. **Create New Crawler**
   ```python
   # crawler/new_source.py
   def get_new_source_jobs():
       # Implementation here
       pass
   ```

2. **Update Aggregator**
   ```python
   # In crawler/aggregator.py
   from .new_source import get_new_source_jobs
   sources.append(("New Source", get_new_source_jobs))
   ```

## Step 9: Monitoring and Maintenance

### Daily Monitoring
- Check GitHub Actions for successful runs
- Review email alerts for quality
- Monitor SendGrid usage

### Weekly Maintenance
- Review job match quality
- Adjust skills keywords if needed
- Check for new job sources

### Monthly Review
- Analyze job sources performance
- Update relocation keywords
- Review and optimize scoring

## Troubleshooting

### Workflow Fails
1. Check Actions tab for error details
2. Verify all secrets are set
3. Check Python dependencies
4. Review logs for specific errors

### No Emails Received
1. Check SendGrid API key
2. Verify sender email is authenticated
3. Check spam folder
4. Review workflow logs

### Poor Job Matches
1. Adjust `MIN_MATCH_SCORE` threshold
2. Update skills keywords in `config.py`
3. Review search terms
4. Check job source availability

### Rate Limiting Issues
1. Increase `REQUEST_DELAY` in secrets
2. Reduce `MAX_JOBS_PER_SOURCE`
3. Add more delay between requests

## Security Considerations

1. **API Key Security**
   - Never commit API keys to code
   - Use GitHub secrets for all sensitive data
   - Rotate keys periodically

2. **Repository Security**
   - Keep repository public for GitHub Actions
   - Don't include personal information in code
   - Use environment variables for configuration

## Performance Optimization

1. **Reduce Execution Time**
   - Limit jobs per source
   - Increase request delays
   - Use caching where possible

2. **Improve Accuracy**
   - Fine-tune scoring algorithms
   - Update keywords regularly
   - Monitor false positives

## Support and Updates

- **GitHub Issues**: Report bugs and request features
- **Regular Updates**: Pull latest changes from main branch
- **Community**: Share improvements and customizations

---

## Quick Start Checklist

- [ ] GitHub repository created
- [ ] SendGrid account set up
- [ ] API key generated
- [ ] Sender email verified
- [ ] GitHub secrets configured
- [ ] Code pushed to repository
- [ ] GitHub Actions enabled
- [ ] Manual test run successful
- [ ] First email received
- [ ] Configuration customized

**🎉 Congratulations! Your Canada Relocation Job Alert system is now live and automated!** 