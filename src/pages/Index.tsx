import { useState, useCallback } from 'react';
import Header from '@/components/ats/Header';
import InputPanel from '@/components/ats/InputPanel';
import ResultsPanel from '@/components/ats/ResultsPanel';
import { EvaluationResponse, UploadedFile, LoadingStatus } from '@/types/candidate';
import { evaluateCandidates } from '@/lib/api';

const Index = () => {
  const [loadingStatus, setLoadingStatus] = useState<LoadingStatus>('idle');
  const [results, setResults] = useState<EvaluationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleEvaluate = useCallback(async (jdText: string, files: UploadedFile[]) => {
    try {
      setError(null);

      // Real processing with backend API
      setLoadingStatus('parsing');

      // Call the real backend API
      const apiResults = await evaluateCandidates(jdText, files);

      setResults(apiResults);
      setLoadingStatus('idle');
    } catch (err) {
      console.error('Evaluation error:', err);
      setError(err instanceof Error ? err.message : 'Failed to evaluate candidates');
      setLoadingStatus('idle');
    }
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[calc(100vh-120px)]">
          {/* Left Panel - Inputs */}
          <div className="lg:col-span-4 xl:col-span-3">
            <InputPanel
              onEvaluate={handleEvaluate}
              loadingStatus={loadingStatus}
            />
          </div>

          {/* Right Panel - Results */}
          <div className="lg:col-span-8 xl:col-span-9">
            {error && (
              <div className="mb-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500">
                <p className="font-semibold">Error</p>
                <p className="text-sm">{error}</p>
              </div>
            )}
            <ResultsPanel results={results} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
