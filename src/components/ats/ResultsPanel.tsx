import { useState } from 'react';
import { Users, Trophy, TrendingUp, Clock, Download, FileJson, FileSpreadsheet, FileSearch } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { EvaluationResponse, CandidateResult } from '@/types/candidate';
import MetricCard from './MetricCard';
import RankingTable from './RankingTable';
import CandidateModal from './CandidateModal';
import { formatField } from '@/lib/formatters';

interface ResultsPanelProps {
  results: EvaluationResponse | null;
}

const ResultsPanel = ({ results }: ResultsPanelProps) => {
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateResult | null>(null);

  const exportToJSON = () => {
    if (!results) return;
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evaluation_results_${results.job_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportToCSV = () => {
    if (!results) return;

    const headers = [
      'Rank',
      'Candidate ID',
      'Final Score (%)',
      'Skill Match (%)',
      'Semantic Similarity (%)',
      'Matched Skills',
      'Missing Skills',
      'Emails',
      'Phones',
      'Short Reason'
    ];

    const rows = results.results.map((c, i) => [
      i + 1,
      c.candidate_id,
      c.final_match_score.toFixed(1),
      c.skill_match_score.toFixed(1),
      c.semantic_similarity_score.toFixed(1),
      c.matched_skills.length > 0 ? c.matched_skills.join('; ') : 'NA',
      c.missing_skills.length > 0 ? c.missing_skills.join('; ') : 'NA',
      formatField(c.emails),
      formatField(c.phones),
      `"${c.short_reason.replace(/"/g, '""')}"`
    ]);

    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evaluation_results_${results.job_id}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const topScore = results?.results[0]?.final_match_score ?? 0;
  const avgScore = results?.results.length
    ? results.results.reduce((sum, c) => sum + c.final_match_score, 0) / results.results.length
    : 0;

  if (!results) {
    return (
      <div className="panel h-full flex flex-col">
        <div className="panel-header rounded-t-xl">
          <h2 className="text-lg font-semibold text-foreground">Results Dashboard</h2>
          <p className="text-sm text-muted-foreground mt-1">Candidate rankings will appear here</p>
        </div>
        <div className="flex-1 flex items-center justify-center p-12">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-secondary/50 flex items-center justify-center">
              <FileSearch className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">No Results Yet</h3>
            <p className="text-sm text-muted-foreground max-w-xs mx-auto">
              Upload resumes and enter a job description to evaluate candidates
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="panel h-full flex flex-col">
        <div className="panel-header rounded-t-xl flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">Results Dashboard</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Job ID: <span className="font-mono text-xs">{results.job_id.slice(0, 8)}...</span>
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={exportToJSON}
              className="border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            >
              <FileJson className="w-4 h-4 mr-1" />
              JSON
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={exportToCSV}
              className="border-border hover:bg-secondary text-muted-foreground hover:text-foreground"
            >
              <FileSpreadsheet className="w-4 h-4 mr-1" />
              CSV
            </Button>
          </div>
        </div>

        <div className="flex-1 overflow-auto p-6 space-y-6 scrollbar-thin">
          {/* Metrics */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              icon={Users}
              label="Total Candidates"
              value={results.total_candidates}
            />
            <MetricCard
              icon={Trophy}
              label="Top Score"
              value={topScore.toFixed(1)}
              suffix="%"
            />
            <MetricCard
              icon={TrendingUp}
              label="Average Score"
              value={avgScore.toFixed(1)}
              suffix="%"
            />
            <MetricCard
              icon={Clock}
              label="Processing Time"
              value={(results.processing_time_ms / 1000).toFixed(2)}
              suffix="s"
            />
          </div>

          {/* Ranking Table */}
          <div className="bg-card rounded-xl border border-border overflow-hidden">
            <div className="px-4 py-3 border-b border-border bg-[hsl(var(--panel-header))]">
              <h3 className="text-sm font-semibold text-foreground">Candidate Rankings</h3>
            </div>
            <RankingTable
              candidates={results.results}
              onViewDetails={setSelectedCandidate}
            />
          </div>
        </div>
      </div>

      {/* Modal */}
      {selectedCandidate && (
        <CandidateModal
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
        />
      )}
    </>
  );
};

export default ResultsPanel;
