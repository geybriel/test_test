import os, logging, tempfile
from crawler.aggregator import aggregate_jobs
from matcher.engine import rank_jobs
from db.master import init_db, is_new_job, save_job
from emailer.sendgrid_client import send_digest, send_no_matches_email
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run():
    try:
        logger.info("Starting enhanced job alert process (Canada & US)...")

        # Initialize database
        init_db()
        logger.info("Database initialized")

        # Aggregate jobs from all sources
        jobs = aggregate_jobs()
        logger.info(f"Found {len(jobs)} total jobs from all sources")

        if not jobs:
            logger.warning("No jobs found from any source")
            # Send no matches email with log
            send_no_matches_email(Config.TARGET_EMAIL, "No jobs found from any source", None)
            return

        # Rank and filter jobs
        matches = rank_jobs(jobs)
        logger.info(f"Ranked {len(matches)} jobs")

        # Process new matches with enhanced filtering
        new_matches = []
        for job in matches:
            try:
                sig = f"{job['company']}|{job['title']}|{job.get('location','')}|{job['url']}"

                meets_score_threshold = job['match_score'] >= Config.MIN_MATCH_SCORE
                has_relocation = job['relocation_detected']
                is_new = is_new_job(sig)

                if is_new and has_relocation and meets_score_threshold:
                    save_job(sig, job)
                    new_matches.append(job)
                    logger.info(
                        f"New match: {job['title']} @ {job['company']} "
                        f"(Score: {job['match_score']}, Confidence: {job['relocation_confidence']})"
                    )
                elif is_new and has_relocation:
                    logger.info(
                        f"Job below threshold: {job['title']} @ {job['company']} "
                        f"(Score: {job['match_score']}, Threshold: {Config.MIN_MATCH_SCORE})"
                    )
                elif is_new and meets_score_threshold:
                    logger.info(
                        f"Job without relocation: {job['title']} @ {job['company']} "
                        f"(Score: {job['match_score']})"
                    )

            except Exception as e:
                logger.error(f"Error processing job {job.get('title', 'Unknown')}: {e}")
                continue

        # Persist logs to a temporary file for emailing
        log_file_path = None
        try:
            tmp_dir = tempfile.gettempdir()
            log_file_path = os.path.join(tmp_dir, "job_alert_run.log")
            with open(log_file_path, "w", encoding="utf-8") as lf:
                lf.write("Job Alert Run Log (Canada & US)\n")
                lf.write("="*60 + "\n\n")
                lf.write(f"Total jobs aggregated: {len(jobs)}\n")
                lf.write(f"Candidates after ranking: {len(matches)}\n")
                lf.write(f"New matches to send: {len(new_matches)}\n\n")
                lf.write("Top 10 ranked jobs:\n")
                for j in matches[:10]:
                    lf.write(
                        f"- {j.get('title')} @ {j.get('company')} | "
                        f"{j.get('location','')} | Score: {j.get('match_score')} | "
                        f"Relocation: {j.get('relocation_confidence','unknown')} | {j.get('url')}\n"
                    )
        except Exception as e:
            logger.warning(f"Failed to write log file: {e}")

        # Send email if new matches found
        if new_matches:
            logger.info(f"Sending email with {len(new_matches)} new matches")
            send_digest(Config.TARGET_EMAIL, new_matches, log_file_path)
            logger.info("Email sent successfully")
        else:
            logger.info("No new matches to send")
            # Send no matches email with detailed log
            reason = f"Found {len(jobs)} jobs but none met criteria (score >= {Config.MIN_MATCH_SCORE} + relocation)"
            send_no_matches_email(Config.TARGET_EMAIL, reason, log_file_path)

    except Exception as e:
        logger.error(f"Critical error in job alert process: {e}")
        # Send error notification email
        try:
            send_no_matches_email(Config.TARGET_EMAIL, f"Error: {str(e)}", None)
        except:
            pass
        raise

if __name__ == "__main__":
    run()
