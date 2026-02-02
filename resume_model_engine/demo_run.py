"""
Demo script showcasing the resume screening pipeline.

This script demonstrates the core functionality with sample job description
and candidate resumes.
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pipeline import evaluate_candidates
from src.pdf_loader import load_resumes_from_folder, load_jd_from_file


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 80 + "\n")


def print_candidate_result(candidate: dict, rank: int):
    """Print candidate result in a readable format."""
    print(f"RANK #{rank}: {candidate['candidate_id'].upper()}")
    print("-" * 80)
    
    print(f"📧 Emails: {', '.join(candidate['emails']) if candidate['emails'] else 'Not found'}")
    print(f"📱 Phones: {', '.join(candidate['phones']) if candidate['phones'] else 'Not found'}")
    print(f"🔗 GitHub: {', '.join(candidate['github']) if candidate['github'] else 'Not found'}")
    print(f"💼 LinkedIn: {', '.join(candidate['linkedin']) if candidate['linkedin'] else 'Not found'}")
    
    print(f"\n📊 SCORES:")
    print(f"   • Skill Match: {candidate['skill_match_score']:.1f}%")
    print(f"   • Semantic Similarity: {candidate['semantic_similarity_score']:.1f}%")
    print(f"   • FINAL SCORE: {candidate['final_match_score']:.1f}%")
    
    print(f"\n✅ Matched Skills ({len(candidate['matched_skills'])}):")
    if candidate['matched_skills']:
        print(f"   {', '.join(candidate['matched_skills'][:10])}")
        if len(candidate['matched_skills']) > 10:
            print(f"   ... and {len(candidate['matched_skills']) - 10} more")
    else:
        print("   None")
    
    print(f"\n❌ Missing Skills ({len(candidate['missing_skills'])}):")
    if candidate['missing_skills']:
        print(f"   {', '.join(candidate['missing_skills'][:10])}")
        if len(candidate['missing_skills']) > 10:
            print(f"   ... and {len(candidate['missing_skills']) - 10} more")
    else:
        print("   None")
    
    print(f"\n🏢 Entities Detected:")
    print(f"   • Companies: {', '.join(candidate['ner_entities']['ORG'][:5]) if candidate['ner_entities']['ORG'] else 'None'}")
    print(f"   • Locations: {', '.join(candidate['ner_entities']['GPE'][:5]) if candidate['ner_entities']['GPE'] else 'None'}")
    print(f"   • Dates: {', '.join(candidate['ner_entities']['DATE'][:3]) if candidate['ner_entities']['DATE'] else 'None'}")
    
    print(f"\n💡 Assessment:")
    print(f"   {candidate['short_reason']}")
    
    print_separator()


def main():
    """Run the demo."""
    print_separator()
    print("🚀 AI RESUME SCREENING ENGINE - DEMO")
    print_separator()
    # Paths
    base = Path(__file__).parent
    data_dir = base / "data"
    jd_dir = data_dir / "Job_descriptions"
    jd_file = jd_dir / "JD.txt"
    resumes_dir = data_dir / "resumes"

    # Load job description
    jd_text = load_jd_from_file(str(jd_file))
    if not jd_text:
        print("⚠️  No job description found at:", jd_file)
        return

    print("📋 JOB DESCRIPTION:")
    print(jd_text[:200] + "...")
    print_separator()
    # Load resumes from folder
    candidates = load_resumes_from_folder(str(resumes_dir))
    num_candidates = len(candidates)
    print(f"📄 Found {num_candidates} PDF resume(s) in: {resumes_dir}")
    print_separator()

    if num_candidates == 0:
        print("⚠️  No PDF resumes found. Please add .pdf files to the resumes folder and try again.")
        return

    # Run the pipeline
    results = evaluate_candidates(jd_text, candidates)
    
    # Print results
    for rank, candidate in enumerate(results, 1):
        print_candidate_result(candidate, rank)
    
    # Save to JSON for backend integration example
    output_file = Path(__file__).parent / "demo_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results also saved to: {output_file}")
    print("\n🎉 Demo completed successfully!")


if __name__ == "__main__":
    main()
