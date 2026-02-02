import { X, Mail, Phone, Github, Linkedin, User, Building, MapPin, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { CandidateResult } from '@/types/candidate';
import ScoreBadge from './ScoreBadge';
import { formatField, formatArrayField } from '@/lib/formatters';

interface CandidateModalProps {
  candidate: CandidateResult;
  onClose: () => void;
}

const CandidateModal = ({ candidate, onClose }: CandidateModalProps) => {
  // Format contact info with NA handling
  const email = formatField(candidate.emails);
  const phone = formatField(candidate.phones);
  const github = formatField(candidate.github);
  const linkedin = formatField(candidate.linkedin);

  // Format NER entities with NA handling
  const personName = formatArrayField(candidate.ner_entities.PERSON);
  const organizations = formatArrayField(candidate.ner_entities.ORG);
  const locations = formatArrayField(candidate.ner_entities.GPE);
  const dates = formatArrayField(candidate.ner_entities.DATE);
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl max-h-[90vh] overflow-hidden rounded-2xl bg-card border border-border shadow-2xl animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-[hsl(var(--panel-header))]">
          <div>
            <h2 className="text-xl font-bold text-foreground">Candidate Report</h2>
            <p className="text-sm text-muted-foreground">{candidate.candidate_id}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-80px)] p-6 space-y-6 scrollbar-thin">
          {/* Scores Summary */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 rounded-xl bg-secondary/50 border border-border">
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Final Score</p>
              <ScoreBadge score={candidate.final_match_score} />
            </div>
            <div className="text-center p-4 rounded-xl bg-secondary/50 border border-border">
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Skill Match</p>
              <span className="text-lg font-bold text-foreground">{candidate.skill_match_score.toFixed(1)}%</span>
            </div>
            <div className="text-center p-4 rounded-xl bg-secondary/50 border border-border">
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Semantic</p>
              <span className="text-lg font-bold text-foreground">{candidate.semantic_similarity_score.toFixed(1)}%</span>
            </div>
          </div>

          {/* Contact Information */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Contact Information</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30 border border-border">
                <Mail className="w-4 h-4 text-primary" />
                <span className="text-sm text-foreground truncate">{email}</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30 border border-border">
                <Phone className="w-4 h-4 text-primary" />
                <span className="text-sm text-foreground">{phone}</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30 border border-border">
                <Github className="w-4 h-4 text-primary" />
                <span className="text-sm text-foreground truncate">{github}</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-secondary/30 border border-border">
                <Linkedin className="w-4 h-4 text-primary" />
                <span className="text-sm text-foreground truncate">{linkedin}</span>
              </div>
            </div>
          </div>

          {/* Extracted Skills */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
              Extracted Skills ({candidate.extracted_skills.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {candidate.extracted_skills.map((skill, i) => (
                <span key={i} className="skill-chip skill-chip-neutral">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Matched Skills */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
              Matched Skills
              <span className="px-2 py-0.5 rounded-full bg-[hsl(var(--score-high-bg))] text-[hsl(var(--score-high))] text-xs">
                {candidate.matched_skills.length}
              </span>
            </h3>
            <div className="flex flex-wrap gap-2">
              {candidate.matched_skills.length > 0 ? (
                candidate.matched_skills.map((skill, i) => (
                  <span key={i} className="skill-chip skill-chip-matched">
                    ✓ {skill}
                  </span>
                ))
              ) : (
                <span className="text-sm text-muted-foreground">No matched skills</span>
              )}
            </div>
          </div>

          {/* Missing Skills */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
              Missing Skills
              <span className="px-2 py-0.5 rounded-full bg-[hsl(var(--score-low-bg))] text-[hsl(var(--score-low))] text-xs">
                {candidate.missing_skills.length}
              </span>
            </h3>
            <div className="flex flex-wrap gap-2">
              {candidate.missing_skills.length > 0 ? (
                candidate.missing_skills.map((skill, i) => (
                  <span key={i} className="skill-chip skill-chip-missing">
                    ✗ {skill}
                  </span>
                ))
              ) : (
                <span className="text-sm text-muted-foreground">No missing skills</span>
              )}
            </div>
          </div>

          {/* NER Entities */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">Named Entities</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-start gap-2">
                <User className="w-4 h-4 text-primary mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground uppercase mb-1">Person</p>
                  <p className="text-sm text-foreground">{personName}</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <Building className="w-4 h-4 text-primary mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground uppercase mb-1">Organizations</p>
                  <p className="text-sm text-foreground">{organizations}</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-primary mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground uppercase mb-1">Locations</p>
                  <p className="text-sm text-foreground">{locations}</p>
                </div>
              </div>
              <div className="flex items-start gap-2">
                <Calendar className="w-4 h-4 text-primary mt-0.5" />
                <div>
                  <p className="text-xs text-muted-foreground uppercase mb-1">Dates</p>
                  <p className="text-sm text-foreground">{dates}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Reason */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">AI Assessment</h3>
            <div className="p-4 rounded-xl bg-secondary/30 border border-border">
              <p className="text-sm text-foreground leading-relaxed">{candidate.short_reason}</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-border bg-[hsl(var(--panel-header))]">
          <Button onClick={onClose} className="w-full">
            Close Report
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CandidateModal;
