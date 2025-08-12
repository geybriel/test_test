# Canada Relocation Job Alert Bot 🇨🇦

Automatically scrapes job boards every 6 hours for roles matching your skills & relocation to Canada, then emails new matches with enhanced scoring and confidence levels.

## Features ✨

- **Multi-Source Scraping**: Indeed, JobBank Canada, and Glassdoor
- **Smart Matching**: TF-IDF based similarity scoring with your skills
- **Relocation Detection**: Advanced keyword analysis with confidence levels
- **Duplicate Prevention**: SQLite database prevents re-sending jobs
- **Beautiful Emails**: Rich HTML templates with job statistics
- **Configurable**: Easy customization of skills, keywords, and thresholds
- **Error Resilient**: Comprehensive error handling and logging

## Setup 🚀

### 1. Repository Setup
```bash
git clone <your-repo-url>
cd canada-relocation-job-alert
```

### 2. GitHub Secrets Configuration
Add these secrets to your GitHub repository:

| Secret | Description | Example |
|--------|-------------|---------|
| `SENDGRID_API_KEY` | Your SendGrid API key | `SG.xxxxxxxxxxxxx` |
| `EMAIL_FROM` | Verified sender email in SendGrid | `alerts@yourdomain.com` |
| `TARGET_EMAIL` | Your target email | `your.email@gmail.com` |

### 3. Optional Environment Variables
You can customize the bot behavior with these optional secrets:

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_MATCH_SCORE` | `70` | Minimum job match score (0-100) |
| `REQUEST_TIMEOUT` | `10` | HTTP request timeout in seconds |
| `REQUEST_DELAY` | `1.0` | Delay between requests in seconds |
| `MAX_JOBS_PER_SOURCE` | `5` | Max jobs to fetch per source |

### 4. Enable GitHub Actions
The workflow runs automatically every 6 hours. You can also trigger it manually from the Actions tab.

## Configuration ⚙️

### Customizing Your Skills
Edit `config.py` to match your profile:

```python
SKILLS_KEYWORDS = [
    "Prisma Access", "PanOS", "DLP", "DataDog", "Kibana", "Grafana",
    "AWS", "SRE", "Linux", "Kubernetes", "Python", "API",
    # Add your specific skills here
]
```

### Relocation Keywords
The bot looks for these phrases to detect relocation opportunities:

```python
RELOCATION_PHRASES = [
    "visa sponsorship", "lmia", "work permit", "relocation package",
    "flight", "housing", "dependent documentation", "immigration support",
    # Add more specific terms if needed
]
```

## How It Works 🔍

1. **Scraping**: Fetches jobs from multiple sources using respectful delays
2. **Matching**: Uses TF-IDF vectorization to compare job descriptions with your skills
3. **Scoring**: Applies additional factors (location, seniority, remote work)
4. **Relocation Detection**: Analyzes text for immigration/relocation indicators
5. **Filtering**: Only sends jobs above the minimum score threshold
6. **Deduplication**: Checks database to avoid re-sending jobs
7. **Email**: Sends beautiful HTML digest with job details and statistics

## Email Features 📧

- **Match Score**: Percentage match with your skills
- **Relocation Confidence**: High/Medium/Low based on keyword analysis
- **Relocation Indicators**: Shows specific phrases found
- **Statistics**: Summary of new jobs and confidence levels
- **Direct Apply Links**: One-click application buttons

## Troubleshooting 🔧

### Common Issues

**No jobs found:**
- Check if job sites are accessible from GitHub Actions
- Verify search terms in `config.py`
- Check logs in GitHub Actions for errors

**Emails not sending:**
- Verify SendGrid API key is correct
- Ensure sender email is verified in SendGrid
- Check GitHub Actions logs for email errors

**Poor job matches:**
- Update `SKILLS_KEYWORDS` in `config.py`
- Adjust `MIN_MATCH_SCORE` threshold
- Review job sources and search terms

### Logs
Check GitHub Actions logs for detailed error information and debugging.

## Development 🛠️

### Local Testing
```bash
pip install -r requirements.txt
python worker.py
```

### Adding New Job Sources
1. Create new crawler file in `crawler/` directory
2. Implement `get_<source>_jobs()` function
3. Add import to `crawler/aggregator.py`
4. Update search terms in `config.py`

### Database Schema
```sql
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    title TEXT, 
    company TEXT, 
    location TEXT, 
    url TEXT,
    match_score REAL, 
    relocation_detected INTEGER, 
    date_added TEXT
);
```

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

MIT License - feel free to use this for your own job search automation.
