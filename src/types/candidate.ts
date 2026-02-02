// Candidate evaluation result schema matching the API contract
export interface NEREntities {
  PERSON: string[];
  ORG: string[];
  GPE: string[];
  DATE: string[];
}

export interface CandidateResult {
  candidate_id: string;
  emails: string[];
  phones: string[];
  github: string[];
  linkedin: string[];
  extracted_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  skill_match_score: number;
  semantic_similarity_score: number;
  final_match_score: number;
  ner_entities: NEREntities;
  short_reason: string;
}

export interface EvaluationResponse {
  job_id: string;
  total_candidates: number;
  processing_time_ms: number;
  results: CandidateResult[];
}

export interface UploadedFile {
  id: string;
  file: File;
  name: string;
  size: number;
}

export type LoadingStatus = 
  | 'idle' 
  | 'parsing' 
  | 'extracting' 
  | 'calculating' 
  | 'complete';

export const LOADING_MESSAGES: Record<LoadingStatus, string> = {
  idle: '',
  parsing: 'Parsing PDFs...',
  extracting: 'Extracting skills...',
  calculating: 'Calculating scores...',
  complete: 'Complete!',
};
