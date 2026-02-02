import { Eye, ChevronUp, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { CandidateResult } from '@/types/candidate';
import ScoreBadge from './ScoreBadge';
import { useState } from 'react';

interface RankingTableProps {
  candidates: CandidateResult[];
  onViewDetails: (candidate: CandidateResult) => void;
}

type SortField = 'rank' | 'final' | 'skill' | 'semantic' | 'matched' | 'missing';
type SortDirection = 'asc' | 'desc';

const RankingTable = ({ candidates, onViewDetails }: RankingTableProps) => {
  const [sortField, setSortField] = useState<SortField>('final');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const sortedCandidates = [...candidates].sort((a, b) => {
    const multiplier = sortDirection === 'asc' ? 1 : -1;
    
    switch (sortField) {
      case 'final':
        return (a.final_match_score - b.final_match_score) * multiplier;
      case 'skill':
        return (a.skill_match_score - b.skill_match_score) * multiplier;
      case 'semantic':
        return (a.semantic_similarity_score - b.semantic_similarity_score) * multiplier;
      case 'matched':
        return (a.matched_skills.length - b.matched_skills.length) * multiplier;
      case 'missing':
        return (a.missing_skills.length - b.missing_skills.length) * multiplier;
      default:
        return 0;
    }
  });

  const SortHeader = ({ field, children }: { field: SortField; children: React.ReactNode }) => (
    <th 
      onClick={() => handleSort(field)}
      className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider cursor-pointer hover:text-foreground transition-colors group"
    >
      <div className="flex items-center gap-1">
        {children}
        <span className="opacity-0 group-hover:opacity-100 transition-opacity">
          {sortField === field ? (
            sortDirection === 'desc' ? <ChevronDown className="w-3 h-3" /> : <ChevronUp className="w-3 h-3" />
          ) : (
            <ChevronDown className="w-3 h-3 text-muted-foreground/50" />
          )}
        </span>
      </div>
    </th>
  );

  return (
    <div className="overflow-x-auto scrollbar-thin">
      <table className="w-full">
        <thead>
          <tr className="border-b border-border">
            <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider w-16">
              Rank
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Candidate ID
            </th>
            <SortHeader field="final">Final Score</SortHeader>
            <SortHeader field="skill">Skill Match</SortHeader>
            <SortHeader field="semantic">Semantic</SortHeader>
            <SortHeader field="matched">Matched</SortHeader>
            <SortHeader field="missing">Missing</SortHeader>
            <th className="px-4 py-3 text-right text-xs font-semibold text-muted-foreground uppercase tracking-wider w-28">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {sortedCandidates.map((candidate, index) => (
            <tr
              key={candidate.candidate_id}
              onClick={() => onViewDetails(candidate)}
              className="table-row-hover"
            >
              <td className="px-4 py-4">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-secondary text-sm font-bold text-foreground">
                  {index + 1}
                </span>
              </td>
              <td className="px-4 py-4">
                <span className="font-medium text-foreground">{candidate.candidate_id}</span>
              </td>
              <td className="px-4 py-4">
                <ScoreBadge score={candidate.final_match_score} />
              </td>
              <td className="px-4 py-4">
                <span className="text-sm text-muted-foreground">
                  {candidate.skill_match_score.toFixed(1)}%
                </span>
              </td>
              <td className="px-4 py-4">
                <span className="text-sm text-muted-foreground">
                  {candidate.semantic_similarity_score.toFixed(1)}%
                </span>
              </td>
              <td className="px-4 py-4">
                <span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-[hsl(var(--score-high-bg))] text-[hsl(var(--score-high))] text-sm font-semibold">
                  {candidate.matched_skills.length}
                </span>
              </td>
              <td className="px-4 py-4">
                <span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-[hsl(var(--score-low-bg))] text-[hsl(var(--score-low))] text-sm font-semibold">
                  {candidate.missing_skills.length}
                </span>
              </td>
              <td className="px-4 py-4 text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    onViewDetails(candidate);
                  }}
                  className="text-primary hover:bg-primary/10 hover:text-primary"
                >
                  <Eye className="w-4 h-4 mr-1" />
                  Details
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RankingTable;
