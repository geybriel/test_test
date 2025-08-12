from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Any
from config import Config

def relocation_check(text: str) -> Dict[str, Any]:
    """
    Enhanced relocation detection with sophisticated scoring and Canadian immigration focus
    """
    text_l = text.lower()
    results = {
        'detected': False,
        'score': 0,
        'phrases_found': [],
        'confidence': 'low',
        'immigration_programs': [],
        'relocation_benefits': [],
        'canadian_locations': []
    }
    
    # Check for high confidence immigration terms
    for phrase in Config.RELOCATION_SCORING_KEYWORDS['high_confidence']:
        if phrase in text_l:
            results['phrases_found'].append(phrase)
            results['score'] += 3
            if phrase in ['visa sponsorship', 'lmia', 'work permit']:
                results['immigration_programs'].append(phrase)
    
    # Check for medium confidence terms
    for phrase in Config.RELOCATION_SCORING_KEYWORDS['medium_confidence']:
        if phrase in text_l:
            results['phrases_found'].append(phrase)
            results['score'] += 2
            if phrase in ['relocation assistance', 'housing allowance']:
                results['relocation_benefits'].append(phrase)
    
    # Check for low confidence terms
    for phrase in Config.RELOCATION_SCORING_KEYWORDS['low_confidence']:
        if phrase in text_l:
            results['phrases_found'].append(phrase)
            results['score'] += 1
            results['canadian_locations'].append(phrase)
    
    # Check for specific Canadian immigration programs
    immigration_programs = [
        'express entry', 'federal skilled worker', 'federal skilled trades',
        'canadian experience class', 'provincial nominee', 'atlantic immigration',
        'rural and northern immigration', 'global talent stream', 'intra-company transfer'
    ]
    
    for program in immigration_programs:
        if program in text_l:
            results['immigration_programs'].append(program)
            results['score'] += 2.5
    
    # Check for relocation benefits
    relocation_benefits = [
        'relocation package', 'relocation bonus', 'flight', 'housing',
        'accommodation', 'dependent documentation', 'family sponsorship',
        'spouse work permit', 'dependent visa'
    ]
    
    for benefit in relocation_benefits:
        if benefit in text_l:
            results['relocation_benefits'].append(benefit)
            results['score'] += 1.5
    
    # Check for Canadian provinces and cities
    canadian_locations = [
        'toronto', 'vancouver', 'montreal', 'calgary', 'ottawa', 'edmonton',
        'winnipeg', 'halifax', 'victoria', 'quebec', 'alberta', 'ontario',
        'british columbia', 'manitoba', 'nova scotia', 'saskatchewan', 'new brunswick'
    ]
    
    for location in canadian_locations:
        if location in text_l:
            results['canadian_locations'].append(location)
            results['score'] += 0.5
    
    # Check for work authorization terms
    work_auth_terms = [
        'open work permit', 'closed work permit', 'post-graduate work permit',
        'nafta work permit', 'ceta', 'comprehensive economic and trade agreement'
    ]
    
    for term in work_auth_terms:
        if term in text_l:
            results['phrases_found'].append(term)
            results['score'] += 2
    
    # Determine confidence level based on comprehensive scoring
    if results['score'] >= 4:
        results['detected'] = True
        results['confidence'] = 'high'
    elif results['score'] >= 2:
        results['detected'] = True
        results['confidence'] = 'medium'
    elif results['score'] >= 1:
        results['detected'] = True
        results['confidence'] = 'low'
    
    # Additional validation for high confidence
    if results['confidence'] == 'high':
        # Must have at least one immigration program or direct sponsorship mention
        if not results['immigration_programs'] and 'visa sponsorship' not in results['phrases_found']:
            results['confidence'] = 'medium'
    
    return results

def calculate_job_score(job: Dict[str, Any], base_score: float) -> float:
    """
    Calculate additional scoring factors for job ranking with enhanced criteria
    """
    score = base_score
    
    # Bonus for Canadian companies and locations
    canadian_cities = ['toronto', 'vancouver', 'montreal', 'calgary', 'ottawa', 'edmonton']
    if any(city in job.get('location', '').lower() for city in canadian_cities):
        score += 15
    
    # Bonus for remote work mentions
    if 'remote' in job.get('description', '').lower() or 'remote' in job.get('title', '').lower():
        score += 8
    
    # Bonus for senior positions
    senior_keywords = ['senior', 'lead', 'principal', 'staff', 'architect', 'manager']
    if any(keyword in job.get('title', '').lower() for keyword in senior_keywords):
        score += 10
    
    # Bonus for customer-facing technical roles
    customer_roles = ['customer success', 'technical account', 'solutions engineer', 
                     'customer support', 'implementation engineer', 'professional services']
    if any(role in job.get('title', '').lower() for role in customer_roles):
        score += 12
    
    # Bonus for specific technical domains
    domain_bonuses = {
        'cloud engineer': 8,
        'cybersecurity': 10,
        'data engineer': 8,
        'iam': 10,
        'devops': 8,
        'sre': 10
    }
    
    for domain, bonus in domain_bonuses.items():
        if domain in job.get('title', '').lower():
            score += bonus
            break
    
    # Penalty for contract/temporary positions
    temp_keywords = ['contract', 'temporary', 'temp', 'part-time', 'freelance']
    if any(keyword in job.get('description', '').lower() for keyword in temp_keywords):
        score -= 20
    
    # Penalty for entry-level positions
    entry_keywords = ['junior', 'entry level', 'graduate', 'intern']
    if any(keyword in job.get('title', '').lower() for keyword in entry_keywords):
        score -= 10
    
    return min(100, max(0, score))  # Clamp between 0-100

def rank_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enhanced job ranking with multiple scoring factors and relocation focus
    """
    if not jobs:
        return []
    
    # Prepare corpus for TF-IDF analysis
    corpus = []
    for job in jobs:
        text_parts = [
            job.get('title', ''),
            job.get('company', ''),
            job.get('description', ''),
            job.get('location', '')
        ]
        corpus.append(" ".join(text_parts))
    
    # Add skills keywords to corpus for comparison
    corpus.append(" ".join(Config.SKILLS_KEYWORDS))
    
    # Calculate TF-IDF similarity
    try:
        tfidf = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        ).fit_transform(corpus)
        
        job_vecs = tfidf[:-1]
        skills_vec = tfidf[-1]
        similarity_scores = cosine_similarity(job_vecs, skills_vec.reshape(1, -1)).flatten()
        
    except Exception as e:
        # Fallback to simple keyword matching if TF-IDF fails
        similarity_scores = []
        for job in jobs:
            text = " ".join([job.get('title', ''), job.get('description', '')]).lower()
            matches = sum(1 for keyword in Config.SKILLS_KEYWORDS if keyword.lower() in text)
            similarity_scores.append(min(1.0, matches / len(Config.SKILLS_KEYWORDS)))
    
    # Process each job with enhanced scoring
    results = []
    for job, base_score in zip(jobs, similarity_scores):
        # Calculate base match score
        match_score = round(float(base_score) * 100, 2)
        
        # Enhanced relocation detection
        relocation_info = relocation_check(
            job.get('description', '') + " " + job.get('title', '')
        )
        
        # Apply additional scoring factors
        final_score = calculate_job_score(job, match_score)
        
        # Update job with all scoring information
        job.update({
            'match_score': final_score,
            'relocation_detected': relocation_info['detected'],
            'relocation_confidence': relocation_info['confidence'],
            'relocation_score': relocation_info['score'],
            'relocation_phrases': relocation_info['phrases_found'],
            'immigration_programs': relocation_info['immigration_programs'],
            'relocation_benefits': relocation_info['relocation_benefits'],
            'canadian_locations': relocation_info['canadian_locations']
        })
        
        results.append(job)
    
    # Sort by match score (highest first)
    return sorted(results, key=lambda x: x['match_score'], reverse=True)
